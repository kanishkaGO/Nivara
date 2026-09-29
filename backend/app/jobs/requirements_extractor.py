import re


def extract_job_requirements(description: str) -> list[str]:
    if not description:
        return []

    requirements = []

    # Experience requirements
    experience_patterns = [
        r"\b\d+\s*[-to]+\s*\d+\s*years?\b",
        r"\b\d+\+\s*years?\b",
        r"\b\d+\s*years?\s+(?:of\s+)?experience\b",
        r"\bminimum\s+(?:of\s+)?\d+\s*years?\b",
        r"\bat\s+least\s+\d+\s*years?\b",
    ]

    for pattern in experience_patterns:
        requirements.extend(
            re.findall(
                pattern,
                description,
                flags=re.IGNORECASE,
            )
        )

    # Explicit qualification / certification phrases
    qualification_patterns = [
        r"(?:bachelor'?s|master'?s|ph\.?d\.?|degree)\s+(?:degree\s+)?(?:in\s+)?[A-Za-z &]+",
        r"\b[A-Z][A-Za-z]+ certification\b",
        r"\b[A-Z][A-Za-z]+ certified\b",
    ]

    for pattern in qualification_patterns:
        requirements.extend(
            re.findall(
                pattern,
                description,
                flags=re.IGNORECASE,
            )
        )

    # Known professional requirements from the same description
    requirement_keywords = [
        "Python",
        "SQL",
        "Java",
        "JavaScript",
        "React",
        "HTML",
        "CSS",
        "Excel",
        "Tally",
        "AWS",
        "Azure",
        "Git",
        "REST API",
        "FastAPI",
        "Django",
        "Recruitment",
        "Talent Acquisition",
        "Employee Relations",
        "Financial Reporting",
        "Bookkeeping",
        "Lesson Planning",
        "Classroom Management",
        "Communication",
        "Graphic Design",
        "UI Design",
        "Figma",
        "Customer Service",
        "Project Management",
        "Sales",
        "Marketing",
    ]

    description_lower = description.lower()

    for keyword in requirement_keywords:
        if keyword.lower() in description_lower:
            requirements.append(keyword)

    # Remove duplicates while preserving order
    cleaned = []

    for requirement in requirements:
        requirement = requirement.strip()

        if requirement and requirement not in cleaned:
            cleaned.append(requirement)

    return cleaned