"""Shared moderngl helpers: context, fullscreen quad geometry, texture, and a basic program.
Used by ShaderTestScene and rendering_shaders for post-process.
"""
from __future__ import annotations

import struct
from pathlib import Path
from typing import Optional, Tuple, Dict

try:
    import moderngl  # type: ignore[import-untyped]
    HAS_MODERNGL = True
except ImportError:
    moderngl = None  # type: ignore[assignment]
    HAS_MODERNGL = False

_gl_ctx: Optional["moderngl.Context"] = None

# Utility shader registry: name -> (vertex_shader_source, fragment_shader_source)
_utility_shaders: Dict[str, Tuple[str, str]] = {}

# Fullscreen quad NDC pos+uv, triangle strip (same layout for all callers)
QUAD_POS_UV = struct.pack(
    "16f",
    -1.0, -1.0, 0.0, 0.0,
    1.0, -1.0, 1.0, 0.0,
    -1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0,
)

VERTEX_SHADER = """
#version 330
in vec2 in_pos;
in vec2 in_uv;
out vec2 v_uv;
void main() {
    gl_Position = vec4(in_pos, 0.0, 1.0);
    v_uv = in_uv;
}
"""

# u_effect: 0 = shader_test (desaturate), 1 = gameplay (contrast + pulse), 2 = passthrough/upscale
FRAGMENT_SHADER = """
#version 330
uniform sampler2D u_frame_texture;
uniform float u_time;
uniform int u_effect;
in vec2 v_uv;
out vec4 fragColor;
void main() {
    vec4 c = texture(u_frame_texture, v_uv);
    if (u_effect == 0) {
        float gray = dot(c.rgb, vec3(0.299, 0.587, 0.114));
        vec3 mixed = mix(c.rgb, vec3(gray), 0.3);
        fragColor = vec4(mixed, c.a);
    } else if (u_effect == 1) {
        vec2 centered = v_uv - 0.5;
        float dist = length(centered);
        float vignette = smoothstep(0.7, 0.3, dist);
        float pulse = 0.9 + 0.1 * sin(u_time * 2.0);
        vec3 base = c.rgb * pulse;
        vec3 final_rgb = base * vignette;
        fragColor = vec4(final_rgb, c.a);
    } else {
        fragColor = c;
    }
}
"""


def get_gl_context() -> Optional["moderngl.Context"]:
    global _gl_ctx
    if moderngl is None:
        return None
    if _gl_ctx is None:
        try:
            _gl_ctx = moderngl.create_context()
        except Exception:
            _gl_ctx = None
    return _gl_ctx


class FullscreenQuad:
    """Holds texture, VBO, VAO, and program for a fullscreen quad at a given size."""

    def __init__(self, ctx: "moderngl.Context", size: Tuple[int, int]) -> None:
        self.ctx = ctx
        self.size = size
        self.texture = ctx.texture(size, 4)
        self.vbo = ctx.buffer(QUAD_POS_UV)
        self.program = ctx.program(
            vertex_shader=VERTEX_SHADER,
            fragment_shader=FRAGMENT_SHADER,
        )
        self.vao = ctx.vertex_array(
            self.program,
            [(self.vbo, "2f 2f", "in_pos", "in_uv")],
        )

    def ensure_size(self, size: Tuple[int, int]) -> None:
        if size == self.size:
            return
        try:
            self.texture.release()
        except Exception:
            pass
        self.size = size
        self.texture = self.ctx.texture(size, 4)

    def render(self) -> None:
        if moderngl is not None:
            self.vao.render(moderngl.TRIANGLE_STRIP)


_quad_cache: dict[Tuple[int, int], "FullscreenQuad"] = {}
_upscale_fbo = None
_upscale_fbo_size: Optional[Tuple[int, int]] = None


def gpu_upscale_surface(surface: "object", target_size: Tuple[int, int]) -> Optional["object"]:
    """Upscale a pygame Surface to target_size on the GPU (bilinear). Returns new Surface or None on failure."""
    global _upscale_fbo, _upscale_fbo_size
    try:
        import pygame
    except ImportError:
        return None
    ctx = get_gl_context()
    if ctx is None:
        return None
    src_size = (surface.get_width(), surface.get_height())
    if src_size[0] < 1 or src_size[1] < 1 or target_size[0] < 1 or target_size[1] < 1:
        return None
    quad = get_fullscreen_quad(src_size)
    if quad is None:
        return None
    if _upscale_fbo is None or _upscale_fbo_size != target_size:
        if _upscale_fbo is not None:
            try:
                _upscale_fbo.release()
            except Exception:
                pass
            _upscale_fbo = None
        try:
            out_tex = ctx.texture(target_size, 4)
            _upscale_fbo = ctx.framebuffer(color_attachments=[out_tex])
            _upscale_fbo_size = target_size
        except Exception:
            _upscale_fbo_size = None
            return None
    try:
        tex_bytes = pygame.image.tostring(surface, "RGBA", False)
    except Exception:
        try:
            tex_bytes = bytes(surface.get_view("0"))
        except Exception:
            return None
    quad.texture.write(tex_bytes)
    quad.program["u_effect"] = 2
    quad.texture.use(0)
    quad.program["u_frame_texture"] = 0
    _upscale_fbo.use()
    ctx.viewport = (0, 0, target_size[0], target_size[1])
    _upscale_fbo.clear(0.0, 0.0, 0.0, 1.0)
    quad.render()
    data = _upscale_fbo.read(components=4)
    out_surf = pygame.image.frombuffer(data, target_size, "RGBA")
    out_surf = pygame.transform.flip(out_surf, False, True)
    return out_surf


