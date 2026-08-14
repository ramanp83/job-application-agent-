from unittest.mock import Mock

from app.ingestion.arbeitnow_source import ArbeitnowJobSource


def test_arbeitnow_source_maps_jobs():
    response = Mock()
    response.json.return_value = {
        "data": [
            {
                "title": "Data Analyst",
                "company_name": "Example Analytics",
                "location": "Berlin",
                "remote": True,
                "job_types": ["Full-time"],
                "tags": ["SQL", "Python"],
                "description": "Analyze business data.",
                "url": "https://example.com/job/1",
                "created_at": "2026-08-14",
            }
        ]
    }

    session = Mock()
    session.get.return_value = response

    source = ArbeitnowJobSource(session=session)

    jobs = source.fetch_jobs()

    assert len(jobs) == 1
    assert jobs[0]["title"] == "Data Analyst"
    assert jobs[0]["company"] == "Example Analytics"
    assert jobs[0]["location"] == "Berlin"
    assert jobs[0]["remote"] is True
    assert jobs[0]["skills"] == ["SQL", "Python"]
    assert jobs[0]["source"] == "Arbeitnow"


def test_arbeitnow_source_calls_api():
    response = Mock()
    response.json.return_value = {"data": []}

    session = Mock()
    session.get.return_value = response

    source = ArbeitnowJobSource(session=session)

    source.fetch_jobs()

    session.get.assert_called_once_with(
        "https://arbeitnow.com/api/job-board-api",
        timeout=10,
    )


def test_arbeitnow_source_raises_for_http_error():
    response = Mock()
    response.raise_for_status.side_effect = RuntimeError("API error")

    session = Mock()
    session.get.return_value = response

    source = ArbeitnowJobSource(session=session)

    try:
        source.fetch_jobs()
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass
