import csv
import os
from datetime import datetime, timedelta
from database import get_connection

EXPORT_DIR = "exports"

def ensure_export_dir():
    os.makedirs(EXPORT_DIR, exist_ok=True)

def get_report_data(period="daily"):
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now()
    if period == "daily":
        since = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        label = "Daily"
    elif period == "weekly":
        since = (now - timedelta(weeks=1)).strftime("%Y-%m-%d %H:%M:%S")
        label = "Weekly"
    else:
        since = (now - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        label = "Monthly"

    cursor.execute("SELECT COUNT(*) FROM logs WHERE timestamp >= ?", (since,))
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE timestamp >= ?", (since,))
    total_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'CRITICAL' AND timestamp >= ?", (since,))
    critical_alerts = cursor.fetchone()[0]

    cursor.execute(
        "SELECT ip, COUNT(*) as c FROM alerts WHERE timestamp >= ? AND ip != '' GROUP BY ip ORDER BY c DESC LIMIT 5",
        (since,)
    )
    top_ips = cursor.fetchall()

    cursor.execute(
        "SELECT alert_type, COUNT(*) as c FROM alerts WHERE timestamp >= ? GROUP BY alert_type ORDER BY c DESC",
        (since,)
    )
    threat_summary = cursor.fetchall()

    conn.close()

    return {
        "label": label,
        "period": period,
        "since": since,
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "total_events": total_events,
        "total_alerts": total_alerts,
        "critical_alerts": critical_alerts,
        "top_ips": [dict(r) for r in top_ips],
        "threat_summary": [dict(r) for r in threat_summary]
    }

def export_csv(period="daily"):
    ensure_export_dir()
    data = get_report_data(period)
    filename = f"{EXPORT_DIR}/report_{period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["SOCVision Security Report"])
        writer.writerow([f"Period: {data['label']}"])
        writer.writerow([f"Generated: {data['generated_at']}"])
        writer.writerow([])
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Total Events", data["total_events"]])
        writer.writerow(["Total Alerts", data["total_alerts"]])
        writer.writerow(["Critical Alerts", data["critical_alerts"]])
        writer.writerow([])
        writer.writerow(["Top Suspicious IPs"])
        writer.writerow(["IP", "Alert Count"])
        for ip in data["top_ips"]:
            writer.writerow([ip["ip"], ip["c"]])
        writer.writerow([])
        writer.writerow(["Threat Summary"])
        writer.writerow(["Threat Type", "Count"])
        for t in data["threat_summary"]:
            writer.writerow([t["alert_type"], t["c"]])

    return filename

def export_txt(period="daily"):
    ensure_export_dir()
    data = get_report_data(period)
    filename = f"{EXPORT_DIR}/report_{period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    lines = [
        "=" * 60,
        f"  SOCVision Security Report — {data['label']}",
        "=" * 60,
        f"  Generated At : {data['generated_at']}",
        f"  Period Since : {data['since']}",
        "-" * 60,
        f"  Total Events    : {data['total_events']}",
        f"  Total Alerts    : {data['total_alerts']}",
        f"  Critical Alerts : {data['critical_alerts']}",
        "-" * 60,
        "  Top Suspicious IPs:",
    ]
    for ip in data["top_ips"]:
        lines.append(f"    {ip['ip']:20s}  {ip['c']} alerts")
    lines.append("-" * 60)
    lines.append("  Threat Summary:")
    for t in data["threat_summary"]:
        lines.append(f"    {t['alert_type']:30s}  {t['c']} occurrences")
    lines.append("=" * 60)

    with open(filename, "w") as f:
        f.write("\n".join(lines))

    return filename