"""
Arbeitnow job-board API source.
"""

from typing import Any

import requests

from .base import JobSource


class ArbeitnowJobSource(JobSource):
    """Fetch jobs from the public Arbeitnow job-board API."""

    API_URL = "https://arbeitnow.com/api/job-board-api"

    def __init__(
        self,
        timeout: int = 10,
        session: requests.Session | None = None,
    ) -> None:
        self.timeout = timeout
        self.session = session or requests.Session()

    def fetch_jobs(self) -> list[dict[str, Any]]:
        """Fetch raw jobs from Arbeitnow."""

        response = self.session.get(
            self.API_URL,
            timeout=self.timeout,
        )

        response.raise_for_status()

        payload = response.json()

        if isinstance(payload, dict):
            jobs = payload.get("data", [])
        elif isinstance(payload, list):
            jobs = payload
        else:
            raise ValueError("Unexpected Arbeitnow API response")

        if not isinstance(jobs, list):
            raise ValueError("Invalid jobs payload")

        return [self._normalize_raw_job(job) for job in jobs]

    @staticmethod
    def _normalize_raw_job(job: dict[str, Any]) -> dict[str, Any]:
        """Map Arbeitnow fields into our internal raw-job format."""

        return {
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "remote": job.get("remote"),
            "job_type": job.get("job_types"),
            "required_years": None,
            "skills": job.get("tags", []),
            "description": job.get("description"),
            "url": job.get("url"),
            "source": "Arbeitnow",
            "date_posted": job.get("created_at"),
        }