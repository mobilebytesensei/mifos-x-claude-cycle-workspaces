#!/usr/bin/env python3
"""
Supabase CRUD Engine - Master Orchestrator

Usage:
    python3 master.py <command>

Commands:
    status      Show current state (RPCs, migrations, data)
    check       Compare design layer APIs vs deployed RPCs
    sync-apis   Generate migrations for missing RPCs
    migrate     Apply pending migrations
    deploy      Run migrations + verify deployment
    sync-data   Sync reference data (catalogs, etc.)
    all         Full deployment (migrate + sync-data + verify)

Examples:
    python3 master.py status
    python3 master.py check
    python3 master.py sync-apis
    python3 master.py all
"""

import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.config import Config
from lib.db import Database
from lib.registry import RPCRegistry
from lib.edge import EdgeFunctions


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def print_section(title: str):
    """Print a section header."""
    print(f"\n--- {title} ---\n")


def cmd_status(config: Config, db: Database, registry: RPCRegistry):
    """Show current state of server layer."""
    print_header("Server Layer Status")

    # Configuration
    print_section("Configuration")
    print(f"  Project: {config.project_name}")
    print(f"  Environment: {config.environment}")
    print(f"  Supabase URL: {config.supabase_url}")

    # Connection test
    print_section("Connection")
    if db.test_connection():
        print("  Database: Connected")
    else:
        print("  Database: DISCONNECTED")
        return

    # Deployed RPCs
    print_section("Deployed RPCs")
    rpcs = db.get_deployed_rpcs()
    if rpcs:
        for rpc in rpcs:
            print(f"  - {rpc.name}({rpc.arguments}) -> {rpc.return_type}")
        print(f"\n  Total: {len(rpcs)} RPCs")
    else:
        print("  No RPCs deployed")

    # Required RPCs
    print_section("Required RPCs (from Design Layer)")
    required = registry.get_required_rpcs()
    if required:
        for rpc in required:
            status = "deployed" if rpc.name in db.get_rpc_names() else "MISSING"
            print(f"  - {rpc.name} [{rpc.feature}] - {status}")
        print(f"\n  Total: {len(required)} required")
    else:
        print("  No APIs defined in design layer")

    # Migrations
    print_section("Migrations")
    migrations = config.get_migration_files()
    if migrations:
        for m in migrations:
            print(f"  - {m.name}")
        print(f"\n  Total: {len(migrations)} migration files")
    else:
        print("  No migrations yet")

    # Tables
    print_section("Database Tables")
    tables = db.get_tables()
    if tables:
        for t in tables:
            print(f"  - {t}")
        print(f"\n  Total: {len(tables)} tables")
    else:
        print("  No tables found")


def cmd_check(config: Config, db: Database, registry: RPCRegistry):
    """Compare design layer APIs vs deployed RPCs."""
    print_header("API Check: Design Layer vs Deployed RPCs")

    # Get required and deployed
    required = registry.get_required_rpcs()
    deployed = db.get_rpc_names()

    if not required:
        print("\n  No APIs defined in design layer.")
        print("  Add endpoints to idea-layer/exports/{feature}/API.md")
        return

    # Check each required RPC
    print_section("RPC Status")
    missing = []
    found = []

    for rpc in required:
        if rpc.name in deployed:
            found.append(rpc)
            print(f"  [OK] {rpc.name} [{rpc.feature}]")
        else:
            missing.append(rpc)
            print(f"  [MISSING] {rpc.name} [{rpc.feature}]")

    # Summary
    print_section("Summary")
    print(f"  Required: {len(required)}")
    print(f"  Deployed: {len(found)}")
    print(f"  Missing: {len(missing)}")

    if missing:
        print("\n  Run 'python3 master.py sync-apis' to generate migrations")
    else:
        print("\n  All design layer APIs have corresponding RPCs")


def cmd_sync_apis(config: Config, db: Database, registry: RPCRegistry):
    """Generate migrations for missing RPCs."""
    print_header("Sync APIs: Generate Missing RPC Migrations")

    missing = registry.get_missing_rpcs()

    if not missing:
        print("\n  No missing RPCs. All APIs are implemented.")
        return

    print_section(f"Generating migrations for {len(missing)} missing RPCs")

    result = registry.sync_apis()

    for feature, paths in result.items():
        for path in paths:
            print(f"  Generated: {path.name}")

    print_section("Summary")
    total_files = sum(len(paths) for paths in result.values())
    print(f"  Generated {total_files} migration file(s)")
    print("\n  Run 'python3 master.py migrate' to apply")


