from pydantic import BaseModel, Field


class Experience(BaseModel):
    job_title: str = ""
    company: str = ""
    duration: str = ""
    description: str = ""


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)


class AccessibilityRequirements(BaseModel):
    screen_reader: bool = False
    captions: bool = False
    sign_language_interpreter: bool = False
    wheelchair_accessible: bool = False
    flexible_working_hours: bool = False
    remote_work: bool = False
    assistive_technology: bool = False
    accessible_transportation: bool = False
    other: str = ""


class WorkPreferences(BaseModel):
    work_mode: list[str] = Field(default_factory=list)
    preferred_locations: list[str] = Field(default_factory=list)
    job_types: list[str] = Field(default_factory=list)
    preferred_roles: list[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""

    # Added to match Member 3's candidate information
    location: str = ""

    skills: list[str] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    experience: list[Experience] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    certifications: list[str] = Field(default_factory=list)

    languages: list[str] = Field(default_factory=list)

    # Candidate-provided information
    accessibility_requirements: AccessibilityRequirements = Field(
        default_factory=AccessibilityRequirements
    )

    work_preferences: WorkPreferences = Field(
        default_factory=WorkPreferences
    )