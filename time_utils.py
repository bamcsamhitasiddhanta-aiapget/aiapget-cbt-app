from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def current_time():
    return datetime.now(IST)


def current_time_iso():
    return current_time().isoformat()


def format_timestamp(iso_timestamp):
    if not iso_timestamp:
        return "N/A"

    dt = datetime.fromisoformat(iso_timestamp)
    return dt.strftime("%d %b %Y, %I:%M %p IST")
