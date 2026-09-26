from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from .data import JOBS
from .schemas import Job
from .accessibility import AccessibilityRequest, AccessibilityResponse


router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=List[Job])
def get_jobs(
    search: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    work_mode: Optional[str] = Query(default=None),
):
    results = JOBS

    if search:
        search_text = search.lower()
        results = [
            job for job in results
            if search_text in job.title.lower()
            or search_text in job.description.lower()
            or any(search_text in skill.lower() for skill in job.skills)
        ]

    if location:
        results = [
            job for job in results
            if location.lower() in job.location.lower()
        ]

    if work_mode:
        results = [
            job for job in results
            if job.work_mode.lower() == work_mode.lower()
        ]

    return results


@router.get("/{job_id}", response_model=Job)
def get_job(job_id: str):
    for job in JOBS:
        if job.id == job_id:
            return job

    raise HTTPException(status_code=404, detail="Job not found")


@router.post("/{job_id}/accessibility", response_model=AccessibilityResponse)
def analyze_accessibility(
    job_id: str,
    request: AccessibilityRequest
):
    for job in JOBS:
        if job.id == job_id:
            job_accessibility = {
                item.lower() for item in job.accessibility
            }

            matched = [
                accommodation
                for accommodation in request.required_accommodations
                if accommodation.lower() in job_accessibility
            ]

            missing = [
                accommodation
                for accommodation in request.required_accommodations
                if accommodation.lower() not in job_accessibility
            ]

            total = len(request.required_accommodations)

            if total == 0:
                score = 100
            else:
                score = round((len(matched) / total) * 100)

            return AccessibilityResponse(
                job_id=job.id,
                compatible=len(missing) == 0,
                matched_accommodations=matched,
                missing_accommodations=missing,
                compatibility_score=score,
            )

    raise HTTPException(status_code=404, detail="Job not found")