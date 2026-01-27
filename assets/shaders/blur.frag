#version 330

uniform sampler2D u_frame_texture;
uniform vec2 u_Direction;  // (1,0) for horizontal, (0,1) for vertical
uniform float u_BlurSize;  // Blur kernel size/radius

in vec2 v_uv;
out vec4 fragColor;

// Gaussian weights for separable blur (9-tap kernel)
// Weights are precomputed for efficiency
const float weights[9] = float[](
    0.2270270270,  // center
    0.1945945946,  // ±1
    0.1216216216,  // ±2
    0.0540540541,  // ±3
    0.0162162162,  // ±4
    0.0033783784,  // ±5
    0.0004054054,  // ±6
    0.0000270270,  // ±7
    0.0000006757   // ±8
);

void main() {
    vec2 texelSize = 1.0 / textureSize(u_frame_texture, 0);
    vec4 color = texture(u_frame_texture, v_uv) * weights[0];
    
    // Apply blur in the specified direction
    vec2 offset = u_Direction * texelSize * u_BlurSize;
    
    for (int i = 1; i < 9; i++) {
        float weight = weights[i];
        vec2 sampleOffset = float(i) * offset;
        color += texture(u_frame_texture, v_uv + sampleOffset) * weight;
        color += texture(u_frame_texture, v_uv - sampleOffset) * weight;
    }
    
    fragColor = color;
}
