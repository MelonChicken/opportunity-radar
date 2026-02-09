import time
from typing import List, Tuple
from .models import Report, OpportunityCard, IngestionStatus
from .storage import load_reports, save_reports, save_cards, load_cards, load_discarded_signals, save_discarded_signals
from .ingestion import fetch_rss_feed
from .parsing import parse_html_content, parse_pdf_content
from .signal_extraction import extract_candidate_sentences
from .llm_service import generate_signal_struct, translate_report

def run_pipeline(log_callback=print) -> Tuple[int, int, int]:
    """
    Runs the full pipeline:
    1. Fetch RSS Stats
    2. Process Pending Reports
    3. Save Cards
    
    Returns (reports_found, reports_processed, cards_created)
    """
    # 1. Fetch
    log_callback("Fetching RSS Feed...")
    new_reports = fetch_rss_feed()
    log_callback(f"Found {len(new_reports)} items in feed.")
    all_reports = load_reports()
    
    # Merge new reports
    existing_ids = {r.report_id for r in all_reports}
    added_count = 0
    for r in new_reports:
        if r.report_id not in existing_ids:
            all_reports.append(r)
            added_count += 1
            
    save_reports(all_reports) # Save immediately so we have the list
    
    # 2. Process Pending
    pending_reports = [r for r in all_reports if r.ingestion_status == IngestionStatus.PENDING]
    processed_count = 0
    new_cards = []
    discarded_signals = []
    
    for report in pending_reports:
        try:
            log_callback(f"Processing {report.title}...")
            
            # Translate Metadata
            translate_report(report)
            
            # Parse
            log_callback("  -> Parsing content...")
            if report.url.lower().endswith('.pdf'):
                text = parse_pdf_content(report.url)
            else:
                text = parse_html_content(report.url)
                
            if not text:
                log_callback(f"Failed to extract text from {report.url}")
                report.ingestion_status = IngestionStatus.FAILED
                continue
                
            # Extract
            candidates = extract_candidate_sentences(text)
            log_callback(f"Extracted {len(candidates)} candidates.")
            
            # Structuring
            # Remove MVP Limit: Increased from 5 to 20 to allow deeper analysis
            MAX_SIGNALS = 20 
            for candidate in candidates[:MAX_SIGNALS]: 
                result = generate_signal_struct(candidate, report.title, report.report_id)
                if isinstance(result, OpportunityCard):
                    new_cards.append(result)
                    log_callback(f"  -> Generated Opportunity: {result.problem_summary[:30]}...")
                elif hasattr(result, 'reason'): # Check for DiscardedSignal (isinstance check might need import)
                    discarded_signals.append(result)
                    log_callback(f"  -> Discarded (Score {result.importance_score})")
            
            report.ingestion_status = IngestionStatus.PROCESSED
            processed_count += 1
            time.sleep(1) # Polite rate limiting
            
        except Exception as e:
            log_callback(f"Failed to process {report.report_id}: {e}")
            print(f"Failed to process {report.report_id}: {e}")
            report.ingestion_status = IngestionStatus.FAILED
            
    # 3. Save
    save_reports(all_reports) # Update statuses
    
    existing_cards = load_cards()
    existing_cards.extend(new_cards)
    save_cards(existing_cards)
    
    # Save Discarded
    if discarded_signals:
        existing_discarded = load_discarded_signals()
        existing_discarded.extend(discarded_signals)
        save_discarded_signals(existing_discarded)
    
    return added_count, processed_count, len(new_cards)