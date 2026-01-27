#version 330

uniform sampler2D u_frame_texture;
uniform float u_Threshold;  // Brightness threshold for bloom extraction

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(u_frame_texture, v_uv);
    
    // Calculate luminance
    float luminance = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    
    // Extract bright pixels above threshold
    float bright = max(0.0, luminance - u_Threshold);
    bright = bright / (1.0 - u_Threshold);  // Normalize
    
    fragColor = vec4(color.rgb * bright, 1.0);
}
