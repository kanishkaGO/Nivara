from pydantic import BaseModel, Field
from typing import List


class Candidate(BaseModel):
    skills: List[str] = Field(default_factory=list)
    accessibility_needs: List[str] = Field(default_factory=list)
    work_preferences: List[str] = Field(default_factory=list)
    experience: str = "Not provided"