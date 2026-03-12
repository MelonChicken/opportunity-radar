"""
Translation service for Korean localization.
Handles translation of reports and cards using LLM.
"""
import json
import logging
from typing import Optional, Dict, Tuple

from .llm_client import LLMClient
from .prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)


class TranslationService:
    """
    Service for translating content to Korean.
    Includes caching to avoid redundant API calls.
    """
    
    def __init__(self):
        """Initialize the translation service."""
        self.llm_client = LLMClient.get_instance()
        self._cache: Dict[str, Tuple[str, str]] = {}  # key: (title_ko, summary_ko)
    
    def translate_report(self, report) -> None:
        """
        Translate Report title and summary to Korean in-place.
        
        Args:
            report: Report object to translate
        """
        # Skip if already translated
        if report.title_ko and report.summary_ko:
            logger.debug(f"Report {report.report_id} already translated. Skipping.")
            return
        
        # Check cache
        cache_key = f"{report.title}|{report.summary or ''}"
        if cache_key in self._cache:
            report.title_ko, report.summary_ko = self._cache[cache_key]
            logger.debug(f"Using cached translation for report {report.report_id}")
            return
        
        # Check if LLM is available
        if not self.llm_client.is_available:
            logger.warning("LLM client not available. Skipping translation.")
            return
        
        try:
            # Format prompt
            prompt = PromptTemplates.format_translation(
                title=report.title,
                summary=report.summary or ""
            )
            
            # Call LLM
            messages = [
                {"role": "system", "content": "You are a professional translator for business intelligence."},
                {"role": "user", "content": prompt}
            ]
            
            response = self.llm_client.chat_completion(
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            if not response or not response.choices:
                logger.warning(f"No response from LLM for report {report.report_id}")
                return
            
            # Parse response
            content = response.choices[0].message.content
            data = json.loads(content)
            
            # Update report
            report.title_ko = data.get("title_ko")
            report.summary_ko = data.get("summary_ko")
            
            # Cache result
            self._cache[cache_key] = (report.title_ko, report.summary_ko)
            
            logger.info(f"Successfully translated report {report.report_id}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse translation JSON for report {report.report_id}: {e}")
        except Exception as e:
            logger.error(f"Error translating report {report.report_id}: {e}", exc_info=True)
    
    def clear_cache(self) -> None:
        """Clear the translation cache."""
        self._cache.clear()
        logger.info("Translation cache cleared")


# Global instance
_translation_service: Optional[TranslationService] = None


def get_translation_service() -> TranslationService:
    """
    Get the global translation service instance.
    
    Returns:
        TranslationService: The singleton instance
    """
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service
