"""
Pipeline Configuration

Configure sources, transforms, and destination settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# =============================================================================
# Supabase Configuration
# =============================================================================

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# =============================================================================
# Source Configuration
# =============================================================================

SOURCES = {
    # API source example
    "api": {
        "type": "api",
        "url": os.getenv("API_BASE_URL", "https://api.example.com"),
        "api_key": os.getenv("API_KEY", ""),
        "endpoints": {
            "items": "/v1/items",
            "categories": "/v1/categories",
        },
        "rate_limit": 100,  # requests per minute
    },

    # CSV source example
    "csv": {
        "type": "csv",
        "path": "data/sources/",
        "files": ["items.csv", "categories.csv"],
        "encoding": "utf-8",
    },

    # Database source example
    "database": {
        "type": "database",
        "connection_string": os.getenv("SOURCE_DATABASE_URL", ""),
        "tables": ["items", "categories"],
    },
}

# =============================================================================
# Transform Configuration
# =============================================================================

TRANSFORMS = {
    # Transform pipeline order
    "pipeline": ["clean", "normalize", "validate", "dedupe"],

    # Clean transform settings
    "clean": {
        "strip_whitespace": True,
        "remove_nulls": False,
        "lowercase_fields": ["category", "type"],
    },

    # Normalize transform settings
    "normalize": {
        "date_format": "%Y-%m-%d",
        "decimal_places": 2,
        "field_mappings": {
            # "source_field": "target_field"
        },
    },

    # Dedupe transform settings
    "dedupe": {
        "key_fields": ["id"],
        "strategy": "keep_latest",  # keep_first, keep_latest
    },
}

# =============================================================================
# Validation Configuration
# =============================================================================

VALIDATION = {
    "rules": {
        "id": {"required": True, "type": "int"},
        "name": {"required": True, "type": "str", "max_length": 255},
        "created_at": {"required": False, "type": "datetime"},
    },
    "on_failure": "skip",  # skip, fail, log
}

# =============================================================================
# Load Configuration
# =============================================================================

LOAD = {
    # Staging database (SQLite)
    "staging": {
        "enabled": True,
        "database": "data/staging.db",
        "table_prefix": "stg_",
    },

    # Supabase destination
    "destination": {
        "type": "supabase",
        "table": "items",
        "upsert_key": "id",
    },

    # Sync settings
    "sync": {
        "mode": "incremental",  # incremental, full
        "batch_size": 100,
        "dirty_column": "sync_status",  # for dirty-row pattern
        "updated_at_column": "updated_at",
    },
}

# =============================================================================
# Logging Configuration
# =============================================================================

LOGGING = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "json",  # json, text
    "output": "stdout",  # stdout, file
    "file_path": "logs/pipeline.log",
}

# =============================================================================
# Pipeline Configuration (Combined)
# =============================================================================

CONFIG = {
    "supabase": {
        "url": SUPABASE_URL,
        "service_key": SUPABASE_SERVICE_KEY,
        "anon_key": SUPABASE_ANON_KEY,
    },
    "sources": SOURCES,
    "transforms": TRANSFORMS,
    "validation": VALIDATION,
    "load": LOAD,
    "logging": LOGGING,
}
