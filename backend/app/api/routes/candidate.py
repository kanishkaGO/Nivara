from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.candidate import BasicProfileUpdate

from app.core.database import get_db
from app.models.candidate import Candidate


router = APIRouter(
    prefix="/api/v1/candidate",
    tags=["Candidate"]
)


@router.get("/{candidate_id}")
async def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "location": candidate.location,
        "skills": candidate.skills,
        "education": candidate.education,
        "experience": candidate.experience,
        "projects": candidate.projects,
        "certifications": candidate.certifications,
        "languages": candidate.languages,
        "accessibility_requirements": (
            candidate.accessibility_requirements
        ),
        "work_preferences": candidate.work_preferences,
    }

@router.get("/{candidate_id}/completeness")
async def get_profile_completeness(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    sections = {
        "basic_information": bool(
            candidate.name
            and candidate.email
            and candidate.phone
            and candidate.location
        ),
        "skills": bool(candidate.skills),
        "education": bool(candidate.education),
        "experience": bool(candidate.experience),
        "projects": bool(candidate.projects),
        "certifications": bool(candidate.certifications),
        "languages": bool(candidate.languages),
        "accessibility_requirements": bool(
            candidate.accessibility_requirements
        ),
        "work_preferences": bool(
            candidate.work_preferences
        ),
    }

    completed = sum(sections.values())
    total = len(sections)

    completion_percentage = round(
        (completed / total) * 100
    )

    missing_sections = [
        section
        for section, completed_status in sections.items()
        if not completed_status
    ]

    return {
        "candidate_id": candidate.id,
        "completion_percentage": completion_percentage,
        "completed_sections": completed,
        "total_sections": total,
        "missing_sections": missing_sections,
    }

@router.put("/{candidate_id}")
async def update_basic_profile(
    candidate_id: int,
    profile: BasicProfileUpdate,
    db: Session = Depends(get_db)
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    candidate.name = profile.name.strip()
    candidate.email = profile.email.strip()
    candidate.phone = profile.phone.strip()
    candidate.location = profile.location.strip()

    db.commit()
    db.refresh(candidate)

    return {
        "message": "Basic profile updated successfully",
        "candidate_id": candidate.id,
        "candidate": {
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "location": candidate.location,
        }
    }