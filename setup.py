"""
Setup script for building the game_physics C extension module.
Run: python setup.py build_ext --inplace
"""

from setuptools import setup, Extension
import py_compile

# Define the extension module
game_physics_module = Extension(
    'game_physics',
    sources=['game_physics.c'],
    extra_compile_args=['-O3', '-march=native'],  # Optimize for speed
    language='c'
)

setup(
    name='game_physics',
    version='1.0',
    description='High-performance physics and collision detection for game.py',
    ext_modules=[game_physics_module],
    zip_safe=False,
)
