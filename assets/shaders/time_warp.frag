#version 330

uniform sampler2D u_frame_texture;
uniform float u_TimeScale;  // Time scale factor (1.0 = normal, <1.0 = slow, >1.0 = fast)
uniform float u_Time;
uniform float u_ChromaticAberration;  // Optional chromatic aberration intensity

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec2 centered = v_uv - 0.5;
    float dist = length(centered);
    
    // Radial distortion based on time scale
    float warp = sin(dist * 5.0 - u_Time * u_TimeScale) * 0.02;
    
    vec2 dir = dist > 0.001 ? normalize(centered) : vec2(0.0, 1.0);
    vec2 warped_uv = v_uv + dir * warp;
    
    // Optional chromatic aberration
    if (u_ChromaticAberration > 0.0) {
        vec2 offset = dir * u_ChromaticAberration * 0.01;
        float r = texture(u_frame_texture, warped_uv + offset).r;
        float g = texture(u_frame_texture, warped_uv).g;
        float b = texture(u_frame_texture, warped_uv - offset).b;
        float a = texture(u_frame_texture, warped_uv).a;
        fragColor = vec4(r, g, b, a);
    } else {
        fragColor = texture(u_frame_texture, warped_uv);
    }
}
