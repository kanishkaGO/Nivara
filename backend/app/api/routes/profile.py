from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import (
    AccessibilityRequirements,
    WorkPreferences,
)


router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Profile"]
)


@router.put("/{candidate_id}/accessibility")
def update_accessibility(
    candidate_id: int,
    requirements: AccessibilityRequirements,
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    candidate.accessibility_requirements = requirements.model_dump()

    db.commit()
    db.refresh(candidate)

    return {
        "candidate_id": candidate.id,
        "accessibility_requirements":
            candidate.accessibility_requirements
    }


@router.put("/{candidate_id}/preferences")
def update_preferences(
    candidate_id: int,
    preferences: WorkPreferences,
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    candidate.work_preferences = preferences.model_dump()

    db.commit()
    db.refresh(candidate)

    return {
        "candidate_id": candidate.id,
        "work_preferences":
            candidate.work_preferences
    }