import re

def parse_result(title, body):
    title = (title or "").replace("| LinkedIn", "").strip()
    body = (body or "").strip()

    parts = [
        part.strip()
        for part in re.split(r"\s[-–—]\s", title)
        if part.strip()
    ]

    name = parts[0] if parts else title
    designation = parts[1] if len(parts) > 1 else ""

    if not designation:
        designation = "Recruitment / Talent Acquisition"

    bad_results = [
        "linkedin jobs",
        "job search",
        "careers",
        "people search",
        "company page"
    ]

    if not name or any(x in name.lower() for x in bad_results):
        return None, None

    return name[:150], designation[:200]

