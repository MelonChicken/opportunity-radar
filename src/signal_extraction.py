import re
from typing import List

KEYWORDS = [
    # PRD Core Keywords
    "problem", "challenge", "gap", "bottleneck", "limitation",
    # Extended Keywords for better recall
    "risk", "shortage", "fail", "difficulty", "threat", "opportunity", 
    "demand", "need", "lack", "unable", "struggle", "barrier", "issue", "concern"
]

def extract_candidate_sentences(text: str) -> List[str]:
    """
    Splits text into sentences and filters by keywords.
    """
    # Simple regex for sentence splitting (handles '.', '?', '!')
    # This isn't perfect but good enough for MVP without heavy NLP libs
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    candidates = []
    seen = set()
    
    for sentence in sentences:
        s_clean = sentence.strip()
        if len(s_clean) < 20 or len(s_clean) > 500: # Filter too short/long noise
            continue
            
        # Check for keywords
        lower_s = s_clean.lower()
        if any(k in lower_s for k in KEYWORDS):
            if s_clean not in seen:
                candidates.append(s_clean)
                seen.add(s_clean)
                
    return candidates
