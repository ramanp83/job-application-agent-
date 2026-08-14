"""
Base interface for job ingestion sources.
"""

from abc import ABC, abstractmethod
from typing import Any


class JobSource(ABC):
    """Abstract interface for all job sources."""

    @abstractmethod
    def fetch_jobs(self) -> list[dict[str, Any]]:
        """Fetch raw jobs from the source."""
        raise NotImplementedError