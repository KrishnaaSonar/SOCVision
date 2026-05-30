from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from database import init_db, get_all_logs, get_all_alerts, get_dashboard_metrics, update_alert_status, get_logs_count, get_alerts_count
from parser import load_all_logs
from detector import run_detection
from analytics import get_failed_logins_over_time, get_alert_severity_distribution, get_top_suspicious_ips, get_event_type_distribution
from reports import get_report_data, export_csv, export_txt
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    metrics = get_dashboard_metrics()
    return render_template("dashboard.html", metrics=metrics)

@app.route("/logs")
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
def update_alert(alert_id):
    new_status = request.form.get("status", "Closed")
    update_alert_status(alert_id, new_status)
    return redirect(url_for("alerts"))

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/api/analytics/failed_logins")
def api_failed_logins():
    return jsonify(get_failed_logins_over_time())

@app.route("/api/analytics/severity_distribution")
def api_severity_distribution():
    return jsonify(get_alert_severity_distribution())

@app.route("/api/analytics/top_ips")
def api_top_ips():
    return jsonify(get_top_suspicious_ips())

@app.route("/api/analytics/event_types")
def api_event_types():
    return jsonify(get_event_type_distribution())

@app.route("/reports")
def reports():
    period = request.args.get("period", "daily")
    data = get_report_data(period)
    return render_template("reports.html", report=data)

@app.route("/reports/export/csv")
def export_report_csv():
    period = request.args.get("period", "daily")
    filepath = export_csv(period)
    return send_file(filepath, as_attachment=True)

@app.route("/reports/export/txt")
def export_report_txt():
    period = request.args.get("period", "daily")
    filepath = export_txt(period)
    return send_file(filepath, as_attachment=True)

@app.route("/admin/load-logs")
def admin_load_logs():
    count = load_all_logs()
    alerts_count = run_detection()
    return jsonify({"logs_loaded": count, "alerts_generated": alerts_count, "status": "success"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)