import re


def extract_experience(description: str) -> str | None:
    if not description:
        return None

    text = description.lower()

    patterns = [
        r"\b(\d+)\s*(?:-|to)\s*(\d+)\s*years?\b",
        r"\b(\d+)\+\s*years?\b",
        r"\b(\d+)\s*years?\s*(?:of\s*)?experience\b",
        r"\bminimum\s*(?:of\s*)?(\d+)\s*years?\b",
        r"\bat\s+least\s+(\d+)\s*years?\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if not match:
            continue

        if len(match.groups()) == 2:
            return f"{match.group(1)}-{match.group(2)} years"

        return f"{match.group(1)}+ years"

    if "fresher" in text or "freshers" in text:
        return "Fresher"

    return None
