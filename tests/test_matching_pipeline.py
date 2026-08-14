import json
from pathlib import Path

from app.jobs.normalizer import normalize_job
from app.matching.scorer import calculate_match


PROFILE_PATH = Path("app/config/profile.json")


def load_profile():
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_normalized_job_can_be_matched_against_profile():
    profile = load_profile()

    raw_job = {
        "title": "Data Analyst",
        "company": "Example Analytics",
        "location": "Mumbai",
        "remote": "Remote",
        "job_type": "Full-time",
        "required_years": "0 years",
        "skills": "SQL, Power BI, Python",
        "url": "https://example.com/jobs/data-analyst-001/",
        "source": "Mock",
    }

    job = normalize_job(raw_job)

    result = calculate_match(job, profile)

    assert result["score"] >= 80
    assert result["decision"] == "APPLY"