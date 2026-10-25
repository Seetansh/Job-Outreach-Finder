# Job Outreach Finder - Free DuckDuckGo Version

## What it does
Input:
- Company
- Location

Then click one button.

The app automatically:
1. Searches multiple recruiter-related queries using DDGS / DuckDuckGo.
2. Finds public LinkedIn profile URLs.
3. Collects up to 30 unique profiles.
4. Extracts best-effort name and designation from public search metadata.
5. Removes duplicates using LinkedIn URLs.
6. Saves new results directly into Google Sheets.

## No paid search API required
This version does NOT need Serper or any API key.

## Setup
Keep these files in your project:
- app.py
- requirements.txt
- .env
- service_account.json
- templates/index.html

Your .env should contain:

SPREADSHEET_ID=your_google_sheet_id
SHEET_NAME=Recruiters
GOOGLE_CREDS_FILE=service_account.json
SECRET_KEY=anything_random

## Install
Activate your virtual environment, then:

python -m pip install -r requirements.txt

## Run

python app.py

Open:

http://127.0.0.1:5000

## Note
The DDGS package is a free search library. Search engines may sometimes rate-limit or return fewer than 30 public LinkedIn results for a particular company/location.
