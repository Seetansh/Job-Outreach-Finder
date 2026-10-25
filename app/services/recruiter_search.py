from datetime import datetime

from app.domain.recruiter import parse_result
from app.integrations.search_provider import search_duckduckgo
from app.integrations.sheets_repository import get_sheet


RECRUITER_ROLES = [
    '"Talent Acquisition"',
    '"Talent Acquisition Specialist"',
    '"Talent Acquisition Partner"',
    '"Technical Recruiter"',
    '"Recruiter"',
    '"HR Recruiter"',
    '"Campus Recruiter"',
    '"Talent Partner"',
    '"Human Resources"',
]


def find_and_save_recruiters(company, location):
    sheet = get_sheet()

    existing_urls = {
        str(row.get("LinkedIn Profile URL", ""))
        .split("?")[0]
        .rstrip("/")
        .lower()
        for row in sheet.get_all_records()
    }

    found = {}

    for role in RECRUITER_ROLES:
        if len(found) >= 30:
            break

        query = f'site:linkedin.com/in/ {company} {role} {location}'

        try:
            results = search_duckduckgo(query, max_results=10)
        except Exception as e:
            print(f"Search skipped: {e}")
            results = []

        for result in results:
            url = result.get("href", "") or result.get("url", "")

            if "linkedin.com/in/" not in url.lower():
                continue

            clean_url = url.split("?")[0].rstrip("/")
            normalized_url = clean_url.lower()

            if normalized_url in existing_urls or normalized_url in found:
                continue

            name, designation = parse_result(
                result.get("title", ""),
                result.get("body", ""),
            )

            if not name:
                continue

            found[normalized_url] = [
                company,
                location,
                name,
                designation,
                clean_url,
                datetime.now().strftime("%d-%b-%Y %H:%M"),
                "Not Contacted",
                result.get("body", "")[:500],
            ]

            if len(found) >= 30:
                break

    latest_results = list(found.values())

    if latest_results:
        sheet.append_rows(
            latest_results,
            value_input_option="USER_ENTERED",
        )

    return latest_results