"""ShaderTestScene: Fullscreen quad with test texture and shader pipeline testing."""
from __future__ import annotations

import math
import time
from typing import TYPE_CHECKING

import pygame

from rendering import draw_centered_text
from scenes.transitions import SceneTransition, KIND_POP
from shader_effects.pipeline import ShaderPipelineManager, ShaderCategory
from shader_effects import (
    BloomEffect,
    VignetteEffect,
    ChromaticAberrationEffect,
    PixelateEffect,
    ShockwaveEffect,
    DistortionEffect,
    ColorGradingEffect,
    BarrelDistortionEffect,
    VHSNoiseEffect,
    HeatDistortionEffect,
    MotionTrailEffect,
    PulseGlowEffect,
)

if TYPE_CHECKING:
    from state import GameState

try:
    from gpu_gl_utils import get_gl_context, get_fullscreen_quad, HAS_MODERNGL
except ImportError:
    HAS_MODERNGL = False
    get_gl_context = None  # type: ignore[assignment]
    get_fullscreen_quad = None  # type: ignore[assignment]

# State id used when this scene is active
SHADER_TEST_STATE_ID = "SHADER_TEST"


def _create_test_texture(width: int, height: int) -> pygame.Surface:
    """Create a simple test texture with patterns for shader testing."""
    surf = pygame.Surface((width, height))
    surf.fill((30, 30, 45))
    
    # Draw a grid pattern
    grid_size = 50
    for y in range(0, height, grid_size):
        pygame.draw.line(surf, (80, 80, 100), (0, y), (width, y), 1)
    for x in range(0, width, grid_size):
        pygame.draw.line(surf, (80, 80, 100), (x, 0), (x, height), 1)
    
    # Draw colored circles
    center_x, center_y = width // 2, height // 2
    for i, (r, color) in enumerate([(100, (255, 100, 100)), (80, (100, 255, 100)), (60, (100, 100, 255))]):
        pygame.draw.circle(surf, color, (center_x, center_y), r, 3)
        angle = (i * 2 * math.pi / 3) + (time.perf_counter() * 0.5)
        px = int(center_x + math.cos(angle) * 150)
        py = int(center_y + math.sin(angle) * 150)
        pygame.draw.circle(surf, color, (px, py), 30)
    
    # Draw text
    try:
        font = pygame.font.Font(None, 36)
        text = font.render("SHADER TEST", True, (255, 255, 255))
        surf.blit(text, (width // 2 - text.get_width() // 2, 50))
    except:
        pass
    
    return surf


class ShaderTestScene:
    """
    Shader test scene with fullscreen quad, test texture, and interactive shader controls.
    
    Controls:
    - LEFT/RIGHT: Cycle through available shaders
    - UP/DOWN: Toggle current shader on/off
    - +/-: Adjust primary intensity parameter
    - SPACE: Trigger shader events (shockwave, ripple, time warp)
    - ESC: Exit back to main menu
    """

    def __init__(self) -> None:
        self._logged = False
        self.time = 0.0
        self.gl = get_gl_context() if (get_gl_context is not None and HAS_MODERNGL) else None
        self.quad = None
        self.offscreen_surface = None
        self.test_texture = None
        
        # Isolated mini-pipeline for shader testing
        self.pipeline = ShaderPipelineManager()
        self._initialize_shaders()
        
        # Current shader index and state
        self.current_shader_index = 0
        self.intensity = 1.0
        self.shockwave_time = -1.0  # -1 means inactive
        
        # Available shaders (name, category, factory function)
        # Note: factory functions are closures that capture self for dynamic parameter updates
        self.shader_list = [
            ("pixelate", ShaderCategory.EARLY, self._make_pixelate),
            ("bloom", ShaderCategory.MID, self._make_bloom),
            ("distortion", ShaderCategory.MID, self._make_distortion),
            ("shockwave", ShaderCategory.MID, self._make_shockwave),
            ("chromatic_aberration", ShaderCategory.MID, self._make_chromatic_aberration),
            ("barrel_distortion", ShaderCategory.MID, self._make_barrel_distortion),
            ("heat_distortion", ShaderCategory.MID, self._make_heat_distortion),
            ("color_grading", ShaderCategory.LATE, self._make_color_grading),
            ("vignette", ShaderCategory.LAST, self._make_vignette),
            ("vhs_noise", ShaderCategory.LATE, self._make_vhs_noise),
            ("motion_trail", ShaderCategory.MID, self._make_motion_trail),
            ("pulse_glow", ShaderCategory.LATE, self._make_pulse_glow),
        ]
    
    def _make_pixelate(self) -> PixelateEffect:
        # PixelateEffect uses pixel_scale parameter
        return PixelateEffect(pixel_scale=max(1, int(4 * self.intensity)), blend_amount=0.7)
    
    def _make_bloom(self) -> BloomEffect:
        return BloomEffect(intensity=0.4 * self.intensity, threshold=210, blur_size=2)
    
    def _make_distortion(self) -> DistortionEffect:
        return DistortionEffect(intensity=1.5 * self.intensity, scale=0.02, speed=2.0)
    
    def _make_shockwave(self) -> ShockwaveEffect:
        radius = max(10.0, self.shockwave_time * 200.0) if self.shockwave_time >= 0 else 80.0
        return ShockwaveEffect(
            origin=(0.5, 0.5),
            radius=radius,
            amplitude=4.0 * self.intensity,
            falloff=0.03,
        )
    
    def _make_chromatic_aberration(self) -> ChromaticAberrationEffect:
        return ChromaticAberrationEffect(shift_strength=0.3 * self.intensity, direction="radial")
    
    def _make_barrel_distortion(self) -> BarrelDistortionEffect:
        return BarrelDistortionEffect(curvature_strength=0.04 * self.intensity, edge_softness=0.12)
    
    def _make_heat_distortion(self) -> HeatDistortionEffect:
        return HeatDistortionEffect(intensity=2.0 * self.intensity, wave_scale=0.025, speed=4.0)
    
    def _make_color_grading(self) -> ColorGradingEffect:
        return ColorGradingEffect(mode="neon", strength=0.2 * self.intensity)
    
    def _make_vignette(self) -> VignetteEffect:
        return VignetteEffect(radius=0.78, softness=0.22, intensity=0.4 * self.intensity, color=(0, 0, 0))
    
    def _make_vhs_noise(self) -> VHSNoiseEffect:
        return VHSNoiseEffect(jitter_strength=max(1, int(self.intensity)), noise_strength=max(1, int(6 * self.intensity)), roll_speed=0.3)
    
    def _make_motion_trail(self) -> MotionTrailEffect:
        return MotionTrailEffect(history_blend=0.8 + 0.1 * self.intensity, fade_speed=0.9)
    
    def _make_pulse_glow(self) -> PulseGlowEffect:
        return PulseGlowEffect(period=2.5, min_intensity=0.97, max_intensity=1.0 + 0.06 * self.intensity, tint_color=(100, 150, 255))
        
        # Add first shader by default
        if self.shader_list:
            self._add_current_shader()
    
    def _initialize_shaders(self) -> None:
        """Initialize the shader pipeline with available effects."""
        pass  # Shaders are added dynamically
    
    def _add_current_shader(self) -> None:
        """Add the current shader to the pipeline."""
        if not self.shader_list:
            return
        name, category, factory = self.shader_list[self.current_shader_index]
        try:
            effect = factory()
            self.pipeline.add_shader(
                name=name,
                category=category,
                pass_fn=effect.apply,
                default_uniforms={"intensity": self.intensity},
            )
            self._log_shader_change(f"Added shader: {name}")
        except Exception as e:
            print(f"[ShaderTest] Failed to add shader {name}: {e}")
    
    def _remove_current_shader(self) -> None:
        """Remove the current shader from the pipeline."""
        if not self.shader_list:
            return
        name, _, _ = self.shader_list[self.current_shader_index]
        if self.pipeline.remove_shader(name):
            self._log_shader_change(f"Removed shader: {name}")
    
    def _update_current_shader(self) -> None:
        """Update the current shader with new intensity."""
        if not self.shader_list:
            return
        name, category, factory = self.shader_list[self.current_shader_index]
        # Remove and re-add with new parameters
        self.pipeline.remove_shader(name)
        try:
            effect = factory()
            self.pipeline.add_shader(
                name=name,
                category=category,
                pass_fn=effect.apply,
                default_uniforms={"intensity": self.intensity},
            )
            self._log_shader_change(f"Updated shader: {name} (intensity={self.intensity:.2f})")
        except Exception as e:
            print(f"[ShaderTest] Failed to update shader {name}: {e}")
    
    def _log_shader_change(self, message: str) -> None:
        """Log shader and uniform changes."""
        print(f"[ShaderTest] {message}")
        enabled = self.pipeline.get_enabled_shaders()
        if enabled:
            print(f"[ShaderTest] Active shaders: {', '.join(enabled)}")
        else:
            print(f"[ShaderTest] No active shaders")
    
    def state_id(self) -> str:
        return SHADER_TEST_STATE_ID

    def handle_input(self, events, game_state: "GameState", ctx: dict) -> dict:
        out = {"screen": None, "quit": False, "restart": False, "restart_to_wave1": False, "replay": False, "pop": False}
        for e in events:
            if getattr(e, "type", None) == pygame.KEYDOWN:
                key = getattr(e, "key", None)
                if key == pygame.K_ESCAPE:
                    out["pop"] = True
                    break
                elif key == pygame.K_LEFT:
                    # Cycle to previous shader
                    if self.shader_list:
                        self._remove_current_shader()
                        self.current_shader_index = (self.current_shader_index - 1) % len(self.shader_list)
                        self._add_current_shader()
                elif key == pygame.K_RIGHT:
                    # Cycle to next shader
                    if self.shader_list:
                        self._remove_current_shader()
                        self.current_shader_index = (self.current_shader_index + 1) % len(self.shader_list)
                        self._add_current_shader()
                elif key == pygame.K_UP:
                    # Enable current shader
                    if self.shader_list:
                        name, _, _ = self.shader_list[self.current_shader_index]
                        if self.pipeline.enable_shader(name):
                            self._log_shader_change(f"Enabled shader: {name}")
                        else:
                            # Shader not in pipeline, add it
                            self._add_current_shader()
                elif key == pygame.K_DOWN:
                    # Disable current shader
                    if self.shader_list:
                        name, _, _ = self.shader_list[self.current_shader_index]
                        if self.pipeline.disable_shader(name):
                            self._log_shader_change(f"Disabled shader: {name}")
                elif key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    # Increase intensity
                    self.intensity = min(2.0, self.intensity + 0.1)
                    self._update_current_shader()
                elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    # Decrease intensity
                    self.intensity = max(0.1, self.intensity - 0.1)
                    self._update_current_shader()
                elif key == pygame.K_SPACE:
                    # Trigger shader events
                    self.shockwave_time = 0.0
                    self._log_shader_change("Triggered shockwave event")
        return out

    def update(self, dt: float, game_state: "GameState", ctx: dict) -> None:
        self.time += dt
        # Update shockwave radius (decay over time)
        shockwave_was_active = self.shockwave_time >= 0
        if self.shockwave_time >= 0:
            self.shockwave_time += dt * 2.0
            if self.shockwave_time > 1.0:
                self.shockwave_time = -1.0  # Reset
            # Update shockwave shader if it's the current one
            if self.shader_list and self.shader_list[self.current_shader_index][0] == "shockwave":
                self._update_current_shader()
            elif "shockwave" in self.pipeline._shader_map:
                # Update shockwave even if not current (it's in the pipeline)
                name, category, factory = [s for s in self.shader_list if s[0] == "shockwave"][0]
                self.pipeline.remove_shader("shockwave")
                try:
                    effect = factory()
                    self.pipeline.add_shader(name=name, category=category, pass_fn=effect.apply, default_uniforms={"intensity": self.intensity})
                except Exception:
                    pass

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

    def render(self, render_ctx, game_state: "GameState", ctx: dict) -> None:
        target_size = (render_ctx.width, render_ctx.height)
        
        # Create or update test texture
        if self.test_texture is None or self.test_texture.get_size() != target_size:
            self.test_texture = _create_test_texture(render_ctx.width, render_ctx.height)
        
        # Create offscreen surface for shader processing
        if self.offscreen_surface is None or self.offscreen_surface.get_size() != target_size:
            self.offscreen_surface = pygame.Surface(target_size)
        
        # Copy test texture to offscreen
        self.offscreen_surface.blit(self.test_texture, (0, 0))
        
        # Apply shader pipeline
        processed_surface = self.pipeline.execute_pipeline(
            self.offscreen_surface,
            dt=0.016,
            context={"time": self.time},
        )
        
        # Render to screen (with or without moderngl)
        quad = get_fullscreen_quad(target_size) if get_fullscreen_quad is not None else None
        if self.gl is not None and quad is not None:
            try:
                tex_bytes = pygame.image.tostring(processed_surface, "RGBA", False)
            except AttributeError:
                tex_bytes = bytes(processed_surface.get_view("0"))
            quad.texture.write(tex_bytes)
            quad.program["u_effect"] = 0
            quad.program["u_time"] = self.time
            quad.texture.use(0)
            quad.program["u_frame_texture"] = 0
            self.gl.viewport = (0, 0, render_ctx.width, render_ctx.height)
            self.gl.clear(0.15, 0.15, 0.2, 1.0)
            quad.render()
        else:
            # Fallback: blit directly to screen
            render_ctx.screen.blit(processed_surface, (0, 0))
        
        # Draw UI overlay with controls and current shader info
        if self.shader_list:
            name, category, _ = self.shader_list[self.current_shader_index]
            enabled = name in self.pipeline.get_enabled_shaders()
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface((render_ctx.width, 200), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            render_ctx.screen.blit(overlay, (0, 0))
            
            # Draw current shader info
            status_color = (100, 255, 100) if enabled else (255, 100, 100)
            status_text = "ENABLED" if enabled else "DISABLED"
            draw_centered_text(
                render_ctx.screen,
                render_ctx.font,
                render_ctx.big_font,
                render_ctx.width,
                f"Shader: {name.upper()} [{status_text}]",
                20,
                color=status_color,
                use_big=False,
            )
            draw_centered_text(
                render_ctx.screen,
                render_ctx.font,
                render_ctx.big_font,
                render_ctx.width,
                f"Intensity: {self.intensity:.2f}",
                50,
                color=(220, 220, 220),
                use_big=False,
            )
            draw_centered_text(
                render_ctx.screen,
                render_ctx.font,
                render_ctx.small_font,
                render_ctx.width,
                "LEFT/RIGHT: Cycle | UP/DOWN: Toggle | +/-: Intensity | SPACE: Event | ESC: Exit",
                80,
                color=(180, 180, 180),
            )
            draw_centered_text(
                render_ctx.screen,
                render_ctx.font,
                render_ctx.small_font,
                render_ctx.width,
                f"Active: {len(self.pipeline.get_enabled_shaders())}/{len(self.shader_list)}",
                110,
                color=(160, 160, 160),
            )

    def on_enter(self, game_state: "GameState", ctx: dict) -> None:
        """Called when scene is entered."""
        print("[ShaderTest] Entered shader test scene")
        if self.shader_list:
            name, _, _ = self.shader_list[self.current_shader_index]
            print(f"[ShaderTest] Current shader: {name}")

    def on_exit(self, game_state: "GameState", ctx: dict) -> None:
        """Called when scene is exited."""
        print("[ShaderTest] Exited shader test scene")
