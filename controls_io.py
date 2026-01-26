"""Load/save control bindings to disk. Used by game.py to initialize and persist key bindings."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pygame

from constants import CONTROLS_PATH, DEFAULT_CONTROLS, MOUSE_BUTTON_RIGHT

# Resolve paths from project root so loading works regardless of cwd
_PROJECT_ROOT = Path(__file__).resolve().parent
_CONTROLS_PATH = _PROJECT_ROOT / CONTROLS_PATH
_LEGACY_CONTROLS = _PROJECT_ROOT / "controls.json"


def _key_name_to_code(name: str) -> int:
    name = (name or "").lower().strip()
    if name in ("right mouse", "right_mouse", "mouse right"):
        return MOUSE_BUTTON_RIGHT
    try:
        return pygame.key.key_code(name)
    except Exception:
        return pygame.K_UNKNOWN


def load_controls() -> dict[str, int]:
    data = {}
    path = _CONTROLS_PATH if _CONTROLS_PATH.exists() else (_LEGACY_CONTROLS if _LEGACY_CONTROLS.exists() else None)
    if path is not None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
        except Exception:
            data = {}

    merged = {**DEFAULT_CONTROLS, **{k: v for k, v in data.items() if isinstance(v, str)}}
    return {action: _key_name_to_code(key_name) for action, key_name in merged.items()}


def save_controls(controls: dict[str, int]) -> None:
    # Persist as human-readable key names so players can edit the file too
    out: dict[str, str] = {}
    for action, key_code in controls.items():
        if key_code == MOUSE_BUTTON_RIGHT:
            out[action] = "right mouse"
        else:
            try:
                out[action] = pygame.key.name(key_code)
            except Exception:
                out[action] = "unknown"
    _CONTROLS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_CONTROLS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
