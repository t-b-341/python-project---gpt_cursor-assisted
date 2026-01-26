"""
Fullscreen quad with CPU-generated texture and a simple fragment effect.
Same window setup as triangle_demo. ESC or close to exit.
"""
import struct
import sys

if __name__ == "__main__":
    try:
        import moderngl
        from moderngl_window import WindowConfig, run_window_config
    except ImportError as e:
        print("moderngl or moderngl-window not available. Install with: pip install moderngl moderngl-window")
        print(f"Import error: {e}")
        sys.exit(1)

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
            vec4 c = texture(tex, v_uv);
            fragColor = vec4(1.0 - c.r, 1.0 - c.g, 1.0 - c.b, c.a);
        }
    """

    # Fullscreen quad in NDC (two triangles), pos then uv per vertex
    QUAD = struct.pack(
        "24f",
        -1.0, -1.0, 0.0, 0.0,
         1.0, -1.0, 1.0, 0.0,
        -1.0,  1.0, 0.0, 1.0,
        -1.0,  1.0, 0.0, 1.0,
         1.0, -1.0, 1.0, 0.0,
         1.0,  1.0, 1.0, 1.0,
    )

    def make_checkerboard(size: int = 8) -> bytes:
        out = bytearray(size * size * 4)
        for y in range(size):
            for x in range(size):
                i = (y * size + x) * 4
                v = 255 if (x + y) % 2 == 0 else 0
                out[i : i + 4] = (v, v, v, 255)
        return bytes(out)

    class QuadEffectConfig(WindowConfig):
        title = "Quad Effect"
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
            tex_data = make_checkerboard(8)
            self.tex = self.ctx.texture((8, 8), 4, tex_data)
            self.tex.use(0)

        def on_render(self, time: float, frame_time: float) -> None:
            self.ctx.clear(0.15, 0.15, 0.2, 1.0)
            self.vao.render(moderngl.TRIANGLES)

    run_window_config(QuadEffectConfig)
