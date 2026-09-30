import json
import ollama

from candidate_ai.models.candidate import CandidateProfile


def analyze_resume(resume_text: str) -> CandidateProfile:

    prompt = f"""
You are Nivara's resume analysis AI.

Nivara is an inclusive career platform for Persons with Disabilities
(PWDs).

Analyze the following resume and return ONLY valid JSON.

Rules:
1. Extract information only if explicitly present in the resume.
2. Never invent missing information.
3. Return empty lists where information is missing.
4. Return null for missing optional scalar values.
5. Education MUST be returned as a list of objects with:
   - institution
   - degree
   - field_of_study
   - year
6. Experience MUST be returned as a list of objects with:
   - company
   - role
   - duration
   - description
7. Extract accessibility_needs only when explicitly mentioned.
8. Extract assistive_technology only when explicitly mentioned.
9. Extract workplace_accommodations only when explicitly mentioned.
10. Return JSON only. No explanation or markdown.

Expected JSON structure:

{{
    "name": null,
    "email": null,
    "phone": null,
    "location": null,
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "languages": [],
    "years_of_experience": null,
    "preferred_roles": [],
    "preferred_work_mode": null,
    "disability_type": null,
    "accessibility_needs": [],
    "assistive_technology": [],
    "workplace_accommodations": []
}}

RESUME:
----------------
{resume_text}
----------------
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_response = response["message"]["content"]

    print("Raw Ollama response:")
    print(raw_response)

    try:
        data = json.loads(raw_response)

        # Normalize education returned by Ollama.
        normalized_education = []

        for item in data.get("education", []):
            if isinstance(item, str):
                normalized_education.append({
                    "institution": None,
                    "degree": item,
                    "field_of_study": None,
                    "year": None
                })

            elif isinstance(item, dict):
                normalized_education.append(item)

        data["education"] = normalized_education

        # Normalize experience returned by Ollama.
        normalized_experience = []

        for item in data.get("experience", []):
            if isinstance(item, str):
                normalized_experience.append({
                    "company": None,
                    "role": item,
                    "duration": None,
                    "description": None
                })

            elif isinstance(item, dict):
                normalized_experience.append(item)

        data["experience"] = normalized_experience

        # Normalize certifications returned by Ollama.
        normalized_certifications = []

        for item in data.get("certifications", []):
            if isinstance(item, str):
                normalized_certifications.append(item)

            elif isinstance(item, dict):
                certification = item.get("certification")

                if certification:
                    normalized_certifications.append(certification)

        data["certifications"] = normalized_certifications

        return CandidateProfile(**data)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Ollama returned invalid JSON: {e}"
        )

    except Exception as e:
        raise ValueError(
            f"Failed to create CandidateProfile: {e}"
        )
