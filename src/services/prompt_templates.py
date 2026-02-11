"""
Prompt templates for LLM interactions.
Centralized location for all prompts used in the application.
"""


class PromptTemplates:
    """Container for all prompt templates."""
    
    # Signal Extraction and Structuring Prompt
    SIGNAL_EXTRACTION = """
You are a Founder-in-Residence identifying **startup opportunities** from generic business reports.
Your goal is not to summarize, but to **deconstruct** the text into a concrete "Pain Point" and a plausible "Attack Vector" for a new startup.

**Framework for Analysis**:
1. **Pain Holder (Who)**: Who exactly is suffering? (e.g., "Middle managers in manufacturing", "Compliance officers in Fintech"). Be specific.
2. **Pain Context (Where)**: In what specific wokflow or situation does this occur? (e.g., "During quarterly reconciliation", "When managing remote fleets").
3. **Pain Mechanism (Why)**: Why is this hard? (e.g., "Data is siloed", "Manual entry causes errors", "Lack of real-time visibility").
4. **Attack Vector (How)**: Suggest a plausible product/service approach. (e.g., "Automated reconciliation agent", "IoT-based fleet dashboard").

**Value Estimation** (Phase 2):
5. **Market Size**: Estimate the addressable market in dollars or user count (e.g., "$500M-1B TAM", "~50K SMBs in the US"). Be realistic.
6. **Value Type**: Categorize the value created (choose one: "Cost Reduction", "Revenue Growth", "Risk Mitigation", "Productivity Gain").
7. **Expected Impact**: Quantify the potential improvement (e.g., "20-30% cost savings", "3x faster processing", "50% error reduction").
8. **Timeline**: Estimate time to MVP/market (e.g., "6-9 months", "12-18 months"). Consider technical complexity.

**Discard Criteria (Score < 50)**:
- Vague statements ("Growth is slowing").
- Problems solvable only by regulation/policy.
- Generic corporate advice ("Leaders must lead").

**Output Format (JSON)**:
{{
  "pain_holder": "...",
  "pain_holder_ko": "...",
  "pain_context": "...",
  "pain_context_ko": "...",
  "pain_mechanism": "...",
  "pain_mechanism_ko": "...",
  "attack_vector": "...",
  "attack_vector_ko": "...",
  "evidence_sentence": "...",
  "evidence_sentence_ko": "...",
  "industry_tags": ["..."],
  "technology_tags": ["..."],
  "importance_score": 0-100,
  "confidence_score": 0.0-1.0,
  "market_size": "...",
  "value_type": "Cost Reduction|Revenue Growth|Risk Mitigation|Productivity Gain",
  "expected_impact": "...",
  "timeline": "..."
}}

If NOT a valid startup opportunity, return {{ "importance_score": 0 }}.

Sentence: "{sentence}"
Context: "{context}" (Report Title or Summary)
"""
    
    # Translation Prompt
    TRANSLATION = """
Translate the following Title and Summary of a business report into professional Korean.
Return ONLY a JSON object: {{"title_ko": "...", "summary_ko": "..."}}

Title: {title}
Summary: {summary}
"""
    
    @classmethod
    def format_signal_extraction(cls, sentence: str, context: str) -> str:
        """
        Format the signal extraction prompt with provided data.
        
        Args:
            sentence: The candidate sentence to analyze
            context: Contextual information (report title or summary)
            
        Returns:
            Formatted prompt string
        """
        return cls.SIGNAL_EXTRACTION.format(sentence=sentence, context=context)
    
    @classmethod
    def format_translation(cls, title: str, summary: str) -> str:
        """
        Format the translation prompt with provided data.
        
        Args:
            title: Report title to translate
            summary: Report summary to translate
            
        Returns:
            Formatted prompt string
        """
        return cls.TRANSLATION.format(title=title, summary=summary)
