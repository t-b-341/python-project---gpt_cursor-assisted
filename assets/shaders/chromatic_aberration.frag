#version 330

uniform sampler2D u_frame_texture;
uniform float u_Intensity;  // Intensity of RGB channel separation

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec2 centered = v_uv - 0.5;
    float dist = length(centered);
    
    // Offset RGB channels outward based on distance from center
    vec2 offset = normalize(centered) * u_Intensity * dist * 0.01;
    
    float r = texture(u_frame_texture, v_uv + offset).r;
    float g = texture(u_frame_texture, v_uv).g;
    float b = texture(u_frame_texture, v_uv - offset).b;
    float a = texture(u_frame_texture, v_uv).a;
    
    fragColor = vec4(r, g, b, a);
}
