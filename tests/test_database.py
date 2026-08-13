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


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Create an isolated SQLite database for each test."""

    database_path = tmp_path / "test_jobs.db"

    import app.database.db as db

    monkeypatch.setattr(db, "DATABASE_PATH", database_path)
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)

    initialize_database()

    yield database_path


def create_sample_job():
    return Job(
        title="Data Analyst",
        company="Example Company",
        location="Mumbai",
        remote=True,
        job_type="Full-time",
        required_years=0,
        skills="SQL, Power BI, Python",
        url="https://example.com/jobs/data-analyst-001",
        source="test",
    )


def test_insert_job(test_database):
    job = create_sample_job()

    job_id = insert_job(job)

    assert job_id is not None
    assert job_id > 0
    assert count_jobs() == 1


def test_get_job(test_database):
    job = create_sample_job()

    job_id = insert_job(job)
    stored_job = get_job(job_id)

    assert stored_job is not None
    assert stored_job["title"] == "Data Analyst"
    assert stored_job["company"] == "Example Company"
    assert stored_job["location"] == "Mumbai"
    assert stored_job["remote"] == 1
    assert stored_job["required_years"] == 0
    assert stored_job["skills"] == "SQL, Power BI, Python"


def test_find_job_by_url(test_database):
    job = create_sample_job()

    insert_job(job)

    stored_job = find_job_by_url(
        "https://example.com/jobs/data-analyst-001"
    )

    assert stored_job is not None
    assert stored_job["title"] == "Data Analyst"


def test_duplicate_job_is_rejected(test_database):
    job = create_sample_job()

    insert_job(job)

    with pytest.raises(ValueError, match="Job already exists"):
        insert_job(job)

    assert count_jobs() == 1

def test_insert_job_if_new(test_database):
    job = create_sample_job()

    first_result = insert_job_if_new(job)

    assert first_result["status"] == "inserted"
    assert first_result["job_id"] > 0

    second_result = insert_job_if_new(job)

    assert second_result["status"] == "duplicate"
    assert second_result["job_id"] == first_result["job_id"]

    assert count_jobs() == 1