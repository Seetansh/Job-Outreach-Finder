import os
import re
from datetime import datetime

import gspread
from ddgs import DDGS
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash
from google.oauth2.service_account import Credentials

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret")

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")
SHEET_NAME = os.getenv("SHEET_NAME", "Recruiters")
GOOGLE_CREDS_FILE = os.getenv("GOOGLE_CREDS_FILE", "service_account.json")


HEADERS = [
    "Company",
    "Search Location",
    "Recruiter Name",
    "Designation",
    "LinkedIn Profile URL",
    "Search Date",
    "Status",
    "Source Snippet"
]

RECRUITER_ROLES = [
    '"Talent Acquisition"',
    '"Talent Acquisition Specialist"',
    '"Talent Acquisition Partner"',
    '"Technical Recruiter"',
    '"Recruiter"',
    '"HR Recruiter"',
    '"Campus Recruiter"',
    '"Talent Partner"',
    '"Human Resources"'
]



def get_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDS_FILE,
        scopes=scopes
    )

    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    try:
        sheet = spreadsheet.worksheet(SHEET_NAME)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(
            title=SHEET_NAME,
            rows=2000,
            cols=len(HEADERS)
        )

    if not sheet.row_values(1):
        sheet.append_row(HEADERS)

    return sheet


def search_duckduckgo(query, max_results=10):
    backends = [
        "bing",
        "brave",
        "yahoo",
        "duckduckgo",
        "yandex"
    ]

    for backend in backends:
        try:
            print(f"Trying backend: {backend}")

            results = DDGS().text(
                query,
                max_results=max_results,
                backend=backend
            )

            results = list(results)

            if results:
                print(f"Success with {backend}: {len(results)} results")
                return results

        except Exception as e:
            print(f"{backend} failed: {e}")

    return []


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


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        location = request.form.get("location", "").strip()

        if not company or not location:
            flash("Please enter both Company and Location.", "danger")

        else:
            try:
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

                        clean_url = (
                            url.split("?")[0]
                            .rstrip("/")
                        )

                        normalized_url = clean_url.lower()

                        if (
                            normalized_url in existing_urls
                            or normalized_url in found
                        ):
                            continue

                        name, designation = parse_result(
                            result.get("title", ""),
                            result.get("body", "")
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
                            result.get("body", "")[:500]
                        ]

                        if len(found) >= 30:
                            break

                if found:
                    latest_results = list(found.values())

                    sheet.append_rows(
                        latest_results,
                        value_input_option="USER_ENTERED"
                    )

                    flash(
                        f"Success! Found and saved {len(latest_results)} new unique profiles.",
                        "success"
                    )

                    return render_template(
                        "index.html",
                        rows=[
                            {
                                "Company": r[0],
                                "Search Location": r[1],
                                "Recruiter Name": r[2],
                                "Designation": r[3],
                                # "LinkedIn Profile URL": r[4],
                                # "Search Date": r[5],
                                # "Status": r[6]
                            }
                            for r in latest_results
                        ]
                    )
                else:
                    flash(
                        "No new profiles were found. Either matching public results "
                        "were limited or the profiles already exist in your sheet.",
                        "warning"
                    )

            except Exception as e:
                flash(f"Error: {str(e)}", "danger")

    rows = []

    try:
        if SPREADSHEET_ID and os.path.exists(GOOGLE_CREDS_FILE):
            rows = get_sheet().get_all_records()[-30:]
    except Exception:
        pass

    return render_template("index.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
