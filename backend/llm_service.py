"""
Signal generation service using LLM.
Converts candidate sentences into structured OpportunityCard objects.
"""
import json
import logging
from datetime import datetime
from typing import Union, Optional

from .models import OpportunityCard, DiscardedSignal
from .services.llm_client import LLMClient
from .services.prompt_templates import PromptTemplates

# Configure logger
logger = logging.getLogger(__name__)


def generate_signal_struct(
    candidate_text: str, 
    context_summary: str, 
    report_id: str
) -> Union[OpportunityCard, DiscardedSignal, None]:
    """
    Calls LLM to restructure the candidate signal into an OpportunityCard.
    
    Args:
        candidate_text: The candidate sentence to analyze
        context_summary: Contextual information (report title or summary)
        report_id: ID of the source report
    
    Returns:
        OpportunityCard: If valid opportunity with score >= 50
        DiscardedSignal: If importance_score < 50
        None: If LLM fails or is not available
    """
    # Get LLM client
    llm_client = LLMClient.get_instance()
    
    if not llm_client.is_available:
        logger.warning("LLM client not available. Returning None.")
        return None

    try:
        # Format prompt
        prompt = PromptTemplates.format_signal_extraction(
            sentence=candidate_text,
            context=context_summary
        )
        
        # Call LLM
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = llm_client.chat_completion(
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        if not response or not response.choices:
            logger.warning("No response from LLM")
            return None
        
        content = response.choices[0].message.content
        logger.debug(f"LLM Response Content: {content}")
        
        # Parse JSON response
        data = json.loads(content)
        score = data.get("importance_score", 0)
        
        # Check if score is below threshold
        if score < 50:
            return DiscardedSignal(
                signal_id=f"disc_{int(datetime.now().timestamp())}_{hash(candidate_text[:10])}",
                report_id=report_id,
                reason=f"Low Score: {score}",
                raw_text=candidate_text,
                importance_score=score
            )
        
        # Create OpportunityCard
        return OpportunityCard(
            card_id=f"card_{int(datetime.now().timestamp())}_{hash(candidate_text[:10])}",
            pain_holder=data.get("pain_holder", "Unknown"),
            pain_holder_ko=data.get("pain_holder_ko"),
            pain_context=data.get("pain_context", "Unknown"),
            pain_context_ko=data.get("pain_context_ko"),
            pain_mechanism=data.get("pain_mechanism", "Unknown"),
            pain_mechanism_ko=data.get("pain_mechanism_ko"),
            attack_vector=data.get("attack_vector", "Unknown"),
            attack_vector_ko=data.get("attack_vector_ko"),
            evidence_sentence=candidate_text,
            evidence_sentence_ko=data.get("evidence_sentence_ko"),
            industry_tags=data.get("industry_tags", []),
            technology_tags=data.get("technology_tags", []),
            importance_score=score,
            confidence_score=data.get("confidence_score", 0.0),
            report_id=report_id,
            # Phase 2: Value Fields
            market_size=data.get("market_size"),
            value_type=data.get("value_type"),
            expected_impact=data.get("expected_impact"),
            timeline=data.get("timeline")
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON response: {e}")
        return None
    except Exception as e:
        logger.error(f"Error calling LLM: {e}", exc_info=True)
        return None


# Backward compatibility: expose translate_report from translation service
def translate_report(report) -> None:
    """
    Translates Report title and summary to Korean in-place.
    
    Args:
        report: Report object to translate
    
    Note:
        This function is maintained for backward compatibility.
        New code should use TranslationService directly.
    """
    from .services.translation_service import get_translation_service
    
    translation_service = get_translation_service()
    translation_service.translate_report(report)
