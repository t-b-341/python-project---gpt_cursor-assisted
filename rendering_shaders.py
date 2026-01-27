"""Optional shader-based gameplay rendering wrapper. Renders to offscreen then blit; ready for future GPU pass."""
from __future__ import annotations

import logging
import time
import pygame

from rendering import RenderContext
from visual_effects import apply_gameplay_effects, apply_gameplay_final_blit
from shader_effects import get_gameplay_shader_stack
from shader_effects.pipeline import ShaderPipelineManager
from shader_effects.context import ShaderContext

try:
    from gpu_gl_utils import get_gl_context, get_fullscreen_quad, gpu_upscale_surface, HAS_MODERNGL
except ImportError:
    HAS_MODERNGL = False
    get_gl_context = None  # type: ignore[assignment]
    get_fullscreen_quad = None  # type: ignore[assignment]
    gpu_upscale_surface = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

# Global shader pipeline (initialized on first use)
_shader_pipeline: ShaderPipelineManager | None = None

# Log rendering path on first import
_rendering_path_logged = False

def _log_rendering_path(config) -> None:
    """Log which rendering path is being used."""
    global _rendering_path_logged
    if _rendering_path_logged:
        return
    
    use_gpu_pipeline = (
        config is not None
        and getattr(config, "use_gpu_shader_pipeline", False)
        and HAS_MODERNGL
    )
    
    if use_gpu_pipeline and HAS_MODERNGL:
        logger.info("Using GPU shader pipeline")
    else:
        logger.info("Using CPU visual effects pipeline")
    
    _rendering_path_logged = True

_gl_start_time = time.perf_counter()

# FBO for readback (gameplay renders to this, then reads pixels to blit to pygame)
_gl_fbo = None
_gl_size: tuple[int, int] | None = None


def _gl_postprocess_offscreen_surface(offscreen_surface, render_ctx, ctx, game_state=None) -> bool:
    if not HAS_MODERNGL or get_fullscreen_quad is None or get_gl_context is None:
        return False
    try:
        width, height = offscreen_surface.get_size()
        size = (width, height)
        quad = get_fullscreen_quad(size)
        if quad is None:
            return False
        gl_ctx = get_gl_context()
        if gl_ctx is None:
            return False

        global _gl_fbo, _gl_size
        if _gl_fbo is None or _gl_size != size:
            if _gl_fbo is not None:
                try:
                    _gl_fbo.release()
                except Exception:
                    pass
                _gl_fbo = None
            try:
                out_tex = gl_ctx.texture(size, 4)
                _gl_fbo = gl_ctx.framebuffer(color_attachments=[out_tex])
                _gl_size = size
            except Exception:
                _gl_size = None
                return False

        try:
            tex_bytes = pygame.image.tostring(offscreen_surface, "RGBA", False)
        except AttributeError:
            tex_bytes = bytes(offscreen_surface.get_view("0"))
        quad.texture.write(tex_bytes)
        quad.program["u_effect"] = 1
        now = time.perf_counter()
        elapsed = float(now - _gl_start_time)
        quad.program["u_time"] = elapsed
        quad.texture.use(0)
        quad.program["u_frame_texture"] = 0
        _gl_fbo.use()
        gl_ctx.viewport = (0, 0, width, height)
        _gl_fbo.clear(0.0, 0.0, 0.0, 1.0)
        quad.render()
        data = _gl_fbo.read(components=4)
        out_surf = pygame.image.frombuffer(data, (width, height), "RGBA")
        out_surf = pygame.transform.flip(out_surf, False, True)
        # Optional damage wobble on final blit (when enable_damage_wobble and timer > 0)
        apply_gameplay_final_blit(out_surf, render_ctx.screen, ctx, game_state)
        return True
    except Exception:
        return False


_offscreen_surface = None
_offscreen_size: tuple[int, int] | None = None


def _get_offscreen_surface(render_ctx: RenderContext, size: tuple[int, int] | None = None) -> pygame.Surface:
    """Return a surface of the given size or render_ctx size; (re)create if size changed.
    When config.internal_resolution_scale < 1, pass a smaller size for CPU-based effects."""
    global _offscreen_surface, _offscreen_size
    if size is None:
        size = (render_ctx.width, render_ctx.height)
    if _offscreen_surface is None or _offscreen_size != size:
        _offscreen_surface = pygame.Surface(size).convert_alpha()
        _offscreen_surface.fill((0, 0, 0, 255))
        _offscreen_size = size
    return _offscreen_surface


def _render_gameplay_frame(render_ctx, game_state, ctx) -> None:
    """Invoke the normal gameplay renderer into the given render_ctx (caller may pass temp ctx with offscreen screen)."""
    from screens import gameplay as gameplay_screen

    gameplay_ctx = ctx.get("gameplay_ctx") if isinstance(ctx, dict) else getattr(ctx, "gameplay_ctx", None)
    if gameplay_ctx is not None:
        gameplay_screen.render(render_ctx, game_state, gameplay_ctx)


def render_gameplay_frame_to_surface(surface, width, height, font, big_font, small_font, game_state, ctx) -> None:
    """Render the raw gameplay frame into the given surface. No shaders or effects. Used for pause backdrop."""
    temp_ctx = RenderContext(
        screen=surface,
        width=width,
        height=height,
        font=font,
        big_font=big_font,
        small_font=small_font,
    )
    _render_gameplay_frame(temp_ctx, game_state, ctx)


