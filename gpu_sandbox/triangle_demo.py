"""
Minimal moderngl + moderngl-window demo: one colored triangle.
Window 800x600, ESC or close to exit. Run with: python gpu_sandbox/triangle_demo.py
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
        void main() {
            gl_Position = vec4(in_pos, 0.0, 1.0);
        }
    """
    FRAGMENT = """
        #version 330
        out vec4 fragColor;
        void main() {
            fragColor = vec4(0.2, 0.6, 1.0, 1.0);
        }
    """

    # Triangle at center (NDC): top, bottom-left, bottom-right
    TRIANGLE = struct.pack("6f", 0.0, 0.5, -0.5, -0.5, 0.5, -0.5)

    class TriangleConfig(WindowConfig):
        title = "Triangle"
        window_size = (800, 600)
        gl_version = (3, 3)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.prog = self.ctx.program(vertex_shader=VERTEX, fragment_shader=FRAGMENT)
            self.vao = self.ctx.vertex_array(
                self.prog,
                [(self.ctx.buffer(TRIANGLE), "2f", ["in_pos"])],
            )

        def on_render(self, time: float, frame_time: float) -> None:
            self.ctx.clear(0.1, 0.1, 0.15, 1.0)
            self.vao.render(moderngl.TRIANGLES)

    run_window_config(TriangleConfig)
