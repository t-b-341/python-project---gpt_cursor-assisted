#version 330

uniform sampler2D u_frame_texture;
uniform float u_Time;

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(u_frame_texture, v_uv);
    
    // Create scanlines using sine wave
    float scanline = sin(v_uv.y * 800.0) * 0.5 + 0.5;
    scanline = mix(1.0, scanline, 0.1);  // Subtle scanline effect
    
    // R/G/B channel misalignment for CRT effect
    float r = texture(u_frame_texture, v_uv + vec2(0.001, 0.0)).r;
    float g = texture(u_frame_texture, v_uv).g;
    float b = texture(u_frame_texture, v_uv - vec2(0.001, 0.0)).b;
    
    // Apply scanlines and channel separation
    vec3 crt_color = vec3(r, g, b) * scanline;
    
    fragColor = vec4(crt_color, color.a);
}
