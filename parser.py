import os
import re
from datetime import datetime
from database import insert_log

LOG_DIR = "logs"

def parse_line(line):
    """
    Expected format:
    2024-01-15 08:23:11 | LOGIN_FAILED | user=john | ip=192.168.1.10 | severity=WARNING
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 2:
        return None

    try:
        timestamp = parts[0]
        event = parts[1] if len(parts) > 1 else "UNKNOWN"
        user = ""
        ip = ""
        severity = "INFO"

        for part in parts[2:]:
            if part.startswith("user="):
                user = part.split("=", 1)[1]
            elif part.startswith("ip="):
                ip = part.split("=", 1)[1]
            elif part.startswith("severity="):
                severity = part.split("=", 1)[1]

        return {
            "timestamp": timestamp,
            "event": event,
            "user": user,
            "ip": ip,
            "severity": severity
        }
    except Exception:
        return None

def load_logs_from_file(filepath):
    loaded = 0
    try:
        with open(filepath, "r") as f:
            for line in f:
                entry = parse_line(line)
                if entry:
                    insert_log(
                        entry["timestamp"],
                        entry["event"],
                        entry["user"],
                        entry["ip"],
                        entry["severity"]
                    )
                    loaded += 1
    except FileNotFoundError:
        pass
    return loaded

def load_all_logs():
    total = 0
    for filename in ["sample_logs.txt", "login_logs.txt", "network_logs.txt"]:
        filepath = os.path.join(LOG_DIR, filename)
        total += load_logs_from_file(filepath)
    return total