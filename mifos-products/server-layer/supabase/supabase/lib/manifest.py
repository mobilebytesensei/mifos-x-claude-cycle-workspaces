"""
Deployment Manifest
===================

Tracks what has been deployed and when.
Provides history of all deployments for audit and rollback.

Manifest Location: .deployment/manifest.json

Usage:
    from lib.manifest import ManifestManager

    manager = ManifestManager()
    manager.record_deployment('migration', '20251214_001_users.sql', 'success')
    manager.save()

    # View history
    history = manager.get_deployment_history()
"""

import json
import hashlib
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


@dataclass
class DeploymentEntry:
    """Single deployment action."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    component_type: str = ''  # migration, edge_function, rpc, trigger
    component_name: str = ''
    action: str = ''  # create, update, delete
    status: str = ''  # success, failed, rolled_back
    checksum: Optional[str] = None
    details: Dict = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class DeploymentSession:
    """A deployment session containing multiple entries."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    status: str = 'in_progress'  # in_progress, success, partial, failed
    entries: List[DeploymentEntry] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)

    def add_entry(self, entry: DeploymentEntry):
        self.entries.append(entry)

    def complete(self, status: str = 'success'):
        self.completed_at = datetime.now().isoformat()
        self.status = status
        self.summary = {
            'total': len(self.entries),
            'success': sum(1 for e in self.entries if e.status == 'success'),
            'failed': sum(1 for e in self.entries if e.status == 'failed'),
        }


@dataclass
class DeploymentManifest:
    """Full deployment manifest."""
    version: str = '1.0.0'
    project: str = ''
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    sessions: List[DeploymentSession] = field(default_factory=list)

    # Current state tracking
    deployed_migrations: Dict[str, Dict] = field(default_factory=dict)
    deployed_functions: Dict[str, Dict] = field(default_factory=dict)
    deployed_rpcs: Dict[str, Dict] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'version': self.version,
            'project': self.project,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sessions': [
                {
                    'session_id': s.session_id,
                    'started_at': s.started_at,
                    'completed_at': s.completed_at,
                    'status': s.status,
                    'summary': s.summary,
                    'entries': [asdict(e) for e in s.entries],
                }
                for s in self.sessions
            ],
            'current_state': {
                'migrations': self.deployed_migrations,
                'functions': self.deployed_functions,
                'rpcs': self.deployed_rpcs,
            },
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'DeploymentManifest':
        manifest = cls(
            version=data.get('version', '1.0.0'),
            project=data.get('project', ''),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', ''),
        )

        # Load current state
        state = data.get('current_state', {})
        manifest.deployed_migrations = state.get('migrations', {})
        manifest.deployed_functions = state.get('functions', {})
        manifest.deployed_rpcs = state.get('rpcs', {})

        # Load sessions
        for session_data in data.get('sessions', []):
            session = DeploymentSession(
                session_id=session_data.get('session_id', ''),
                started_at=session_data.get('started_at', ''),
                completed_at=session_data.get('completed_at'),
                status=session_data.get('status', 'unknown'),
                summary=session_data.get('summary', {}),
            )

            for entry_data in session_data.get('entries', []):
                entry = DeploymentEntry(
                    id=entry_data.get('id', ''),
                    timestamp=entry_data.get('timestamp', ''),
                    component_type=entry_data.get('component_type', ''),
                    component_name=entry_data.get('component_name', ''),
                    action=entry_data.get('action', ''),
                    status=entry_data.get('status', ''),
                    checksum=entry_data.get('checksum'),
                    details=entry_data.get('details', {}),
                    error=entry_data.get('error'),
                )
                session.entries.append(entry)

            manifest.sessions.append(session)

        return manifest


