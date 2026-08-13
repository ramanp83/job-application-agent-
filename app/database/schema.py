"""
SQLite database schema for the Job Application Agent.
"""

CREATE_JOBS_TABLE = """
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,
    company TEXT NOT NULL,

    location TEXT,
    remote INTEGER DEFAULT 0,

    job_type TEXT,

    salary_min REAL,
    salary_max REAL,
    currency TEXT,

    required_years REAL,
    seniority TEXT,

    skills TEXT,
    description TEXT,

    url TEXT,
    source TEXT,

    date_posted TEXT,
    date_discovered TEXT NOT NULL,

    match_score INTEGER,
    decision TEXT,

    application_status TEXT DEFAULT 'not_applied',
    applied_at TEXT,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    UNIQUE(company, title, url)
);
"""