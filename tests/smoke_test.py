
import sys
import os
import shutil
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.models import DiscardedSignal, OpportunityCard
from src.storage import save_discarded_signals, load_discarded_signals, save_cards, load_cards

def test_discarded_storage():
    print("Testing Discarded Signal Storage...")
    
    # Create dummy signal
    sig = DiscardedSignal(
        signal_id="test_sig_1",
        report_id="test_rep_1",
        reason="Low Score",
        raw_text="This is a test signal.",
        importance_score=30
    )
    
    # Save
    save_discarded_signals([sig])
    print("Saved discarded signal.")
    
    # Load
    loaded = load_discarded_signals()
    assert len(loaded) > 0
    assert loaded[0].signal_id == "test_sig_1"
    assert loaded[0].importance_score == 30
    print("Verified discarded signal storage: PASS")

def test_card_model():
    print("Testing Opportunity Card Model...")
    card = OpportunityCard(
        card_id="test_card_1",
        problem_summary="Test Problem",
        evidence_sentence="Test Evidence",
        industry_tags=["Tech"],
        technology_tags=["AI"],
        expected_value="High",
        importance_score=85,
        confidence_score=0.9,
        report_id="test_rep_1"
    )
    assert card.importance_score == 85
    print("Verified Card Model: PASS")

if __name__ == "__main__":
    try:
        test_discarded_storage()
        test_card_model()
        print("\nALL SMOKE TESTS PASSED!")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
