from app.jobs.normalizer import (
    normalize_experience,
    normalize_job,
    normalize_job_type,
    normalize_remote,
    normalize_skills,
    normalize_url,
)


def test_normalize_job_title_and_company():
    raw_job = {
        "title": "  Data   Analyst  ",
        "company": "  Example   Company ",
    }

    result = normalize_job(raw_job)

    assert result["title"] == "Data Analyst"
    assert result["company"] == "Example Company"


def test_normalize_remote_values():
    assert normalize_remote("Remote") is True
    assert normalize_remote("fully remote") is True
    assert normalize_remote("Work From Home") is True
    assert normalize_remote("Hybrid") is False
    assert normalize_remote("On-site") is False


def test_normalize_job_type():
    assert normalize_job_type("full time") == "Full-time"
    assert normalize_job_type("FULL-TIME") == "Full-time"
    assert normalize_job_type("intern") == "Internship"
    assert normalize_job_type("contract") == "Contract"


def test_normalize_experience():
    assert normalize_experience("Fresher") == 0.0
    assert normalize_experience("0 years") == 0.0
    assert normalize_experience("1 year") == 1.0
    assert normalize_experience("2-3 years") == 2.0


def test_normalize_skills():
    skills = normalize_skills(
        "SQL, mysql, PowerBI, Microsoft Power BI, Python, SQL"
    )

    assert skills == [
        "SQL",
        "MySQL",
        "Power BI",
        "Python",
    ]


def test_normalize_url():
    assert (
        normalize_url("https://example.com/job/123/")
        == "https://example.com/job/123"
    )


def test_normalize_complete_job():
    raw_job = {
        "title": "  Junior Data Analyst ",
        "company": " Example Corp ",
        "location": " Mumbai ",
        "remote": "Fully Remote",
        "job_type": "full time",
        "required_years": "0-1 years",
        "skills": "SQL, PowerBI, Python",
        "url": "https://example.com/job/123/",
        "source": " LinkedIn ",
    }

    result = normalize_job(raw_job)

    assert result["title"] == "Junior Data Analyst"
    assert result["company"] == "Example Corp"
    assert result["location"] == "Mumbai"
    assert result["remote"] is True
    assert result["job_type"] == "Full-time"
    assert result["required_years"] == 0.0
    assert result["skills"] == ["SQL", "Power BI", "Python"]
    assert result["url"] == "https://example.com/job/123"
    assert result["source"] == "LinkedIn"