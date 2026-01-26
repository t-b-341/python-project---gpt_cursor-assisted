"""
Tests for asset_manager: fallback behavior when assets are missing.

Ensures get_image, get_sound, get_font return sane fallbacks and get_music_path
returns None for missing files, without raising.
"""
from __future__ import annotations

import pytest

import pygame

import asset_manager


@pytest.fixture(autouse=True)
def _setup():
    """Ensure pygame is inited and caches are clear to avoid cross-test interference."""
    if not pygame.get_init():
        pygame.init()
    asset_manager.clear_caches()
    yield
    asset_manager.clear_caches()


def test_get_image_fallback_returns_surface():
    """get_image with nonexistent key returns a Surface with small non-zero size and does not raise."""
    surf = asset_manager.get_image("nonexistent_test_image")
    assert isinstance(surf, pygame.Surface)
    assert surf.get_width() > 0 and surf.get_height() > 0


def test_get_image_fallback_does_not_raise():
    """get_image with nonexistent key does not raise."""
    asset_manager.get_image("nonexistent_test_image")


def test_get_sound_fallback_does_not_raise():
    """get_sound with nonexistent key does not raise."""
    result = asset_manager.get_sound("nonexistent_test_sound")
    if result is not None:
        result.play()


def test_get_sound_fallback_returns_playable_or_none():
    """get_sound returns either a Sound, a playable object, or None; no exception."""
    result = asset_manager.get_sound("nonexistent_test_sound")
    if result is not None:
        assert hasattr(result, "play")
        result.play()


def test_get_font_fallback_has_render():
    """get_font with nonexistent key returns a font-like object with render(text, antialias, color)."""
    f = asset_manager.get_font("nonexistent_test_font", size=24)
    assert hasattr(f, "render")
    out = f.render("Hi", True, (255, 255, 255))
    assert isinstance(out, pygame.Surface)


def test_get_font_fallback_does_not_raise():
    """get_font with nonexistent key does not raise."""
    asset_manager.get_font("nonexistent_test_font", size=24)


def test_get_music_path_missing_returns_none():
    """get_music_path with nonexistent key returns None and does not raise."""
    path = asset_manager.get_music_path("nonexistent_test_music")
    assert path is None


def test_get_music_path_missing_does_not_raise():
    """get_music_path with nonexistent key does not raise."""
    asset_manager.get_music_path("nonexistent_test_music")
