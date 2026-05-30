import sqlite3
from datetime import datetime

DB_PATH = "socvision.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event TEXT NOT NULL,
            user TEXT,
            ip TEXT,
            severity TEXT DEFAULT 'INFO'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            severity TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            message TEXT NOT NULL,
            ip TEXT,
            status TEXT DEFAULT 'Open'
        )
    ''')

    conn.commit()
    conn.close()

def insert_log(timestamp, event, user, ip, severity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (timestamp, event, user, ip, severity) VALUES (?, ?, ?, ?, ?)",
        (timestamp, event, user, ip, severity)
    )
    conn.commit()
    conn.close()

def insert_alert(timestamp, severity, alert_type, message, ip, status="Open"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO alerts (timestamp, severity, alert_type, message, ip, status) VALUES (?, ?, ?, ?, ?, ?)",
        (timestamp, severity, alert_type, message, ip, status)
    )
    conn.commit()
    conn.close()

def get_all_logs(search=None, severity=None, limit=100, offset=0):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM logs WHERE 1=1"
    params = []
    if search:
        query += " AND (user LIKE ? OR ip LIKE ? OR event LIKE ?)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if severity:
        query += " AND severity = ?"
        params.append(severity)
    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params += [limit, offset]
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_alerts(search=None, severity=None, status=None, limit=100, offset=0):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM alerts WHERE 1=1"
    params = []
    if search:
        query += " AND (ip LIKE ? OR alert_type LIKE ? OR message LIKE ?)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if severity:
        query += " AND severity = ?"
        params.append(severity)
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params += [limit, offset]
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_dashboard_metrics():
    conn = get_connection()
    cursor = conn.cursor()
    metrics = {}

    cursor.execute("SELECT COUNT(*) FROM logs")
    metrics['total_logs'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts")
    metrics['total_alerts'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'CRITICAL'")
    metrics['critical_alerts'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'HIGH'")
    metrics['high_alerts'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT ip) FROM logs WHERE ip IS NOT NULL AND ip != ''")
    metrics['unique_ips'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT user) FROM logs WHERE user IS NOT NULL AND user != ''")
    metrics['users_monitored'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Open'")
    metrics['open_alerts'] = cursor.fetchone()[0]

    conn.close()
    return metrics

def update_alert_status(alert_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE alerts SET status = ? WHERE id = ?", (status, alert_id))
    conn.commit()
    conn.close()

def get_logs_count(search=None, severity=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM logs WHERE 1=1"
    params = []
    if search:
        query += " AND (user LIKE ? OR ip LIKE ? OR event LIKE ?)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if severity:
        query += " AND severity = ?"
        params.append(severity)
    cursor.execute(query, params)
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_alerts_count(search=None, severity=None, status=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM alerts WHERE 1=1"
    params = []
    if search:
        query += " AND (ip LIKE ? OR alert_type LIKE ? OR message LIKE ?)"
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]
    if severity:
        query += " AND severity = ?"
        params.append(severity)
    if status:
        query += " AND status = ?"
        params.append(status)
    cursor.execute(query, params)
    count = cursor.fetchone()[0]
    conn.close()
    return count