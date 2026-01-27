#version 330

uniform sampler2D u_frame_texture;
uniform float u_Start;       // Fog start position (0.0 to 1.0, typically 0.0 = top)
uniform float u_End;          // Fog end position (0.0 to 1.0)
uniform vec3 u_FogColor;      // Fog color (RGB)
uniform float u_Intensity;   // Fog intensity (0.0 to 1.0)

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(u_frame_texture, v_uv);
    
    // Calculate fog factor based on vertical position (UV.y)
    // smoothstep returns 0.0 at u_Start, 1.0 at u_End
    float fogFactor = smoothstep(u_Start, u_End, v_uv.y);
    
    // Mix original color with fog color
    vec3 fogged = mix(color.rgb, u_FogColor, fogFactor * u_Intensity);
    
    fragColor = vec4(fogged, color.a);
}
