"""
Reprocessing script for regenerating all opportunity cards from existing reports.
Uses the refactored service layer and repository pattern.
"""
import os
import sys
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from src.repositories import get_report_repository, get_card_repository
from src.parsing import parse_html_content, parse_pdf_content
from src.signal_extraction import extract_candidate_sentences
from src.llm_service import generate_signal_struct
from src.services.translation_service import get_translation_service
from src.models import OpportunityCard, DiscardedSignal


def reprocess_all():
    """Reprocess all reports to regenerate opportunity cards."""
    logger.info("Starting Reprocessing of ALL Reports...")
    
    # Get repositories
    report_repo = get_report_repository()
    card_repo = get_card_repository()
    translation_service = get_translation_service()
    
    # 1. Clear existing Cards and Discarded Signals
    logger.info("Clearing old cards/discarded data...")
    card_repo.save_cards([])
    card_repo.save_discarded([])
    
    # 2. Load Reports
    reports = report_repo.find_all()
    logger.info(f"Loaded {len(reports)} reports to process.")
    
    new_cards = []
    new_discarded = []
    
    for i, report in enumerate(reports):
        logger.info(f"[{i+1}/{len(reports)}] Processing: {report.title[:50]}...")
        
        # Translate Report Metadata if missing
        if not report.title_ko:
            translation_service.translate_report(report)
        
        try:
            # Parse Content
            if report.url.lower().endswith('.pdf'):
                text = parse_pdf_content(report.url)
            else:
                text = parse_html_content(report.url)
            
            if not text:
                logger.warning(f"Failed to extract text from {report.url}")
                continue
            
            # Extract
            candidates = extract_candidate_sentences(text)
            
            # Structuring
            opp_count = 0
            discard_count = 0
            for candidate in candidates:  # Process all candidates
                result = generate_signal_struct(candidate, report.title, report.report_id)
                
                if isinstance(result, OpportunityCard):
                    new_cards.append(result)
                    opp_count += 1
                elif hasattr(result, 'reason'):
                    new_discarded.append(result)
                    discard_count += 1
            
            logger.info(f"  -> Extracted: {opp_count} Opportunities, {discard_count} Discarded")
            
        except Exception as e:
            logger.error(f"  -> Error: {e}", exc_info=True)
    
    # 3. Save
    card_repo.save_cards(new_cards)
    logger.info(f"Saved {len(new_cards)} new Opportunity Cards.")
    
    # Save Updated Reports (with translations)
    report_repo.save_all(reports)
    logger.info(f"Saved {len(reports)} Updated Reports (with Korean translations).")
    
    # Save Discarded Signals
    card_repo.save_discarded(new_discarded)
    logger.info(f"Saved {len(new_discarded)} Discarded Signals.")
    
    logger.info("\nReprocessing Complete.")


if __name__ == "__main__":
    reprocess_all()

