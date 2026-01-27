#version 330

uniform sampler2D u_frame_texture;  // Base texture
uniform sampler2D u_normal_map;      // Normal map texture
uniform vec2 u_light_positions[8];   // Light positions (screen space 0.0-1.0)
uniform vec3 u_light_colors[8];      // Light colors (RGB)
uniform float u_light_radii[8];      // Light radii
uniform float u_light_intensities[8]; // Light intensities
uniform int u_light_count;            // Number of active lights (0-8)
uniform vec3 u_ambient_color;        // Ambient light color
uniform float u_ambient_intensity;   // Ambient light intensity

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 base_color = texture(u_frame_texture, v_uv);
    
    // Sample normal map (assuming normal maps store normals in 0-1 range, convert to -1 to 1)
    vec3 normal = texture(u_normal_map, v_uv).rgb;
    normal = normalize(normal * 2.0 - 1.0);  // Convert from 0-1 to -1 to 1
    
    // Start with ambient lighting
    vec3 final_color = base_color.rgb * u_ambient_color * u_ambient_intensity;
    
    // Add contribution from each light
    for (int i = 0; i < u_light_count && i < 8; i++) {
        vec2 light_pos = u_light_positions[i];
        vec3 light_color = u_light_colors[i];
        float light_radius = u_light_radii[i];
        float light_intensity = u_light_intensities[i];
        
        // Calculate light direction in screen space
        vec2 light_dir = light_pos - v_uv;
        float dist = length(light_dir);
        
        // Calculate attenuation (falloff with distance)
        float attenuation = 1.0 / (1.0 + dist * dist / (light_radius * light_radius));
        
        // Calculate light contribution using normal map
        // For 2D, we use the normal's Z component and distance-based falloff
        vec3 light_direction_3d = normalize(vec3(light_dir, 0.1));  // Slight Z for depth
        float NdotL = max(0.0, dot(normal, light_direction_3d));
        
        // Combine distance attenuation and normal-based lighting
        float light_contribution = NdotL * attenuation * light_intensity;
        
        // Add light contribution
        final_color += base_color.rgb * light_color * light_contribution;
    }
    
    fragColor = vec4(final_color, base_color.a);
}
