"""
Distortions, waves, warps, and glitch-style effects.
"""
from __future__ import annotations

import math
import random
from typing import Any

import pygame

from .base import PostProcessEffect


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
