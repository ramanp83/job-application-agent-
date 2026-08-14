"""
Reporting utilities for matched jobs.
"""

from app.database.db import get_connection


def get_job_summary() -> dict[str, int]:
    """Return job counts grouped by application decision."""

    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) AS count FROM jobs"
        ).fetchone()["count"]

        apply_count = connection.execute(
            "SELECT COUNT(*) AS count FROM jobs WHERE decision = 'APPLY'"
        ).fetchone()["count"]

        review_count = connection.execute(
            "SELECT COUNT(*) AS count FROM jobs WHERE decision = 'REVIEW'"
        ).fetchone()["count"]

        skip_count = connection.execute(
            "SELECT COUNT(*) AS count FROM jobs WHERE decision = 'SKIP'"
        ).fetchone()["count"]

    return {
        "total": total,
        "apply": apply_count,
        "review": review_count,
        "skip": skip_count,
    }


def get_jobs_by_decision(
    decision: str,
    limit: int = 10,
) -> list[dict]:
    """Return highest-scoring jobs for a decision."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                title,
                company,
                location,
                match_score,
                decision,
                url
            FROM jobs
            WHERE decision = ?
            ORDER BY match_score DESC, id DESC
            LIMIT ?
            """,
            (decision, limit),
        ).fetchall()

    return [dict(row) for row in rows]


def print_job_section(
    title: str,
    jobs: list[dict],
) -> None:
    """Print a formatted job section."""

    print(title)
    print("-" * 60)

    if not jobs:
        print("No jobs found.")
        print()
        return

    for index, job in enumerate(jobs, start=1):
        location = job["location"] or "Location not specified"
        score = job["match_score"] if job["match_score"] is not None else 0

        print(
            f"{index}. {job['title']}"
        )
        print(
            f"   Company:  {job['company']}"
        )
        print(
            f"   Location: {location}"
        )
        print(
            f"   Score:    {score}"
        )

        if job["url"]:
            print(
                f"   URL:      {job['url']}"
            )

        print()


def print_report(limit: int = 10) -> None:
    """Print the current job matching report."""

    summary = get_job_summary()

    print()
    print("=" * 60)
    print("JOB APPLICATION AGENT")
    print("=" * 60)
    print()

    print(f"Total Jobs: {summary['total']}")
    print(f"Apply:      {summary['apply']}")
    print(f"Review:     {summary['review']}")
    print(f"Skip:       {summary['skip']}")
    print()

    print_job_section(
        "APPLY",
        get_jobs_by_decision("APPLY", limit),
    )

    print_job_section(
        "REVIEW",
        get_jobs_by_decision("REVIEW", limit),
    )

    print_job_section(
        "SKIP",
        get_jobs_by_decision("SKIP", limit),
    )

    print("=" * 60)