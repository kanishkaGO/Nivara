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

    # Accessibility information explicitly found in the job posting
    accessibility: List[str] = Field(default_factory=list)

    # Whether the posting contains any accessibility information
    accessibility_info_available: bool = False

    # More precise status of accessibility information
    accessibility_info_status: str = "not_mentioned"

    # Requirements extracted from the job posting
    job_requirements: List[str] = Field(default_factory=list)

    # Experience requirement extracted from the posting
    experience: Optional[str] = None