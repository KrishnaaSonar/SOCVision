from database import get_connection
from collections import defaultdict

def get_failed_logins_over_time():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp FROM logs WHERE event = 'LOGIN_FAILED' ORDER BY timestamp ASC"
    )
    rows = cursor.fetchall()
    conn.close()

    daily = defaultdict(int)
    for row in rows:
        try:
            date = row["timestamp"][:10]
            daily[date] += 1
        except Exception:
            pass

    sorted_dates = sorted(daily.keys())
    return {
        "labels": sorted_dates,
        "data": [daily[d] for d in sorted_dates]
    }

def get_alert_severity_distribution():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT severity, COUNT(*) as count FROM alerts GROUP BY severity"
    )
    rows = cursor.fetchall()
    conn.close()

    result = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for row in rows:
        if row["severity"] in result:
            result[row["severity"]] = row["count"]
    return result

def get_top_suspicious_ips(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ip, COUNT(*) as count FROM alerts WHERE ip IS NOT NULL AND ip != '' GROUP BY ip ORDER BY count DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return {"labels": [r["ip"] for r in rows], "data": [r["count"] for r in rows]}

def get_event_type_distribution():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT event, COUNT(*) as count FROM logs GROUP BY event ORDER BY count DESC LIMIT 8"
    )
    rows = cursor.fetchall()
    conn.close()
    return {"labels": [r["event"] for r in rows], "data": [r["count"] for r in rows]}