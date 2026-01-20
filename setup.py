"""
Setup script for building the game_physics C extension module.
Run: python setup.py build_ext --inplace
"""

from setuptools import setup, Extension
import sys
import py_compile

# Compiler-specific flags
if sys.platform == 'win32':
    # MSVC flags (Windows)
    extra_compile_args = ['/O2']  # Optimization level 2 (max for MSVC)
else:
    # GCC/Clang flags (Linux/Mac)
    extra_compile_args = ['-O3', '-march=native']

# Define the extension module
game_physics_module = Extension(
    'game_physics',
    sources=['game_physics.c'],
    extra_compile_args=extra_compile_args,
    language='c'
)

setup(
    name='game_physics',
    version='1.0',
    description='High-performance physics and collision detection for game.py',
    ext_modules=[game_physics_module],
    zip_safe=False,
)
