import json

import ollama

from app.schemas.resume import ResumeProfile


MODEL_NAME = "llama3.2:3b"


def parse_resume_with_ai(resume_text: str) -> ResumeProfile:

    prompt = f"""
You are a resume parsing assistant for Nivara,
an inclusive career platform.

Extract only information explicitly present in the resume.

Do NOT invent information.

Return ONLY valid JSON using exactly this structure:

{{
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "skills": [],
    "education": [
        {{
            "degree": "",
            "field_of_study": "",
            "institution": "",
            "year": ""
        }}
    ],
    "experience": [
        {{
            "job_title": "",
            "company": "",
            "duration": "",
            "description": ""
        }}
    ],
    "projects": [
        {{
            "name": "",
            "description": "",
            "technologies": []
        }}
    ],
    "certifications": [],
    "languages": []
}}

If information is missing, use an empty string or empty list.

Resume:

{resume_text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    content = response["message"]["content"]

    data = json.loads(content)

    return ResumeProfile.model_validate(data)