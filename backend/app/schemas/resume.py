from pydantic import BaseModel, Field


class Experience(BaseModel):
    job_title: str = ""
    company: str = ""
    duration: str = ""
    description: str = ""


class Education(BaseModel):
    degree: str = ""
    field_of_study: str = ""
    institution: str = ""
    year: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)


class ResumeProfile(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""

    location: str = ""

    skills: list[str] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    experience: list[Experience] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    certifications: list[str] = Field(default_factory=list)

    languages: list[str] = Field(default_factory=list)