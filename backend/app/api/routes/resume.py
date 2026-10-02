from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.candidate import Candidate
from app.services.ai_parser import parse_resume_with_ai
from app.services.resume_parser import extract_resume_text


router = APIRouter(
    prefix="/api/v1/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a resume, parse it with Ollama, and save the candidate."""

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    extension = "." + file.filename.split(".")[-1].lower()

    if extension not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        resume_text = extract_resume_text(
            file.filename,
            file_bytes
        )

        if not resume_text:
            raise HTTPException(
                status_code=422,
                detail="No readable text was found in the resume."
            )

        resume_profile = parse_resume_with_ai(resume_text)

        candidate = Candidate(
            name=resume_profile.name,
            email=resume_profile.email,
            phone=resume_profile.phone,
            location=resume_profile.location,
            skills=resume_profile.skills,
            education=[
                education.model_dump()
                for education in resume_profile.education
            ],
            experience=[
                experience.model_dump()
                for experience in resume_profile.experience
            ],
            projects=[
                project.model_dump()
                for project in resume_profile.projects
            ],
            certifications=resume_profile.certifications,
            languages=resume_profile.languages
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

    except HTTPException:
        raise

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=f"Could not process resume: {str(error)}"
        )

    return {
        "message": "Resume processed successfully",
        "candidate_id": candidate.id,
        "candidate": {
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
            "work_preferences": candidate.work_preferences
        }
    }