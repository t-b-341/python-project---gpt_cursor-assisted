#version 330

uniform sampler2D u_frame_texture;
uniform vec3 u_Color;      // Light color (RGB)
uniform float u_Intensity; // Light intensity

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(u_frame_texture, v_uv);
    
    // Additive blending: add light color * intensity
    vec3 additive = color.rgb + u_Color * u_Intensity;
    
    fragColor = vec4(additive, color.a);
}
