from io import BytesIO

import fitz
from docx import Document


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    document = fitz.open(stream=file_bytes, filetype="pdf")

    text = []

    for page in document:
        text.append(page.get_text())

    document.close()

    return "\n".join(text).strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    document = Document(BytesIO(file_bytes))

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    """Extract text from a supported resume file."""
    extension = "." + filename.split(".")[-1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_bytes)

    if extension == ".docx":
        return extract_text_from_docx(file_bytes)

    raise ValueError(
        "Unsupported file type. Only PDF and DOCX files are allowed."
    )