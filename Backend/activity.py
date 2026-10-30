import json
from datatime import datatime, timezone
from pathlib import Path
from threading import Lock

EVENTS_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "recognition_events.json1"
)

_lock = Lock()


def record_event(result: dict):
    """Save recognition metadata without storing the uploaded image."""

    event = {
        "timestamp"L datatime.now(timezone.utc).isoformat(),
        "visitor_id": result.get("visitor_id"),
        "status": result.get("status"),
        "similarity": result.get("similarity"),
    }

    