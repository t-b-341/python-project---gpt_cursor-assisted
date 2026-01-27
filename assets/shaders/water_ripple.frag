#version 330

uniform sampler2D u_frame_texture;
uniform vec2 u_Center;        // Ripple center point
uniform float u_Time;         // Time for animation
uniform float u_Speed;        // Wave speed
uniform float u_Frequency;    // Wave frequency
uniform float u_Amplitude;    // Wave amplitude

in vec2 v_uv;
out vec4 fragColor;

void main() {
    // Calculate distance from center
    vec2 centered = v_uv - u_Center;
    float dist = length(centered);
    
    // Create circular wave using sine
    float wave = sin(dist * u_Frequency - u_Time * u_Speed) * u_Amplitude;
    
    // Normalize direction
    vec2 dir = dist > 0.001 ? normalize(centered) : vec2(0.0, 1.0);
    
    // Apply radial distortion
    vec2 rippled_uv = v_uv + dir * wave * 0.01;
    
    fragColor = texture(u_frame_texture, rippled_uv);
}
