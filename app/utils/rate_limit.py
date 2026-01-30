import time
from fastapi import HTTPException

# user_id -> [timestamps]
_REQUEST_LOG = {}

RATE_LIMIT = 30      # requests
WINDOW_SECONDS = 60  # per minute


def check_rate_limit(user_id: int):
    now = time.time()
    window_start = now - WINDOW_SECONDS

    timestamps = _REQUEST_LOG.get(user_id, [])
    timestamps = [t for t in timestamps if t > window_start]

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please slow down.",
        )

    timestamps.append(now)
    _REQUEST_LOG[user_id] = timestamps
