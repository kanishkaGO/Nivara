from pydantic import BaseModel, Field
from typing import List, Optional

class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    work_mode: str
    description: str
    skills: List[str] = Field(default_factory=list)
    accessibility: List[str] = Field(default_factory=list)
    accessibility_info_available: bool = False
    accessibility_info_status: str = "not_mentioned"
    job_requirements: List[str] = Field(default_factory=list)
    experience: Optional[str] = None
