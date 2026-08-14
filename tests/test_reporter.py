from app.database.db import get_connection
from app.reporting.reporter import (
    get_job_summary,
    get_jobs_by_decision,
)


def insert_test_job(
    title: str,
    company: str,
    score: int,
    decision: str,
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO jobs (
                title,
                company,
                location,
                remote,
                job_type,
                date_discovered,
                match_score,
                decision,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                company,
                "Mumbai",
                0,
                "full-time",
                "2026-08-14T00:00:00+00:00",
                score,
                decision,
                "2026-08-14T00:00:00+00:00",
                "2026-08-14T00:00:00+00:00",
            ),
        )

        connection.commit()


def test_job_summary(test_database):
    insert_test_job(
        "Data Analyst",
        "Company A",
        95,
        "APPLY",
    )

    insert_test_job(
        "BI Analyst",
        "Company B",
        75,
        "REVIEW",
    )

    insert_test_job(
        "Developer",
        "Company C",
        40,
        "SKIP",
    )

    summary = get_job_summary()

    assert summary["total"] == 3
    assert summary["apply"] == 1
    assert summary["review"] == 1
    assert summary["skip"] == 1


def test_jobs_are_ordered_by_score(test_database):
    insert_test_job(
        "Data Analyst Junior",
        "Company A",
        82,
        "APPLY",
    )

    insert_test_job(
        "Data Analyst",
        "Company B",
        95,
        "APPLY",
    )

    jobs = get_jobs_by_decision("APPLY")

    assert len(jobs) == 2
    assert jobs[0]["match_score"] == 95
    assert jobs[1]["match_score"] == 82