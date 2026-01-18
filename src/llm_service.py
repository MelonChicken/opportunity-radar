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
You are an expert technology analyst identifying opportunities for **startups and software developers**.
Analyze the following sentence extracted from a PwC report and the report context.

**Goal**: Determine if this sentence indicates a specific **Market Problem**, **Technology Gap**, or **Unmet Customer Need** that a startup could solve.

**Discard Criteria (Score < 50)**:
- Vague high-level statements (e.g., "Sustainability is important").
- Macro-economic forecasts without specific business angles to build on.
- Problems requiring only government policy changes.
- Abstract corporate advice (e.g., "Leaders must adapt").

**Keep Criteria (Score > 70)**:
- Specific pain points (e.g., "Banks struggle to process unstructured data").
- Emerging demand (e.g., "Rising need for AI-driven ESG reporting tools").
- Operational inefficiencies.

If it is a valid signal, structure it into a JSON object with the following fields:
- problem_summary: A concise 1-sentence summary of the problem/opportunity.
- problem_summary_ko: Korean translation of problem_summary.
- evidence_sentence: The exact sentence provided.
- evidence_sentence_ko: Korean translation of evidence_sentence.
- industry_tags: List of relevant industries (e.g., Finance, Healthcare, Auto).
- technology_tags: List of relevant technologies (e.g., AI, Blockchain, Cloud).
- expected_value: Description of the potential value/impact.
- expected_value_ko: Korean translation of expected_value.
- importance_score: Integer 1-100 (100 being critical disruption/opportunity).
- confidence_score: Float 0.0-1.0 (How confident are you this is a real signal).

If it is NOT a valid signal based on the criteria above, return a JSON with importance_score: 0.

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
        data = json.loads(content)
        
        score = data.get("importance_score", 0)
        
        if score < 50:
            return DiscardedSignal(
                signal_id=f"disc_{int(datetime.now().timestamp())}_{hash(candidate_text[:10])}",
                report_id=report_id,
                reason=f"Low Score: {score}",
                raw_text=candidate_text,
                importance_score=score
            )
            
        return OpportunityCard(
            card_id=f"card_{int(datetime.now().timestamp())}_{hash(candidate_text[:10])}",
            problem_summary=data.get("problem_summary", "Unknown Issue"),
            problem_summary_ko=data.get("problem_summary_ko"),
            evidence_sentence=candidate_text,
            evidence_sentence_ko=data.get("evidence_sentence_ko"),
            industry_tags=data.get("industry_tags", []),
            technology_tags=data.get("technology_tags", []),
            expected_value=data.get("expected_value", "Unknown"),
            expected_value_ko=data.get("expected_value_ko"),
            importance_score=score,
            confidence_score=data.get("confidence_score", 0.0),
            report_id=report_id
        )
        
    except Exception as e:
        print(f"Error calling LLM: {e}")

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
