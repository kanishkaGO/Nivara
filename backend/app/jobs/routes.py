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
    recommendations = []

    for job in JOBS:
        job_data = job.model_dump()

        match_result = generate_job_match(
            candidate=candidate,
            job=job_data,
        )

        # Only recommend jobs with at least one matching skill.
        if not match_result.skill_match.startswith("Matched skills:"):
            continue

        recommendations.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "match_score": match_result.match_score,
            "skill_match": match_result.skill_match,
            "accessibility_match": match_result.accessibility_match,
            "work_preference_match": match_result.work_preference_match,
            "concerns": match_result.concerns,
            "overall_explanation": match_result.overall_explanation,
            "accessibility": job.accessibility,
            "accessibility_info_available": job.accessibility_info_available,
            "work_mode": job.work_mode,
            "experience": job.experience,
        })

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True,
    )

    return {
        "candidate": candidate.model_dump(),
        "recommendations": recommendations,
    }
from .agent import generate_match_explanation

@router.post("/{job_id}/explain-match")
def explain_job_match(
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

            ai_explanation = generate_match_explanation(
                candidate=candidate.model_dump(),
                job=job_data,
                match_result=match_result.model_dump(),
            )

            return {
                "job_id": job.id,
                "match_score": match_result.match_score,
                "ai_explanation": ai_explanation,
            }

    raise HTTPException(
        status_code=404,
        detail="Job not found",
    )