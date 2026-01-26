"""Application-level context: display, timing, fonts, telemetry, and global config flags.

Holds resources and mode flags that are shared for the lifetime of the window.
Does NOT hold dynamic game state (entities, score, wave, etc.); that lives in GameState.
"""
from dataclasses import dataclass, field
from typing import Any, Optional

import pygame


@dataclass
class AppContext:
    """Application-level resources and configuration.

    Created after Pygame init and passed into the main loop and screen/context
    consumers. Contains only true app-level resources and mode flags, not
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

    # Telemetry (optional; None or no-op when disabled)
    telemetry_client: Optional[Any] = None  # Telemetry | NoOpTelemetry
    telemetry_enabled: bool = False

    # Run timestamp for telemetry (ISO string when a run starts)
    run_started_at: Optional[str] = None

    # Key bindings (loaded once per run from controls file)
    controls: dict[str, int] = field(default_factory=dict)

    # Menu/session configuration (chosen before or during run, apply app-wide)
    difficulty: str = "NORMAL"
    aiming_mode: str = "MOUSE"
    profile_enabled: bool = False  # use_character_profile
    player_class: str = "BALANCED"  # PLAYER_CLASS_BALANCED etc.

    # Testing / dev mode flags
    testing_mode: bool = False
    invulnerability_mode: bool = False

    # UI visibility and options (application-wide display preferences)
    ui_show_metrics: bool = True
    ui_show_hud: bool = True
    ui_show_health_bars: bool = True
    ui_show_player_health_bar: bool = True
