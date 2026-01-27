#version 330

uniform sampler2D u_frame_texture;
uniform float u_PixelSize;  // Pixel size multiplier (1.0 = no pixelation)

in vec2 v_uv;
out vec4 fragColor;

void main() {
    // Quantize UV coordinates to create pixelation effect
    vec2 pixelated_uv = floor(v_uv * u_PixelSize) / u_PixelSize;
    
    fragColor = texture(u_frame_texture, pixelated_uv);
}
