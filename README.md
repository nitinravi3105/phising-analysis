<<<<<<< HEAD
# Group 18 — PhishGuard Evidence Lab

**CSDF:** Phishing Message Analysis and Digital Evidence Reporting System  
**STQA Manual:** Manual Testing of a Phishing Message Analysis Web Application  
**STQA Automation:** Automated Testing Using Selenium WebDriver and Pytest

## Features
- Rule-based analysis of a pasted SMS, email, message, or URL.
- Risk score from 0 to 100 and Low / Medium / High classification.
- Explanations for configured warning indicators.
- SQLite evidence records with UTC timestamp and SHA-256 content hash.
- Evidence history and downloadable PDF reports.
- Manual test scenarios, test cases, defect template, unit tests, and Selenium tests.

## Requirements
- Python 3.10 or newer
- Google Chrome for Selenium automation
- Internet connection during initial setup if installing packages and loading Bootstrap CDN

## Setup (Windows PowerShell)
1. Extract the ZIP and open the project folder in VS Code.
2. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.
3. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Start the web app:
   ```powershell
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in Chrome.

The SQLite database is created automatically at `database/phishing.db`.

## Setup (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

## Demo messages
Use synthetic examples only:
- Low-risk example: `The team meeting is at 3 PM tomorrow.`
- Higher-risk example: `URGENT: verify your password immediately at https://bit.ly/demo`
- Payment/reward example: `You won a prize. Claim reward now by visiting https://example.invalid`

Do not click suspicious links. The analyzer does not visit or fetch submitted URLs.

## Run tests
Keep the Flask app running in one terminal. In another terminal, with the same virtual environment active:

Unit tests:
```bash
python -m pytest tests -v
```

Selenium tests (requires Chrome and a compatible Selenium Manager/ChromeDriver setup):
```bash
python -m pytest automation -v --html=reports/automation-report.html --self-contained-html
```

If the browser is not found, update Chrome and Selenium, ensure Chrome can start, then rerun. Selenium 4 uses Selenium Manager to help obtain a compatible driver.

## Project structure
- `app.py`: Flask routes and request validation.
- `analyzer.py`: transparent rule-based indicators and scoring.
- `database.py`: SQLite evidence storage.
- `evidence_report.py`: PDF evidence report generator.
- `templates/`, `static/`: web interface.
- `tests/`: unit tests for analysis logic.
- `automation/`: Selenium + Pytest browser tests.
- `manual_testing/`: CSV templates that open in Excel or Google Sheets.

## Risk scoring used in this prototype
- Urgency / pressure terms: +20
- Credential or sensitive-data terms: +25
- Payment / prize / reward terms: +15
- Shortened URL: +20
- IP-address URL: +20
- `@` symbol in a URL: +15
- selected internationalized-domain prefix: +15
- Final score is capped at 100. High >= 50, Medium >= 25, otherwise Low.

This scoring is a teaching heuristic, not a validated security model. Results are not proof that a message is malicious or safe.

## Digital evidence notes
The app stores the exact submitted text, UTC timestamp, findings, and SHA-256 hash. The hash can help detect whether the stored text later changes, but it does not authenticate the sender or establish a full forensic chain of custody. For real investigations, preserve original files, headers, source metadata, acquisition details, access logs, and documented custody procedures.

## Security and privacy notes
- Use only test data or content you are authorized to analyze.
- Never submit passwords, OTPs, private data, or confidential evidence to a public deployment.
- This is a local educational prototype. It has no user authentication, role-based access, encryption-at-rest, or production hardening.
- Before deployment, disable Flask debug mode, use a strong secret key, add authentication and CSRF protection, set secure deployment configuration, and review privacy requirements.
- Submitted URLs are parsed as text only; the app does not browse to them or query external threat-intelligence services.

## Suggested viva topics
1. What is phishing?
2. What are indicators of compromise and social engineering?
3. What is a SHA-256 hash, and what does it not prove?
4. Why is SQLite suitable for a mini project?
5. What are positive and negative test cases?
6. What is the difference between a test scenario and a test case?
7. What are Selenium WebDriver and Pytest?
8. Why use explicit waits?
9. What is regression testing?
10. What are the limitations of rule-based classification?
=======
# phising-analysis
>>>>>>> 3e9bbe19ad6c1ce3c103df64b1a4b327090e33d8
