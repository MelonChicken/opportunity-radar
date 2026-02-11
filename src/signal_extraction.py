"""
Signal extraction from text using keyword filtering.
Extracts candidate sentences that may contain startup opportunities.
"""
import re
import logging
from typing import List

from .config import get_settings

logger = logging.getLogger(__name__)


# Keywords for identifying opportunity signals
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
    
    Args:
        text: Input text to extract sentences from
        
    Returns:
        List of candidate sentences containing keywords
    """
    settings = get_settings()
    
    # Simple regex for sentence splitting (handles '.', '?', '!')
    # This isn't perfect but good enough for MVP without heavy NLP libs
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    candidates = []
    seen = set()
    
    for sentence in sentences:
        s_clean = sentence.strip()
        
        # Filter by length using config
        if len(s_clean) < settings.min_sentence_length or len(s_clean) > settings.max_sentence_length:
            continue
        
        # Check for keywords
        lower_s = s_clean.lower()
        if any(k in lower_s for k in KEYWORDS):
            if s_clean not in seen:
                candidates.append(s_clean)
                seen.add(s_clean)
    
    logger.debug(f"Extracted {len(candidates)} candidate sentences from {len(sentences)} total sentences")
    return candidates

