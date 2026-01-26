"""
Upload a small Pygame surface as a moderngl texture and draw it on a fullscreen quad.
Minimal, self-contained. ESC or close to exit.
"""
import struct
import sys

if __name__ == "__main__":
    try:
        import pygame
        import moderngl
        from moderngl_window import WindowConfig, run_window_config
    except ImportError as e:
        print("pygame and moderngl/moderngl-window required. pip install pygame moderngl moderngl-window")
        print(f"Import error: {e}")
        sys.exit(1)

    pygame.init()
    w, h = 64, 64
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for y in range(h):
        for x in range(w):
            r = int(255 * x / w)
            g = int(255 * y / h)
            surf.set_at((x, y), (r, g, 180, 255))
    try:
        tex_bytes = pygame.image.tostring(surf, "RGBA", False)
    except AttributeError:
        tex_bytes = bytes(surf.get_view("0"))

    VERTEX = """
        #version 330
        in vec2 in_pos;
        in vec2 in_uv;
        out vec2 v_uv;
        void main() {
            gl_Position = vec4(in_pos, 0.0, 1.0);
            v_uv = in_uv;
        }
    """
    FRAGMENT = """
        #version 330
        uniform sampler2D tex;
        in vec2 v_uv;
        out vec4 fragColor;
        void main() {
            fragColor = texture(tex, v_uv);
        }
    """
    QUAD = struct.pack(
        "24f",
        -1.0, -1.0, 0.0, 0.0,
         1.0, -1.0, 1.0, 0.0,
        -1.0,  1.0, 0.0, 1.0,
        -1.0,  1.0, 0.0, 1.0,
         1.0, -1.0, 1.0, 0.0,
         1.0,  1.0, 1.0, 1.0,
    )

    class PygameToGLConfig(WindowConfig):
        title = "Pygame → GL"
        window_size = (800, 600)
        gl_version = (3, 3)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.prog = self.ctx.program(vertex_shader=VERTEX, fragment_shader=FRAGMENT)
            buf = self.ctx.buffer(QUAD)
            self.vao = self.ctx.vertex_array(
                self.prog,
                [(buf, "2f 2f", "in_pos", "in_uv")],
            )
            self.tex = self.ctx.texture((w, h), 4, tex_bytes)
            self.tex.use(0)

        def on_render(self, time: float, frame_time: float) -> None:
            self.ctx.clear(0.1, 0.1, 0.15, 1.0)
            self.vao.render(moderngl.TRIANGLES)

    run_window_config(PygameToGLConfig)
