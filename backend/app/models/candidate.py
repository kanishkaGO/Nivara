from sqlalchemy import JSON, Column, Integer, String


from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, default="")
    email = Column(String, nullable=False, default="")
    phone = Column(String, nullable=False, default="")
    location = Column(String, nullable=False, default="")

    skills = Column(JSON, nullable=False, default=list)
    education = Column(JSON, nullable=False, default=list)
    experience = Column(JSON, nullable=False, default=list)
    projects = Column(JSON, nullable=False, default=list)
    certifications = Column(JSON, nullable=False, default=list)
    languages = Column(JSON, nullable=False, default=list)

    accessibility_requirements = Column(
        JSON,
        nullable=False,
        default=dict
    )

    work_preferences = Column(
        JSON,
        nullable=False,
        default=dict
    )