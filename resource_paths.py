"""
Resource path helper for development and PyInstaller builds.

Provides get_resource_path() which works both in development (relative to project root)
and in PyInstaller bundles (using sys._MEIPASS).
"""
from __future__ import annotations

import os
import sys
from typing import Union

PathLike = Union[str, "os.PathLike[str]"]


def get_resource_path(relative_path: PathLike) -> str:
    """
    Get absolute path to resource, working both in development and in a PyInstaller bundle.
    
    Args:
        relative_path: Path relative to project root (e.g., "assets/shaders/blur.frag")
    
    Returns:
        Absolute path to the resource
    
    Example:
        shader_path = get_resource_path(os.path.join("assets", "shaders", "blur.frag"))
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)
