import re


def extract_experience(description: str) -> str | None:
    if not description:
        return None

    text = description.lower()

    patterns = [
        r"(\d+)\s*-\s*(\d+)\s*years?\s*(?:of\s*)?experience",
        r"(\d+)\s*to\s*(\d+)\s*years?\s*(?:of\s*)?experience",
        r"(\d+)\+\s*years?\s*(?:of\s*)?experience",
        r"minimum\s*(?:of\s*)?(\d+)\s*years?",
        r"at least\s*(\d+)\s*years?",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            if len(match.groups()) == 2:
                return f"{match.group(1)}-{match.group(2)} years"

            return f"{match.group(1)}+ years"

    if "fresher" in text or "freshers" in text:
        return "Fresher"

    return None