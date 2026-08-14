from app.ingestion.mock_source import MockJobSource
from app.ingestion.pipeline import run_ingestion


def test_mock_source_returns_jobs():
    source = MockJobSource()

    jobs = source.fetch_jobs()

    assert isinstance(jobs, list)
    assert len(jobs) == 3


def test_mock_source_returns_raw_job_fields():
    source = MockJobSource()

    jobs = source.fetch_jobs()

    job = jobs[0]

    assert job["title"] == "Data Analyst"
    assert job["company"] == "Example Analytics"
    assert job["url"].startswith("https://")
    assert job["source"] == "Mock"


def test_mock_source_returns_unique_urls():
    source = MockJobSource()

    jobs = source.fetch_jobs()

    urls = [job["url"] for job in jobs]

    assert len(urls) == len(set(urls))


def test_ingestion_pipeline_inserts_jobs(test_database):
    source = MockJobSource()

    result = run_ingestion(source)

    assert result["fetched"] == 3
    assert result["inserted"] == 3
    assert result["duplicates"] == 0
    assert result["failed"] == 0


def test_ingestion_pipeline_detects_duplicates(test_database):
    source = MockJobSource()

    first_result = run_ingestion(source)
    second_result = run_ingestion(source)

    assert first_result["inserted"] == 3
    assert second_result["inserted"] == 0
    assert second_result["duplicates"] == 3


def test_ingestion_pipeline_stores_normalized_jobs(test_database):
    source = MockJobSource()

    run_ingestion(source)

    from app.jobs.repository import count_jobs, find_job_by_url

    assert count_jobs() == 3

    job = find_job_by_url(
        "https://example.com/jobs/data-analyst-001"
    )

    assert job is not None
    assert job.title == "Data Analyst"
    assert job.remote is True