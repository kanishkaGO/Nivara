from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from .data import JOBS
from .schemas import Job
from .accessibility import AccessibilityRequest, AccessibilityResponse
from .candidate import Candidate
from .matching import generate_job_match
from .adzuna import search_adzuna_jobs

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
@router.get("/live", response_model=List[Job])
def get_live_jobs(
    search: str = Query(...),
    location: str = Query(default="India"),
):
    return search_adzuna_jobs(
        query=search,
        location=location,
        page=1,
        results_per_page=10,
    )


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


@router.post("/{job_id}/match")
def match_candidate_to_job(
    job_id: str,
    candidate: Candidate,
):
    for job in JOBS:
        if job.id == job_id:
            job_data = job.model_dump()

            match_result = generate_job_match(
                candidate=candidate,
                job=job_data,
            )

            return {
                "job_id": job.id,
                "match_analysis": match_result,
            }

    raise HTTPException(status_code=404, detail="Job not found")

@router.post("/recommend")
def recommend_jobs(candidate: Candidate):
    candidate_skills = {
        skill.lower()
        for skill in candidate.skills
    }

    recommendations = []

    for job in JOBS:
        job_skills = {
            skill.lower()
            for skill in job.skills
        }

        # Fast deterministic skill matching
        matched_skills = [
            skill for skill in job.skills
            if skill.lower() in candidate_skills
        ]

        if not matched_skills:
            continue

        skill_score = round(
            (len(matched_skills) / len(job_skills)) * 100
        )

        recommendations.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "skill_match_score": skill_score,
            "matched_skills": list(matched_skills),
            "accessibility": job.accessibility,
            "work_mode": job.work_mode,
        })

    recommendations.sort(
        key=lambda x: x["skill_match_score"],
        reverse=True
    )

    return {
        "candidate": candidate.model_dump(),
        "recommendations": recommendations,
    }
