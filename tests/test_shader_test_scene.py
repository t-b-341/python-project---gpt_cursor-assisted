"""
Tests for ShaderTestScene fallback path when moderngl is NOT available.

Ensures ShaderTestScene works without moderngl or GPU. Does not require moderngl to be installed.
"""
from __future__ import annotations

import pytest

import pygame

from rendering import RenderContext

# Import the module so we can monkeypatch HAS_MODERNGL before using the class.
import scenes.shader_test as shader_test_module


@pytest.fixture(autouse=True)
def _pygame_init():
    """Ensure pygame is inited before creating surfaces."""
    if not pygame.get_init():
        pygame.init()
    yield


@pytest.fixture
def render_ctx():
    """Dummy RenderContext with a small screen and default-style fonts."""
    from asset_manager import get_font

    screen = pygame.Surface((640, 480))
    font = get_font("main", 28)
    big_font = get_font("main", 56)
    small_font = get_font("main", 20)
    return RenderContext(
        screen=screen,
        font=font,
        big_font=big_font,
        small_font=small_font,
        width=640,
        height=480,
    )


def test_fallback_path_no_moderngl(monkeypatch, render_ctx):
    """With HAS_MODERNGL forced to False, ShaderTestScene runs handle_input/update/render without raising."""
    monkeypatch.setattr(shader_test_module, "HAS_MODERNGL", False, raising=False)

    scene = shader_test_module.ShaderTestScene()

    assert scene.state_id() == "SHADER_TEST"

    scene.handle_input([], game_state=None, ctx={})
    scene.update(0.016, game_state=None, ctx={})
    scene.render(render_ctx, game_state=None, ctx={})