def render_gameplay_with_optional_shaders(render_ctx, game_state, ctx) -> None:
    """
    Renders to an offscreen surface, then blits (or runs GL post-process) according to
    config.use_shaders / config.use_gpu_shaders and config.shader_profile.
    GPU path when (use_gpu_shaders or use_shaders) and profile "gl_basic".
    GPU shader pipeline when config.use_gpu_shader_pipeline is True.
    CPU effects can use config.internal_resolution_scale for a smaller offscreen, then scale up.
    """
    config = getattr(ctx, "config", None)
    if config is None and isinstance(ctx, dict):
        app_ctx = ctx.get("app_ctx")
        config = getattr(app_ctx, "config", None) if app_ctx else None
    use_shaders = bool(getattr(config, "use_shaders", False))
    use_gpu_shaders = bool(getattr(config, "use_gpu_shaders", False))
    profile = "none"
    if config is not None:
        profile = getattr(config, "shader_profile", "none")
    if profile not in ("none", "cpu_tint", "gl_basic"):
        profile = "none"
    if not use_shaders and not use_gpu_shaders:
        profile = "none"

    use_gl_path = profile == "gl_basic" and HAS_MODERNGL and (use_gpu_shaders or use_shaders)
    scale = 1.0
    if config is not None and not use_gl_path:
        scale = max(0.25, min(1.0, float(getattr(config, "internal_resolution_scale", 1.0))))
    offscreen_w = max(1, int(render_ctx.width * scale))
    offscreen_h = max(1, int(render_ctx.height * scale))
    offscreen_size = (offscreen_w, offscreen_h)

    offscreen_surface = _get_offscreen_surface(render_ctx, offscreen_size)
    temp_ctx = RenderContext(
        screen=offscreen_surface,
        width=offscreen_w,
        height=offscreen_h,
        font=render_ctx.font,
        big_font=render_ctx.big_font,
        small_font=render_ctx.small_font,
    )
    offscreen_surface.fill((0, 0, 0, 255))
    _render_gameplay_frame(temp_ctx, game_state, ctx)
    
    # Log rendering path once
    _log_rendering_path(config)

    # Config-based gameplay shader stack when enable_gameplay_shaders and gameplay_shader_profile != "none"
    # Run CPU effect chain at reduced resolution (default 0.5) to keep framerate up at full screen sizes.
    if config is not None and getattr(config, "enable_gameplay_shaders", False) and (not use_gpu_shaders or not use_gl_path):
        gameplay_stack = get_gameplay_shader_stack(config)
        if gameplay_stack:
            t = time.perf_counter() - _gl_start_time
            eff_ctx = {"time": t}
            effect_scale = max(0.25, min(1.0, float(getattr(config, "internal_resolution_scale", 1.0))))
            if effect_scale >= 0.99:
                effect_scale = 0.5  # default half-res for effect chain when at full res (avoids low fps)
            ew = max(1, int(offscreen_w * effect_scale))
            eh = max(1, int(offscreen_h * effect_scale))
            surf = pygame.transform.smoothscale(offscreen_surface, (ew, eh))
            for eff in gameplay_stack:
                surf = eff.apply(surf, 0.016, eff_ctx)
            # Prefer GPU upscale when available to keep resolution high without CPU cost
            if HAS_MODERNGL and (use_gpu_shaders or use_shaders) and gpu_upscale_surface is not None:
                scaled_back = gpu_upscale_surface(surf, (offscreen_w, offscreen_h))
            else:
                scaled_back = None
            if scaled_back is None:
                scaled_back = pygame.transform.smoothscale(surf, (offscreen_w, offscreen_h))
            offscreen_surface.blit(scaled_back, (0, 0))

    # GPU shader pipeline path (when use_gpu_shader_pipeline is enabled)
    use_gpu_pipeline = (
        config is not None
        and getattr(config, "use_gpu_shader_pipeline", False)
        and HAS_MODERNGL
    )
    
    if use_gpu_pipeline:
        global _shader_pipeline
        if _shader_pipeline is None:
            _shader_pipeline = ShaderPipelineManager()
            logger.info("Initialized GPU shader pipeline")
        
        # Build shader context
        t = time.perf_counter() - _gl_start_time
        shader_ctx: ShaderContext = {
            "time": t,
            "delta_time": 0.016,
        }
        if game_state is not None:
            max_hp = max(1, getattr(game_state, "player_max_hp", 100))
            current_hp = getattr(game_state, "player_hp", 100)
            shader_ctx["health"] = current_hp / max_hp
        
        # Execute GPU shader pipeline
        try:
            processed = _shader_pipeline.execute_pipeline(offscreen_surface, dt=0.016, context=shader_ctx)
            offscreen_surface = processed
        except Exception as e:
            logger.error(f"GPU shader pipeline failed: {e}", exc_info=True)
            # Fall through to CPU path
    
    # Lightweight CPU effects (vignette, scanlines) by gameplay_effect_profile when enable_gameplay_shaders
    # Only apply if NOT using GPU pipeline (avoid double-processing)
    if not use_gpu_pipeline:
        apply_gameplay_effects(offscreen_surface, ctx, game_state)

    if use_gl_path:
        ok = _gl_postprocess_offscreen_surface(offscreen_surface, render_ctx, ctx, game_state)
        if ok:
            return

    if profile == "cpu_tint" or (profile == "gl_basic" and (use_shaders or use_gpu_shaders)):
        overlay = pygame.Surface(offscreen_surface.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((80, 0, 120, 60))  # RGBA: mild purple tint, low alpha
        offscreen_surface.blit(overlay, (0, 0))

    # Scale up to screen size when we rendered at lower internal resolution (CPU path)
    if scale < 1.0:
        scaled = pygame.transform.smoothscale(offscreen_surface, (render_ctx.width, render_ctx.height))
        apply_gameplay_final_blit(scaled, render_ctx.screen, ctx, game_state)
    else:
        apply_gameplay_final_blit(offscreen_surface, render_ctx.screen, ctx, game_state)