def cmd_migrate(config: Config, db: Database, registry: RPCRegistry):
    """Apply pending migrations."""
    print_header("Migrate: Apply Pending Migrations")

    migrations = config.get_migration_files()

    if not migrations:
        print("\n  No pending migrations")
        return

    print_section(f"Applying {len(migrations)} migrations")

    applied, failed = db.apply_all_migrations()

    print_section("Summary")
    print(f"  Applied: {applied}")
    print(f"  Failed: {failed}")

    if failed > 0:
        print("\n  Some migrations failed. Check errors above.")
    else:
        print("\n  All migrations applied successfully")


def cmd_deploy(config: Config, db: Database, registry: RPCRegistry):
    """Run migrations + verify deployment."""
    print_header("Deploy: Migrations + Verification")

    # Run migrations
    print_section("Step 1: Apply Migrations")
    migrations = config.get_migration_files()
    if migrations:
        applied, failed = db.apply_all_migrations()
        print(f"  Applied: {applied}, Failed: {failed}")
    else:
        print("  No migrations to apply")

    # Verify
    print_section("Step 2: Verify Deployment")
    missing = registry.get_missing_rpcs()
    if missing:
        print(f"  WARNING: {len(missing)} RPCs still missing:")
        for rpc in missing:
            print(f"    - {rpc.name}")
    else:
        print("  All APIs implemented")

    print_section("Deployment Complete")


def cmd_sync_data(config: Config, db: Database, registry: RPCRegistry):
    """Sync reference data (catalogs, etc.)."""
    print_header("Sync Data: Reference Data Synchronization")

    data_scripts = list(config.data_path.glob('sync_*.py'))

    if not data_scripts:
        print("\n  No data sync scripts found.")
        print(f"  Add scripts to: {config.data_path}/sync_*.py")
        return

    print_section(f"Running {len(data_scripts)} sync scripts")

    for script in sorted(data_scripts):
        print(f"\n  Running: {script.name}")
        try:
            # Execute the script
            exec(script.read_text(), {'config': config, 'db': db})
            print(f"    Completed")
        except Exception as e:
            print(f"    Error: {e}")

    print_section("Data Sync Complete")


def cmd_all(config: Config, db: Database, registry: RPCRegistry):
    """Full deployment (sync-apis + migrate + sync-data + verify)."""
    print_header("Full Deployment")

    # Step 1: Sync APIs
    print("\n[1/4] Syncing APIs...")
    missing = registry.get_missing_rpcs()
    if missing:
        registry.sync_apis()
        print(f"  Generated migrations for {len(missing)} RPCs")
    else:
        print("  No missing APIs")

    # Step 2: Migrate
    print("\n[2/4] Applying migrations...")
    migrations = config.get_migration_files()
    if migrations:
        applied, failed = db.apply_all_migrations()
        print(f"  Applied: {applied}, Failed: {failed}")
    else:
        print("  No migrations")

    # Step 3: Sync data
    print("\n[3/4] Syncing data...")
    data_scripts = list(config.data_path.glob('sync_*.py'))
    if data_scripts:
        for script in sorted(data_scripts):
            try:
                exec(script.read_text(), {'config': config, 'db': db})
            except Exception as e:
                print(f"  Error in {script.name}: {e}")
        print(f"  Ran {len(data_scripts)} sync scripts")
    else:
        print("  No data scripts")

    # Step 4: Verify
    print("\n[4/4] Verifying deployment...")
    still_missing = registry.get_missing_rpcs()
    if still_missing:
        print(f"  WARNING: {len(still_missing)} APIs still missing")
    else:
        print("  All APIs implemented")

    print_section("DEPLOYMENT COMPLETE")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    # Load configuration
    try:
        config = Config.load()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nMake sure .env file exists with required variables.")
        print("See .env.example for template.")
        sys.exit(1)

    # Initialize components
    db = Database(config)
    registry = RPCRegistry(config, db)

    # Route command
    commands = {
        'status': cmd_status,
        'check': cmd_check,
        'sync-apis': cmd_sync_apis,
        'migrate': cmd_migrate,
        'deploy': cmd_deploy,
        'sync-data': cmd_sync_data,
        'all': cmd_all,
    }

    if command in commands:
        commands[command](config, db, registry)
    else:
        print(f"Unknown command: {command}")
        print(f"Available commands: {', '.join(commands.keys())}")
        sys.exit(1)


if __name__ == '__main__':
    main()
