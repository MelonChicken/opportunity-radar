def build_prompt_from_card(card, report_url="N/A"):
    """
    Constructs the prompt text based on the card data and template.
    """
    title = card.get('title', 'N/A')
    score = card.get('importance_score', 0)
    confidence = int(card.get('confidence_score', 0) * 100)
    who = card.get('pain_holder', 'N/A')
    why = card.get('pain_mechanism', 'N/A')
    evidence_sentence = card.get('evidence_sentence', 'N/A')
    
    # Handle lists
    industry_tags = card.get('industry_tags', [])
    if isinstance(industry_tags, list):
        industry_tags = ", ".join(industry_tags)
        
    tech_tags = card.get('technology_tags', [])
    if isinstance(tech_tags, list):
        tech_tags = ", ".join(tech_tags)

    prompt = f"""You are a startup product strategist.
Turn the following research signal into a short, readable opportunity brief for a founder.
This is NOT a pitch deck and NOT a solution spec.

Rules:
- Treat the Evidence sentence as FACT. Anything else must be clearly labeled as an ASSUMPTION.
- Do not invent statistics, market size, or sources.
- Be concrete and practical.
- Keep the total length under ~500 words.
- Use the exact section headers provided below.

RESEARCH SIGNAL
Title: {title}
Score: {score}
Confidence: {confidence}
Target customer (Who): {who}
Pain point (Why): {why}
Industry tags: {industry_tags}
Technology tags: {tech_tags}
Evidence (verbatim): "{evidence_sentence}"
Source: {report_url}

WRITE A SHORT OPPORTUNITY BRIEF USING THE FOLLOWING STRUCTURE:

## 1. Who Is in Pain
- Clearly describe who is experiencing the problem (role, team, or organization).
- Mark each sentence as [FACT] or [ASSUMPTION].

## 2. Where the Pain Occurs
- Explain in which workflow, process, or situation the pain shows up.
- Focus on *when and where*, not why yet.

## 3. Why This Pain Persists
- List 2–3 concrete reasons the problem exists or remains unsolved.
- Separate structural causes from temporary ones.
- Mark assumptions clearly.

## 4. Why This Is a Real Opportunity (Now)
- Explain why this pain is economically or strategically meaningful.
- Tie directly back to the Evidence sentence.
- Avoid generic statements.

## 5. Possible Attack Vectors (Not Solutions)
For each vector:
- Describe the angle of attack (automation, simplification, decision support, replacement, etc.).
- Explain *what kind of product or system* this implies (no feature lists).
- State why this vector could work.

Provide 2 attack vectors.

## 6. How to Validate This Quickly
- Who to talk to first (specific roles).
- 3–5 concrete validation questions.
- One fast experiment that could be done in 1–2 weeks.

## 7. Key Assumptions to Watch
- List the most dangerous assumptions behind this opportunity.

"""
    return prompt
