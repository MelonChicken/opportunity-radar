"""
Storage module with backward compatibility.
Delegates to repository pattern implementation.

Note: This module is maintained for backward compatibility.
New code should use repositories directly:
    from .repositories import get_report_repository, get_card_repository
"""
import json
import os
from typing import List, Optional
from .models import Report, OpportunityCard, IngestionStatus
from .repositories import get_report_repository, get_card_repository

# Legacy constants (kept for compatibility)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.json")
CARDS_FILE = os.path.join(DATA_DIR, "cards.json")
DISCARDED_FILE = os.path.join(DATA_DIR, "discarded_signals.json")


def ensure_data_dir():
    """Ensure data directory exists. Delegates to repositories."""
    # Repositories handle this automatically
    get_report_repository()
    get_card_repository()


def load_reports() -> List[Report]:
    """Load all reports. Delegates to ReportRepository."""
    return get_report_repository().find_all()


def save_reports(reports: List[Report]):
    """Save all reports. Delegates to ReportRepository."""
    get_report_repository().save_all(reports)


def load_cards() -> List[OpportunityCard]:
    """Load all cards. Delegates to CardRepository."""
    return get_card_repository().find_all_cards()


def save_cards(cards: List[OpportunityCard]):
    """Save all cards. Delegates to CardRepository."""
    get_card_repository().save_cards(cards)


def update_report_status(report_id: str, status: IngestionStatus):
    """Update report status. Delegates to ReportRepository."""
    get_report_repository().update_status(report_id, status)


def load_discarded_signals() -> List['DiscardedSignal']:
    """Load all discarded signals. Delegates to CardRepository."""
    from .models import DiscardedSignal
    return get_card_repository().find_all_discarded()


def save_discarded_signals(signals: List['DiscardedSignal']):
    """Save all discarded signals. Delegates to CardRepository."""
    from .models import DiscardedSignal
    get_card_repository().save_discarded(signals)

