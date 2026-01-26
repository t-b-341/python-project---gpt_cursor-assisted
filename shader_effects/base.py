"""
Base effect classes, registry logic, and stack helpers.

PostProcessEffect is the base for all effects. EFFECT_REGISTRY and SHADER_PROFILES
define the central registry and profile lists. get_*_shader_stack build stacks from config.
"""
from __future__ import annotations

from typing import Any, Callable, Union

import pygame


class PostProcessEffect:
    """Base for post-process effects. Subclasses implement apply(surface, dt, context)."""

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        """Apply effect. May modify surface in place or return a new surface. Default: no-op."""
        return surface


# -----------------------------------------------------------------------------
# Shader profiles: name -> list of (registry_key, param_overrides)
# Used by get_menu_shader_stack, get_pause_shader_stack, get_gameplay_shader_stack.
# -----------------------------------------------------------------------------

EffectDef = Union[tuple[str, dict], str]  # (key, params) or bare key

SHADER_PROFILES: dict[str, list[EffectDef]] = {
    "none": [],
    "menu_crt": [
        ("barrel_distortion", {"curvature_strength": 0.04, "edge_softness": 0.12}),
        ("vignette", {"radius": 0.78, "softness": 0.22, "intensity": 0.4, "color": (0, 0, 0)}),
        ("chromatic_aberration", {"shift_strength": 0.15, "direction": "radial"}),
        ("vhs_noise", {"jitter_strength": 1, "noise_strength": 6, "roll_speed": 0.3}),
    ],
    "menu_neon": [
        ("color_grading", {"mode": "neon", "strength": 0.2}),
        ("vignette", {"radius": 0.8, "softness": 0.2, "intensity": 0.3, "color": (0, 0, 0)}),
        ("pulse_glow", {"period": 2.5, "min_intensity": 0.97, "max_intensity": 1.06, "tint_color": (100, 150, 255)}),
    ],
    "pause_dim_vignette": [
        ("vignette", {"radius": 0.7, "softness": 0.3, "intensity": 0.5, "color": (0, 0, 0)}),
        ("color_grading", {"mode": "noir", "strength": 0.35}),
    ],
    "gameplay_subtle_vignette": [
        ("vignette", {"radius": 0.8, "softness": 0.25, "intensity": 0.2, "color": (0, 0, 0)}),
    ],
    "gameplay_retro": [
        ("vignette", {"radius": 0.78, "softness": 0.22, "intensity": 0.28, "color": (0, 0, 0)}),
        ("color_grading", {"mode": "retro", "strength": 0.2}),
    ],
}


_warned_missing_keys: set[str] = set()


def _build_stack_from_profile(
    profile_name: str,
    registry: dict[str, Callable[[], PostProcessEffect]],
    profiles: dict[str, list[EffectDef]] | None = None,
) -> list[PostProcessEffect]:
    """Return a list of effect instances for the given profile. Uses SHADER_PROFILES if profiles is None."""
    profs = profiles if profiles is not None else SHADER_PROFILES
    if profile_name and profile_name != "none" and profile_name not in profs:
        print(f"[shader] unknown profile {profile_name!r}, using empty stack")
        return []
    defs = profs.get(profile_name, []) if profile_name else []
    out: list[PostProcessEffect] = []
    for d in defs:
        if isinstance(d, str):
            key, params = d, {}
        else:
            key, params = d[0], d[1] if len(d) > 1 else {}
        if key not in registry:
            if key not in _warned_missing_keys:
                _warned_missing_keys.add(key)
                print(f"[shader] effect key {key!r} not in registry, skipping")
            continue
        eff = registry[key]()
        for k, v in params.items():
            if hasattr(eff, k):
                setattr(eff, k, v)
        out.append(eff)
    return out


def get_effect_registry() -> dict[str, Callable[[], PostProcessEffect]]:
    """Return EFFECT_REGISTRY, built lazily to avoid circular imports."""
    from . import color_effects, distort_effects

    return {
        "chromatic_aberration": lambda: distort_effects.ChromaticAberrationEffect(shift_strength=0.3, direction="radial"),
        "bloom": lambda: color_effects.BloomEffect(intensity=0.35, threshold=210, blur_size=2),
        "god_rays": lambda: color_effects.GodRaysEffect(source_pos=(0.5, 0.5), strength=0.12, ray_length=6, samples=4),
        "distortion": lambda: distort_effects.DistortionEffect(intensity=1.5, scale=0.02, speed=2.0),
        "vhs_noise": lambda: distort_effects.VHSNoiseEffect(jitter_strength=1, noise_strength=8, roll_speed=0.5),
        "barrel_distortion": lambda: distort_effects.BarrelDistortionEffect(curvature_strength=0.05, edge_softness=0.15),
        "vignette": lambda: color_effects.VignetteEffect(radius=0.75, softness=0.25, intensity=0.35, color=(0, 0, 0)),
        "heat_distortion": lambda: distort_effects.HeatDistortionEffect(intensity=2.0, wave_scale=0.025, speed=4.0),
        "pulse_glow": lambda: color_effects.PulseGlowEffect(period=2.0, min_intensity=0.95, max_intensity=1.05, tint_color=(255, 255, 255)),
        "color_grading": lambda: color_effects.ColorGradingEffect(mode="retro", strength=0.25),
        "pixelate": lambda: distort_effects.PixelateEffect(pixel_scale=4, blend_amount=0.7),
        "shockwave": lambda: distort_effects.ShockwaveEffect(origin=(0.5, 0.5), radius=80, amplitude=4, falloff=0.03),
        "edge_detect": lambda: color_effects.EdgeDetectEffect(threshold=50, outline_color=(255, 255, 0), blend_strength=0.25),
        "posterize": lambda: color_effects.PosterizeEffect(levels=5, contrast_boost=1.05),
        "motion_trail": lambda: distort_effects.MotionTrailEffect(history_blend=0.8, fade_speed=0.9),
    }


def get_menu_shader_stack(
    config: Any,
    registry: dict[str, Callable[[], PostProcessEffect]] | None = None,
) -> list[PostProcessEffect]:
    """Return the menu effect stack for the current config. Empty if disabled or profile is 'none'."""
    if not getattr(config, "enable_menu_shaders", False):
        return []
    profile = getattr(config, "menu_shader_profile", "none") or "none"
    if profile == "none":
        return []
    reg = registry if registry is not None else get_effect_registry()
    return _build_stack_from_profile(profile, reg, SHADER_PROFILES)


def get_pause_shader_stack(
    config: Any,
    registry: dict[str, Callable[[], PostProcessEffect]] | None = None,
) -> list[PostProcessEffect]:
    """Return the pause effect stack for the current config. Empty if disabled or profile is 'none'."""
    if not getattr(config, "enable_pause_shaders", False):
        return []
    profile = getattr(config, "pause_shader_profile", "none") or "none"
    if profile == "none":
        return []
    reg = registry if registry is not None else get_effect_registry()
    return _build_stack_from_profile(profile, reg, SHADER_PROFILES)


def get_gameplay_shader_stack(
    config: Any,
    registry: dict[str, Callable[[], PostProcessEffect]] | None = None,
) -> list[PostProcessEffect]:
    """Return the gameplay effect stack for the current config. Empty if disabled or profile is 'none'."""
    if not getattr(config, "enable_gameplay_shaders", False):
        return []
    profile = getattr(config, "gameplay_shader_profile", "none") or "none"
    if profile == "none":
        return []
    reg = registry if registry is not None else get_effect_registry()
    return _build_stack_from_profile(profile, reg, SHADER_PROFILES)
