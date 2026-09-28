from .schemas import Job


JOBS = [
    Job(
        id="J001",
        title="Python Developer",
        company="TechNova",
        location="Remote",
        work_mode="remote",
        description="Develop and maintain Python applications and REST APIs.",
        skills=["Python", "FastAPI", "SQL", "REST API"],
        accessibility=["Remote work", "Flexible hours", "Screen reader compatible"],
        experience="1-3 years"
    ),
    Job(
        id="J002",
        title="Frontend Developer",
        company="DigitalWorks",
        location="Bengaluru",
        work_mode="hybrid",
        description="Build accessible web interfaces using React and JavaScript.",
        skills=["React", "JavaScript", "HTML", "CSS"],
        accessibility=["Accessible office", "Flexible hours", "Captioned meetings"],
        experience="1-2 years"
    ),
    Job(
        id="J003",
        title="Data Analyst",
        company="InsightLabs",
        location="Remote",
        work_mode="remote",
        description="Analyze business data and create reports using Python and SQL.",
        skills=["Python", "SQL", "Excel", "Data Analysis"],
        accessibility=["Remote work", "Flexible hours"],
        experience="1-3 years"
    )
]
