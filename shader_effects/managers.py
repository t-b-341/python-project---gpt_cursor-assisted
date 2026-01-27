"""
Managers for shader effects that require state tracking (shockwave, screenshake, lighting, etc.).
"""
from __future__ import annotations

from typing import Optional, List, Tuple
import math
import pygame


class ShockwaveManager:
    """Manages shockwave effect state and timing."""
    
    def __init__(self) -> None:
        self.active_waves: list[dict] = []
        self.time = 0.0
        self.amplitude = 5.0
        self.speed = 10.0
    
    def update(self, dt: float) -> None:
        """Update shockwave manager state."""
        self.time += dt
        # Remove expired waves
        self.active_waves = [
            w for w in self.active_waves
            if self.time - w["start_time"] < w["duration"]
        ]
    
    def trigger(self, center_x: float = 0.5, center_y: float = 0.5, duration: float = 1.0) -> None:
        """
        Trigger a shockwave effect.
        
        Args:
            center_x: X position of shockwave center (0.0 to 1.0)
            center_y: Y position of shockwave center (0.0 to 1.0)
            duration: Duration of shockwave in seconds
        """
        self.active_waves.append({
            "center": (center_x, center_y),
            "start_time": self.time,
            "duration": duration,
        })
    
    def get_active_wave(self) -> Optional[dict]:
        """Get the most recent active wave, or None if no waves active."""
        if not self.active_waves:
            return None
        # Return most recent wave
        return max(self.active_waves, key=lambda w: w["start_time"])
    
    def get_wave_params(self) -> tuple[float, float, float]:
        """
        Get current wave parameters for shader.
        
        Returns:
            Tuple of (center_x, center_y, time) or (0.5, 0.5, 0.0) if no active wave
        """
        wave = self.get_active_wave()
        if wave is None:
            return (0.5, 0.5, 0.0)
        
        center_x, center_y = wave["center"]
        elapsed = self.time - wave["start_time"]
        return (center_x, center_y, elapsed)


class ScreenShakeManager:
    """Manages screen shake effect state and timing."""
    
    def __init__(self) -> None:
        self.shake_intensity = 0.0
        self.shake_time = 0.0
        self.decay_rate = 5.0  # Intensity decay per second
    
    def update(self, dt: float) -> None:
        """Update screen shake manager state."""
        if self.shake_intensity > 0:
            self.shake_time += dt
            # Decay intensity over time
            self.shake_intensity = max(0.0, self.shake_intensity - self.decay_rate * dt)
            if self.shake_intensity <= 0:
                self.shake_time = 0.0
    
    def trigger(self, intensity: float = 1.0) -> None:
        """
        Trigger a screen shake effect.
        
        Args:
            intensity: Shake intensity (0.0 to 1.0+)
        """
        self.shake_intensity = max(self.shake_intensity, intensity)
        if self.shake_time == 0.0:
            self.shake_time = 0.001  # Start timer if not already shaking
    
    def get_shake_params(self) -> tuple[float, float]:
        """
        Get current shake parameters for shader.
        
        Returns:
            Tuple of (intensity, time)
        """
        return (self.shake_intensity, self.shake_time)


# Global managers (can be accessed from game code)
_shockwave_manager: Optional[ShockwaveManager] = None
_screenshake_manager: Optional[ScreenShakeManager] = None


def get_shockwave_manager() -> ShockwaveManager:
    """Get or create the global ShockwaveManager instance."""
    global _shockwave_manager
    if _shockwave_manager is None:
        _shockwave_manager = ShockwaveManager()
    return _shockwave_manager


def get_screenshake_manager() -> ScreenShakeManager:
    """Get or create the global ScreenShakeManager instance."""
    global _screenshake_manager
    if _screenshake_manager is None:
        _screenshake_manager = ScreenShakeManager()
    return _screenshake_manager


class Light:
    """Represents a single light source."""
    
    def __init__(
        self,
        pos: Tuple[float, float],
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        radius: float = 0.2,
        intensity: float = 1.0,
    ) -> None:
        self.pos = pos  # Screen space (0.0 to 1.0)
        self.color = color  # RGB (0.0 to 1.0)
        self.radius = radius  # Screen space radius
        self.intensity = intensity  # Light intensity multiplier


class LightManager:
    """Manages 2D dynamic lighting system."""
    
    def __init__(self) -> None:
        self.lights: List[Light] = []
        self.max_lights = 8  # Match shader array size
        self.ambient_color = (0.2, 0.2, 0.3)  # Default ambient (slightly blue)
        self.ambient_intensity = 0.3
    
    def add_light(
        self,
        pos: Tuple[float, float],
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        radius: float = 0.2,
        intensity: float = 1.0,
    ) -> Optional[Light]:
        """
        Add a light to the scene.
        
        Args:
            pos: Light position in screen space (0.0 to 1.0)
            color: Light color (RGB, 0.0 to 1.0)
            radius: Light radius in screen space
            intensity: Light intensity multiplier
        
        Returns:
            Light object or None if max lights reached
        """
        if len(self.lights) >= self.max_lights:
            return None
        
        light = Light(pos, color, radius, intensity)
        self.lights.append(light)
        return light
    
    def remove_light(self, light: Light) -> bool:
        """Remove a light from the scene. Returns True if removed."""
        if light in self.lights:
            self.lights.remove(light)
            return True
        return False
    
    def clear_lights(self) -> None:
        """Remove all lights."""
        self.lights.clear()
    
    def get_light_data(self) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float, float]], List[float], List[float]]:
        """
        Get light data formatted for shader uniforms.
        
        Returns:
            Tuple of (positions, colors, radii, intensities) lists
        """
        positions = [light.pos for light in self.lights]
        colors = [light.color for light in self.lights]
        radii = [light.radius for light in self.lights]
        intensities = [light.intensity for light in self.lights]
        
        # Pad to max_lights with zeros
        while len(positions) < self.max_lights:
            positions.append((0.0, 0.0))
            colors.append((0.0, 0.0, 0.0))
            radii.append(0.0)
            intensities.append(0.0)
        
        return positions, colors, radii, intensities
    
    def update_light_positions(self, dt: float) -> None:
        """Update light positions (for moving lights). Override in subclasses if needed."""
        pass


# Global light manager
_light_manager: Optional[LightManager] = None


def get_light_manager() -> LightManager:
    """Get or create the global LightManager instance."""
    global _light_manager
    if _light_manager is None:
        _light_manager = LightManager()
    return _light_manager


# Export LightManager and Light
__all__ = [
    "ShockwaveManager",
    "ScreenShakeManager",
    "LightManager",
    "Light",
    "get_shockwave_manager",
    "get_screenshake_manager",
    "get_light_manager",
]
