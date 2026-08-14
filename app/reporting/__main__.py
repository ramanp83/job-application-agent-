"""
Command-line entry point for the job matching report.
"""

from app.database.db import initialize_database
from app.reporting.reporter import print_report


def main() -> None:
    """Initialize the database and print the job report."""

    initialize_database()

    print_report()


if __name__ == "__main__":
    main()