"""
Post-processing effect classes and central registry.

Each effect implements apply(surface, dt, context) and can be looked up by key
from EFFECT_REGISTRY. All effects are CPU-based 2D post-process (pygame surfaces).
"""
from __future__ import annotations

import math
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
# 1) ChromaticAberrationEffect
# -----------------------------------------------------------------------------


class ChromaticAberrationEffect(PostProcessEffect):
    """Slight RGB channel offset. Params: shift_strength (float), direction ("radial" or "horizontal")."""

    def __init__(
        self,
        shift_strength: float = 0.3,
        direction: str = "radial",
    ) -> None:
        self.shift_strength = shift_strength
        self.direction = direction

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        if self.shift_strength <= 0:
            return surface
        w, h = surface.get_size()
        shift = max(1, min(5, int(self.shift_strength * 4)))
        out = surface.copy()
        cx, cy = w / 2.0, h / 2.0
        for y in range(0, h, 2):  # step to keep cheap
            for x in range(0, w, 2):
                if self.direction == "radial":
                    dx = (x - cx) / max(cx, 1)
                    dy = (y - cy) / max(cy, 1)
                    d = math.sqrt(dx * dx + dy * dy)
                    sx = int(shift * dx * d) if d > 0 else 0
                    sy = int(shift * dy * d) if d > 0 else 0
                else:
                    sx, sy = shift, 0
                r = surface.get_at((min(w - 1, max(0, x + sx)), min(h - 1, max(0, y + sy))))[0]
                g = surface.get_at((x, y))[1]
                b = surface.get_at((min(w - 1, max(0, x - sx)), min(h - 1, max(0, y - sy))))[2]
                out.set_at((x, y), (r, g, b, 255))
        return out


# -----------------------------------------------------------------------------
# 2) BloomEffect
# -----------------------------------------------------------------------------


