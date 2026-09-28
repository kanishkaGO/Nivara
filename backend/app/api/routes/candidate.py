from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import (
    AccessibilityRequirements,
    WorkPreferences,
)


router = APIRouter(
    prefix="/candidate",
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


@router.put("/{candidate_id}/accessibility")
async def update_accessibility(
    candidate_id: int,
    requirements: AccessibilityRequirements,
    db: Session = Depends(get_db),
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

    candidate.accessibility_requirements = requirements.model_dump()

    db.commit()
    db.refresh(candidate)

    return {
        "message": "Accessibility requirements updated",
        "candidate_id": candidate.id,
        "accessibility_requirements": (
            candidate.accessibility_requirements
        ),
    }


@router.put("/{candidate_id}/preferences")
async def update_preferences(
    candidate_id: int,
    preferences: WorkPreferences,
    db: Session = Depends(get_db),
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

    candidate.work_preferences = preferences.model_dump()

    db.commit()
    db.refresh(candidate)

    return {
        "message": "Work preferences updated",
        "candidate_id": candidate.id,
        "work_preferences": candidate.work_preferences,
    }