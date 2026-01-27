"""
Shader uniform helper functions for setting shader parameters.

Provides a consistent interface for setting shader uniforms across different
shader backends (moderngl, pygame shaders, etc.).
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import moderngl

logger = logging.getLogger(__name__)
_FAILED_UNIFORMS: set[tuple[int, str]] = set()


def set_float(shader: Any, name: str, value: float) -> None:
    """Set a float uniform on a shader."""
    try:
        if hasattr(shader, "uniforms") and name in shader.uniforms:
            shader.uniforms[name].value = float(value)
        elif hasattr(shader, name):
            setattr(shader, name, float(value))
        elif hasattr(shader, "set_uniform"):
            shader.set_uniform(name, float(value))
    except (AttributeError, KeyError, TypeError) as e:
        key = (id(shader), name)
        if key not in _FAILED_UNIFORMS:
            _FAILED_UNIFORMS.add(key)
            logger.debug(
                "Failed to set uniform '%s' on shader %r: %s",
                name, shader, e,
            )
        return


def set_int(shader: Any, name: str, value: int) -> None:
    """Set an integer uniform on a shader."""
    try:
        if hasattr(shader, "uniforms") and name in shader.uniforms:
            shader.uniforms[name].value = int(value)
        elif hasattr(shader, name):
            setattr(shader, name, int(value))
        elif hasattr(shader, "set_uniform"):
            shader.set_uniform(name, int(value))
    except (AttributeError, KeyError, TypeError) as e:
        key = (id(shader), name)
        if key not in _FAILED_UNIFORMS:
            _FAILED_UNIFORMS.add(key)
            logger.debug(
                "Failed to set uniform '%s' on shader %r: %s",
                name, shader, e,
            )
        return


def set_vec2(shader: Any, name: str, value: tuple[float, float]) -> None:
    """Set a vec2 uniform on a shader."""
    try:
        x, y = float(value[0]), float(value[1])
        if hasattr(shader, "uniforms") and name in shader.uniforms:
            shader.uniforms[name].value = (x, y)
        elif hasattr(shader, name):
            setattr(shader, name, (x, y))
        elif hasattr(shader, "set_uniform"):
            shader.set_uniform(name, (x, y))
    except (AttributeError, KeyError, TypeError, IndexError) as e:
        key = (id(shader), name)
        if key not in _FAILED_UNIFORMS:
            _FAILED_UNIFORMS.add(key)
            logger.debug(
                "Failed to set uniform '%s' on shader %r: %s",
                name, shader, e,
            )
        return


def set_vec3(shader: Any, name: str, value: tuple[float, float, float]) -> None:
    """Set a vec3 uniform on a shader."""
    try:
        r, g, b = float(value[0]), float(value[1]), float(value[2])
        if hasattr(shader, "uniforms") and name in shader.uniforms:
            shader.uniforms[name].value = (r, g, b)
        elif hasattr(shader, name):
            setattr(shader, name, (r, g, b))
        elif hasattr(shader, "set_uniform"):
            shader.set_uniform(name, (r, g, b))
    except (AttributeError, KeyError, TypeError, IndexError) as e:
        key = (id(shader), name)
        if key not in _FAILED_UNIFORMS:
            _FAILED_UNIFORMS.add(key)
            logger.debug(
                "Failed to set uniform '%s' on shader %r: %s",
                name, shader, e,
            )
        return


def set_sampler(shader: Any, name: str, texture: Any) -> None:
    """Set a sampler/texture uniform on a shader."""
    try:
        if hasattr(shader, "uniforms") and name in shader.uniforms:
            shader.uniforms[name].value = texture
        elif hasattr(shader, name):
            setattr(shader, name, texture)
        elif hasattr(shader, "set_uniform"):
            shader.set_uniform(name, texture)
    except (AttributeError, KeyError, TypeError) as e:
        key = (id(shader), name)
        if key not in _FAILED_UNIFORMS:
            _FAILED_UNIFORMS.add(key)
            logger.debug(
                "Failed to set uniform '%s' on shader %r: %s",
                name, shader, e,
            )
        return
