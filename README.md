# 🛡️ SOCVision — Security Operations Center Dashboard

A full-stack cybersecurity monitoring dashboard built with Python, Flask, SQLite, and Chart.js.  
SOCVision simulates a real SOC environment where security analysts can monitor logs, detect threats, manage alerts, visualize trends, and generate reports — all from a single dark-themed, authenticated web interface.

---

## ✨ Features

- 🔐 **Authentication** — Login-protected dashboard with hashed password storage (no plaintext credentials), session-based access control, and automatic session invalidation on server restart
- 🗂️ **Log Management** — Ingests and parses every `.txt`/`.log` file dropped into the `logs/` folder into a structured SQLite database, without duplicating data on repeated loads
- 🔍 **Threat Detection Engine** — Rule-based detector that automatically identifies brute force attacks, shared-source logins, excessive requests, unusual login times, and possible account compromise
- 🚨 **Alert Management** — Full alert lifecycle with severity levels (LOW / MEDIUM / HIGH / CRITICAL), sorted worst-first, with open/close workflow, search, and filtering
- 📋 **Log Viewer** — Paginated log table with search and severity filtering across all collected events
- 📊 **Analytics Dashboard** — 4 live Chart.js visualizations: failed login trends, alert severity distribution, top suspicious IPs, and event type breakdown
- 📄 **Report Generation** — Daily, Weekly, and Monthly security summaries with CSV and TXT export
- 🎛️ **Operational UI** — Confirmation modal with live feedback when loading logs, empty-state guidance for first-time use, and a live Data Sources panel instead of placeholder integrations

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Auth | Flask sessions, Werkzeug password hashing (scrypt) |
| Frontend | HTML5, CSS3, JavaScript |
| Visualization | Chart.js |

---

## 📁 Project Structure

```text
socvision/
├── app.py            # Flask routes, auth, and application entry point
├── database.py       # SQLite setup, schema, and all query functions
├── parser.py         # Log file ingestion and parsing engine
├── detector.py       # Rule-based threat detection logic
├── analytics.py      # Data aggregation for chart API endpoints
├── reports.py        # Report generation and CSV/TXT export
├── logs/             # Log files (auth, login, network) — drop any .txt/.log file here
├── templates/        # HTML templates
├── static/           # CSS, JavaScript, Chart.js charts
└── exports/          # Generated report output directory
```

---

## 🔴 Threat Detection Rules

| Rule | Condition | Alert Severity |
|---|---|---|
| Possible Account Compromise | Successful login from an IP with 5+ prior failed attempts | 🔴 CRITICAL |
| Brute Force Attack | 5+ failed logins from same IP | 🟠 HIGH |
| Shared Source Activity | 3+ different users from same IP | 🟡 MEDIUM |
| Excessive Requests | 20+ requests from same IP | 🟡 MEDIUM |
| Unusual Login Time | Successful login between 00:00–04:00 | 🟢 LOW |

---

## ⚙️ Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/KrishnaaSonar/SOCVision.git
cd SOCVision
```

**2. Install dependencies**
```bash
pip install flask
```

**3. Run the application**
```bash
python app.py
```

**4. Open in browser and log in**
```bash
http://127.0.0.1:5000/
```

**5. Load log data**  
Click **⟳ Load Logs** in the sidebar and confirm in the dialog — this parses every log file in `logs/`, stores them in SQLite, and runs the threat detection engine. Re-running it is safe: existing logs and alerts are cleared first, so nothing duplicates.

**Adding your own logs:** drop any `.txt` or `.log` file into the `logs/` folder, following this line format, then click Load Logs:
```text
2026-09-24 10:15:00 | LOGIN_FAILED | user=priya.nair | ip=192.168.1.20 | severity=WARNING
```
`user=`, `ip=`, and `severity=` are optional; timestamp and event are required, in `YYYY-MM-DD HH:MM:SS` format.

---

## 🔐 Security Notes

- Passwords are hashed with Werkzeug's `scrypt`-based hashing — never stored or compared in plaintext
- All routes require login; unauthenticated requests redirect to `/login`
- The session signing key is regenerated randomly on every app restart, so logins don't persist across restarts

---

## 🗺️ Pages

| Route | Description |
|---|---|
| `/login` | Authentication page |
| `/` | Dashboard with security metrics overview and data source status |
| `/alerts` | Alert management with search, filter, and open/close actions |
| `/logs` | Full log viewer with pagination and severity filtering |
| `/analytics` | Chart.js visualizations of security trends |
| `/reports` | Report generation with CSV and TXT export |

---

## 🎯 Learning Objectives Demonstrated

- Flask web application development with session-based authentication
- Secure credential storage and password hashing
- SQLite database design, querying, and connection lifecycle management
- Rule-based threat detection in Python
- Security log analysis and parsing
- Chart.js data visualization
- Incident management workflow design
- UI/UX iteration based on real usability feedback

---

## 📜 License
This project is intended for educational and portfolio purposes.