# Build Instructions

## Running the Game (Development)

Use `run_game.bat` to launch the game during development. This requires:
- Python 3.x installed
- All dependencies from `requirements.txt` installed

Simply double-click `run_game.bat` or run it from the command line.

### Optional Dependencies

If you want to use the GPU shader pipeline, Shader Test Mode, or Shader Settings GPU preview, install moderngl:
```
pip install moderngl
```

When moderngl is NOT installed, the game will fall back to CPU effects and hide/disable GPU-specific scenes.

## Building a Standalone Executable

Use `build_game.bat` to create a self-contained Windows `.exe` file using PyInstaller.

### Prerequisites
- Python 3.x installed
- PyInstaller installed: `pip install pyinstaller`

### Usage
1. Double-click `build_game.bat` or run it from the command line
2. The executable will be created in `dist\MyGame.exe`
3. This EXE can be distributed to other Windows users who do not have Python installed

### Notes
- The build process cleans previous build artifacts automatically
- The resulting EXE is self-contained and includes all dependencies
- GPU shaders (moderngl) will work if the target system has OpenGL support
- If moderngl is not available, the game will fall back to CPU-based visual effects

## Shader System

The game supports two rendering paths:

1. **GPU Shader Pipeline** (when `use_gpu_shader_pipeline=True` and moderngl is available):
   - Uses OpenGL shaders for post-processing effects
   - Higher performance for complex effects
   - Requires moderngl library and OpenGL support

2. **CPU Visual Effects** (fallback):
   - Uses CPU-based pygame surface manipulation
   - Works on all systems
   - Lower performance but more compatible

The game automatically detects moderngl availability and chooses the appropriate path.
