#version 330

uniform sampler2D u_frame_texture;
uniform float u_Radius;      // Radius of vignette (0.0 to 1.0)
uniform float u_Smoothness;  // Smoothness of vignette edge (0.0 to 1.0)
uniform float u_Intensity;   // Intensity of darkening (0.0 to 1.0)

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(u_frame_texture, v_uv);
    
    // Compute radial distance from screen center
    vec2 centered = v_uv - 0.5;
    float dist = length(centered);
    
    // Create smooth vignette mask using smoothstep
    // smoothstep(edge0, edge1, x) returns 0.0 for x < edge0, 1.0 for x > edge1, smooth in between
    float vignette = 1.0 - smoothstep(u_Radius, u_Radius + u_Smoothness, dist);
    
    // Apply intensity and darken edges
    float darken = mix(1.0, vignette, u_Intensity);
    
    fragColor = vec4(color.rgb * darken, color.a);
}
