import pytest


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """Create an isolated SQLite database for each test."""

    database_path = tmp_path / "test_jobs.db"

    import app.database.db as db

    monkeypatch.setattr(db, "DATABASE_PATH", database_path)
    monkeypatch.setattr(db, "DATA_DIR", tmp_path)

    db.initialize_database()

    yield database_path