#version 330 core
// Pixelation shader; u_PixelSize is block size in screen pixels.

uniform sampler2D u_frame_texture;
uniform float u_PixelSize;

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec2 texSize = vec2(textureSize(u_frame_texture, 0));
    vec2 pixelSize = vec2(u_PixelSize) / texSize;
    vec2 uvQuantized = floor(v_uv / pixelSize) * pixelSize;
    fragColor = texture(u_frame_texture, uvQuantized);
}
