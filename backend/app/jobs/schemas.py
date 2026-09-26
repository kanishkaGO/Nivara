from pydantic import BaseModel, Field
from typing import List, Optional


class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    work_mode: str
    description: str
    skills: List[str]
    accessibility: List[str] = Field(default_factory=list)
    experience: Optional[str] = None
