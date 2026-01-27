"""ShaderSettingsScreen: UI for configuring shader effects with preview."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Dict, Any

import pygame

from rendering import draw_centered_text, RenderContext
from scenes.transitions import SceneTransition, KIND_POP
from gpu_gl_utils import (
    get_gl_context,
    get_fullscreen_quad,
    get_utility_shader,
    get_shaders_by_category,
    get_all_categories,
    ShaderCategory,
    create_utility_shader_program,
    HAS_MODERNGL,
)
from shader_effects.managers import get_shockwave_manager, get_screenshake_manager, get_light_manager
from shader_effects.pipeline import ShaderPipelineManager, ShaderCategory as PipelineCategory
from shader_effects.registry import SHADER_SPECS, ShaderCategory as RegistryCategory, get_shader_spec
from collections import defaultdict

if TYPE_CHECKING:
    from state import GameState

SHADER_SETTINGS_STATE_ID = "SHADER_SETTINGS"

# Build shaders by category from registry
shaders_by_category: dict[RegistryCategory, list[str]] = defaultdict(list)
for spec in SHADER_SPECS.values():
    shaders_by_category[spec.category].append(spec.name)


class ShaderSettingsScreen:
    """Screen for configuring shader effects with live preview."""
    
    def __init__(self) -> None:
        self.selected_category: Optional[str] = None
        self.selected_shader: Optional[str] = None
        self.time = 0.0
        
        # UI state
        self.category_scroll = 0
        self.shader_scroll = 0
        self.param_scroll = 0
        
        # Preview pipeline (isolated from main game)
        self.preview_pipeline = ShaderPipelineManager()
        self.preview_surface: Optional[pygame.Surface] = None
        
        # Shader uniform values (current settings)
        self.shader_uniforms: Dict[str, Dict[str, Any]] = {}
        self.shader_enabled: Dict[str, bool] = {}
        
        # Initialize with defaults from registry
        for shader_name, spec in SHADER_SPECS.items():
            self.shader_uniforms[shader_name] = spec.default_uniforms.copy()
        
        # Load saved settings (will merge with defaults)
        self._load_settings()
        
        # Demo animation state
        self.demo_time = 0.0
        self.last_shockwave_trigger = 0.0
        self.last_ripple_trigger = 0.0
        
        # Debug overlay
        self.debug_overlay_enabled = False
    
    def state_id(self) -> str:
        return SHADER_SETTINGS_STATE_ID
    
    def handle_input(self, events, game_state: "GameState", ctx: dict) -> dict:
        out = {"screen": None, "quit": False, "restart": False, "restart_to_wave1": False, "replay": False, "pop": False}
        
        keys_pressed = pygame.key.get_pressed()
        
        for e in events:
            if getattr(e, "type", None) == pygame.KEYDOWN:
                key = getattr(e, "key", None)
                if key == pygame.K_ESCAPE:
                    out["pop"] = True
                    break
                elif key == pygame.K_F12:
                    self.debug_overlay_enabled = not self.debug_overlay_enabled
                elif key == pygame.K_s and keys_pressed[pygame.K_LCTRL]:
                    # Ctrl+S to save
                    self._save_settings()
                elif key == pygame.K_l and keys_pressed[pygame.K_LCTRL]:
                    # Ctrl+L to load
                    self._load_settings()
                elif key == pygame.K_UP:
                    self._navigate_up()
                elif key == pygame.K_DOWN:
                    self._navigate_down()
                elif key == pygame.K_LEFT:
                    self._navigate_left()
                elif key == pygame.K_RIGHT:
                    self._navigate_right()
                elif key == pygame.K_RETURN or key == pygame.K_SPACE:
                    self._toggle_selected_shader()
                elif key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    self._adjust_parameter(0.1)
                elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self._adjust_parameter(-0.1)
        
        return out
    
    def _navigate_up(self) -> None:
        """Navigate up in current selection."""
        if self.selected_shader:
            # Navigate shader list
            try:
                cat_enum = RegistryCategory[self.selected_category] if self.selected_category else RegistryCategory.CORE
                shaders = shaders_by_category.get(cat_enum, [])
            except KeyError:
                shaders = []
            if shaders:
                idx = shaders.index(self.selected_shader) if self.selected_shader in shaders else 0
                idx = max(0, idx - 1)
                self.selected_shader = shaders[idx]
        elif self.selected_category:
            # Navigate category list
            categories = list(RegistryCategory)
            if categories:
                try:
                    current_cat = RegistryCategory[self.selected_category]
                    idx = categories.index(current_cat)
                except (KeyError, ValueError):
                    idx = 0
                idx = max(0, idx - 1)
                self.selected_category = categories[idx].value.upper()
                # Select first shader in new category
                shaders = shaders_by_category.get(categories[idx], [])
                self.selected_shader = shaders[0] if shaders else None
    
    def _navigate_down(self) -> None:
        """Navigate down in current selection."""
        if self.selected_shader:
            try:
                cat_enum = RegistryCategory[self.selected_category] if self.selected_category else RegistryCategory.CORE
                shaders = shaders_by_category.get(cat_enum, [])
            except KeyError:
                shaders = []
            if shaders:
                idx = shaders.index(self.selected_shader) if self.selected_shader in shaders else 0
                idx = min(len(shaders) - 1, idx + 1)
                self.selected_shader = shaders[idx]
        elif self.selected_category:
            categories = list(RegistryCategory)
            if categories:
                try:
                    current_cat = RegistryCategory[self.selected_category]
                    idx = categories.index(current_cat)
                except (KeyError, ValueError):
                    idx = 0
                idx = min(len(categories) - 1, idx + 1)
                self.selected_category = categories[idx].value.upper()
                shaders = shaders_by_category.get(categories[idx], [])
                self.selected_shader = shaders[0] if shaders else None
    
    def _navigate_left(self) -> None:
        """Navigate to category selection."""
        if self.selected_shader:
            self.selected_shader = None
    
    def _navigate_right(self) -> None:
        """Navigate to shader selection."""
        if self.selected_category and not self.selected_shader:
            try:
                cat_enum = RegistryCategory[self.selected_category]
                shaders = shaders_by_category.get(cat_enum, [])
            except KeyError:
                shaders = []
            self.selected_shader = shaders[0] if shaders else None
    
    def _toggle_selected_shader(self) -> None:
        """Toggle selected shader on/off."""
        if self.selected_shader:
            self.shader_enabled[self.selected_shader] = not self.shader_enabled.get(self.selected_shader, False)
            self._update_preview_pipeline()
    
    def _adjust_parameter(self, delta: float) -> None:
        """Adjust current shader parameter."""
        if not self.selected_shader:
            return
        
        # Get first float parameter to adjust
        uniforms = self.shader_uniforms.get(self.selected_shader, {})
        for key, value in uniforms.items():
            if isinstance(value, (int, float)):
                uniforms[key] = max(0.0, min(10.0, value + delta))
                self._update_preview_pipeline()
                break
    
    def _update_preview_pipeline(self) -> None:
        """Update preview pipeline with enabled shaders."""
        self.preview_pipeline.clear()
        
        # Add enabled shaders to pipeline
        for shader_name, enabled in self.shader_enabled.items():
            if enabled:
                shader_info = get_utility_shader(shader_name)
                if shader_info:
                    _, _, category = shader_info
                    # Create a simple pass function
                    def make_pass_fn(name: str):
                        def pass_fn(surface, dt, context):
                            # In real implementation, this would use moderngl
                            return surface
                        return pass_fn
                    
                    # For now, just mark as enabled
                    # Full implementation would create actual shader programs
                    pass
    
    def update(self, dt: float, game_state: "GameState", ctx: dict) -> None:
        """Update scene state."""
        self.time += dt
        self.demo_time += dt
        
        # Update demo animations
        self._update_demo_animations(dt)
    
    def _update_demo_animations(self, dt: float) -> None:
        """Update demo animations based on selected category."""
        if not self.selected_category:
            return
        
        # Update time-based uniforms
        for shader_name in self.shader_enabled:
            if self.shader_enabled[shader_name]:
                uniforms = self.shader_uniforms.get(shader_name, {})
                if "u_Time" in uniforms:
                    uniforms["u_Time"] = self.demo_time
        
        # Category-specific animations
        if self.selected_category == ShaderCategory.COMBAT:
            # Trigger shockwave every few seconds
            if self.demo_time - self.last_shockwave_trigger > 3.0:
                get_shockwave_manager().trigger(0.5, 0.5, 1.0)
                self.last_shockwave_trigger = self.demo_time
        
        elif self.selected_category == ShaderCategory.WATER:
            # Trigger ripple every few seconds
            if self.demo_time - self.last_ripple_trigger > 2.5:
                self.last_ripple_trigger = self.demo_time
                # Update water_ripple center if enabled
                if "water_ripple" in self.shader_enabled and self.shader_enabled["water_ripple"]:
                    uniforms = self.shader_uniforms.get("water_ripple", {})
                    uniforms["u_Center"] = (0.3 + (self.demo_time * 0.1) % 0.4, 0.3 + (self.demo_time * 0.15) % 0.4)
        
        elif self.selected_category == ShaderCategory.LIGHTING:
            # Rotate light source
            light_mgr = get_light_manager()
            if light_mgr.lights:
                angle = self.demo_time * 0.5
                light_mgr.lights[0].pos = (0.5 + math.cos(angle) * 0.3, 0.5 + math.sin(angle) * 0.3)
    
    def handle_input_transition(self, events, game_state: "GameState", ctx: dict) -> SceneTransition:
        """Handle input and return transition."""
        result = self.handle_input(events, game_state, ctx)
        if result.get("pop"):
            return SceneTransition.pop()
        return SceneTransition.none()
    
    def update_transition(self, dt: float, game_state: "GameState", ctx: dict) -> SceneTransition:
        """Update scene and return transition."""
        self.update(dt, game_state, ctx)
        return SceneTransition.none()
    
    def render(self, render_ctx: RenderContext, game_state: "GameState", ctx: dict) -> None:
        """Render shader settings screen."""
        screen = render_ctx.screen
        width, height = render_ctx.width, render_ctx.height
        
        # Clear screen
        screen.fill((20, 20, 30))
        
        # Layout: Left panel (categories), Middle (shaders), Right (preview), Bottom (params)
        panel_width = width // 4
        preview_width = width // 2
        param_height = height // 3
        
        # Draw category list (left)
        self._render_category_list(screen, 0, 0, panel_width, height - param_height, render_ctx)
        
        # Draw shader list (middle-left)
        self._render_shader_list(screen, panel_width, 0, panel_width, height - param_height, render_ctx)
        
        # Draw preview (right)
        self._render_preview(screen, panel_width * 2, 0, preview_width, height - param_height, render_ctx)
        
        # Draw parameters (bottom)
        self._render_parameters(screen, 0, height - param_height, width, param_height, render_ctx)
        
        # Draw debug overlay if enabled
        if self.debug_overlay_enabled:
            self._render_debug_overlay(screen, render_ctx)
    
    def _render_category_list(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, render_ctx: RenderContext) -> None:
        """Render category list."""
        pygame.draw.rect(screen, (30, 30, 40), (x, y, w, h))
        pygame.draw.rect(screen, (60, 60, 80), (x, y, w, h), 2)
        
        categories = list(RegistryCategory)
        font = render_ctx.font
        start_y = y + 20
        
        for i, cat in enumerate(categories):
            cat_name = cat.value.upper()
            color = (255, 255, 255) if cat_name == self.selected_category else (180, 180, 180)
            if cat_name == self.selected_category:
                pygame.draw.rect(screen, (60, 60, 100), (x + 5, start_y + i * 30 - 2, w - 10, 26))
            
            text = font.render(cat_name, True, color)
            screen.blit(text, (x + 10, start_y + i * 30))
    
    def _render_shader_list(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, render_ctx: RenderContext) -> None:
        """Render shader list for selected category."""
        pygame.draw.rect(screen, (30, 30, 40), (x, y, w, h))
        pygame.draw.rect(screen, (60, 60, 80), (x, y, w, h), 2)
        
        if not self.selected_category:
            text = render_ctx.font.render("Select a category", True, (150, 150, 150))
            screen.blit(text, (x + 10, y + 20))
            return
        
        # Find category enum from string
        try:
            cat_enum = RegistryCategory[self.selected_category]
            shaders = shaders_by_category.get(cat_enum, [])
        except KeyError:
            shaders = []
        
        font = render_ctx.font
        start_y = y + 20
        
        for i, shader_name in enumerate(shaders):
            enabled = self.shader_enabled.get(shader_name, False)
            color = (100, 255, 100) if enabled else (255, 100, 100)
            if shader_name == self.selected_shader:
                pygame.draw.rect(screen, (60, 60, 100), (x + 5, start_y + i * 30 - 2, w - 10, 26))
                color = (255, 255, 100)
            
            status = "[ON]" if enabled else "[OFF]"
            text = font.render(f"{status} {shader_name}", True, color)
            screen.blit(text, (x + 10, start_y + i * 30))
    
    def _render_preview(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, render_ctx: RenderContext) -> None:
        """Render shader preview."""
        pygame.draw.rect(screen, (15, 15, 25), (x, y, w, h))
        pygame.draw.rect(screen, (60, 60, 80), (x, y, w, h), 2)
        
        # Create or update preview surface
        if self.preview_surface is None or self.preview_surface.get_size() != (w - 20, h - 40):
            self.preview_surface = pygame.Surface((w - 20, h - 40))
        
        # Render demo scene
        self._render_demo_scene(self.preview_surface)
        
        # Apply shader pipeline (placeholder - would use actual GPU shaders)
        # For now, just blit the demo scene
        screen.blit(pygame.transform.scale(self.preview_surface, (w - 20, h - 40)), (x + 10, y + 30))
        
        # Draw title
        title = render_ctx.font.render("Preview", True, (200, 200, 200))
        screen.blit(title, (x + 10, y + 5))
    
    def _render_demo_scene(self, surface: pygame.Surface) -> None:
        """Render a simple demo scene for preview."""
        w, h = surface.get_size()
        surface.fill((40, 50, 60))
        
        # Draw background pattern
        for i in range(0, w, 20):
            pygame.draw.line(surface, (60, 70, 80), (i, 0), (i, h), 1)
        for i in range(0, h, 20):
            pygame.draw.line(surface, (60, 70, 80), (0, i), (w, i), 1)
        
        # Draw sample sprite (circle)
        center_x, center_y = w // 2, h // 2
        pygame.draw.circle(surface, (255, 200, 100), (center_x, center_y), 30)
        pygame.draw.circle(surface, (255, 150, 50), (center_x, center_y), 20)
        
        # Draw moving elements based on category
        if self.selected_category == ShaderCategory.RETRO:
            # Scrolling background
            offset = int(self.demo_time * 10) % 40
            for i in range(-40, w + 40, 40):
                pygame.draw.rect(surface, (100, 150, 200), (i + offset, h // 3, 20, 20))
    
    def _render_parameters(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, render_ctx: RenderContext) -> None:
        """Render shader parameters."""
        pygame.draw.rect(screen, (25, 25, 35), (x, y, w, h))
        pygame.draw.rect(screen, (60, 60, 80), (x, y, w, h), 2)
        
        if not self.selected_shader:
            text = render_ctx.font.render("Select a shader to adjust parameters", True, (150, 150, 150))
            screen.blit(text, (x + 10, y + 10))
            return
        
        # Render parameter controls
        uniforms = self.shader_uniforms.get(self.selected_shader, {})
        font = render_ctx.small_font
        start_y = y + 10
        
        for i, (key, value) in enumerate(uniforms.items()):
            if isinstance(value, (int, float)):
                text = font.render(f"{key}: {value:.2f} (+/- to adjust)", True, (200, 200, 200))
                screen.blit(text, (x + 10, start_y + i * 25))
            elif isinstance(value, tuple) and len(value) == 2:
                text = font.render(f"{key}: ({value[0]:.2f}, {value[1]:.2f})", True, (200, 200, 200))
                screen.blit(text, (x + 10, start_y + i * 25))
            elif isinstance(value, tuple) and len(value) == 3:
                text = font.render(f"{key}: ({value[0]:.2f}, {value[1]:.2f}, {value[2]:.2f})", True, (200, 200, 200))
                screen.blit(text, (x + 10, start_y + i * 25))
    
    def _render_debug_overlay(self, screen: pygame.Surface, render_ctx: RenderContext) -> None:
        """Render debug overlay showing active shaders and uniforms."""
        font = render_ctx.small_font
        y = 10
        
        # Show active shaders
        active = [name for name, enabled in self.shader_enabled.items() if enabled]
        text = font.render(f"Active shaders: {', '.join(active) if active else 'None'}", True, (255, 255, 0))
        screen.blit(text, (10, y))
        y += 25
        
        # Show selected shader uniforms
        if self.selected_shader:
            uniforms = self.shader_uniforms.get(self.selected_shader, {})
            for key, value in list(uniforms.items())[:5]:  # Show first 5
                text = font.render(f"{key} = {value}", True, (200, 200, 200))
                screen.blit(text, (10, y))
                y += 20
    
    def _save_settings(self) -> None:
        """Save shader settings to config file."""
        settings = {
            "enabled": self.shader_enabled,
            "uniforms": self.shader_uniforms,
        }
        
        config_path = Path("config/shaders.json")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, "w") as f:
                json.dump(settings, f, indent=2)
            print(f"[ShaderSettings] Saved settings to {config_path}")
        except Exception as e:
            print(f"[ShaderSettings] Failed to save: {e}")
    
    def _load_settings(self) -> None:
        """Load shader settings from config file."""
        config_path = Path("config/shaders.json")
        
        if not config_path.exists():
            # Already initialized with defaults in __init__
            return
        
        try:
            with open(config_path, "r") as f:
                settings = json.load(f)
            
            # Load enabled flags
            saved_enabled = settings.get("enabled", {})
            self.shader_enabled.update(saved_enabled)
            
            # Load uniforms, merging with registry defaults
            saved_uniforms = settings.get("uniforms", {})
            for shader_name, saved_values in saved_uniforms.items():
                spec = get_shader_spec(shader_name)
                if spec:
                    # Start with registry defaults, then apply saved values
                    self.shader_uniforms[shader_name] = spec.default_uniforms.copy()
                    self.shader_uniforms[shader_name].update(saved_values)
                else:
                    # Unknown shader, use saved values as-is
                    self.shader_uniforms[shader_name] = saved_values
            
            print(f"[ShaderSettings] Loaded settings from {config_path}")
        except Exception as e:
            print(f"[ShaderSettings] Failed to load: {e}")
            # Keep defaults already set in __init__
    
    def on_enter(self, game_state: "GameState", ctx: dict) -> None:
        """Called when scene is entered."""
        if not HAS_MODERNGL:
            import logging
            logger = logging.getLogger(__name__)
            logger.info("Shader settings unavailable: moderngl not installed")
            return
        
        if not self.selected_category:
            categories = list(RegistryCategory)
            if categories:
                self.selected_category = categories[0].value.upper()
                shaders = shaders_by_category.get(categories[0], [])
                self.selected_shader = shaders[0] if shaders else None
    
    def on_exit(self, game_state: "GameState", ctx: dict) -> None:
        """Called when scene is exited."""
        self._save_settings()
