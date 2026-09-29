ACCESSIBILITY_CATEGORIES = {
    "work_arrangements": [
        "Remote work",
        "Work from home",
        "Hybrid work",
        "Flexible hours",
        "Flexible schedule",
        "Flexible working hours",
        "Part-time",
        "Flexible working arrangements",
    ],
    "physical_accessibility": [
        "Wheelchair accessible",
        "Wheelchair accessibility",
        "Accessible office",
        "Accessible workplace",
        "Accessible building",
        "Accessible facilities",
        "Accessible parking",
        "Elevator access",
        "Step-free access",
    ],
    "communication_accessibility": [
        "Screen reader compatible",
        "Captioned meetings",
        "Closed captions",
        "Live captions",
        "Sign language interpreter",
        "Sign language",
        "Communication support",
    ],
    "assistive_technology": [
        "Assistive technology",
        "Assistive devices",
        "Accessibility software",
        "Adaptive technology",
        "Screen magnification",
        "Text-to-speech",
        "Speech-to-text",
    ],
    "workplace_support": [
        "Reasonable accommodation",
        "Workplace accommodations",
        "Disability accommodations",
        "Accessibility accommodations",
        "Individual accommodations",
        "Modified workspace",
        "Ergonomic equipment",
    ],
}


def extract_accessibility(description: str) -> list[str]:
    if not description:
        return []

    description_lower = description.lower()
    found = []

    for requirements in ACCESSIBILITY_CATEGORIES.values():
        matched = []

        for requirement in requirements:
            if requirement.lower() in description_lower:
                matched.append(requirement)

        # Keep the most specific phrase when phrases overlap.
        matched.sort(key=len, reverse=True)

        for requirement in matched:
            if not any(
                requirement.lower() in existing.lower()
                for existing in found
            ):
                found.append(requirement)

    return found
