import json
import ollama


def extract_job_intelligence(description: str) -> dict:
    if not description:
        return {
            "job_requirements": [],
            "accessibility": [],
            "accessibility_info_status": "not_mentioned",
        }

    prompt = f"""Extract information from this job description.

Job description:
{description}

Return ONLY JSON in this exact format:
{{
  "job_requirements": [],
  "accessibility": [],
  "accessibility_info_status": "not_mentioned"
}}

Rules:
- job_requirements: include explicitly stated skills, qualifications, certifications, responsibilities, experience, education, or professional requirements.
- accessibility: include only explicitly stated accessibility or accommodation information.
- Do not assume accessibility.
- accessibility_info_status must be "available" if accessibility information is explicitly stated, otherwise "not_mentioned".
- Keep items short.
- Return JSON only.
"""

    response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    options={
        "num_ctx": 2048,
        "num_predict": 300,
    },
    )

    content = response["message"]["content"].strip()

    # Remove accidental markdown fences
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        return {
            "job_requirements": [],
            "accessibility": [],
            "accessibility_info_status": "not_mentioned",
        }

    status = result.get(
        "accessibility_info_status",
        "not_mentioned"
    )

    if status not in {
        "available",
        "partially_available",
        "not_mentioned",
    }:
        status = "not_mentioned"

    return {
        "job_requirements": result.get(
            "job_requirements", []
        ),
        "accessibility": result.get(
            "accessibility", []
        ),
        "accessibility_info_status": status,
    }