#version 330

uniform sampler2D u_frame_texture;
uniform float u_ShakeIntensity;  // Intensity of shake
uniform float u_ShakeTime;       // Time for shake animation

in vec2 v_uv;
out vec4 fragColor;

// Simple noise function for shake pattern
float noise(float x) {
    return fract(sin(x * 12.9898) * 43758.5453);
}

void main() {
    // Generate shake offset using sine waves with noise
    float shake_x = sin(u_ShakeTime * 20.0) * cos(u_ShakeTime * 15.0) * u_ShakeIntensity;
    float shake_y = cos(u_ShakeTime * 18.0) * sin(u_ShakeTime * 12.0) * u_ShakeIntensity;
    
    // Add noise for more chaotic shake
    shake_x += (noise(u_ShakeTime * 10.0) - 0.5) * u_ShakeIntensity * 0.5;
    shake_y += (noise(u_ShakeTime * 13.0) - 0.5) * u_ShakeIntensity * 0.5;
    
    vec2 offset = vec2(shake_x, shake_y) * 0.01;
    vec2 shaken_uv = v_uv + offset;
    
    fragColor = texture(u_frame_texture, shaken_uv);
}
