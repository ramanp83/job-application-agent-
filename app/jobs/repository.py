"""
Database operations for jobs.
"""

import sqlite3
from datetime import datetime, timezone
from typing import Optional

from app.database.db import get_connection
from .models import Job


def _now() -> str:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def insert_job(job: Job) -> int:
    """Insert a new job and return its database ID.

    Raises:
        ValueError: If the job already exists.
    """

    now = _now()
    date_discovered = job.date_discovered or now

    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO jobs (
                    title,
                    company,
                    location,
                    remote,
                    job_type,
                    salary_min,
                    salary_max,
                    currency,
                    required_years,
                    seniority,
                    skills,
                    description,
                    url,
                    source,
                    date_posted,
                    date_discovered,
                    match_score,
                    decision,
                    application_status,
                    applied_at,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.title,
                    job.company,
                    job.location,
                    int(job.remote),
                    job.job_type,
                    job.salary_min,
                    job.salary_max,
                    job.currency,
                    job.required_years,
                    job.seniority,
                    job.skills,
                    job.description,
                    job.url,
                    job.source,
                    job.date_posted,
                    date_discovered,
                    job.match_score,
                    job.decision,
                    job.application_status,
                    job.applied_at,
                    now,
                    now,
                ),
            )

            connection.commit()

            return cursor.lastrowid

    except sqlite3.IntegrityError as error:
        if "UNIQUE constraint failed" in str(error):
            raise ValueError("Job already exists") from error

        raise


def get_job(job_id: int) -> Optional[dict]:
    """Retrieve a job by ID."""

    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,),
        ).fetchone()

    if row is None:
        return None

    return dict(row)


def count_jobs() -> int:
    """Return the number of stored jobs."""

    with get_connection() as connection:
        row = connection.execute(
            "SELECT COUNT(*) AS count FROM jobs"
        ).fetchone()

    return row["count"]


def find_job_by_url(url: str) -> Optional[dict]:
    """Find a job using its URL."""

    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM jobs WHERE url = ?",
            (url,),
        ).fetchone()

    if row is None:
        return None

    return dict(row)


def insert_job_if_new(job: Job) -> dict:
    """Insert a job if it does not already exist.

    Returns:
        A dictionary containing the operation result and job ID.
    """

    existing_job = find_job_by_url(job.url) if job.url else None

    if existing_job is not None:
        return {
            "status": "duplicate",
            "job_id": existing_job["id"],
        }

    job_id = insert_job(job)

    return {
        "status": "inserted",
        "job_id": job_id,
    }