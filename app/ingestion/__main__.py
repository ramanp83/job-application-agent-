"""
Command-line entry point for job ingestion.
"""

from app.database.db import initialize_database
from app.ingestion.arbeitnow_source import ArbeitnowJobSource
from app.ingestion.pipeline import run_ingestion


def main() -> None:
    """Initialize the database and run job ingestion."""

    initialize_database()

    source = ArbeitnowJobSource()

    result = run_ingestion(source)

    print("Job ingestion completed.")
    print(f"Fetched: {result['fetched']}")
    print(f"Inserted: {result['inserted']}")
    print(f"Duplicates: {result['duplicates']}")
    print(f"Failed: {result['failed']}")


if __name__ == "__main__":
    main()