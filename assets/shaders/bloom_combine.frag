#version 330

uniform sampler2D u_frame_texture;  // Original image
uniform sampler2D u_bloom_texture;  // Blurred bloom texture
uniform float u_Intensity;  // Bloom intensity multiplier

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 original = texture(u_frame_texture, v_uv);
    vec4 bloom = texture(u_bloom_texture, v_uv);
    
    // Additive blend: original + bloom
    vec3 combined = original.rgb + bloom.rgb * u_Intensity;
    
    fragColor = vec4(combined, original.a);
}
