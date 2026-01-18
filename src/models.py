from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class IngestionStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"
    SKIPPED = "skipped"

class Report(BaseModel):
    report_id: str
    title: str
    title_ko: Optional[str] = None
    source: str = "PwC"
    url: str
    published_at: datetime
    ingestion_status: IngestionStatus = IngestionStatus.PENDING
    summary: Optional[str] = None
    summary_ko: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class OpportunityCard(BaseModel):
    card_id: str
    pain_holder: str
    pain_holder_ko: Optional[str] = None
    pain_context: str
    pain_context_ko: Optional[str] = None
    pain_mechanism: str
    pain_mechanism_ko: Optional[str] = None
    attack_vector: str
    attack_vector_ko: Optional[str] = None
    evidence_sentence: str
    evidence_sentence_ko: Optional[str] = None
    industry_tags: List[str]
    technology_tags: List[str]
    importance_score: int
    confidence_score: float
    report_id: str
    created_at: datetime = Field(default_factory=datetime.now)

class DiscardedSignal(BaseModel):
    signal_id: str
    report_id: str
    reason: str
    raw_text: str
    importance_score: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
