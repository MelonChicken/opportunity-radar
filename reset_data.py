import os
import shutil

# Paths
DATA_DIR = "c:\\Users\\osca0\\Github\\radar\\data"
CARDS_FILE = os.path.join(DATA_DIR, "cards.json")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.json")
DISCARDED_FILE = os.path.join(DATA_DIR, "discarded_signals.json")

def reset_data():
    print("Resetting data related to content generation...")
    
    # 1. Remove cards.json (Forces regeneration of insights)
    if os.path.exists(CARDS_FILE):
        os.remove(CARDS_FILE)
        print(f"Deleted {CARDS_FILE}")
    else:
        print(f"{CARDS_FILE} not found (already clean).")
        
    # 2. We keep reports.json so we don't have to re-download the same files?
    # Actually, if we want to re-process them, we need to mark them as PENDING.
    # But a simpler way for MVP is just to clear reports too, and fetch RSS fresh.
    # Let's clear reports to be safe and ensure full re-run.
    if os.path.exists(REPORTS_FILE):
        os.remove(REPORTS_FILE)
        print(f"Deleted {REPORTS_FILE}")
    
    if os.path.exists(DISCARDED_FILE):
        os.remove(DISCARDED_FILE)
        print(f"Deleted {DISCARDED_FILE}")
        
    print("\nData reset complete. Please running the Ingestion Pipeline in Streamlit now.")

if __name__ == "__main__":
    reset_data()
