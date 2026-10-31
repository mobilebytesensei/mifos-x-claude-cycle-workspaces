#!/usr/bin/env python3
"""
Engine Runner (Framework Level)
===============================

Reusable ETL pipeline runner that reads ENGINE_CONFIG.yaml
and executes enabled phases.

This is the framework-level runner that projects can extend
with custom phase handlers.

Usage:
    python engine_runner.py                    # Run all enabled phases
    python engine_runner.py --phase extract    # Run specific phase
    python engine_runner.py --status           # Show pipeline status
    python engine_runner.py --config           # Show current config
    python engine_runner.py --dry-run          # Preview without executing

Example:
    from engine_runner import EngineRunner

    runner = EngineRunner()
    results = runner.run()

    for result in results:
        print(f"{result.phase}: {result.status} ({result.records_processed} records)")
"""

import os
import sys
import yaml
import time
import logging
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class PhaseResult:
    """Result of executing a single pipeline phase."""
    phase: str
    status: str  # success, failed, skipped, dry_run
    records_processed: int = 0
    records_failed: int = 0
    duration_seconds: float = 0.0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PipelineResult:
    """Result of executing the full pipeline."""
    status: str  # success, partial, failed
    phases: List[PhaseResult] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    total_records: int = 0
    total_errors: int = 0
    duration_seconds: float = 0.0

    def complete(self):
        self.completed_at = datetime.now().isoformat()
        self.total_records = sum(p.records_processed for p in self.phases)
        self.total_errors = sum(p.records_failed for p in self.phases)
        self.duration_seconds = sum(p.duration_seconds for p in self.phases)

        # Determine overall status
        failed = sum(1 for p in self.phases if p.status == 'failed')
        success = sum(1 for p in self.phases if p.status == 'success')

        if failed == 0:
            self.status = 'success'
        elif success > 0:
            self.status = 'partial'
        else:
            self.status = 'failed'


# ============================================================================
# Phase Handler Base Class
# ============================================================================

class PhaseHandler(ABC):
    """Abstract base class for phase handlers."""

    @abstractmethod
    def execute(self, config: Dict) -> PhaseResult:
        """Execute the phase with given configuration."""
        pass

    def get_name(self) -> str:
        """Return the phase name."""
        return self.__class__.__name__.replace('Handler', '').lower()


class ExtractHandler(PhaseHandler):
    """Default extract phase handler."""

    def execute(self, config: Dict) -> PhaseResult:
        start_time = time.time()
        result = PhaseResult(
            phase='extract',
            status='success',
            started_at=datetime.now().isoformat(),
        )

        sources = config.get('sources', [])
        total_records = 0

        for source in sources:
            if not source.get('enabled', True):
                continue

            source_name = source.get('name', 'unknown')
            logger.info(f"Extracting from source: {source_name}")

            # Default implementation - override in project
            # This is a placeholder that projects should extend
            try:
                # Placeholder: projects override this
                records = self._extract_source(source)
                total_records += records
            except Exception as e:
                logger.error(f"Failed to extract from {source_name}: {e}")
                result.errors.append(f"{source_name}: {str(e)}")

        result.records_processed = total_records
        result.duration_seconds = time.time() - start_time
        result.completed_at = datetime.now().isoformat()

        if result.errors:
            result.status = 'partial' if total_records > 0 else 'failed'

        return result

    def _extract_source(self, source: Dict) -> int:
        """Override in project-specific handler."""
        logger.warning(f"Default extract handler - override in project")
        return 0


class TransformHandler(PhaseHandler):
    """Default transform phase handler."""

    def execute(self, config: Dict) -> PhaseResult:
        start_time = time.time()
        result = PhaseResult(
            phase='transform',
            status='success',
            started_at=datetime.now().isoformat(),
        )

        strategies = config.get('strategies', ['clean', 'normalize'])

        for strategy in strategies:
            logger.info(f"Applying transform strategy: {strategy}")
            # Placeholder - projects override

        result.duration_seconds = time.time() - start_time
        result.completed_at = datetime.now().isoformat()

        return result


class ValidateHandler(PhaseHandler):
    """Default validate phase handler."""

    def execute(self, config: Dict) -> PhaseResult:
        start_time = time.time()
        result = PhaseResult(
            phase='validate',
            status='success',
            started_at=datetime.now().isoformat(),
        )

        rules = config.get('rules', ['required_fields', 'type_validation'])

        for rule in rules:
            logger.info(f"Applying validation rule: {rule}")
            # Placeholder - projects override

        result.duration_seconds = time.time() - start_time
        result.completed_at = datetime.now().isoformat()

        return result


