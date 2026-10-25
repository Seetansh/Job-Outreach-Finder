import os

from flask import Blueprint, flash, render_template, request

from app.config import GOOGLE_CREDS_FILE, SPREADSHEET_ID
from app.integrations.sheets_repository import get_sheet
from app.services.recruiter_search import find_and_save_recruiters


web = Blueprint("web", __name__)


@web.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        location = request.form.get("location", "").strip()

        if not company or not location:
            flash("Please enter both Company and Location.", "danger")
        else:
            try:
                latest_results = find_and_save_recruiters(company, location)

                if latest_results:
                    flash(
                        f"Success! Found and saved {len(latest_results)} new unique profiles.",
                        "success",
                    )
                    return render_template(
                        "index.html",
                        rows=[
                            {
                                "Company": row[0],
                                "Search Location": row[1],
                                "Recruiter Name": row[2],
                                "Designation": row[3],
                            }
                            for row in latest_results
                        ],
                    )

                flash(
                    "No new profiles were found. Either matching public results "
                    "were limited or the profiles already exist in your sheet.",
                    "warning",
                )
            except Exception as error:
                flash(f"Error: {error}", "danger")

    rows = []

    try:
        if SPREADSHEET_ID and os.path.exists(GOOGLE_CREDS_FILE):
            rows = get_sheet().get_all_records()[-30:]
    except Exception:
        pass

    return render_template("index.html", rows=rows)