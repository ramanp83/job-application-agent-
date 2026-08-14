"""
Job ingestion pipeline.

Connects a job source to normalization, matching,
and database persistence.
"""

import json
from pathlib import Path
from typing import Any

from app.jobs.models import Job
from app.jobs.normalizer import normalize_job
from app.jobs.repository import insert_job_if_new
from app.matching.scorer import calculate_match

from .base import JobSource


PROFILE_PATH = Path("app/config/profile.json")


def load_profile() -> dict[str, Any]:
    """Load the candidate profile used for job matching."""

    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def run_ingestion(source: JobSource) -> dict[str, Any]:
    """
    Fetch jobs from a source, normalize them, match them
    against the candidate profile, and persist new jobs.

    Returns:
        Summary containing fetched, inserted, duplicate,
        and failed counts.
    """

    profile = load_profile()

    fetched = 0
    inserted = 0
    duplicates = 0
    failed = 0

    for raw_job in source.fetch_jobs():
        fetched += 1

        try:
            normalized = normalize_job(raw_job)

            match_result = calculate_match(
                normalized,
                profile,
            )

            normalized["skills"] = ", ".join(
                normalized["skills"]
            )

            normalized["match_score"] = match_result["score"]
            normalized["decision"] = match_result["decision"]

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