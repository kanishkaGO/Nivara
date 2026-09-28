import ollama
from .match_schema import MatchResult

def generate_job_match(candidate: dict, job: dict) -> MatchResult:
    candidate = candidate.model_dump()
    prompt = f"""
You are Nivara's Job Matching Agent.

Compare the candidate with the job using ONLY the information provided.

Candidate:
Skills: {candidate.get("skills", [])}
Accessibility needs: {candidate.get("accessibility_needs", [])}
Work preferences: {candidate.get("work_preferences", [])}
Experience: {candidate.get("experience", "Not provided")}

Job:
Title: {job.get("title")}
Company: {job.get("company")}
Location: {job.get("location")}
Work mode: {job.get("work_mode")}
Skills: {job.get("skills", [])}
Accessibility: {job.get("accessibility", [])}
Experience: {job.get("experience", "Not provided")}
Description: {job.get("description")}

Return ONLY valid JSON matching this exact structure:

{{
  "match_score": 0,
  "skill_match": "Brief explanation of skill alignment",
  "accessibility_match": "Brief explanation of accessibility alignment",
  "work_preference_match": "Brief explanation of work preference alignment",
  "concerns": ["Concern 1", "Concern 2"],
  "overall_explanation": "Brief overall explanation"
}}

Rules:
- match_score must be an integer from 0 to 100.
- concerns must always be a JSON list.
- Use only the candidate and job information provided.
- Do not make assumptions about disability, abilities, or accessibility needs.
- Return JSON only. No markdown and no extra text.

Do not make assumptions about the candidate's disability, abilities, or needs.
Use only the information provided.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return MatchResult.model_validate_json(
        response["message"]["content"]
    )
