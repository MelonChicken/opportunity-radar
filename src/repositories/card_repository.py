"""
Card Repository for data access.
Handles all OpportunityCard and DiscardedSignal persistence operations.
"""
import logging
from typing import List, Optional

from ..models import OpportunityCard, DiscardedSignal
from ..config import get_settings
from .base_repository import BaseRepository

logger = logging.getLogger(__name__)


class CardRepository:
    """Repository for OpportunityCard and DiscardedSignal data access."""
    
    def __init__(self):
        """Initialize the repository with file paths from config."""
        settings = get_settings()
        self._cards_repo = BaseRepository(settings.cards_file, OpportunityCard)
        self._discarded_repo = BaseRepository(settings.discarded_file, DiscardedSignal)
    
    # OpportunityCard methods
    
    def find_all_cards(self) -> List[OpportunityCard]:
        """Load all opportunity cards from storage."""
        return self._cards_repo._load_all()
    
    def find_card_by_id(self, card_id: str) -> Optional[OpportunityCard]:
        """Find a card by its ID."""
        cards = self.find_all_cards()
        for card in cards:
            if card.card_id == card_id:
                return card
        return None
    
    def find_cards_by_report(self, report_id: str) -> List[OpportunityCard]:
        """Find all cards associated with a specific report."""
        cards = self.find_all_cards()
        return [c for c in cards if c.report_id == report_id]
    
    def save_cards(self, cards: List[OpportunityCard]) -> None:
        """Save all opportunity cards to storage."""
        self._cards_repo._save_all(cards)
    
    def add_cards(self, new_cards: List[OpportunityCard]) -> None:
        """Add new cards to existing storage."""
        existing_cards = self.find_all_cards()
        existing_cards.extend(new_cards)
        self.save_cards(existing_cards)
        logger.info(f"Added {len(new_cards)} new cards to storage")
    
    # DiscardedSignal methods
    
    def find_all_discarded(self) -> List[DiscardedSignal]:
        """Load all discarded signals from storage."""
        return self._discarded_repo._load_all()
    
    def save_discarded(self, signals: List[DiscardedSignal]) -> None:
        """Save all discarded signals to storage."""
        self._discarded_repo._save_all(signals)
    
    def add_discarded(self, new_signals: List[DiscardedSignal]) -> None:
        """Add new discarded signals to existing storage."""
        existing_signals = self.find_all_discarded()
        existing_signals.extend(new_signals)
        self.save_discarded(existing_signals)
        logger.info(f"Added {len(new_signals)} new discarded signals to storage")


# Global instance
_card_repository: Optional[CardRepository] = None


def get_card_repository() -> CardRepository:
    """Get the global card repository instance."""
    global _card_repository
    if _card_repository is None:
        _card_repository = CardRepository()
    return _card_repository

