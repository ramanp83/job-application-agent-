import pytest

from app.database.db import get_connection, initialize_database
from app.jobs.models import Job
from app.jobs.repository import (
    count_jobs,
    find_job_by_url,
    get_job,
    insert_job,
    insert_job_if_new,
)


def test_insert_job(test_database):
    job = Job(
        title="Data Analyst",
        company="Test Company",
        location="Mumbai",
        remote=False,
        job_type="Full-time",
        required_years=0,
        skills="SQL, Power BI",
        url="https://example.com/jobs/1",
        source="LinkedIn",
    )

    job_id = insert_job(job)

    assert job_id == 1
    assert count_jobs() == 1


def test_get_job(test_database):
    job = Job(
        title="BI Analyst",
        company="Test Company",
        location="Mumbai",
        remote=True,
        job_type="Full-time",
        required_years=1,
        skills="SQL, Tableau",
        url="https://example.com/jobs/2",
        source="Indeed",
    )

    job_id = insert_job(job)

    stored_job = get_job(job_id)

    assert stored_job is not None
    assert stored_job.title == "BI Analyst"
    assert stored_job.company == "Test Company"
    assert stored_job.location == "Mumbai"


def test_find_job_by_url(test_database):
    job = Job(
        title="Junior Data Analyst",
        company="Analytics Company",
        location="Mumbai",
        remote=True,
        job_type="Internship",
        required_years=0,
        skills="SQL, Python",
        url="https://example.com/jobs/3",
        source="Wellfound",
    )

    insert_job(job)

    stored_job = find_job_by_url("https://example.com/jobs/3")

    assert stored_job is not None
    assert stored_job.title == "Junior Data Analyst"


def test_duplicate_job_is_rejected(test_database):
    job = Job(
        title="Data Analyst",
        company="Duplicate Company",
        location="Mumbai",
        remote=False,
        job_type="Full-time",
        required_years=0,
        skills="SQL",
        url="https://example.com/jobs/duplicate",
        source="LinkedIn",
    )

    insert_job(job)

    with pytest.raises(Exception):
        insert_job(job)

    assert count_jobs() == 1


def test_insert_job_if_new(test_database):
    job = Job(
        title="Reporting Analyst",
        company="Reporting Company",
        location="Mumbai",
        remote=True,
        job_type="Full-time",
        required_years=0,
        skills="Excel, Power BI",
        url="https://example.com/jobs/4",
        source="Naukri",
    )

    first_result = insert_job_if_new(job)
    second_result = insert_job_if_new(job)

    assert first_result["status"] == "inserted"
    assert second_result["status"] == "duplicate"

    assert first_result["job_id"] == second_result["job_id"]
    assert count_jobs() == 1