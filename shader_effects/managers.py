"""
Managers for shader effects that require state tracking (shockwave, screenshake, etc.).
"""
from __future__ import annotations

from typing import Optional
import math


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
