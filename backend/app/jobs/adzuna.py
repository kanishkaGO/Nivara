import os
import requests
from .work_mode_extractor import extract_work_mode

from dotenv import load_dotenv
from .experience_extractor import extract_experience
from .schemas import Job
from .skill_extractor import extract_skills
from .accessibility_extractor import extract_accessibility
from .requirements_extractor import extract_job_requirements

load_dotenv()

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search"


def search_adzuna_jobs(
    query: str,
    location: str = "India",
    page: int = 1,
    results_per_page: int = 10,
):
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise RuntimeError(
            "Adzuna API credentials are not configured."
        )

    url = f"{ADZUNA_BASE_URL}/{page}"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": query,
        "where": location,
        "results_per_page": results_per_page,
    }

    response = requests.get(
        url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for item in data.get("results", []):
        description = item.get("description", "")
        extracted_skills = extract_skills(description)
        extracted_accessibility = extract_accessibility(description)

        jobs.append(
            Job(
                id=item.get(
                    "id",
                    item.get("adref", ""),
                ),
                title=item.get(
                    "title",
                    "Unknown",
                ),
                company=item.get(
                    "company",
                    {}
                ).get(
                    "display_name",
                    "Unknown",
                ),
                location=item.get(
                    "location",
                    {}
                ).get(
                    "display_name",
                    location,
                ),
                work_mode=extract_work_mode(description),
                description=description,
                skills=extracted_skills,
                accessibility=extracted_accessibility,
                accessibility_info_available=bool(
                    extracted_accessibility
                ),
                accessibility_info_status=(
                    "available"
                    if extracted_accessibility
                    else "not_mentioned"
                ),
                experience=extract_experience(description),
                job_requirements=extract_job_requirements(description),
            )
        )

    return jobs
