"""
Pipeline Orchestrator

Main entry point for ETL pipeline execution.

Usage:
    python pipeline.py --source api --table items
    python pipeline.py --source csv --full-sync
"""

import argparse
import logging
from datetime import datetime
from typing import Any

from config import CONFIG
from extract.base import Extractor
from transform.base import Transformer
from load.staging import StagingLoader
from load.supabase_sync import SupabaseSync
from validate.validators import Validator

# Configure logging
logging.basicConfig(
    level=getattr(logging, CONFIG["logging"]["level"]),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Pipeline:
    """
    ETL Pipeline Orchestrator.

    Coordinates Extract → Transform → Validate → Load flow.
    """

    def __init__(self, config: dict = None):
        self.config = config or CONFIG
        self.extractor = None
        self.transformer = Transformer(self.config.get("transforms", {}))
        self.validator = Validator(self.config.get("validation", {}))
        self.staging = StagingLoader(self.config.get("load", {}).get("staging", {}))
        self.sync = SupabaseSync(self.config)
        self.stats = {
            "extracted": 0,
            "transformed": 0,
            "validated": 0,
            "loaded": 0,
            "errors": 0,
        }

    def run(
        self,
        source: str,
        table: str = None,
        full_sync: bool = False,
    ) -> dict:
        """
        Run the complete ETL pipeline.

        Args:
            source: Source name from config
            table: Destination table (overrides config)
            full_sync: If True, sync all records; else incremental

        Returns:
            Pipeline execution statistics
        """
        start_time = datetime.now()
        logger.info(f"Starting pipeline: source={source}, table={table}")

        try:
            # Step 1: Extract
            logger.info("Step 1: Extracting data...")
            raw_data = self._extract(source)
            self.stats["extracted"] = len(raw_data)
            logger.info(f"Extracted {len(raw_data)} records")

            if not raw_data:
                logger.warning("No data extracted, skipping pipeline")
                return self.stats

            # Step 2: Transform
            logger.info("Step 2: Transforming data...")
            transformed_data = self._transform(raw_data)
            self.stats["transformed"] = len(transformed_data)
            logger.info(f"Transformed {len(transformed_data)} records")

            # Step 3: Validate
            logger.info("Step 3: Validating data...")
            valid_data, invalid_data = self._validate(transformed_data)
            self.stats["validated"] = len(valid_data)
            self.stats["errors"] = len(invalid_data)
            logger.info(f"Validated {len(valid_data)} records, {len(invalid_data)} errors")

            # Step 4: Stage (optional)
            if self.config.get("load", {}).get("staging", {}).get("enabled"):
                logger.info("Step 4a: Staging data...")
                self._stage(valid_data, table or self.config["load"]["destination"]["table"])

            # Step 5: Load to Supabase
            logger.info("Step 5: Loading to Supabase...")
            dest_table = table or self.config["load"]["destination"]["table"]
            loaded = self._load(valid_data, dest_table, full_sync)
            self.stats["loaded"] = loaded
            logger.info(f"Loaded {loaded} records to {dest_table}")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.stats["errors"] += 1
            raise

        finally:
            duration = (datetime.now() - start_time).total_seconds()
            self.stats["duration_seconds"] = duration
            logger.info(f"Pipeline completed in {duration:.2f}s")
            logger.info(f"Stats: {self.stats}")

        return self.stats

    def _extract(self, source: str) -> list[dict]:
        """Extract data from source."""
        source_config = self.config["sources"].get(source)
        if not source_config:
            raise ValueError(f"Unknown source: {source}")

        self.extractor = Extractor(source_config)
        return self.extractor.extract()

    def _transform(self, data: list[dict]) -> list[dict]:
        """Transform extracted data."""
        return self.transformer.transform(data)

    def _validate(self, data: list[dict]) -> tuple[list[dict], list[dict]]:
        """Validate transformed data."""
        return self.validator.validate(data)

    def _stage(self, data: list[dict], table: str) -> None:
        """Stage data to SQLite."""
        self.staging.load(data, table)

    def _load(self, data: list[dict], table: str, full_sync: bool) -> int:
        """Load data to Supabase."""
        if full_sync:
            return self.sync.full_sync(data, table)
        return self.sync.incremental_sync(data, table)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="ETL Pipeline")
    parser.add_argument(
        "--source",
        required=True,
        help="Source name (api, csv, database)",
    )
    parser.add_argument(
        "--table",
        help="Destination table (overrides config)",
    )
    parser.add_argument(
        "--full-sync",
        action="store_true",
        help="Perform full sync instead of incremental",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without loading to Supabase",
    )

    args = parser.parse_args()

    pipeline = Pipeline()

    if args.dry_run:
        logger.info("DRY RUN - No data will be loaded")
        # Run extract and transform only
        raw = pipeline._extract(args.source)
        transformed = pipeline._transform(raw)
        valid, invalid = pipeline._validate(transformed)
        print(f"Would load {len(valid)} records to {args.table or CONFIG['load']['destination']['table']}")
        return

    stats = pipeline.run(
        source=args.source,
        table=args.table,
        full_sync=args.full_sync,
    )

    print(f"Pipeline completed: {stats}")


if __name__ == "__main__":
    main()
