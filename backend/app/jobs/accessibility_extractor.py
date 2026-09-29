ACCESSIBILITY_CATEGORIES = {
    "work_arrangements": [
        "Remote work",
        "Remote",
        "Work from home",
        "Hybrid work",
        "Hybrid",
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
        "Screen reader",
        "Captioned meetings",
        "Closed captions",
        "Live captions",
        "Sign language",
        "Sign language interpreter",
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

    found_accessibility = []

    for requirements in ACCESSIBILITY_CATEGORIES.values():
        for requirement in requirements:
            if requirement.lower() in description_lower:
                found_accessibility.append(requirement)

    return list(dict.fromkeys(found_accessibility))