# Job Outreach Finder

A Flask web application that searches for publicly indexed recruiter profiles by company and location, then saves new results to a Google Sheet.

Names and designations are inferred from public search-result metadata. Results may be incomplete, outdated, or inaccurate and should be independently verified.

## Features

- Search by company and location.
- Search recruiter-related roles using the DDGS library.
- Collect up to 30 unique LinkedIn profile URLs per search.
- Skip profile URLs that are already in the Google Sheet.
- Save new results to a configured Google Sheets worksheet.
- Display recent results in the web interface.

## Requirements

- Python
- A Google Cloud service account with access to the target Google Sheet
- A Google Sheet for storing results

## Setup

### 1. Get the project

Clone the repository or download the source code, then open a terminal in the project directory.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS or Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Google Sheets access

1. Create or select a Google Cloud project.
2. Enable the Google Sheets API and Google Drive API for that project.
3. Create a service account and download its JSON key file.
4. Save the key in the project directory as `service_account.json`, or choose another path and set `GOOGLE_CREDS_FILE` accordingly.
5. Share the target spreadsheet with the service account's email address and grant it editing access.
6. Copy the spreadsheet ID from its URL. It is the value between `/d/` and `/edit`.

**Never commit your service-account key to GitHub.** The project's `.gitignore` is intended to exclude it.

### 5. Configure environment variables

Copy `.env.example` to `.env`.

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

**macOS or Linux**

```bash
cp .env.example .env
```

Edit `.env` with your local settings:

```env
SECRET_KEY=replace-this-with-a-long-random-secret
SPREADSHEET_ID=your_google_spreadsheet_id
SHEET_NAME=Recruiters
GOOGLE_CREDS_FILE=service_account.json
```

Keep `.env` private. Use placeholder values in `.env.example`; do not put real secrets or credentials there.

## Run locally

From the project directory, with your virtual environment activated:

```bash
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

`run.py` uses Flask's development server. It is suitable for local development, not public production deployment. Use a production WSGI server and disable debug mode when deploying.

## Google Sheet columns

The application creates the configured worksheet if it does not exist and adds a header row if the worksheet is empty. Saved results use these columns:

- Company
- Search Location
- Recruiter Name
- Designation
- LinkedIn Profile URL
- Search Date
- Status
- Source Snippet

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── domain/
│   │   └── recruiter.py
│   ├── integrations/
│   │   ├── search_provider.py
│   │   └── sheets_repository.py
│   ├── routes/
    │   ├── __init__.py
│   │   └── web.py
│   ├── services/
│   │   └── recruiter_search.py
│   ├── templates/
│   │    └── index.html
    ├── static/
│   │   └── css/
│           └── style.css
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt
└── run.py
```

## Privacy and responsible use

This tool helps identify publicly indexed professional profiles. Search metadata can be inaccurate or outdated. Verify information independently, use it responsibly, and follow applicable privacy laws and the terms of the websites and search providers you use.

## Troubleshooting

- **Google authentication errors:** Check that the service-account JSON path is correct and that the Google Sheets and Google Drive APIs are enabled.
- **Permission errors:** Share the spreadsheet with the service account's email address and grant it editing access.
- **No results:** Search providers may return limited results, or there may be no matching public results for the selected company and location.
- **Outdated or inaccurate results:** Search-result metadata is provided by external search providers and may not reflect current profile information.