class BloomEffect(PostProcessEffect):
    """Brightness threshold + blur for glow. Params: intensity, threshold, blur_size."""

    def __init__(
        self,
        intensity: float = 0.4,
        threshold: int = 200,
        blur_size: int = 2,
    ) -> None:
        self.intensity = intensity
        self.threshold = threshold
        self.blur_size = max(1, min(3, blur_size))

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        bright = pygame.Surface((w, h), flags=pygame.SRCALPHA)
        for y in range(h):
            for x in range(w):
                c = surface.get_at((x, y))
                m = (c[0] + c[1] + c[2]) / 3.0
                if m >= self.threshold:
                    bright.set_at((x, y), (*c[:3], int(255 * self.intensity)))
        b = self.blur_size
        blurred = bright.copy()
        for y in range(b, h - b):
            for x in range(b, w - b):
                r = g = bl = a = 0
                n = 0
                for dy in range(-b, b + 1):
                    for dx in range(-b, b + 1):
                        c = bright.get_at((x + dx, y + dy))
                        r += c[0]
                        g += c[1]
                        bl += c[2]
                        a += c[3]
                        n += 1
                if n:
                    blurred.set_at((x, y), (r // n, g // n, bl // n, a // n))
        surface.blit(blurred, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return surface


# -----------------------------------------------------------------------------
# 3) GodRaysEffect
# -----------------------------------------------------------------------------


class GodRaysEffect(PostProcessEffect):
    """Simple radial blur from a source point. Params: source_pos, strength, ray_length, samples."""

    def __init__(
        self,
        source_pos: tuple[float, float] = (0.5, 0.5),
        strength: float = 0.15,
        ray_length: int = 8,
        samples: int = 4,
    ) -> None:
        self.source_pos = source_pos
        self.strength = strength
        self.ray_length = max(2, min(12, ray_length))
        self.samples = max(2, min(8, samples))

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        sx = int(self.source_pos[0] * w)
        sy = int(self.source_pos[1] * h)
        out = surface.copy()
        step = max(2, w // 80)
        for y in range(0, h, step):
            for x in range(0, w, step):
                dx = x - sx
                dy = y - sy
                d = math.sqrt(dx * dx + dy * dy)
                if d < 1:
                    continue
                nx, ny = dx / d, dy / d
                r = g = b = 0
                for i in range(self.samples):
                    t = (i + 1) / self.samples * self.ray_length
                    ix = int(sx + nx * t)
                    iy = int(sy + ny * t)
                    if 0 <= ix < w and 0 <= iy < h:
                        c = surface.get_at((ix, iy))
                        r += c[0]
                        g += c[1]
                        b += c[2]
                if self.samples:
                    r = int(r / self.samples * self.strength)
                    g = int(g / self.samples * self.strength)
                    b = int(b / self.samples * self.strength)
                    c0 = surface.get_at((x, y))
                    out.set_at((x, y), (
                        min(255, c0[0] + r),
                        min(255, c0[1] + g),
                        min(255, c0[2] + b),
                        255,
                    ))
        return out


# -----------------------------------------------------------------------------
# 4) DistortionEffect
# -----------------------------------------------------------------------------


class DistortionEffect(PostProcessEffect):
    """2D displacement using a time-based offset pattern. Params: intensity, scale, speed."""

    def __init__(
        self,
        intensity: float = 2.0,
        scale: float = 0.02,
        speed: float = 3.0,
    ) -> None:
        self.intensity = intensity
        self.scale = scale
        self.speed = speed

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        t = context.get("time", 0.0) + dt * self.speed
        w, h = surface.get_size()
        out = surface.copy()
        step = max(2, w // 60)
        for y in range(0, h, step):
            for x in range(0, w, step):
                ox = int(self.intensity * math.sin(x * self.scale + t) * 2)
                oy = int(self.intensity * math.sin(y * self.scale + t * 1.1) * 2)
                sx = min(w - 1, max(0, x + ox))
                sy = min(h - 1, max(0, y + oy))
                out.set_at((x, y), surface.get_at((sx, sy)))
        return out


# -----------------------------------------------------------------------------
# 5) VHSNoiseEffect
# -----------------------------------------------------------------------------


class VHSNoiseEffect(PostProcessEffect):
    """Horizontal jitter + scanline noise. Params: jitter_strength, noise_strength, roll_speed."""

    def __init__(
        self,
        jitter_strength: int = 2,
        noise_strength: int = 12,
        roll_speed: float = 1.0,
    ) -> None:
        self.jitter_strength = max(0, min(8, jitter_strength))
        self.noise_strength = max(0, min(80, noise_strength))
        self.roll_speed = roll_speed

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        import random
        w, h = surface.get_size()
        t = context.get("time", 0.0) + dt * self.roll_speed
        out = surface.copy()
        for y in range(h):
            j = int(self.jitter_strength * (random.random() * 2 - 1)) if self.jitter_strength else 0
            for x in range(w):
                sx = (x + j) % w
                c = list(out.get_at((sx, y)))
                if self.noise_strength and y % 3 == int(t) % 3:
                    n = int((random.random() - 0.5) * self.noise_strength)
                    c[0] = min(255, max(0, c[0] + n))
                    c[1] = min(255, max(0, c[1] + n))
                    c[2] = min(255, max(0, c[2] + n))
                out.set_at((x, y), tuple(c))
        return out


# -----------------------------------------------------------------------------
# 6) BarrelDistortionEffect
# -----------------------------------------------------------------------------


class BarrelDistortionEffect(PostProcessEffect):
    """CRT-like curvature. Params: curvature_strength, edge_softness."""

    def __init__(
        self,
        curvature_strength: float = 0.08,
        edge_softness: float = 0.1,
    ) -> None:
        self.curvature_strength = curvature_strength
        self.edge_softness = edge_softness

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        cx, cy = (w - 1) / 2.0, (h - 1) / 2.0
        out = surface.copy()
        step = max(2, w // 80)
        for y in range(0, h, step):
            for x in range(0, w, step):
                nx = (x - cx) / max(cx, 1)
                ny = (y - cy) / max(cy, 1)
                r = math.sqrt(nx * nx + ny * ny)
                r2 = r * (1.0 + self.curvature_strength * r * r)
                sx = int(cx + nx * r2 / max(r, 1e-6) * cx)
                sy = int(cy + ny * r2 / max(r, 1e-6) * cy)
                if 0 <= sx < w and 0 <= sy < h:
                    out.set_at((x, y), surface.get_at((sx, sy)))
        return out


# -----------------------------------------------------------------------------
# 7) VignetteEffect
# -----------------------------------------------------------------------------


class VignetteEffect(PostProcessEffect):
    """Darkens corners. Params: radius, softness, intensity, color."""

    def __init__(
        self,
        radius: float = 0.75,
        softness: float = 0.2,
        intensity: float = 0.4,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        self.radius = radius
        self.softness = softness
        self.intensity = intensity
        self.color = color

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        m = 32
        mask = pygame.Surface((m, m), flags=pygame.SRCALPHA)
        cx, cy = (m - 1) / 2.0, (m - 1) / 2.0
        mx = math.sqrt(cx * cx + cy * cy)
        for i in range(m):
            for j in range(m):
                d = math.sqrt((i - cx) ** 2 + (j - cy) ** 2) / mx
                t = (d - self.radius) / max(self.softness, 0.01)
                t = max(0, min(1, t))
                a = int(255 * self.intensity * t)
                mask.set_at((i, j), (*self.color, a))
        scaled = pygame.transform.smoothscale(mask, (w, h))
        surface.blit(scaled, (0, 0))
        return surface


# -----------------------------------------------------------------------------
# 8) HeatDistortionEffect
# -----------------------------------------------------------------------------


class HeatDistortionEffect(PostProcessEffect):
    """Wavy distortion using time-based sin. Params: intensity, wave_scale, speed."""

    def __init__(
        self,
        intensity: float = 3.0,
        wave_scale: float = 0.03,
        speed: float = 5.0,
    ) -> None:
        self.intensity = intensity
        self.wave_scale = wave_scale
        self.speed = speed

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        t = context.get("time", 0.0) * self.speed
        w, h = surface.get_size()
        out = surface.copy()
        step = max(2, w // 50)
        for y in range(0, h, step):
            for x in range(0, w, step):
                ox = int(self.intensity * math.sin(y * self.wave_scale + t))
                oy = int(self.intensity * 0.5 * math.sin(x * self.wave_scale + t * 1.3))
                sx = min(w - 1, max(0, x + ox))
                sy = min(h - 1, max(0, y + oy))
                out.set_at((x, y), surface.get_at((sx, sy)))
        return out


# -----------------------------------------------------------------------------
# 9) PulseGlowEffect
# -----------------------------------------------------------------------------


class PulseGlowEffect(PostProcessEffect):
    """Periodic brightness/tint modulation. Params: period, min_intensity, max_intensity, tint_color."""

    def __init__(
        self,
        period: float = 2.0,
        min_intensity: float = 0.9,
        max_intensity: float = 1.1,
        tint_color: tuple[int, int, int] | None = None,
    ) -> None:
        self.period = max(0.1, period)
        self.min_intensity = min_intensity
        self.max_intensity = max_intensity
        self.tint_color = tint_color or (255, 255, 255)

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        t = context.get("time", 0.0)
        v = (math.sin(2 * math.pi * t / self.period) + 1.0) / 2.0
        mult = self.min_intensity + (self.max_intensity - self.min_intensity) * v
        w, h = surface.get_size()
        overlay = pygame.Surface((w, h), flags=pygame.SRCALPHA)
        alpha = int(32 * (mult - 1.0)) if self.tint_color else 0
        if alpha != 0:
            overlay.fill((*self.tint_color[:3], min(255, abs(alpha))))
            surface.blit(overlay, (0, 0))
        return surface


# -----------------------------------------------------------------------------
# 10) ColorGradingEffect
# -----------------------------------------------------------------------------


class ColorGradingEffect(PostProcessEffect):
    """Simple curve-based grading. Params: mode ("retro","noir","neon"), strength."""

    def __init__(self, mode: str = "retro", strength: float = 0.3) -> None:
        self.mode = mode
        self.strength = max(0, min(1, strength))

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        out = surface.copy()
        step = max(2, w // 40)
        for y in range(0, h, step):
            for x in range(0, w, step):
                r, g, b, a = surface.get_at((x, y))
                if self.mode == "noir":
                    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                    r = int(r + (gray - r) * self.strength)
                    g = int(g + (gray - g) * self.strength)
                    b = int(b + (gray - b) * self.strength)
                elif self.mode == "neon":
                    r = min(255, int(r * (1 + self.strength * 0.3)))
                    b = min(255, int(b * (1 + self.strength * 0.4)))
                    g = min(255, int(g * (1 + self.strength * 0.2)))
                else:  # retro
                    r = min(255, int(r * (1 + self.strength * 0.15)))
                    g = min(255, int(g * (1 + self.strength * 0.05)))
                    b = min(255, int(b * (1 - self.strength * 0.1)))
                out.set_at((x, y), (r, g, b, a))
        return out


# -----------------------------------------------------------------------------
# 11) PixelateEffect
# -----------------------------------------------------------------------------


class PixelateEffect(PostProcessEffect):
    """Downscale/upscale for pixel look. Params: pixel_scale, blend_amount."""

    def __init__(self, pixel_scale: int = 4, blend_amount: float = 1.0) -> None:
        self.pixel_scale = max(1, min(32, pixel_scale))
        self.blend_amount = max(0, min(1, blend_amount))

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        if self.pixel_scale <= 1 or self.blend_amount <= 0:
            return surface
        w, h = surface.get_size()
        small_w = max(1, w // self.pixel_scale)
        small_h = max(1, h // self.pixel_scale)
        small = pygame.transform.smoothscale(surface, (small_w, small_h))
        scaled = pygame.transform.smoothscale(small, (w, h))
        if self.blend_amount < 1:
            scaled.set_alpha(int(255 * self.blend_amount))
        surface.blit(scaled, (0, 0))
        return surface


# -----------------------------------------------------------------------------
# 12) ShockwaveEffect
# -----------------------------------------------------------------------------


class ShockwaveEffect(PostProcessEffect):
    """Radial displacement from origin. Params: origin, radius, amplitude, falloff."""

    def __init__(
        self,
        origin: tuple[float, float] = (0.5, 0.5),
        radius: float = 100.0,
        amplitude: float = 5.0,
        falloff: float = 0.02,
    ) -> None:
        self.origin = origin
        self.radius = radius
        self.amplitude = amplitude
        self.falloff = falloff

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        ox = self.origin[0] * w
        oy = self.origin[1] * h
        out = surface.copy()
        step = max(2, w // 60)
        for y in range(0, h, step):
            for x in range(0, w, step):
                dx, dy = x - ox, y - oy
                d = math.sqrt(dx * dx + dy * dy)
                if d < 1:
                    continue
                nd = d - self.radius
                disp = self.amplitude * math.exp(-self.falloff * nd * nd)
                sx = int(x + (dx / d) * disp)
                sy = int(y + (dy / d) * disp)
                if 0 <= sx < w and 0 <= sy < h:
                    out.set_at((x, y), surface.get_at((sx, sy)))
        return out


# -----------------------------------------------------------------------------
# 13) EdgeDetectEffect
# -----------------------------------------------------------------------------


class EdgeDetectEffect(PostProcessEffect):
    """Sobel-like edges blended over the frame. Params: threshold, outline_color, blend_strength."""

    def __init__(
        self,
        threshold: int = 40,
        outline_color: tuple[int, int, int] = (255, 255, 0),
        blend_strength: float = 0.3,
    ) -> None:
        self.threshold = threshold
        self.outline_color = outline_color
        self.blend_strength = max(0, min(1, blend_strength))

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        out = surface.copy()
        step = max(2, w // 50)
        for y in range(1, h - 1, step):
            for x in range(1, w - 1, step):
                gx = gy = 0
                for dy in range(3):
                    for dx in range(3):
                        c = surface.get_at((x + dx - 1, y + dy - 1))
                        gray = (c[0] + c[1] + c[2]) / 3
                        gx += gray * sobel_x[dy][dx]
                        gy += gray * sobel_y[dy][dx]
                mag = math.sqrt(gx * gx + gy * gy)
                if mag >= self.threshold:
                    c0 = surface.get_at((x, y))
                    r = int(c0[0] * (1 - self.blend_strength) + self.outline_color[0] * self.blend_strength)
                    g = int(c0[1] * (1 - self.blend_strength) + self.outline_color[1] * self.blend_strength)
                    b = int(c0[2] * (1 - self.blend_strength) + self.outline_color[2] * self.blend_strength)
                    out.set_at((x, y), (min(255, r), min(255, g), min(255, b), c0[3]))
        return out


# -----------------------------------------------------------------------------
# 14) PosterizeEffect
# -----------------------------------------------------------------------------


class PosterizeEffect(PostProcessEffect):
    """Reduce color levels. Params: levels, contrast_boost."""

    def __init__(self, levels: int = 4, contrast_boost: float = 1.0) -> None:
        self.levels = max(2, min(256, levels))
        self.contrast_boost = contrast_boost

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        step = 255.0 / (self.levels - 1) if self.levels > 1 else 255
        out = surface.copy()
        for y in range(h):
            for x in range(w):
                r, g, b, a = surface.get_at((x, y))
                r = int(round(r / step) * step) * self.contrast_boost
                g = int(round(g / step) * step) * self.contrast_boost
                b = int(round(b / step) * step) * self.contrast_boost
                out.set_at((x, y), (min(255, int(r)), min(255, int(g)), min(255, int(b)), a))
        return out


# -----------------------------------------------------------------------------
# 15) MotionTrailEffect
# -----------------------------------------------------------------------------


class MotionTrailEffect(PostProcessEffect):
    """Frame history blending for simple streaks. Params: history_blend, fade_speed."""

    def __init__(self, history_blend: float = 0.85, fade_speed: float = 0.92) -> None:
        self.history_blend = max(0, min(1, history_blend))
        self.fade_speed = fade_speed
        self._last: pygame.Surface | None = None

    def apply(
        self,
        surface: pygame.Surface,
        dt: float,
        context: dict[str, Any],
    ) -> pygame.Surface:
        w, h = surface.get_size()
        if self._last is None or self._last.get_size() != (w, h):
            self._last = surface.copy()
            return surface
        out = surface.copy()
        out.blit(self._last, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self._last = surface.copy()
        self._last.set_alpha(int(255 * self.history_blend * self.fade_speed))
        return out


# -----------------------------------------------------------------------------
# Central registry: key -> factory returning effect with default params
# -----------------------------------------------------------------------------

EFFECT_REGISTRY: dict[str, Callable[[], PostProcessEffect]] = {
    "chromatic_aberration": lambda: ChromaticAberrationEffect(shift_strength=0.3, direction="radial"),
    "bloom": lambda: BloomEffect(intensity=0.35, threshold=210, blur_size=2),
    "god_rays": lambda: GodRaysEffect(source_pos=(0.5, 0.5), strength=0.12, ray_length=6, samples=4),
    "distortion": lambda: DistortionEffect(intensity=1.5, scale=0.02, speed=2.0),
    "vhs_noise": lambda: VHSNoiseEffect(jitter_strength=1, noise_strength=8, roll_speed=0.5),
    "barrel_distortion": lambda: BarrelDistortionEffect(curvature_strength=0.05, edge_softness=0.15),
    "vignette": lambda: VignetteEffect(radius=0.75, softness=0.25, intensity=0.35, color=(0, 0, 0)),
    "heat_distortion": lambda: HeatDistortionEffect(intensity=2.0, wave_scale=0.025, speed=4.0),
    "pulse_glow": lambda: PulseGlowEffect(period=2.0, min_intensity=0.95, max_intensity=1.05, tint_color=(255, 255, 255)),
    "color_grading": lambda: ColorGradingEffect(mode="retro", strength=0.25),
    "pixelate": lambda: PixelateEffect(pixel_scale=4, blend_amount=0.7),
    "shockwave": lambda: ShockwaveEffect(origin=(0.5, 0.5), radius=80, amplitude=4, falloff=0.03),
    "edge_detect": lambda: EdgeDetectEffect(threshold=50, outline_color=(255, 255, 0), blend_strength=0.25),
    "posterize": lambda: PosterizeEffect(levels=5, contrast_boost=1.05),
    "motion_trail": lambda: MotionTrailEffect(history_blend=0.8, fade_speed=0.9),
}


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


def _build_stack_from_profile(
    profile_name: str,
    registry: dict[str, Callable[[], PostProcessEffect]],
    profiles: dict[str, list[EffectDef]] | None = None,
) -> list[PostProcessEffect]:
    """Return a list of effect instances for the given profile. Uses SHADER_PROFILES if profiles is None."""
    profs = profiles if profiles is not None else SHADER_PROFILES
    defs = profs.get(profile_name, []) if profile_name else []
    out: list[PostProcessEffect] = []
    for d in defs:
        if isinstance(d, str):
            key, params = d, {}
        else:
            key, params = d[0], d[1] if len(d) > 1 else {}
        if key not in registry:
            continue
        eff = registry[key]()
        for k, v in params.items():
            if hasattr(eff, k):
                setattr(eff, k, v)
        out.append(eff)
    return out


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
    reg = registry if registry is not None else EFFECT_REGISTRY
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
    reg = registry if registry is not None else EFFECT_REGISTRY
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
    reg = registry if registry is not None else EFFECT_REGISTRY
    return _build_stack_from_profile(profile, reg, SHADER_PROFILES)
