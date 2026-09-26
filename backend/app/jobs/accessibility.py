from pydantic import BaseModel
from typing import List


class AccessibilityRequest(BaseModel):
    required_accommodations: List[str]


class AccessibilityResponse(BaseModel):
    job_id: str
    compatible: bool
    matched_accommodations: List[str]
    missing_accommodations: List[str]
    compatibility_score: int