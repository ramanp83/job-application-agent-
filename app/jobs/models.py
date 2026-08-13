"""
Job data model.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    title: str
    company: str

    location: Optional[str] = None
    remote: bool = False

    job_type: Optional[str] = None

    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None

    required_years: Optional[float] = None
    seniority: Optional[str] = None

    skills: Optional[str] = None
    description: Optional[str] = None

    url: Optional[str] = None
    source: Optional[str] = None

    date_posted: Optional[str] = None
    date_discovered: Optional[str] = None

    match_score: Optional[int] = None
    decision: Optional[str] = None

    application_status: str = "not_applied"
    applied_at: Optional[str] = None