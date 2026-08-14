"""
Mock job source used for development and testing.
"""

from typing import Any

from .base import JobSource


class MockJobSource(JobSource):
    """Return deterministic sample jobs."""

    def fetch_jobs(self) -> list[dict[str, Any]]:
        return [
            {
                "title": "Data Analyst",
                "company": "Example Analytics",
                "location": "Mumbai",
                "remote": "Remote",
                "job_type": "Full-time",
                "required_years": "0 years",
                "skills": "SQL, Power BI, Python",
                "url": "https://example.com/jobs/data-analyst-001/",
                "source": "Mock",
            },
            {
                "title": "BI Analyst",
                "company": "Business Intelligence Corp",
                "location": "Mumbai",
                "remote": "Hybrid",
                "job_type": "Full-time",
                "required_years": "1 year",
                "skills": "SQL, Tableau, Power BI",
                "url": "https://example.com/jobs/bi-analyst-001/",
                "source": "Mock",
            },
            {
                "title": "Senior Data Analyst",
                "company": "Senior Analytics Corp",
                "location": "Mumbai",
                "remote": "On-site",
                "job_type": "Full-time",
                "required_years": "5 years",
                "skills": "SQL, Python, Tableau",
                "url": "https://example.com/jobs/senior-data-analyst-001/",
                "source": "Mock",
            },
        ]