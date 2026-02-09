import os
import time
from src.storage import load_reports, save_cards, save_reports
from src.parsing import parse_html_content, parse_pdf_content
from src.signal_extraction import extract_candidate_sentences
from src.llm_service import generate_signal_struct, translate_report
from src.models import OpportunityCard, DiscardedSignal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CARDS_FILE = os.path.join(DATA_DIR, "cards.json")
DISCARDED_FILE = os.path.join(DATA_DIR, "discarded_signals.json")

def reprocess_all():
    print("Starting Reprocessing of ALL Reports...")
    
    # 1. Clear existing Cards
    if os.path.exists(CARDS_FILE):
        os.remove(CARDS_FILE)
    if os.path.exists(DISCARDED_FILE):
        os.remove(DISCARDED_FILE)
        
    print("Cleared old cards/discarded data.")
    
    # 2. Load Reports
    reports = load_reports()
    print(f"Loaded {len(reports)} reports to process.")
    
    new_cards = []
    new_discarded = []
    
    for i, report in enumerate(reports): 
        print(f"[{i+1}/{len(reports)}] Processing: {report.title[:50]}...")
        
        # [NEW] Translate Report Metadata if missing
        if not report.title_ko:
            translate_report(report)
        
        try:
            # Parse Content
            if report.url.lower().endswith('.pdf'):
                text = parse_pdf_content(report.url)
            else:
                text = parse_html_content(report.url)
            
            if not text:
                continue
                
            # Extract
            candidates = extract_candidate_sentences(text)
            
            # Structuring
            opp_count = 0
            discard_count = 0
            for candidate in candidates: # Process all candidates
                result = generate_signal_struct(candidate, report.title, report.report_id)
                
                if isinstance(result, OpportunityCard):
                    new_cards.append(result)
                    opp_count += 1
                elif hasattr(result, 'reason'): 
                    new_discarded.append(result)
                    discard_count += 1
            
            print(f"  -> Extracted: {opp_count} Opportunities, {discard_count} Discarded")
                    
        except Exception as e:
            print(f"  -> Error: {e}")
                    
        except Exception as e:
            print(f"  -> Error: {e}")
            
    # 3. Save
    save_cards(new_cards)
    print(f"Saved {len(new_cards)} new Opportunity Cards.")
    
    # [NEW] Save Updated Reports (with translations)
    save_reports(reports)
    print(f"Saved {len(reports)} Updated Reports (with Korean translations).")
    
    print("\nReprocessing Complete.")

if __name__ == "__main__":
    reprocess_all()
