#version 330

uniform sampler2D u_frame_texture;
uniform vec2 u_LightCenter;  // Light center position (0.0 to 1.0)
uniform float u_InnerRadius; // Inner bright radius
uniform float u_OuterRadius; // Outer dark radius
uniform float u_Intensity;   // Light intensity multiplier

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(u_frame_texture, v_uv);
    
    // Calculate distance from light center
    vec2 centered = v_uv - u_LightCenter;
    float dist = length(centered);
    
    // Create radial mask: bright at center, dark at edges
    float mask = 1.0 - smoothstep(u_InnerRadius, u_OuterRadius, dist);
    
    // Apply intensity
    float light_factor = mix(0.3, 1.0, mask * u_Intensity);
    
    fragColor = vec4(color.rgb * light_factor, color.a);
}
