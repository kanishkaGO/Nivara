from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.resume_parser import extract_resume_text


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a PDF/DOCX resume and extract its text."""

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
        extracted_text = extract_resume_text(
            file.filename,
            file_bytes
        )
    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=f"Could not process resume: {str(error)}"
        )

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No readable text was found in the resume."
        )

    return {
        "filename": file.filename,
        "file_type": extension,
        "text": extracted_text
    }