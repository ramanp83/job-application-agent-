from app.database.db import initialize_database
from app.jobs.models import Job
from app.jobs.normalizer import normalize_job
from app.jobs.repository import (
    count_jobs,
    insert_job_if_new,
)


def create_job_from_raw(raw_job: dict) -> Job:
    """Convert raw portal data into our Job model."""

    normalized = normalize_job(raw_job)

    return Job(
        title=normalized["title"],
        company=normalized["company"],
        location=normalized["location"],
        remote=normalized["remote"],
        job_type=normalized["job_type"],
        salary_min=normalized["salary_min"],
        salary_max=normalized["salary_max"],
        currency=normalized["currency"],
        required_years=normalized["required_years"],
        seniority=normalized["seniority"],
        skills=", ".join(normalized["skills"]),
        description=normalized["description"],
        url=normalized["url"],
        source=normalized["source"],
        date_posted=normalized["date_posted"],
    )


def test_raw_job_to_database_pipeline(test_database):
    raw_job = {
        "title": "  Junior Data Analyst ",
        "company": " Example Analytics ",
        "location": " Mumbai ",
        "remote": "Fully Remote",
        "job_type": "full time",
        "required_years": "0-1 years",
        "skills": "SQL, PowerBI, Python, SQL",
        "url": "https://example.com/jobs/data-analyst-001/",
        "source": " LinkedIn ",
    }

    job = create_job_from_raw(raw_job)

    result = insert_job_if_new(job)

    assert result["status"] == "inserted"
    assert result["job_id"] > 0
    assert count_jobs() == 1


def test_same_raw_job_is_detected_as_duplicate(test_database):
    raw_job = {
        "title": "Data Analyst",
        "company": "Example Analytics",
        "location": "Mumbai",
        "remote": "Remote",
        "job_type": "Full-time",
        "required_years": "0 years",
        "skills": "SQL, Power BI, Python",
        "url": "https://example.com/jobs/data-analyst-002/",
        "source": "Indeed",
    }

    first_job = create_job_from_raw(raw_job)
    first_result = insert_job_if_new(first_job)

    second_job = create_job_from_raw(raw_job)
    second_result = insert_job_if_new(second_job)

    assert first_result["status"] == "inserted"
    assert second_result["status"] == "duplicate"
    assert second_result["job_id"] == first_result["job_id"]

    assert count_jobs() == 1


def test_two_different_jobs_are_stored(test_database):
    raw_job_1 = {
        "title": "Data Analyst",
        "company": "Company A",
        "location": "Mumbai",
        "remote": "Hybrid",
        "job_type": "Full-time",
        "required_years": "0 years",
        "skills": "SQL, Power BI",
        "url": "https://example.com/jobs/001",
        "source": "LinkedIn",
    }

    raw_job_2 = {
        "title": "BI Analyst",
        "company": "Company B",
        "location": "Mumbai",
        "remote": "Remote",
        "job_type": "Full-time",
        "required_years": "1 year",
        "skills": "SQL, Tableau",
        "url": "https://example.com/jobs/002",
        "source": "Indeed",
    }

    result_1 = insert_job_if_new(create_job_from_raw(raw_job_1))
    result_2 = insert_job_if_new(create_job_from_raw(raw_job_2))

    assert result_1["status"] == "inserted"
    assert result_2["status"] == "inserted"

    assert result_1["job_id"] != result_2["job_id"]
    assert count_jobs() == 2


def test_normalization_happens_before_storage(test_database):
    raw_job = {
        "title": "   Data   Analyst   ",
        "company": "   Test   Company   ",
        "location": " Mumbai ",
        "remote": "Work From Home",
        "job_type": "full time",
        "required_years": "Fresher",
        "skills": "SQL, mysql, PowerBI",
        "url": "https://example.com/jobs/003/",
        "source": " LinkedIn ",
    }

    job = create_job_from_raw(raw_job)

    result = insert_job_if_new(job)

    assert result["status"] == "inserted"