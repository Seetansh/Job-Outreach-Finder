# deliver sheet - google sheet helper
import gspread
from google.oauth2.service_account import Credentials

from app.config import GOOGLE_CREDS_FILE, SHEET_NAME, SPREADSHEET_ID


HEADERS = [
    "Company",
    "Search Location",
    "Recruiter Name",
    "Designation",
    "LinkedIn Profile URL",
    "Search Date",
    "Status",
    "Source Snippet",
]


def get_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDS_FILE,
        scopes=scopes,
    )

    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    try:
        sheet = spreadsheet.worksheet(SHEET_NAME)
    except gspread.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(
            title=SHEET_NAME,
            rows=2000,
            cols=len(HEADERS),
        )

    if not sheet.row_values(1):
        sheet.append_row(HEADERS)

    return sheet