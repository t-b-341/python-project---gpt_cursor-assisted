"""Load/save control bindings to disk. Used by game.py to initialize and persist key bindings."""
import json
import os

import pygame

from constants import CONTROLS_PATH, DEFAULT_CONTROLS, MOUSE_BUTTON_RIGHT


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
    if os.path.exists(CONTROLS_PATH):
        try:
            with open(CONTROLS_PATH, "r", encoding="utf-8") as f:
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
    with open(CONTROLS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
