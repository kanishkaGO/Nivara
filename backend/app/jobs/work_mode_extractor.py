WORK_MODE_CATEGORIES = {
    "remote": [
        "remote",
        "remote work",
        "work from home",
        "working remotely",
        "fully remote",
    ],

    "hybrid": [
        "hybrid",
        "hybrid work",
        "hybrid working",
        "partially remote",
        "remote and office",
    ],

    "onsite": [
    "on-site",
    "onsite",
    "on site",
    "office-based",
    "office based",
    "work from office",
    "in-office",
    ],
}
def extract_work_mode(description: str) -> str:
    if not description:
        return "unknown"

    description_lower = description.lower()

    matches = []

    for work_mode, phrases in WORK_MODE_CATEGORIES.items():
        for phrase in phrases:
            if phrase in description_lower:
                matches.append(work_mode)
                break

    # If exactly one work mode is mentioned, use it.
    if len(matches) == 1:
        return matches[0]

    # If multiple work modes are mentioned,
    # don't make an assumption.
    return "unknown"
