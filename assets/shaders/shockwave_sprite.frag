#version 330

uniform sampler2D u_frame_texture;
uniform sampler2D u_ring_texture;  // Ring texture for shockwave sprite
uniform vec2 u_Center;             // Shockwave center
uniform float u_Radius;             // Current radius
uniform float u_Amplitude;          // Distortion amplitude

in vec2 v_uv;
out vec4 fragColor;

void main() {
    // Calculate distance from center
    vec2 centered = v_uv - u_Center;
    float dist = length(centered);
    
    // Sample ring texture at current radius
    vec2 ring_uv = vec2(dist / u_Radius, atan(centered.y, centered.x) / (3.14159 * 2.0));
    float ring = texture(u_ring_texture, ring_uv).r;
    
    // Apply radial distortion based on ring
    vec2 dir = dist > 0.001 ? normalize(centered) : vec2(0.0, 1.0);
    vec2 distorted_uv = v_uv + dir * ring * u_Amplitude * 0.01;
    
    fragColor = texture(u_frame_texture, distorted_uv);
}
