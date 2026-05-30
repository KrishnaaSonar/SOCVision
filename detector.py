from collections import defaultdict
from datetime import datetime
from database import get_connection, insert_alert

def run_detection():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp ASC")
    logs = cursor.fetchall()
    conn.close()

    alerts_generated = 0
    ip_failed = defaultdict(int)
    ip_users = defaultdict(set)
    ip_requests = defaultdict(int)

    for log in logs:
        event = log["event"]
        ip = log["ip"] or ""
        user = log["user"] or ""
        timestamp = log["timestamp"]

        # Rule 1: Brute Force Detection
        if event == "LOGIN_FAILED" and ip:
            ip_failed[ip] += 1
            if ip_failed[ip] == 5:
                insert_alert(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "HIGH",
                    "Brute Force Attack",
                    f"5+ failed login attempts detected from IP {ip}",
                    ip
                )
                alerts_generated += 1

        # Rule 2: Suspicious Login - Multiple users same IP
        if event in ("LOGIN_SUCCESS", "LOGIN_FAILED") and ip and user:
            ip_users[ip].add(user)
            if len(ip_users[ip]) == 3:
                insert_alert(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "MEDIUM",
                    "Shared Source Activity",
                    f"Multiple users ({len(ip_users[ip])}) detected from same IP {ip}",
                    ip
                )
                alerts_generated += 1

        # Rule 3: Excessive Requests
        if ip:
            ip_requests[ip] += 1
            if ip_requests[ip] == 20:
                insert_alert(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "MEDIUM",
                    "Excessive Activity",
                    f"More than 20 requests detected from IP {ip}",
                    ip
                )
                alerts_generated += 1

        # Rule 4: Unusual Login Time (00:00 - 04:00)
        if event == "LOGIN_SUCCESS":
            try:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                if 0 <= dt.hour < 4:
                    insert_alert(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "LOW",
                        "Unusual Login Time",
                        f"Login by '{user}' at unusual hour ({dt.strftime('%H:%M')}) from IP {ip}",
                        ip
                    )
                    alerts_generated += 1
            except Exception:
                pass

    return alerts_generated