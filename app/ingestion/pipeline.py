"""
Job ingestion pipeline.

Connects a job source to normalization and database persistence.
"""

from typing import Any

from app.jobs.models import Job
from app.jobs.normalizer import normalize_job
from app.jobs.repository import insert_job_if_new

from .base import JobSource


def run_ingestion(source: JobSource) -> dict[str, Any]:
    """
    Fetch jobs from a source, normalize them, and persist new jobs.

    Returns:
        Summary containing fetched, inserted, duplicate, and failed counts.
    """

    fetched = 0
    inserted = 0
    duplicates = 0
    failed = 0

    for raw_job in source.fetch_jobs():
        fetched += 1

        try:
            normalized = normalize_job(raw_job)

            normalized["skills"] = ", ".join(normalized["skills"])

            job = Job(**normalized)

            result = insert_job_if_new(job)

            if result["status"] == "inserted":
                inserted += 1
            elif result["status"] == "duplicate":
                duplicates += 1

        except (KeyError, TypeError, ValueError):
            failed += 1

    return {
        "fetched": fetched,
        "inserted": inserted,
        "duplicates": duplicates,
        "failed": failed,
    }