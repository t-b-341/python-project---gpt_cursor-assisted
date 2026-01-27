#version 330

uniform sampler2D u_frame_texture;
uniform sampler2D u_LUT;      // Color lookup table texture
uniform float u_LUT_Size;     // Size of LUT (e.g., 16.0 for 16x16x16)
uniform float u_Intensity;    // Intensity of color grading (0.0 to 1.0)

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(u_frame_texture, v_uv);
    
    // Sample LUT (assuming 3D LUT stored as 2D texture)
    // For a 16x16x16 LUT, we need to map RGB to UV coordinates
    float cellSize = 1.0 / u_LUT_Size;
    float cellIndex = floor(color.b * (u_LUT_Size - 1.0));
    float z = cellIndex / u_LUT_Size;
    
    vec2 lut_uv = vec2(
        color.r * cellSize + (cellIndex * cellSize),
        color.g * cellSize + z
    );
    
    vec4 lut_color = texture(u_LUT, lut_uv);
    
    // Blend original with LUT result
    vec3 graded = mix(color.rgb, lut_color.rgb, u_Intensity);
    
    fragColor = vec4(graded, color.a);
}
