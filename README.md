# 🛡️ SOCVision — Security Operations Center Dashboard

A full-stack cybersecurity monitoring dashboard built with Python, Flask, SQLite, and Chart.js.  
SOCVision simulates a real SOC environment where security analysts can monitor logs, detect threats, manage alerts, visualize trends, and generate reports — all from a single dark-themed web interface.

---

## ✨ Features

- 🗂️ **Log Management** — Ingests and parses authentication, login, and network log files into a structured SQLite database
- 🔍 **Threat Detection Engine** — Rule-based detector that automatically identifies brute force attacks, shared-source logins, excessive requests, and unusual login times
- 🚨 **Alert Management** — Full alert lifecycle with severity levels (LOW / MEDIUM / HIGH / CRITICAL), open/close workflow, search, and filtering
- 📋 **Log Viewer** — Paginated log table with search and severity filtering across all collected events
- 📊 **Analytics Dashboard** — 4 live Chart.js visualizations: failed login trends, alert severity distribution, top suspicious IPs, and event type breakdown
- 📄 **Report Generation** — Daily, Weekly, and Monthly security summaries with CSV and TXT export

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Visualization | Chart.js |

---

## 📁 Project Structure

```text
socvision/
├── app.py            # Flask routes and application entry point
├── database.py       # SQLite setup, schema, and all query functions
├── parser.py         # Log file ingestion and parsing engine
├── detector.py       # Rule-based threat detection logic
├── analytics.py      # Data aggregation for chart API endpoints
├── reports.py        # Report generation and CSV/TXT export
├── logs/             # Sample log files (auth, login, network)
├── templates/        # HTML templates
├── static/           # CSS, JavaScript, Chart.js charts
└── exports/          # Generated report output directory
```

---

## 🔴 Threat Detection Rules

| Rule | Condition | Alert Severity |
|---|---|---|
| Brute Force Attack | 5+ failed logins from same IP | 🔴 HIGH |
| Shared Source Activity | 3+ different users from same IP | 🟠 MEDIUM |
| Excessive Requests | 20+ requests from same IP | 🟠 MEDIUM |
| Unusual Login Time | Successful login between 00:00–04:00 | 🟡 LOW |

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

**4. Open in browser**
```bash
http://127.0.0.1:5000/
```

**5. Load sample data**  
Click **⟳ Load Logs** in the sidebar — this parses all log files, stores them in SQLite, and runs the threat detection engine automatically.

---

## 🗺️ Pages

| Route | Description |
|---|---|
| `/` | Dashboard with security metrics overview |
| `/alerts` | Alert management with search, filter, and open/close actions |
| `/logs` | Full log viewer with pagination and severity filtering |
| `/analytics` | Chart.js visualizations of security trends |
| `/reports` | Report generation with CSV and TXT export |

---

## 🔗 Future Integrations

SOCVision is designed to receive alerts from external security tools:

- 🌐 **NetScout** → Open port and network scan alerts
- 🎣 **PhishGuard** → Phishing detection alerts

Both would feed into SOCVision as the central monitoring dashboard.

---

## 🎯 Learning Objectives Demonstrated

- Flask web application development
- SQLite database design and querying
- Rule-based threat detection in Python
- Security log analysis and parsing
- Chart.js data visualization
- Incident management workflow design

---

## 📜 License
This project is intended for educational and portfolio purposes.
