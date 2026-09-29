from .match_schema import MatchResult


def _normalize(values):
    return {value.strip().lower() for value in values if value.strip()}


def _experience_range(value):
    if not value:
        return None

    import re

    text = str(value).lower()

    # Example: "1-3 years" or "1 to 3 years"
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)", text)

    if match:
        return float(match.group(1)), float(match.group(2))

    # Example: "3+ years"
    match = re.search(r"(\d+(?:\.\d+)?)\s*\+", text)

    if match:
        minimum = float(match.group(1))
        return minimum, None

    # Example: "2 years"
    match = re.search(r"(\d+(?:\.\d+)?)\s*years?", text)

    if match:
        years = float(match.group(1))
        return years, years

    return None


def generate_job_match(candidate, job: dict) -> MatchResult:
    candidate_skills = _normalize(candidate.skills)
    job_skills = _normalize(job.get("skills", []))

    matched_skills = candidate_skills & job_skills

    if job_skills:
        skill_score = round(
            len(matched_skills) / len(job_skills) * 100
        )
    else:
        skill_score = 0

    # -------------------------
    # Experience matching
    # -------------------------

    candidate_experience = _experience_range(candidate.experience)
    job_experience = _experience_range(job.get("experience"))

    if candidate_experience is None or job_experience is None:
        experience_score = 50
        experience_text = "Experience information is incomplete."

    else:
        candidate_min, candidate_max = candidate_experience
        job_min, job_max = job_experience

        # Candidate meets the minimum requirement.
        if candidate_max >= job_min:
            experience_score = 100
            experience_text = (
                "The candidate meets the stated experience requirement."
            )
        else:
            experience_score = 0
            experience_text = (
                "The candidate has less experience than the stated requirement."
            )

    # -------------------------
    # Accessibility matching
    # -------------------------

    candidate_needs = _normalize(candidate.accessibility_needs)
    job_accessibility = _normalize(job.get("accessibility", []))

    if not candidate_needs:
        accessibility_score = 100
        accessibility_text = (
            "No specific accessibility requirement was provided."
        )

    elif not job_accessibility:
        accessibility_score = 50
        accessibility_text = (
            "The job does not provide explicit accessibility information."
        )

    else:
        matched_accessibility = candidate_needs & job_accessibility

        accessibility_score = round(
            len(matched_accessibility)
            / len(candidate_needs)
            * 100
        )

        if accessibility_score == 100:
            accessibility_text = (
                "The stated accessibility needs are explicitly supported."
            )
        elif accessibility_score > 0:
            accessibility_text = (
                "Some stated accessibility needs are explicitly supported."
            )
        else:
            accessibility_text = (
                "The stated accessibility needs are not explicitly listed."
            )

    # -------------------------
    # Work preference matching
    # -------------------------

    preferences = _normalize(candidate.work_preferences)
    work_mode = str(job.get("work_mode", "unknown")).lower()

    if not preferences:
        preference_score = 100
        preference_text = (
            "No specific work preference was provided."
        )

    elif work_mode == "unknown":
        preference_score = 50
        preference_text = (
            "The job does not explicitly state its work mode."
        )

    elif any(
        preference in work_mode
        or work_mode in preference
        for preference in preferences
    ):
        preference_score = 100
        preference_text = (
            "The job work mode matches the candidate's preference."
        )

    else:
        preference_score = 0
        preference_text = (
            "The job work mode does not match the candidate's stated preference."
        )

    # -------------------------
    # Overall score
    # -------------------------

    match_score = round(
        (
            skill_score * 0.40
            + experience_score * 0.20
            + accessibility_score * 0.25
            + preference_score * 0.15
        )
    )

    # -------------------------
    # Concerns
    # -------------------------

    concerns = []

    # Only report missing job skills when the candidate
    # actually fails to match some required job skills.
    missing_job_skills = job_skills - candidate_skills

    if missing_job_skills:
        concerns.append(
            "Some required job skills are not present in the candidate profile."
        )

    if experience_score == 0:
        concerns.append(
            "The candidate does not meet the stated experience requirement."
        )

    if candidate_needs and not job_accessibility:
        concerns.append(
            "Accessibility information is not mentioned in the job description."
        )

    if preference_score == 0:
        concerns.append(
            "The stated work preference does not match the job work mode."
        )

    # -------------------------
    # Explanations
    # -------------------------

    skill_text = (
        "Matched skills: "
        + ", ".join(sorted(matched_skills))
        if matched_skills
        else "No matching skills were identified."
    )

    overall_explanation = (
        f"Overall match score: {match_score}/100. "
        f"{skill_text}. "
        f"{experience_text} "
        f"{accessibility_text} "
        f"{preference_text}"
    )

    return MatchResult(
        match_score=match_score,
        skill_match=skill_text,
        accessibility_match=accessibility_text,
        work_preference_match=preference_text,
        concerns=concerns,
        overall_explanation=overall_explanation,
    )
