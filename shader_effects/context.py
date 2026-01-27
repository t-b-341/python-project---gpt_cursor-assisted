"""
Typed context for shader execution.
"""
from __future__ import annotations

from typing import TypedDict


class ShaderContext(TypedDict, total=False):
    """Context passed to shader pipeline execution."""
    time: float
    delta_time: float
    health: float
    damage_wobble: float
    # Add any other shared context keys we already pass to shaders
