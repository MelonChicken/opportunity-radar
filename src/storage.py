import json
import os
from typing import List, Optional
from .models import Report, OpportunityCard, IngestionStatus

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.json")
CARDS_FILE = os.path.join(DATA_DIR, "cards.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
            
    if not os.path.exists(CARDS_FILE):
        with open(CARDS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def load_reports() -> List[Report]:
    ensure_data_dir()
    try:
        with open(REPORTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Report(**item) for item in data]
    except json.JSONDecodeError:
        return []

def save_reports(reports: List[Report]):
    ensure_data_dir()
    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        # dump model compatible json
        json.dump([r.model_dump(mode='json') for r in reports], f, indent=2, ensure_ascii=False)

def load_cards() -> List[OpportunityCard]:
    ensure_data_dir()
    try:
        with open(CARDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [OpportunityCard(**item) for item in data]
    except json.JSONDecodeError:
        return []

def save_cards(cards: List[OpportunityCard]):
    ensure_data_dir()
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump([c.model_dump(mode='json') for c in cards], f, indent=2, ensure_ascii=False)

def update_report_status(report_id: str, status: IngestionStatus):
    reports = load_reports()
    for r in reports:
        if r.report_id == report_id:
            r.ingestion_status = status
            break
    save_reports(reports)

# --- Discarded Signals Storage ---
DISCARDED_FILE = os.path.join(DATA_DIR, "discarded_signals.json")

def load_discarded_signals() -> List['DiscardedSignal']: # Forward ref resolved by imports or runtime
    from .models import DiscardedSignal
    ensure_data_dir()
    
    if not os.path.exists(DISCARDED_FILE):
        with open(DISCARDED_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
            
    try:
        with open(DISCARDED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [DiscardedSignal(**item) for item in data]
    except json.JSONDecodeError:
        return []

def save_discarded_signals(signals: List['DiscardedSignal']):
    from .models import DiscardedSignal
    ensure_data_dir()
    with open(DISCARDED_FILE, "w", encoding="utf-8") as f:
        json.dump([s.model_dump(mode='json') for s in signals], f, indent=2, ensure_ascii=False)
