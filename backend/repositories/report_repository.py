"""
Report Repository for data access.
Handles all Report model persistence operations.
"""
import logging
from typing import List, Optional

from ..models import Report, IngestionStatus
from ..config import get_settings
from .base_repository import BaseRepository

logger = logging.getLogger(__name__)


class ReportRepository(BaseRepository[Report]):
    """Repository for Report data access."""
    
    def __init__(self):
        """Initialize the repository with file path from config."""
        settings = get_settings()
        super().__init__(settings.reports_file, Report)
    
    def find_all(self) -> List[Report]:
        """Load all reports from storage."""
        return self._load_all()
    
    def find_by_id(self, report_id: str) -> Optional[Report]:
        """Find a report by its ID."""
        reports = self.find_all()
        for report in reports:
            if report.report_id == report_id:
                return report
        return None
    
    def find_by_status(self, status: IngestionStatus) -> List[Report]:
        """Find all reports with a specific status."""
        reports = self.find_all()
        return [r for r in reports if r.ingestion_status == status]
    
    def save(self, report: Report) -> None:
        """Save a single report (update if exists, insert if new)."""
        reports = self.find_all()
        
        # Update existing or append new
        for i, existing_report in enumerate(reports):
            if existing_report.report_id == report.report_id:
                reports[i] = report
                self.save_all(reports)
                logger.debug(f"Updated report: {report.report_id}")
                return
        
        reports.append(report)
        self.save_all(reports)
        logger.debug(f"Inserted report: {report.report_id}")
    
    def save_all(self, reports: List[Report]) -> None:
        """Save all reports to storage."""
        self._save_all(reports)
    
    def update_status(self, report_id: str, status: IngestionStatus) -> bool:
        """Update the ingestion status of a report."""
        reports = self.find_all()
        
        for report in reports:
            if report.report_id == report_id:
                report.ingestion_status = status
                self.save_all(reports)
                logger.info(f"Updated report {report_id} status to {status}")
                return True
        
        logger.warning(f"Report {report_id} not found for status update")
        return False


# Global instance
_report_repository: Optional[ReportRepository] = None


def get_report_repository() -> ReportRepository:
    """Get the global report repository instance."""
    global _report_repository
    if _report_repository is None:
        _report_repository = ReportRepository()
    return _report_repository

