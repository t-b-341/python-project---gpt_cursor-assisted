"""
Post-processing effect classes and central registry.

Each effect implements apply(surface, dt, context) and can be looked up by key
from EFFECT_REGISTRY. All effects are CPU-based 2D post-process (pygame surfaces).

Re-exports from base, color_effects, and distort_effects so existing imports
continue to work, e.g.:
  from shader_effects import get_menu_shader_stack, get_pause_shader_stack, get_gameplay_shader_stack
  import shader_effects as se  # se.SHADER_PROFILES, se.EFFECT_REGISTRY, se.get_*_shader_stack
"""
from __future__ import annotations

from .base import (
    PostProcessEffect,
    EffectDef,
    SHADER_PROFILES,
    get_effect_registry,
    get_gameplay_shader_stack,
    get_menu_shader_stack,
    get_pause_shader_stack,
)
from . import color_effects
from . import distort_effects

# Backward compatibility: EFFECT_REGISTRY as module-level dict (built via get_effect_registry).
EFFECT_REGISTRY = get_effect_registry()

# Effect classes for code that imports them by name
from .color_effects import (
    BloomEffect,
    GodRaysEffect,
    VignetteEffect,
    PulseGlowEffect,
    ColorGradingEffect,
    PosterizeEffect,
    EdgeDetectEffect,
)
from .distort_effects import (
    ChromaticAberrationEffect,
    DistortionEffect,
    VHSNoiseEffect,
    BarrelDistortionEffect,
    HeatDistortionEffect,
    PixelateEffect,
    ShockwaveEffect,
    MotionTrailEffect,
)

# Export managers
from .managers import (
    ShockwaveManager,
    ScreenShakeManager,
    LightManager,
    Light,
    get_shockwave_manager,
    get_screenshake_manager,
    get_light_manager,
)

__all__ = [
    "PostProcessEffect",
    "EffectDef",
    "SHADER_PROFILES",
    "EFFECT_REGISTRY",
    "get_effect_registry",
    "get_menu_shader_stack",
    "get_pause_shader_stack",
    "get_gameplay_shader_stack",
    "BloomEffect",
    "GodRaysEffect",
    "VignetteEffect",
    "PulseGlowEffect",
    "ColorGradingEffect",
    "PosterizeEffect",
    "EdgeDetectEffect",
    "ChromaticAberrationEffect",
    "DistortionEffect",
    "VHSNoiseEffect",
    "BarrelDistortionEffect",
    "HeatDistortionEffect",
    "PixelateEffect",
    "ShockwaveEffect",
    "MotionTrailEffect",
    "ShockwaveManager",
    "ScreenShakeManager",
    "LightManager",
    "Light",
    "get_shockwave_manager",
    "get_screenshake_manager",
    "get_light_manager",
]
