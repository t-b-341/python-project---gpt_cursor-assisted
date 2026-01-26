"""
Color-based post-process effects: bloom, vignette, color grading, etc.
"""
from __future__ import annotations

import math
from typing import Any

import pygame

from .base import PostProcessEffect


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
