#version 330

uniform sampler2D u_frame_texture;
uniform sampler2D u_noise_texture;  // Noise texture for distortion
uniform float u_Strength;           // Distortion strength
uniform float u_Time;               // Time for scrolling

in vec2 v_uv;
out vec4 fragColor;

// Simple procedural noise if no texture provided
float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    // Sample noise texture with time-based scrolling
    vec2 noise_uv = v_uv + vec2(u_Time * 0.1, u_Time * 0.15);
    
    // Get noise value (0.0 to 1.0)
    float noise_val = noise(noise_uv);
    
    // Convert to offset (-1.0 to 1.0)
    vec2 noise_offset = (noise_val - 0.5) * 2.0;
    
    // Apply distortion to UV coordinates
    vec2 distorted_uv = v_uv + noise_offset * u_Strength * 0.01;
    
    fragColor = texture(u_frame_texture, distorted_uv);
}