class EnrichHandler(PhaseHandler):
    """Default enrich phase handler."""

    def execute(self, config: Dict) -> PhaseResult:
        start_time = time.time()
        result = PhaseResult(
            phase='enrich',
            status='success',
            started_at=datetime.now().isoformat(),
        )

        enrichers = config.get('enrichers', [])

        for enricher in enrichers:
            logger.info(f"Running enricher: {enricher}")
            # Placeholder - projects override

        result.duration_seconds = time.time() - start_time
        result.completed_at = datetime.now().isoformat()

        return result


class LoadHandler(PhaseHandler):
    """Default load phase handler."""

    def execute(self, config: Dict) -> PhaseResult:
        start_time = time.time()
        result = PhaseResult(
            phase='load',
            status='success',
            started_at=datetime.now().isoformat(),
        )

        mode = config.get('mode', 'incremental')
        destination = config.get('destination', 'supabase')

        logger.info(f"Loading to {destination} in {mode} mode")
        # Placeholder - projects override

        result.duration_seconds = time.time() - start_time
        result.completed_at = datetime.now().isoformat()

        return result


# ============================================================================
# Engine Configuration
# ============================================================================

@dataclass
class EngineConfig:
    """Engine configuration loaded from ENGINE_CONFIG.yaml."""
    phases: Dict[str, Dict] = field(default_factory=dict)
    execution: Dict[str, Any] = field(default_factory=dict)
    logging: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> 'EngineConfig':
        """Load configuration from YAML file."""
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {path}")

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(
            phases=data.get('phases', {}),
            execution=data.get('execution', {}),
            logging=data.get('logging', {}),
        )

    def is_phase_enabled(self, phase: str) -> bool:
        """Check if a phase is enabled."""
        phase_config = self.phases.get(phase, {})
        return phase_config.get('enabled', False)

    def get_phase_config(self, phase: str) -> Dict:
        """Get configuration for a specific phase."""
        return self.phases.get(phase, {})


# ============================================================================
# Engine Runner
# ============================================================================

class EngineRunner:
    """
    Framework-level ETL pipeline runner.

    Reads ENGINE_CONFIG.yaml and executes enabled phases in order.
    Projects can extend this by registering custom phase handlers.

    Usage:
        runner = EngineRunner()
        runner.register_handler('extract', MyExtractHandler())
        results = runner.run()
    """

    PHASE_ORDER = ['extract', 'transform', 'validate', 'enrich', 'load']

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path('ENGINE_CONFIG.yaml')
        self.config: Optional[EngineConfig] = None
        self.handlers: Dict[str, PhaseHandler] = {}
        self._checkpoints: Dict[str, Any] = {}

        # Register default handlers
        self._register_default_handlers()

    def _register_default_handlers(self):
        """Register default phase handlers."""
        self.handlers = {
            'extract': ExtractHandler(),
            'transform': TransformHandler(),
            'validate': ValidateHandler(),
            'enrich': EnrichHandler(),
            'load': LoadHandler(),
        }

    def register_handler(self, phase: str, handler: PhaseHandler):
        """Register a custom phase handler."""
        self.handlers[phase] = handler
        logger.info(f"Registered custom handler for phase: {phase}")

    def load_config(self) -> EngineConfig:
        """Load engine configuration."""
        self.config = EngineConfig.load(self.config_path)
        return self.config

    def run(
        self,
        phase: Optional[str] = None,
        dry_run: bool = False,
    ) -> PipelineResult:
        """
        Execute the pipeline.

        Args:
            phase: Optional specific phase to run (runs all if None)
            dry_run: If True, preview without executing

        Returns:
            PipelineResult with all phase results
        """
        if self.config is None:
            self.load_config()

        result = PipelineResult()
        phases_to_run = [phase] if phase else self.PHASE_ORDER

        logger.info(f"Starting pipeline run (dry_run={dry_run})")

        for phase_name in phases_to_run:
            if not self.config.is_phase_enabled(phase_name):
                logger.info(f"Phase '{phase_name}' is disabled, skipping")
                result.phases.append(PhaseResult(
                    phase=phase_name,
                    status='skipped',
                ))
                continue

            phase_config = self.config.get_phase_config(phase_name)

            if dry_run:
                logger.info(f"[DRY RUN] Would execute phase: {phase_name}")
                result.phases.append(PhaseResult(
                    phase=phase_name,
                    status='dry_run',
                    details={'config': phase_config},
                ))
                continue

            # Execute phase
            handler = self.handlers.get(phase_name)
            if handler is None:
                logger.error(f"No handler for phase: {phase_name}")
                result.phases.append(PhaseResult(
                    phase=phase_name,
                    status='failed',
                    errors=[f"No handler registered for phase: {phase_name}"],
                ))
                continue

            try:
                logger.info(f"Executing phase: {phase_name}")
                phase_result = handler.execute(phase_config)
                result.phases.append(phase_result)

                # Stop on error unless continue_on_error is set
                if phase_result.status == 'failed':
                    if not self.config.execution.get('continue_on_error', False):
                        logger.error(f"Phase '{phase_name}' failed, stopping pipeline")
                        break

            except Exception as e:
                logger.exception(f"Phase '{phase_name}' raised exception")
                result.phases.append(PhaseResult(
                    phase=phase_name,
                    status='failed',
                    errors=[str(e)],
                ))
                if not self.config.execution.get('continue_on_error', False):
                    break

        result.complete()
        return result

    def get_status(self) -> Dict:
        """Get current pipeline status."""
        if self.config is None:
            self.load_config()

        status = {
            'config_path': str(self.config_path),
            'config_exists': self.config_path.exists(),
            'phases': {},
        }

        for phase in self.PHASE_ORDER:
            phase_config = self.config.get_phase_config(phase)
            status['phases'][phase] = {
                'enabled': self.config.is_phase_enabled(phase),
                'handler': self.handlers.get(phase).__class__.__name__ if phase in self.handlers else 'None',
                'config': phase_config,
            }

        return status

    def print_status(self):
        """Print human-readable status."""
        status = self.get_status()

        print("=" * 60)
        print("ENGINE STATUS")
        print("=" * 60)
        print(f"Config: {status['config_path']}")
        print(f"Exists: {status['config_exists']}")
        print()
        print("PHASES")
        print("-" * 40)

        for phase, info in status['phases'].items():
            enabled = "+" if info['enabled'] else "-"
            handler = info['handler']
            print(f"  [{enabled}] {phase:12} - {handler}")

        print("=" * 60)

    def print_config(self):
        """Print current configuration."""
        if self.config is None:
            self.load_config()

        print("=" * 60)
        print("ENGINE CONFIGURATION")
        print("=" * 60)
        print(yaml.dump({
            'phases': self.config.phases,
            'execution': self.config.execution,
            'logging': self.config.logging,
        }, default_flow_style=False))
        print("=" * 60)


