"""
Shader pipeline manager for ordered shader execution.

Manages a list of shaders with categories and execution order, providing
safe error handling and uniform management.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

from shader_effects.registry import get_shader_spec, ShaderCategory as RegistryCategory
from shader_effects.context import ShaderContext

if TYPE_CHECKING:
    import pygame

logger = logging.getLogger(__name__)


class ShaderCategory(Enum):
    """Shader execution categories in pipeline order."""
    EARLY = 1  # pixelation, blur
    MID = 2    # distortion, shockwave, bloom
    LATE = 3   # color grading, fog, CRT
    LAST = 4   # vignette


@dataclass
class ShaderEntry:
    """Represents a shader in the pipeline."""
    name: str
    category: ShaderCategory
    enabled: bool = True
    render_pass: Optional[Callable[[Any, float, dict], Any]] = None
    default_uniforms: dict[str, Any] = field(default_factory=dict)
    custom_uniforms: dict[str, Any] = field(default_factory=dict)
    fail_count: int = 0
    max_failures: int = 5


class ShaderPipelineManager:
    """
    Manages an ordered list of shaders with execution pipeline.
    
    Shaders are executed in category order (EARLY -> MID -> LATE -> LAST),
    then by insertion order within each category.
    """
    
    def __init__(self):
        """Initialize an empty pipeline."""
        self._shaders: list[ShaderEntry] = []
        self._shader_map: dict[str, ShaderEntry] = {}
        self._safe_mode: bool = True  # Skip failed shaders instead of crashing
        self._order_logged: bool = False  # Track if we've logged the order
    
    def add_shader(
        self,
        name: str,
        category: ShaderCategory,
        pass_fn: Callable[[Any, float, dict], Any],
        default_uniforms: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Add a shader to the pipeline.
        
        Args:
            name: Unique identifier for the shader
            category: Execution category (EARLY, MID, LATE, LAST)
            pass_fn: Function that takes (surface, dt, context) and returns processed surface
            default_uniforms: Optional default uniform values
        """
        if name in self._shader_map:
            logger.warning(f"Shader '{name}' already exists, replacing it")
            self.remove_shader(name)
        
        entry = ShaderEntry(
            name=name,
            category=category,
            enabled=True,
            render_pass=pass_fn,
            default_uniforms=default_uniforms or {},
        )
        
        # Look up registry defaults
        spec = get_shader_spec(name)
        if spec is not None:
            # Only populate uniforms if they're not already provided
            if not entry.default_uniforms:
                entry.default_uniforms.update(spec.default_uniforms)
            else:
                # Merge: registry defaults for missing keys
                for key, value in spec.default_uniforms.items():
                    if key not in entry.default_uniforms:
                        entry.default_uniforms[key] = value
        
        self._shaders.append(entry)
        self._shader_map[name] = entry
        self._sort_shaders()
        
        # Log pipeline order once when first shader is added
        if not self._order_logged and len(self._shaders) > 0:
            logger.info("Shader pipeline order: %s", [e.name for e in self._shaders])
            self._order_logged = True
    
    def remove_shader(self, name: str) -> bool:
        """
        Remove a shader from the pipeline.
        
        Returns:
            True if shader was found and removed, False otherwise
        """
        if name not in self._shader_map:
            return False
        
        entry = self._shader_map.pop(name)
        self._shaders.remove(entry)
        return True
    
    def enable_shader(self, name: str) -> bool:
        """
        Enable a shader in the pipeline.
        
        Returns:
            True if shader was found and enabled, False otherwise
        """
        if name not in self._shader_map:
            return False
        self._shader_map[name].enabled = True
        return True
    
    def disable_shader(self, name: str) -> bool:
        """
        Disable a shader in the pipeline.
        
        Returns:
            True if shader was found and disabled, False otherwise
        """
        if name not in self._shader_map:
            return False
        self._shader_map[name].enabled = False
        return True
    
    def set_uniform(self, name: str, uniform: str, value: Any) -> bool:
        """
        Set a uniform value for a specific shader.
        
        Args:
            name: Shader name
            uniform: Uniform parameter name
            value: Value to set
            
        Returns:
            True if shader was found and uniform was set, False otherwise
        """
        if name not in self._shader_map:
            return False
        self._shader_map[name].custom_uniforms[uniform] = value
        return True
    
    def get_uniform(self, name: str, uniform: str, default: Any = None) -> Any:
        """
        Get a uniform value for a specific shader.
        
        Returns custom uniform if set, otherwise default uniform, otherwise default value.
        """
        if name not in self._shader_map:
            return default
        entry = self._shader_map[name]
        if uniform in entry.custom_uniforms:
            return entry.custom_uniforms[uniform]
        return entry.default_uniforms.get(uniform, default)
    
    def execute_pipeline(
        self,
        screen_texture: "pygame.Surface",
        dt: float = 0.016,
        context: Optional[ShaderContext] = None,
    ) -> "pygame.Surface":
        """
        Execute all enabled shaders in the pipeline order.
        
        Args:
            screen_texture: Input surface to process
            dt: Delta time for time-based effects
            context: Optional context dictionary for shader passes
            
        Returns:
            Processed surface (may be the original if no shaders ran)
        """
        if context is None:
            context = {}
        
        current_surface = screen_texture
        
        for entry in self._shaders:
            if not entry.enabled or entry.render_pass is None:
                continue
            
            try:
                # Merge default and custom uniforms into context
                shader_ctx: dict[str, Any] = {**context}
                shader_ctx.update(entry.default_uniforms)
                shader_ctx.update(entry.custom_uniforms)
                
                result = entry.render_pass(current_surface, dt, shader_ctx)
                if result is not None:
                    current_surface = result
            except Exception as e:
                entry.fail_count += 1
                cat = getattr(entry, "category", None)
                cat_name = getattr(cat, "name", str(cat)) if cat else "unknown"
                logger.error(
                    "Shader '%s' (category %s) failed (%d/%d): %s",
                    entry.name, cat_name, entry.fail_count, entry.max_failures, e,
                    exc_info=True,
                )
                if self._safe_mode and entry.fail_count >= entry.max_failures:
                    entry.enabled = False
                    logger.error(
                        "Disabling shader '%s' after %d repeated failures",
                        entry.name, entry.max_failures
                    )
                if not self._safe_mode:
                    raise
        
        return current_surface
    
    def _sort_shaders(self) -> None:
        """Sort shaders by category, then by insertion order."""
        # Sort by category enum value, then maintain insertion order (stable sort)
        # Filter out any entries with None category (shouldn't happen, but be safe)
        self._shaders.sort(key=lambda s: s.category.value if s.category is not None else 999)
    
    def clear(self) -> None:
        """Remove all shaders from the pipeline."""
        self._shaders.clear()
        self._shader_map.clear()
    
    def get_enabled_shaders(self) -> list[str]:
        """Return list of enabled shader names."""
        return [s.name for s in self._shaders if s.enabled]
    
    def get_shader_info(self, name: str) -> Optional[dict]:
        """Get information about a shader."""
        if name not in self._shader_map:
            return None
        entry = self._shader_map[name]
        return {
            "name": entry.name,
            "category": entry.category.name,
            "enabled": entry.enabled,
            "default_uniforms": entry.default_uniforms.copy(),
            "custom_uniforms": entry.custom_uniforms.copy(),
        }
