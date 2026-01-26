"""
Lightweight performance instrumentation for DEBUG/DEV mode.
Frame time (and optional per-system timings) stored in-memory for real-time
debug display or offline inspection. Off by default; set GAME_DEBUG_PERF=1 to enable.
Overhead is minimal when disabled (single env check per frame).
"""
from __future__ import annotations

import os
from collections import deque

_DEBUG_PERF = os.environ.get("GAME_DEBUG_PERF", "0").strip() == "1"
_frame_times: deque[float] = deque(maxlen=300)  # ~5 s at 60 fps


def is_enabled() -> bool:
    """True if GAME_DEBUG_PERF=1."""
    return _DEBUG_PERF


def record_frame(dt: float) -> None:
    """Record this frame's wall-clock dt (seconds). No-op when GAME_DEBUG_PERF is not set."""
    if _DEBUG_PERF:
        _frame_times.append(dt)


def get_last_frame_times() -> list[float]:
    """Return the last N frame times (seconds). Empty when perf logging disabled."""
    return list(_frame_times)


def clear() -> None:
    """Clear stored frame times."""
    _frame_times.clear()
