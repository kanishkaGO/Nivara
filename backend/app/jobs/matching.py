import ollama


def generate_job_match(candidate: dict, job: dict) -> str:
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

Provide a concise job-match analysis with these sections:

1. Skill match
2. Accessibility match
3. Work preference match
4. Missing requirements or possible concerns
5. Overall match explanation

Do not make assumptions about the candidate's disability, abilities, or needs.
Use only the information provided.
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]