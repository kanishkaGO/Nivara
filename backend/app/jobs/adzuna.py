import os
import requests

from dotenv import load_dotenv
from .skill_extractor import extract_skills
from .schemas import Job

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
        raise RuntimeError("Adzuna API credentials are not configured.")

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
        jobs.append(
            Job(
                id=item.get("id", item.get("adref", "")),
                title=item.get("title", "Unknown"),
                company=item.get("company", {}).get(
                    "display_name",
                    "Unknown",
                ),
                location=item.get("location", {}).get(
                    "display_name",
                    location,
                ),
                work_mode="unknown",
                description=item.get("description", ""),
                skills=extract_skills(
                    item.get("description", "")
                ),
                accessibility=[],
                experience=None,
            )
        )

    return jobs
