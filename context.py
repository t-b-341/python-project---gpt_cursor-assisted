"""Application-level context: display, timing, fonts, telemetry, and config.

Holds resources and config that are shared for the lifetime of the window.
Does NOT hold dynamic game state (entities, score, wave, etc.); that lives in GameState.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import pygame

from config.game_config import GameConfig


@dataclass
class AppContext:
    """Application-level resources and configuration.

    Created after Pygame init and passed into the main loop and screen/context
    consumers. Contains only true app-level resources and config, not
    per-run game state.
    """
    # Display and timing (from pygame)
    screen: pygame.Surface
    clock: pygame.time.Clock
    font: pygame.font.Font
    big_font: pygame.font.Font
    small_font: pygame.font.Font

    # Dimensions (from display mode; used by layout and helpers)
    width: int
    height: int

    # Telemetry (optional; None or no-op when disabled). Enable/disable is in config.
    telemetry_client: Optional[Any] = None  # Telemetry | NoOpTelemetry
    last_telemetry_sample_t: float = -1.0  # per-frame sampling clock; updated by telemetry_system

    # Run timestamp for telemetry (ISO string when a run starts)
    run_started_at: Optional[str] = None

    # Key bindings (loaded once per run from controls file)
    controls: dict[str, int] = field(default_factory=dict)

    # Centralized game options (difficulty, player class, aim mode, toggles).
    # Graphics/performance: config.graphics_preset, config.use_gpu_physics, config.use_gpu_shaders, config.internal_resolution_scale.
    config: GameConfig = field(default_factory=GameConfig)

    # Physics backend: True if C-accelerated game_physics is in use, False if Python fallback
    using_c_physics: bool = False

    # Event bus for decoupling systems (optional; None or no-op when not set)
    event_bus: Optional[Any] = None
