"""
Repositories package for data access layer.
Implements repository pattern for clean data access.
"""
from .report_repository import ReportRepository, get_report_repository
from .card_repository import CardRepository, get_card_repository

__all__ = ["ReportRepository", "CardRepository", "get_report_repository", "get_card_repository"]

