"""
Fullscreen quad with a fragment shader animated over time.
Same setup as quad_effect_demo. u_time from time.perf_counter(). ESC or close to exit.
"""
import struct
import sys
import time

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
        uniform float u_time;
        in vec2 v_uv;
        out vec4 fragColor;
        void main() {
            float t = 0.5 + 0.5 * sin(u_time);
            vec2 c = v_uv * t;
            fragColor = vec4(c.x, c.y, 0.5, 1.0);
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

    class AnimatedEffectConfig(WindowConfig):
        title = "Animated Effect"
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
            self.start_time = time.perf_counter()

        def on_render(self, _time: float, frame_time: float) -> None:
            self.ctx.clear(0.08, 0.08, 0.12, 1.0)
            self.prog["u_time"].value = time.perf_counter() - self.start_time
            self.vao.render(moderngl.TRIANGLES)

    run_window_config(AnimatedEffectConfig)
