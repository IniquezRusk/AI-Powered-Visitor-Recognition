import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

EVENTS_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "recognition_events.jsonl"
)

_lock = Lock()


def record_event(result: dict):
    """Save recognition metadata without storing the uploaded image."""

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "visitor_id": result.get("visitor_id"),
        "status": result.get("status"),
        "similarity": result.get("similarity"),
    }

    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with _lock:
        with EVENTS_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    return event


def get_events(limit: int = 50):
    """Return the most recent recognition events."""

    if not EVENTS_FILE.exists():
        return []

    with _lock:
        with EVENTS_FILE.open("r", encoding="utf-8") as f:
            events = [
                json.loads(line)
                for line in f
                if line.strip()
            ]

    return list(reversed(events[-limit:]))


def get_summary():
    """Calculate recognition statistics."""

    events = get_events(limit=100000)

    today = datetime.now(timezone.utc).date().isoformat()

    recognized = [
        event for event in events
        if event["status"] == "recognized"
    ]

    unique_visitors = {
        event["visitor_id"]
        for event in recognized
        if event["visitor_id"]
    }

    return {
        "total_events": len(events),
        "successful_recognitions": len(recognized),
        "unknown_attempts": sum(
            event["status"] == "unknown"
            for event in events
        ),
        "unique_visitors": len(unique_visitors),
        "events_today": sum(
            event["timestamp"].startswith(today)
            for event in events
        ),
    }