class ManifestManager:
    """
    Manages the deployment manifest file.

    The manifest tracks:
    - All deployment sessions
    - Currently deployed state (migrations, functions, RPCs)
    - Success/failure history
    """

    def __init__(self, manifest_dir: Optional[Path] = None):
        self.manifest_dir = manifest_dir or Path('.deployment')
        self.manifest_path = self.manifest_dir / 'manifest.json'
        self.manifest: Optional[DeploymentManifest] = None
        self.current_session: Optional[DeploymentSession] = None

    def load(self) -> DeploymentManifest:
        """Load manifest from disk."""
        if self.manifest_path.exists():
            try:
                data = json.loads(self.manifest_path.read_text())
                self.manifest = DeploymentManifest.from_dict(data)
            except Exception as e:
                logger.error(f"Failed to load manifest: {e}")
                self.manifest = DeploymentManifest()
        else:
            self.manifest = DeploymentManifest()

        return self.manifest

    def save(self):
        """Save manifest to disk."""
        if self.manifest is None:
            self.manifest = DeploymentManifest()

        self.manifest.updated_at = datetime.now().isoformat()

        # Ensure directory exists
        self.manifest_dir.mkdir(parents=True, exist_ok=True)

        # Write manifest
        self.manifest_path.write_text(
            json.dumps(self.manifest.to_dict(), indent=2)
        )

        logger.info(f"Manifest saved to {self.manifest_path}")

    def start_session(self) -> DeploymentSession:
        """Start a new deployment session."""
        if self.manifest is None:
            self.load()

        self.current_session = DeploymentSession()
        return self.current_session

    def record_deployment(
        self,
        component_type: str,
        component_name: str,
        status: str,
        action: str = 'create',
        checksum: Optional[str] = None,
        details: Optional[Dict] = None,
        error: Optional[str] = None,
    ) -> DeploymentEntry:
        """Record a single deployment action."""
        if self.current_session is None:
            self.start_session()

        entry = DeploymentEntry(
            component_type=component_type,
            component_name=component_name,
            action=action,
            status=status,
            checksum=checksum,
            details=details or {},
            error=error,
        )

        self.current_session.add_entry(entry)

        # Update current state on success
        if status == 'success' and self.manifest:
            if component_type == 'migration':
                self.manifest.deployed_migrations[component_name] = {
                    'deployed_at': entry.timestamp,
                    'checksum': checksum,
                }
            elif component_type == 'edge_function':
                self.manifest.deployed_functions[component_name] = {
                    'deployed_at': entry.timestamp,
                    'checksum': checksum,
                }
            elif component_type == 'rpc':
                self.manifest.deployed_rpcs[component_name] = {
                    'deployed_at': entry.timestamp,
                }

        return entry

    def end_session(self, status: str = 'success'):
        """End current deployment session."""
        if self.current_session is None:
            return

        self.current_session.complete(status)

        if self.manifest:
            self.manifest.sessions.append(self.current_session)

        self.current_session = None
        self.save()

    def get_deployment_history(self, limit: int = 10) -> List[Dict]:
        """Get recent deployment history."""
        if self.manifest is None:
            self.load()

        sessions = self.manifest.sessions[-limit:]
        return [
            {
                'session_id': s.session_id,
                'started_at': s.started_at,
                'completed_at': s.completed_at,
                'status': s.status,
                'summary': s.summary,
            }
            for s in reversed(sessions)
        ]

    def get_current_state(self) -> Dict:
        """Get currently deployed state."""
        if self.manifest is None:
            self.load()

        return {
            'migrations': list(self.manifest.deployed_migrations.keys()),
            'functions': list(self.manifest.deployed_functions.keys()),
            'rpcs': list(self.manifest.deployed_rpcs.keys()),
        }

    def is_deployed(self, component_type: str, component_name: str) -> bool:
        """Check if a component is currently deployed."""
        if self.manifest is None:
            self.load()

        if component_type == 'migration':
            return component_name in self.manifest.deployed_migrations
        elif component_type == 'edge_function':
            return component_name in self.manifest.deployed_functions
        elif component_type == 'rpc':
            return component_name in self.manifest.deployed_rpcs

        return False

    def get_checksum(self, component_type: str, component_name: str) -> Optional[str]:
        """Get checksum of deployed component."""
        if self.manifest is None:
            self.load()

        if component_type == 'migration':
            return self.manifest.deployed_migrations.get(component_name, {}).get('checksum')
        elif component_type == 'edge_function':
            return self.manifest.deployed_functions.get(component_name, {}).get('checksum')

        return None

    def generate_report(self) -> str:
        """Generate human-readable deployment report."""
        if self.manifest is None:
            self.load()

        lines = [
            "=" * 60,
            "DEPLOYMENT MANIFEST",
            "=" * 60,
            f"Project: {self.manifest.project or 'Unknown'}",
            f"Created: {self.manifest.created_at}",
            f"Updated: {self.manifest.updated_at}",
            "",
            "CURRENT STATE",
            "-" * 40,
            f"Migrations: {len(self.manifest.deployed_migrations)}",
            f"Edge Functions: {len(self.manifest.deployed_functions)}",
            f"RPCs: {len(self.manifest.deployed_rpcs)}",
            "",
            "RECENT SESSIONS",
            "-" * 40,
        ]

        for session in self.manifest.sessions[-5:]:
            status_icon = {'success': '+', 'failed': 'x', 'partial': '~'}.get(session.status, '?')
            lines.append(f"  [{status_icon}] {session.session_id} - {session.started_at}")
            if session.summary:
                lines.append(f"      Success: {session.summary.get('success', 0)}, Failed: {session.summary.get('failed', 0)}")

        lines.append("=" * 60)

        return '\n'.join(lines)
