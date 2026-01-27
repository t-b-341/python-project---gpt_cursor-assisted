#version 330

uniform sampler2D u_frame_texture;
uniform vec2 u_Center;       // Center point of shockwave (0.0 to 1.0)
uniform float u_Time;        // Current time for animation
uniform float u_Amplitude;  // Amplitude of distortion
uniform float u_Speed;       // Speed of wave propagation

in vec2 v_uv;
out vec4 fragColor;

void main() {
    // Calculate distance from center
    vec2 centered = v_uv - u_Center;
    float dist = length(centered);
    
    // Create radial wave based on time
    float wave = sin(dist * 10.0 - u_Time * u_Speed) * u_Amplitude;
    
    // Normalize direction vector
    vec2 dir = dist > 0.001 ? normalize(centered) : vec2(0.0, 1.0);
    
    // Apply radial distortion
    vec2 distorted_uv = v_uv + dir * wave * 0.01;
    
    fragColor = texture(u_frame_texture, distorted_uv);
}
