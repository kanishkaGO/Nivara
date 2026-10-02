from typing import Any, Dict, List

from .candidate import Candidate


def _split_skill_groups(skills: List[str]) -> List[str]:
    """Convert grouped resume skills into individual skills."""
    result = []

    for skill_group in skills or []:
        if ":" in skill_group:
            _, values = skill_group.split(":", 1)
            parts = values.split(",")
        else:
            parts = [skill_group]

        for part in parts:
            skill = part.strip()
            if skill:
                result.append(skill)

    return list(dict.fromkeys(result))


def _extract_accessibility_needs(
    accessibility_requirements: Dict[str, Any] | None,
) -> List[str]:
    """Convert stored accessibility flags into matcher-friendly labels."""
    if not accessibility_requirements:
        return []

    labels = {
        "screen_reader": "Screen reader compatible",
        "captions": "Captioned meetings",
        "sign_language_interpreter": "Sign language interpreter",
        "wheelchair_accessible": "Wheelchair accessible",
        "flexible_working_hours": "Flexible hours",
        "remote_work": "Remote work",
        "assistive_technology": "Assistive technology",
        "accessible_transportation": "Accessible transportation",
    }

    needs = []

    for key, label in labels.items():
        if accessibility_requirements.get(key):
            needs.append(label)

    other = accessibility_requirements.get("other", "")
    if other:
        needs.append(str(other))

    return needs


def _extract_work_preferences(
    work_preferences: Dict[str, Any] | None,
) -> List[str]:
    """Convert stored work preferences into matcher-friendly labels."""
    if not work_preferences:
        return []

    preferences = []

    work_modes = work_preferences.get("work_mode", [])
    if isinstance(work_modes, list):
        preferences.extend(str(value) for value in work_modes)
    elif work_modes:
        preferences.append(str(work_modes))

    return list(dict.fromkeys(preferences))


def _calculate_experience(experience: List[Dict[str, Any]] | None) -> str:
    """
    Convert structured experience records into a total experience
    expressed in years, while preserving sub-year experience.
    """
    if not experience:
        return "Not provided"

    import re

    total_months = 0.0

    for item in experience:
        duration = str(item.get("duration", "")).lower()

        weeks = re.findall(r"(\d+(?:\.\d+)?)\s*weeks?", duration)
        months = re.findall(r"(\d+(?:\.\d+)?)\s*months?", duration)

        if weeks:
            total_months += sum(float(value) for value in weeks) / 4.345

        if months:
            total_months += sum(float(value) for value in months)

    if total_months <= 0:
        return "Not provided"

    years = total_months / 12

    if years < 1:
        return f"{round(total_months, 1)} months"

    return f"{round(years, 1)} years"

def candidate_from_profile(profile: Dict[str, Any]) -> Candidate:
    """Convert a persisted Candidate API response into matcher Candidate."""
    return Candidate(
        skills=_split_skill_groups(profile.get("skills", [])),
        accessibility_needs=_extract_accessibility_needs(
            profile.get("accessibility_requirements")
        ),
        work_preferences=_extract_work_preferences(
            profile.get("work_preferences")
        ),
        experience=_calculate_experience(profile.get("experience", [])),
    )
