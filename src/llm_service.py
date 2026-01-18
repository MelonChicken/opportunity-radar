import os
import json
from openai import OpenAI
from .models import OpportunityCard
from datetime import datetime
from dotenv import load_dotenv

# Initialize client (requires OPENAI_API_KEY env var)
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_TEMPLATE = """
You are a Founder-in-Residence identifying **startup opportunities** from generic business reports.
Your goal is not to summarize, but to **deconstruct** the text into a concrete "Pain Point" and a plausible "Attack Vector" for a new startup.

**Framework for Analysis**:
1. **Pain Holder (Who)**: Who exactly is suffering? (e.g., "Middle managers in manufacturing", "Compliance officers in Fintech"). Be specific.
2. **Pain Context (Where)**: In what specific wokflow or situation does this occur? (e.g., "During quarterly reconciliation", "When managing remote fleets").
3. **Pain Mechanism (Why)**: Why is this hard? (e.g., "Data is siloed", "Manual entry causes errors", "Lack of real-time visibility").
4. **Attack Vector (How)**: Suggest a plausible product/service approach. (e.g., "Automated reconciliation agent", "IoT-based fleet dashboard").

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
  "confidence_score": 0.0-1.0
}}

If NOT a valid startup opportunity, return {{ "importance_score": 0 }}.

Sentence: "{sentence}"
Context: "{context}" (Report Title or Summary)
"""

def generate_signal_struct(candidate_text: str, context_summary: str, report_id: str) -> OpportunityCard | None:
    """
    Calls OpenAI to restructure the candidate signal into an OpportunityCard.
    Returns DiscardedSignal if importance_score is too low.
    Returns None if LLM fails completely.
    """
    from .models import DiscardedSignal # Import here to avoid circular dep if any

    if not os.environ.get("OPENAI_API_KEY"):
        # Fallback or Mock for dev without key
        print("Warning: No OPENAI_API_KEY found. Returning Mock.")
        return None # Or return a mock object if desired for testing

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", # Cost effective, supports json_object
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": PROMPT_TEMPLATE.format(sentence=candidate_text, context=context_summary)}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        print(f"DEBUG LLM CONTENT: {content!r}") # Print raw content
        data = json.loads(content)
        print(f"DEBUG PARSED DATA: {data}")
        
        score = data.get("importance_score", 0)
        
        if score < 50:
             # ... existing logic ...
             return DiscardedSignal(
                signal_id=f"disc_{int(datetime.now().timestamp())}_{hash(candidate_text[:10])}",
                report_id=report_id,
                reason=f"Low Score: {score}",
                raw_text=candidate_text,
                importance_score=score
            )
            
        return OpportunityCard(
            card_id=f"card_{int(datetime.now().timestamp())}_{hash(candidate_text[:10])}",
            
            # v2 Fields
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
            report_id=report_id
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error calling LLM: {e!r}") # Use repr to see full error structure

def translate_report(report) -> None:
    """
    Translates Report title and summary to Korean in-place.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        return

    try:
        # Simple translation prompt
        prompt = f"""
        Translate the following Title and Summary of a business report into professional Korean.
        Return ONLY a JSON object: {{"title_ko": "...", "summary_ko": "..."}}
        
        Title: {report.title}
        Summary: {report.summary}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a professional translator for business intelligence."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        report.title_ko = data.get("title_ko")
        report.summary_ko = data.get("summary_ko")
        
    except Exception as e:
        print(f"Error translating report {report.report_id}: {e}")
