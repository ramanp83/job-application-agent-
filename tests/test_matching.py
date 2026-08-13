import json
from pathlib import Path

from app.matching.scorer import calculate_match


PROFILE_PATH = Path("app/config/profile.json")


def load_profile():
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_excellent_data_analyst_match():
    profile = load_profile()

    job = {
        "title": "Data Analyst",
        "location": "Mumbai",
        "job_type": "Full-time",
        "required_years": 0,
        "skills": [
            "SQL",
            "Power BI",
            "Python",
            "Microsoft Excel",
            "Data Cleaning"
        ]
    }

    result = calculate_match(job, profile)

    assert result["score"] >= 80
    assert result["decision"] == "APPLY"


def test_bi_analyst_match():
    profile = load_profile()

    job = {
        "title": "BI Analyst",
        "location": "Mumbai",
        "job_type": "Full-time",
        "required_years": 1,
        "skills": [
            "SQL",
            "Power BI",
            "Tableau",
            "Data Visualization"
        ]
    }

    result = calculate_match(job, profile)

    assert result["score"] >= 80
    assert result["decision"] == "APPLY"


def test_senior_data_analyst_should_be_skipped():
    profile = load_profile()

    job = {
        "title": "Senior Data Analyst",
        "location": "Mumbai",
        "job_type": "Full-time",
        "required_years": 5,
        "seniority": "Senior",
        "skills": [
            "SQL",
            "Power BI",
            "Python",
            "Tableau"
        ]
    }

    result = calculate_match(job, profile)

    assert result["decision"] == "SKIP"


def test_unrelated_role_should_be_skipped():
    profile = load_profile()

    job = {
        "title": "Senior Graphic Designer",
        "location": "Mumbai",
        "job_type": "Full-time",
        "required_years": 5,
        "seniority": "Senior",
        "skills": [
            "Adobe Photoshop",
            "Illustrator",
            "Graphic Design"
        ]
    }

    result = calculate_match(job, profile)

    assert result["decision"] == "SKIP"