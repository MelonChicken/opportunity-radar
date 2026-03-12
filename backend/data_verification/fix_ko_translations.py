import os, json, re, csv
from pathlib import Path
from typing import Any, Dict, List, Tuple

# pip install openai python-dotenv
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

INPUT_PATH = "data/cards.json"
OUTPUT_PATH = "data/cards_ko_fixed.json"
LOG_PATH = "data/ko_fix_log.csv"

KO_SUFFIX_FIELDS = [
    "pain_holder",
    "pain_context",
    "pain_mechanism",
    "attack_vector",
    "evidence_sentence",
]

PLACEHOLDERS = {"...", "…", "-", "null", "None"}

hangul_re = re.compile(r"[가-힣]")

def is_placeholder(v: Any) -> bool:
    if v is None:
        return True
    if not isinstance(v, str):
        return False
    s = v.strip()
    return (s == "" or s in PLACEHOLDERS)

def has_hangul(v: Any) -> bool:
    if not isinstance(v, str):
        return False
    return bool(hangul_re.search(v))

def needs_fix(ko_value: Any) -> Tuple[bool, str]:
    if is_placeholder(ko_value):
        return True, "null/empty/placeholder"
    if isinstance(ko_value, str) and not has_hangul(ko_value):
        return True, "no_hangul(looks_non_korean)"
    return False, ""

def load_json(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return [data]
    raise ValueError("JSON must be an object or a list of objects")

def save_json(path: str, data: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_to_korean(client: OpenAI, text: str) -> str:
    # 한국어만 출력, 불필요한 접두/설명 금지, 약어/고유명사 유지
    system = (
        "You are a professional Korean translator for business/consulting text. "
        "Translate the user's text into natural Korean. "
        "Rules: output Korean only; keep proper nouns, acronyms (e.g., ESG, AI, PwC) as-is; "
        "keep quotation marks; do not add explanations."
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 환경변수를 설정해주세요.")
    client = OpenAI(api_key=api_key)

    cards = load_json(INPUT_PATH)
    changes = []

    for card in cards:
        card_id = card.get("card_id", "")

        for base in KO_SUFFIX_FIELDS:
            ko_key = f"{base}_ko"
            en_key = base

            ko_val = card.get(ko_key)
            fix, reason = needs_fix(ko_val)
            if not fix:
                continue

            # 번역 원문 선택:
            # - ko가 실제 문장인데 한글이 없는 경우(스/포/영 등) -> ko 자체를 번역
            # - placeholder/null이면 -> 영어 필드를 번역
            source_text = None
            if isinstance(ko_val, str) and not is_placeholder(ko_val) and not has_hangul(ko_val):
                source_text = ko_val.strip()
                source_from = "ko_non_korean"
            else:
                source_text = (card.get(en_key) or "")
                source_from = "en_field"

            if not isinstance(source_text, str) or source_text.strip() == "":
                # 번역할 원문이 없으면 스킵(로그만 남김)
                changes.append({
                    "card_id": card_id,
                    "field": ko_key,
                    "reason": reason,
                    "source_from": source_from,
                    "old_value": ko_val,
                    "new_value": ko_val,
                    "note": "no_source_text_skip"
                })
                continue

            new_ko = translate_to_korean(client, source_text)

            old = ko_val
            card[ko_key] = new_ko

            changes.append({
                "card_id": card_id,
                "field": ko_key,
                "reason": reason,
                "source_from": source_from,
                "old_value": old,
                "new_value": new_ko,
                "note": ""
            })

    save_json(OUTPUT_PATH, cards)

    # 변경 로그 저장
    with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["card_id", "field", "reason", "source_from", "old_value", "new_value", "note"]
        )
        writer.writeheader()
        writer.writerows(changes)

    print(f"OK: saved {OUTPUT_PATH}")
    print(f"OK: log  {LOG_PATH}")
    print(f"Changed rows: {len([c for c in changes if c.get('old_value') != c.get('new_value')])}")

if __name__ == "__main__":
    main()
