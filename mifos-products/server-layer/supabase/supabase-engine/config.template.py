"""
Supabase Engine Configuration Template

Template Variables:
    {PROJECT_NAME}     - Project name (e.g., mood_movies)
    {POSTGRES_USER}    - PostgreSQL username
    {POSTGRES_PASSWORD}- PostgreSQL password
    {HOST_PORT}        - PostgreSQL port (default: 5432)
    {PRIMARY_TABLE}    - Main table name (e.g., movies)

Usage:
    1. Copy this file to your project's server-layer/supabase-engine/config.py
    2. Replace template variables with actual values
    3. Create .env file with secrets

Rule: RULE-ENGINE-AUTO-001
"""

import os
from pathlib import Path
from typing import Set

from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# =============================================================================
# Database Configuration (PostgreSQL)
# =============================================================================

# Local PostgreSQL (Docker)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{HOST_PORT}/{PROJECT_NAME}"
)

# Parse for individual components if needed
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "{HOST_PORT}"))
DB_NAME = os.getenv("DB_NAME", "{PROJECT_NAME}")
DB_USER = os.getenv("DB_USER", "{POSTGRES_USER}")
DB_PASSWORD = os.getenv("DB_PASSWORD", "{POSTGRES_PASSWORD}")

# =============================================================================
# Supabase Configuration (Remote)
# =============================================================================

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# =============================================================================
# Sync Configuration
# =============================================================================

# Batch size for sync operations
# Higher = faster but more memory, lower = slower but memory-efficient
# Recommended: 1000 for ~2,500-4,000 records/second
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))

# Sync tracking columns (excluded from data sync)
SYNC_COLUMNS: Set[str] = {"sync_status", "sync_timestamp", "sync_error"}

# Primary table for this engine
PRIMARY_TABLE = "{PRIMARY_TABLE}"

# =============================================================================
# Data Directories
# =============================================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Source data directories (for extractors)
SOURCES_DIR = DATA_DIR / "sources"
SOURCES_DIR.mkdir(exist_ok=True)

# Exported data directory
EXPORTS_DIR = DATA_DIR / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

# =============================================================================
# Logging Configuration
# =============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # json, text
LOG_FILE = LOGS_DIR / "engine.log"

# =============================================================================
# Pipeline Configuration
# =============================================================================

CONFIG = {
    # Database connections
    "database": {
        "url": DATABASE_URL,
        "host": DB_HOST,
        "port": DB_PORT,
        "name": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
    },

    # Supabase remote
    "supabase": {
        "url": SUPABASE_URL,
        "service_key": SUPABASE_SERVICE_KEY,
        "anon_key": SUPABASE_ANON_KEY,
    },

    # Sync settings
    "sync": {
        "batch_size": BATCH_SIZE,
        "sync_columns": list(SYNC_COLUMNS),
        "primary_table": PRIMARY_TABLE,
        "mode": "incremental",  # incremental, full
        "dirty_column": "sync_status",
        "updated_at_column": "updated_at",
    },

    # Directories
    "paths": {
        "base": str(BASE_DIR),
        "data": str(DATA_DIR),
        "logs": str(LOGS_DIR),
        "sources": str(SOURCES_DIR),
        "exports": str(EXPORTS_DIR),
    },

    # Logging
    "logging": {
        "level": LOG_LEVEL,
        "format": LOG_FORMAT,
        "file": str(LOG_FILE),
    },
}

# =============================================================================
# Validation
# =============================================================================

def validate_config() -> bool:
    """Validate required configuration is present."""
    errors = []

    if not SUPABASE_URL:
        errors.append("SUPABASE_URL is not set")
    if not SUPABASE_SERVICE_KEY:
        errors.append("SUPABASE_SERVICE_ROLE_KEY is not set")

    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    return True


# =============================================================================
# Example .env file content:
# =============================================================================
#
# # Local PostgreSQL (Docker)
# DATABASE_URL=postgresql://engine:local_dev@localhost:5432/mood_movies
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=mood_movies
# DB_USER=engine
# DB_PASSWORD=local_dev
#
# # Supabase Remote
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
# SUPABASE_ANON_KEY=your-anon-key
#
# # Sync Settings
# BATCH_SIZE=1000
# LOG_LEVEL=INFO
