from typing import List, Optional
from pydantic import BaseModel, Field


class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    year: Optional[str] = None


class CandidateProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

    skills: List[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)

    years_of_experience: Optional[float] = None

    preferred_roles: List[str] = Field(default_factory=list)
    preferred_work_mode: Optional[str] = None
    disability_type: Optional[str] = None
    accessibility_needs: List[str] = Field(default_factory=list)
    assistive_technology: List[str] = Field(default_factory=list)
    workplace_accommodations: List[str] = Field(default_factory=list)