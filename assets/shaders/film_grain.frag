#version 330

uniform sampler2D u_frame_texture;
uniform float u_Intensity;  // Grain intensity (0.0 to 1.0)
uniform float u_Time;       // Time for animated grain

in vec2 v_uv;
out vec4 fragColor;

// Procedural noise function
float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec4 color = texture(u_frame_texture, v_uv);
    
    // Generate grain noise
    vec2 grain_uv = v_uv * 512.0 + vec2(u_Time * 10.0);
    float grain = noise(grain_uv);
    
    // Convert to -1.0 to 1.0 range and apply intensity
    grain = (grain - 0.5) * 2.0 * u_Intensity;
    
    // Add grain to color
    vec3 grained = color.rgb + grain * 0.1;
    
    fragColor = vec4(grained, color.a);
}
