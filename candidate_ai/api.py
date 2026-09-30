from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from candidate_ai.utils.resume_parser import extract_resume_text
from candidate_ai.services.resume_analyzer import analyze_resume


router = APIRouter()


@router.get("/candidate/health")
def candidate_health():
    return {
        "status": "healthy",
        "service": "candidate-ai"
    }


@router.post("/analyze-resume")
async def analyze_resume_endpoint(
    file: UploadFile = File(...)
):
    allowed_extensions = {".pdf", ".docx", ".doc"}

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and DOC files are supported."
        )

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume_text = extract_resume_text(str(file_path))

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        profile = analyze_resume(resume_text)

        return {
            "filename": file.filename,
            "status": "success",
            "candidate_profile": profile.model_dump()
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
