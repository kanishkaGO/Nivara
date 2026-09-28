from pydantic import BaseModel
from typing import List


class MatchResult(BaseModel):
    match_score: int
    skill_match: str
    accessibility_match: str
    work_preference_match: str
    concerns: List[str]
    overall_explanation: str