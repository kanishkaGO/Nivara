import json
import ollama


def generate_match_explanation(
    candidate: dict,
    job: dict,
    match_result: dict,
) -> str:

    prompt = f"""
You are Nivara, an inclusive career assistant.

Explain this job match in 3-5 clear sentences.

Candidate skills: {candidate.get("skills", [])}
Candidate accessibility needs: {candidate.get("accessibility_needs", [])}
Candidate work preferences: {candidate.get("work_preferences", [])}
Candidate experience: {candidate.get("experience")}

Job title: {job.get("title")}
Company: {job.get("company")}
Job skills: {job.get("skills", [])}
Job accessibility: {job.get("accessibility", [])}
Job work mode: {job.get("work_mode")}
Job experience: {job.get("experience")}

Match score: {match_result.get("match_score")}
Skill match: {match_result.get("skill_match")}
Accessibility match: {match_result.get("accessibility_match")}
Work preference match: {match_result.get("work_preference_match")}
Concerns: {match_result.get("concerns", [])}

Use only the information provided.
Do not invent salary, qualifications, accessibility features, or other job details.
If accessibility information is missing, say that it is not mentioned.

Return only the explanation text.
"""

    try:
        response = ollama.generate(
            model="llama3.2:3b",
            prompt=prompt,
            stream=True,
            options={
                "num_ctx": 4096,
                "num_predict": 250,
            },
        )

        parts = []

        for chunk in response:
            text = chunk.get("response", "")

            if text:
                parts.append(text)

        return "".join(parts).strip()

    except Exception as exc:
        return f"AI explanation unavailable: {exc}"