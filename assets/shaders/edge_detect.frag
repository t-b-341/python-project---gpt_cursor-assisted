#version 330

uniform sampler2D u_frame_texture;
uniform float u_Threshold;  // Edge detection threshold
uniform vec3 u_Color;       // Outline color
uniform float u_Intensity;  // Outline intensity

in vec2 v_uv;
out vec4 fragColor;

void main() {
    vec2 texelSize = 1.0 / textureSize(u_frame_texture, 0);
    
    // Sobel edge detection kernel
    // Sample surrounding pixels
    float tl = length(texture(u_frame_texture, v_uv + vec2(-texelSize.x, -texelSize.y)).rgb);
    float tm = length(texture(u_frame_texture, v_uv + vec2(0.0, -texelSize.y)).rgb);
    float tr = length(texture(u_frame_texture, v_uv + vec2(texelSize.x, -texelSize.y)).rgb);
    float ml = length(texture(u_frame_texture, v_uv + vec2(-texelSize.x, 0.0)).rgb);
    float mc = length(texture(u_frame_texture, v_uv).rgb);
    float mr = length(texture(u_frame_texture, v_uv + vec2(texelSize.x, 0.0)).rgb);
    float bl = length(texture(u_frame_texture, v_uv + vec2(-texelSize.x, texelSize.y)).rgb);
    float bm = length(texture(u_frame_texture, v_uv + vec2(0.0, texelSize.y)).rgb);
    float br = length(texture(u_frame_texture, v_uv + vec2(texelSize.x, texelSize.y)).rgb);
    
    // Sobel X and Y gradients
    float gx = -tl + tr - 2.0 * ml + 2.0 * mr - bl + br;
    float gy = -tl - 2.0 * tm - tr + bl + 2.0 * bm + br;
    
    // Calculate edge magnitude
    float edge = sqrt(gx * gx + gy * gy);
    
    // Threshold and create outline
    float outline = step(u_Threshold, edge);
    
    vec4 original = texture(u_frame_texture, v_uv);
    vec3 outlined = mix(original.rgb, u_Color, outline * u_Intensity);
    
    fragColor = vec4(outlined, original.a);
}