def get_fullscreen_quad(size: Tuple[int, int]) -> Optional["FullscreenQuad"]:
    ctx = get_gl_context()
    if ctx is None:
        return None
    if size not in _quad_cache:
        _quad_cache[size] = FullscreenQuad(ctx, size)
    else:
        _quad_cache[size].ensure_size(size)
    return _quad_cache[size]


def load_shader_file(shader_path: str | Path) -> Optional[str]:
    """
    Load a shader file from disk.
    
    Args:
        shader_path: Path to the shader file (relative to project root or absolute)
    
    Returns:
        Shader source code as string, or None if file not found or error occurred
    """
    try:
        path = Path(shader_path)
        if not path.is_absolute():
            # Try relative to project root
            project_root = Path(__file__).resolve().parent
            path = project_root / path
        if not path.exists():
            # Try assets/shaders directory
            project_root = Path(__file__).resolve().parent
            assets_path = project_root / "assets" / "shaders" / Path(shader_path).name
            if assets_path.exists():
                path = assets_path
            else:
                print(f"[Shader] File not found: {shader_path}")
                return None
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[Shader] Error loading {shader_path}: {e}")
        return None


def register_utility_shader(name: str, vertex_shader: Optional[str] = None, fragment_shader: Optional[str] = None) -> bool:
    """
    Register a utility shader that can be used for post-processing.
    
    Args:
        name: Unique name for the shader (e.g., "blur")
        vertex_shader: Vertex shader source code (uses default if None)
        fragment_shader: Fragment shader source code or path to .frag file
    
    Returns:
        True if registration successful, False otherwise
    """
    if not HAS_MODERNGL:
        print(f"[Shader] Cannot register utility shader '{name}': moderngl not available")
        return False
    
    # Use default vertex shader if not provided
    vert_src = vertex_shader if vertex_shader is not None else VERTEX_SHADER
    
    # Load fragment shader from file if it looks like a path
    frag_src = fragment_shader
    if frag_src and (frag_src.endswith(".frag") or "/" in frag_src or "\\" in frag_src):
        loaded = load_shader_file(frag_src)
        if loaded is None:
            return False
        frag_src = loaded
    
    if frag_src is None:
        print(f"[Shader] Fragment shader required for utility shader '{name}'")
        return False
    
    _utility_shaders[name] = (vert_src, frag_src)
    print(f"[Shader] Registered utility shader: {name}")
    return True


def get_utility_shader(name: str) -> Optional[Tuple[str, str]]:
    """
    Get a registered utility shader by name.
    
    Args:
        name: Shader name (e.g., "blur")
    
    Returns:
        Tuple of (vertex_shader_source, fragment_shader_source) or None if not found
    """
    return _utility_shaders.get(name)


def create_utility_shader_program(ctx: "moderngl.Context", name: str) -> Optional["moderngl.Program"]:
    """
    Create a moderngl Program from a registered utility shader.
    
    Args:
        ctx: moderngl context
        name: Shader name (e.g., "blur")
    
    Returns:
        moderngl.Program or None if shader not found or creation failed
    """
    shader_sources = get_utility_shader(name)
    if shader_sources is None:
        print(f"[Shader] Utility shader '{name}' not found")
        return None
    
    vert_src, frag_src = shader_sources
    try:
        return ctx.program(vertex_shader=vert_src, fragment_shader=frag_src)
    except Exception as e:
        print(f"[Shader] Failed to create program for '{name}': {e}")
        return None


# Register built-in utility shaders on module load
def _register_builtin_utility_shaders() -> None:
    """Register built-in utility shaders."""
    if not HAS_MODERNGL:
        return
    
    # Core utility shaders
    register_utility_shader("blur", fragment_shader="assets/shaders/blur.frag")
    
    # Post-processing effects
    register_utility_shader("vignette", fragment_shader="assets/shaders/vignette.frag")
    register_utility_shader("pixelate", fragment_shader="assets/shaders/pixelate.frag")
    register_utility_shader("chromatic_aberration", fragment_shader="assets/shaders/chromatic_aberration.frag")
    register_utility_shader("distortion", fragment_shader="assets/shaders/distortion.frag")
    register_utility_shader("shockwave", fragment_shader="assets/shaders/shockwave.frag")
    register_utility_shader("screenshake", fragment_shader="assets/shaders/screenshake.frag")
    register_utility_shader("gradient_fog", fragment_shader="assets/shaders/gradient_fog.frag")
    register_utility_shader("film_grain", fragment_shader="assets/shaders/film_grain.frag")
    register_utility_shader("crt_scanlines", fragment_shader="assets/shaders/crt_scanlines.frag")
    register_utility_shader("radial_light_mask", fragment_shader="assets/shaders/radial_light_mask.frag")
    register_utility_shader("edge_detect", fragment_shader="assets/shaders/edge_detect.frag")
    register_utility_shader("time_warp", fragment_shader="assets/shaders/time_warp.frag")
    register_utility_shader("water_ripple", fragment_shader="assets/shaders/water_ripple.frag")
    register_utility_shader("additive_light", fragment_shader="assets/shaders/additive_light.frag")
    register_utility_shader("shockwave_sprite", fragment_shader="assets/shaders/shockwave_sprite.frag")
    
    # Bloom pipeline shaders
    register_utility_shader("bloom_extract", fragment_shader="assets/shaders/bloom_extract.frag")
    register_utility_shader("bloom_combine", fragment_shader="assets/shaders/bloom_combine.frag")
    
    # Color grading (requires LUT texture)
    register_utility_shader("color_grade", fragment_shader="assets/shaders/color_grade.frag")


# Auto-register on import
_register_builtin_utility_shaders()
