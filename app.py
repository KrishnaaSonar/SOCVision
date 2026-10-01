from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session
from functools import wraps
from database import init_db, get_all_logs, get_all_alerts, get_dashboard_metrics, update_alert_status, get_logs_count, get_alerts_count, clear_data
from parser import load_all_logs
from detector import run_detection
from analytics import get_failed_logins_over_time, get_alert_severity_distribution, get_top_suspicious_ips, get_event_type_distribution
from reports import get_report_data, export_csv, export_txt
from werkzeug.security import check_password_hash
from datetime import datetime
from parser import load_all_logs, LOG_DIR
import secrets
import os

app = Flask(__name__)

last_load = {"time": None}
app.secret_key = secrets.token_hex(32)
ADMIN_USERNAME = os.environ.get("SOC_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.environ.get(
    "SOC_PASSWORD_HASH",
    "scrypt:32768:8:1$zLpnx3L9hjvjoe3o$acf88c93beb81b44d52de74e4eeff426bc2b1562f97b7f44a2687cb934d21a8a18a797a20ae736514dc079d684f461b9027f76c8921789fc30f74bff57bd197f"
)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, request.form.get("password", "")):
            session["logged_in"] = True
            session["username"] = ADMIN_USERNAME
            return redirect(request.args.get("next") or url_for("dashboard"))
        error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/")
@login_required
def dashboard():
    metrics = get_dashboard_metrics()
    try:
        log_files = [f for f in os.listdir(LOG_DIR) if f.lower().endswith((".txt", ".log"))]
    except FileNotFoundError:
        log_files = []
    return render_template("dashboard.html", metrics=metrics, log_files=log_files, last_loaded=last_load["time"])

@app.route("/logs")
@login_required
def logs():
    search = request.args.get("search", "")
    severity = request.args.get("severity", "")
    page = int(request.args.get("page", 1))
    per_page = 50
    offset = (page - 1) * per_page

    total = get_logs_count(search=search or None, severity=severity or None)
    log_list = get_all_logs(search=search or None, severity=severity or None, limit=per_page, offset=offset)
    total_pages = (total + per_page - 1) // per_page

    return render_template("logs.html",
        logs=log_list,
        search=search,
        severity=severity,
        page=page,
        total_pages=total_pages,
        total=total
    )

@app.route("/alerts")
@login_required
def alerts():
    search = request.args.get("search", "")
    severity = request.args.get("severity", "")
    status = request.args.get("status", "")
    page = int(request.args.get("page", 1))
    per_page = 50
    offset = (page - 1) * per_page

    total = get_alerts_count(search=search or None, severity=severity or None, status=status or None)
    alert_list = get_all_alerts(search=search or None, severity=severity or None, status=status or None, limit=per_page, offset=offset)
    total_pages = (total + per_page - 1) // per_page

    return render_template("alerts.html",
        alerts=alert_list,
        search=search,
        severity=severity,
        status=status,
        page=page,
        total_pages=total_pages,
        total=total
    )

@app.route("/alerts/update/<int:alert_id>", methods=["POST"])
@login_required
def update_alert(alert_id):
    new_status = request.form.get("status", "Closed")
    update_alert_status(alert_id, new_status)
    return redirect(url_for("alerts"))

@app.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html")

@app.route("/api/analytics/failed_logins")
@login_required
def api_failed_logins():
    return jsonify(get_failed_logins_over_time())

@app.route("/api/analytics/severity_distribution")
@login_required
def api_severity_distribution():
    return jsonify(get_alert_severity_distribution())

@app.route("/api/analytics/top_ips")
@login_required
def api_top_ips():
    return jsonify(get_top_suspicious_ips())

@app.route("/api/analytics/event_types")
@login_required
def api_event_types():
    return jsonify(get_event_type_distribution())

@app.route("/reports")
@login_required
def reports():
    period = request.args.get("period", "daily")
    data = get_report_data(period)
    return render_template("reports.html", report=data)

@app.route("/reports/export/csv")
@login_required
def export_report_csv():
    period = request.args.get("period", "daily")
    filepath = export_csv(period)
    return send_file(filepath, as_attachment=True)

@app.route("/reports/export/txt")
@login_required
def export_report_txt():
    period = request.args.get("period", "daily")
    filepath = export_txt(period)
    return send_file(filepath, as_attachment=True)

@app.route("/admin/load-logs")
@login_required
def admin_load_logs():
    clear_data()
    count = load_all_logs()
    alerts_count = run_detection()
    last_load["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"logs_loaded": count, "alerts_generated": alerts_count, "status": "success"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)