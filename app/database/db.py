"""
Database connection and initialization utilities.
"""

import sqlite3
from pathlib import Path

from .schema import CREATE_JOBS_TABLE


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "jobs.db"


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite database connection."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """Create required database tables."""

    with get_connection() as connection:
        connection.execute(CREATE_JOBS_TABLE)
        connection.commit()