# ============================================================================
# CLI
# ============================================================================

def main():
    """Command-line interface for engine runner."""
    parser = argparse.ArgumentParser(
        description='ETL Pipeline Engine Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python engine_runner.py                    # Run all enabled phases
    python engine_runner.py --phase extract    # Run specific phase
    python engine_runner.py --status           # Show pipeline status
    python engine_runner.py --config           # Show current config
    python engine_runner.py --dry-run          # Preview without executing
        """
    )

    parser.add_argument(
        '--phase',
        choices=['extract', 'transform', 'validate', 'enrich', 'load'],
        help='Run specific phase only',
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show pipeline status',
    )
    parser.add_argument(
        '--config',
        action='store_true',
        help='Show current configuration',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview without executing',
    )
    parser.add_argument(
        '--config-path',
        type=Path,
        default=Path('ENGINE_CONFIG.yaml'),
        help='Path to ENGINE_CONFIG.yaml',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output',
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )

    # Create runner
    runner = EngineRunner(config_path=args.config_path)

    try:
        runner.load_config()
    except FileNotFoundError:
        print(f"ERROR: Configuration not found: {args.config_path}")
        print("Create ENGINE_CONFIG.yaml or specify path with --config-path")
        sys.exit(1)

    # Handle commands
    if args.status:
        runner.print_status()
        return

    if args.config:
        runner.print_config()
        return

    # Run pipeline
    result = runner.run(phase=args.phase, dry_run=args.dry_run)

    # Print results
    print()
    print("=" * 60)
    print("PIPELINE RESULTS")
    print("=" * 60)
    print(f"Status: {result.status.upper()}")
    print(f"Duration: {result.duration_seconds:.2f}s")
    print(f"Records: {result.total_records}")
    print(f"Errors: {result.total_errors}")
    print()
    print("PHASE RESULTS")
    print("-" * 40)

    for phase_result in result.phases:
        icon = {
            'success': '+',
            'failed': 'x',
            'skipped': '-',
            'partial': '~',
            'dry_run': '?',
        }.get(phase_result.status, '?')

        print(f"  [{icon}] {phase_result.phase:12} - {phase_result.status}")
        if phase_result.records_processed > 0:
            print(f"        Records: {phase_result.records_processed}")
        if phase_result.errors:
            for error in phase_result.errors:
                print(f"        Error: {error}")

    print("=" * 60)

    # Exit with error code if failed
    if result.status == 'failed':
        sys.exit(1)


if __name__ == '__main__':
    main()
