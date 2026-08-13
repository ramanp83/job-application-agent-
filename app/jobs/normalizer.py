"""
Utilities for normalizing raw job data into a consistent format.
"""

import re
from typing import Any


REMOTE_TRUE_VALUES = {
    "remote",
    "fully remote",
    "100% remote",
    "work from home",
    "wfh",
    "remote only",
}

REMOTE_FALSE_VALUES = {
    "onsite",
    "on-site",
    "office",
    "in office",
    "hybrid",
}


JOB_TYPE_MAP = {
    "full time": "Full-time",
    "full-time": "Full-time",
    "fulltime": "Full-time",
    "permanent": "Full-time",

    "part time": "Part-time",
    "part-time": "Part-time",
    "parttime": "Part-time",

    "intern": "Internship",
    "internship": "Internship",

    "contract": "Contract",
    "contractual": "Contract",
}


SKILL_MAP = {
    "sql": "SQL",
    "mysql": "MySQL",
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "microsoft power bi": "Power BI",
    "tableau": "Tableau",
    "python": "Python",
    "excel": "Microsoft Excel",
    "microsoft excel": "Microsoft Excel",
    "dax": "DAX",
    "power query": "Power Query",
}


def clean_text(value: Any) -> str | None:
    """Remove unnecessary whitespace from text."""

    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    return re.sub(r"\s+", " ", text)


def normalize_title(title: Any) -> str | None:
    """Normalize a job title."""

    return clean_text(title)


def normalize_company(company: Any) -> str | None:
    """Normalize a company name."""

    return clean_text(company)


def normalize_location(location: Any) -> str | None:
    """Normalize a job location."""

    return clean_text(location)


def normalize_remote(value: Any) -> bool:
    """Convert different remote representations into a boolean."""

    if isinstance(value, bool):
        return value

    if value is None:
        return False

    normalized = clean_text(value)

    if normalized is None:
        return False

    normalized = normalized.lower()

    if normalized in REMOTE_TRUE_VALUES:
        return True

    if normalized in REMOTE_FALSE_VALUES:
        return False

    return "remote" in normalized or "work from home" in normalized


def normalize_job_type(job_type: Any) -> str | None:
    """Normalize common job type representations."""

    value = clean_text(job_type)

    if value is None:
        return None

    key = value.lower()

    return JOB_TYPE_MAP.get(key, value)


def normalize_experience(value: Any) -> float | None:
    """Convert experience requirements into a numeric value."""

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = clean_text(value)

    if text is None:
        return None

    text = text.lower()

    if "fresher" in text or "no experience" in text:
        return 0.0

    match = re.search(r"(\d+(?:\.\d+)?)", text)

    if match:
        return float(match.group(1))

    return None


def normalize_skills(skills: Any) -> list[str]:
    """Normalize skills and remove duplicates."""

    if skills is None:
        return []

    if isinstance(skills, str):
        raw_skills = re.split(r",|;|\n|\|", skills)
    else:
        raw_skills = skills

    normalized_skills = []
    seen = set()

    for skill in raw_skills:
        cleaned = clean_text(skill)

        if cleaned is None:
            continue

        key = cleaned.lower()

        canonical = SKILL_MAP.get(key, cleaned)

        if canonical.lower() not in seen:
            normalized_skills.append(canonical)
            seen.add(canonical.lower())

    return normalized_skills


def normalize_url(url: Any) -> str | None:
    """Normalize a job URL."""

    value = clean_text(url)

    if value is None:
        return None

    return value.rstrip("/")


def normalize_job(raw_job: dict) -> dict:
    """Normalize a raw job dictionary."""

    return {
        "title": normalize_title(raw_job.get("title")),
        "company": normalize_company(raw_job.get("company")),
        "location": normalize_location(raw_job.get("location")),
        "remote": normalize_remote(raw_job.get("remote")),
        "job_type": normalize_job_type(raw_job.get("job_type")),
        "salary_min": raw_job.get("salary_min"),
        "salary_max": raw_job.get("salary_max"),
        "currency": clean_text(raw_job.get("currency")),
        "required_years": normalize_experience(
            raw_job.get("required_years")
        ),
        "seniority": clean_text(raw_job.get("seniority")),
        "skills": normalize_skills(raw_job.get("skills")),
        "description": clean_text(raw_job.get("description")),
        "url": normalize_url(raw_job.get("url")),
        "source": clean_text(raw_job.get("source")),
        "date_posted": clean_text(raw_job.get("date_posted")),
    }