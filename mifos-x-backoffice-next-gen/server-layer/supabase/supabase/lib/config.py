"""
Configuration module for Supabase CRUD Engine.
Loads environment variables and provides project settings.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@dataclass
class Config:
    """Configuration settings for Supabase connection."""

    supabase_url: str
    supabase_key: str
    db_url: str
    project_name: str
    environment: str

    # Paths
    project_root: Path
    design_layer_path: Path
    migrations_path: Path
    data_path: Path

    @classmethod
    def load(cls) -> 'Config':
        """Load configuration from environment variables."""

        # Required environment variables
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        db_url = os.getenv('SUPABASE_DB_URL')

        if not all([supabase_url, supabase_key, db_url]):
            missing = []
            if not supabase_url:
                missing.append('SUPABASE_URL')
            if not supabase_key:
                missing.append('SUPABASE_SERVICE_KEY')
            if not db_url:
                missing.append('SUPABASE_DB_URL')
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        # Optional variables
        project_name = os.getenv('PROJECT_NAME', 'unnamed-project')
        environment = os.getenv('ENVIRONMENT', 'development')

        # Calculate paths
        # Assuming we're in server-layer/supabase/
        current_dir = Path(__file__).parent.parent  # supabase/
        server_layer = current_dir.parent  # server-layer/
        project_root = server_layer.parent  # project root

        return cls(
            supabase_url=supabase_url,
            supabase_key=supabase_key,
            db_url=db_url,
            project_name=project_name,
            environment=environment,
            project_root=project_root,
            design_layer_path=project_root / 'idea-layer' / 'exports',
            migrations_path=current_dir / 'migrations',
            data_path=current_dir / 'data',
        )

    def get_feature_api_path(self, feature: str) -> Path:
        """Get the path to a feature's API.md file."""
        return self.design_layer_path / 'features' / feature / 'API.md'

    def get_all_feature_paths(self) -> list[Path]:
        """Get all feature directories in design layer."""
        features_dir = self.design_layer_path / 'features'
        if not features_dir.exists():
            return []
        return [d for d in features_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]

    def get_migration_files(self) -> list[Path]:
        """Get all migration files sorted by name."""
        if not self.migrations_path.exists():
            return []
        return sorted(self.migrations_path.glob('*.sql'))

    def __str__(self) -> str:
        return f"""Config:
  Project: {self.project_name}
  Environment: {self.environment}
  Supabase URL: {self.supabase_url}
  Project Root: {self.project_root}
  Design Layer: {self.design_layer_path}
  Migrations: {self.migrations_path}"""
