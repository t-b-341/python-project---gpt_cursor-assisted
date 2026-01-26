"""
Tests for shader_effects: EFFECT_REGISTRY, SHADER_PROFILES, get_*_shader_stack.

Verifies that stack getters return [] when disabled or profile "none", return
non-empty stacks for valid profiles, and that built stacks run apply() without raising.
"""
from __future__ import annotations

import pytest

import pygame

import shader_effects as se


@pytest.fixture(autouse=True)
def _pygame_init():
    if not pygame.get_init():
        pygame.init()
    yield


@pytest.fixture
def surface_64x64():
    s = pygame.Surface((64, 64))
    s.fill((60, 80, 100))
    return s


class _Config:
    enable_menu_shaders = False
    enable_pause_shaders = False
    enable_gameplay_shaders = False
    menu_shader_profile = "none"
    pause_shader_profile = "none"
    gameplay_shader_profile = "none"


# ---- get_menu_shader_stack ----

def test_get_menu_shader_stack_empty_when_disabled():
    cfg = _Config()
    cfg.enable_menu_shaders = False
    cfg.menu_shader_profile = "menu_crt"
    assert se.get_menu_shader_stack(cfg) == []


def test_get_menu_shader_stack_empty_when_profile_none():
    cfg = _Config()
    cfg.enable_menu_shaders = True
    cfg.menu_shader_profile = "none"
    assert se.get_menu_shader_stack(cfg) == []


def test_get_menu_shader_stack_nonempty_for_menu_crt():
    cfg = _Config()
    cfg.enable_menu_shaders = True
    cfg.menu_shader_profile = "menu_crt"
    stack = se.get_menu_shader_stack(cfg)
    assert len(stack) > 0
    assert len(stack) == len(se.SHADER_PROFILES["menu_crt"])


def test_get_menu_shader_stack_nonempty_for_menu_neon():
    cfg = _Config()
    cfg.enable_menu_shaders = True
    cfg.menu_shader_profile = "menu_neon"
    stack = se.get_menu_shader_stack(cfg)
    assert len(stack) > 0


# ---- get_pause_shader_stack ----

def test_get_pause_shader_stack_empty_when_disabled():
    cfg = _Config()
    cfg.enable_pause_shaders = False
    cfg.pause_shader_profile = "pause_dim_vignette"
    assert se.get_pause_shader_stack(cfg) == []


def test_get_pause_shader_stack_empty_when_profile_none():
    cfg = _Config()
    cfg.enable_pause_shaders = True
    cfg.pause_shader_profile = "none"
    assert se.get_pause_shader_stack(cfg) == []


def test_get_pause_shader_stack_nonempty_for_pause_dim_vignette():
    cfg = _Config()
    cfg.enable_pause_shaders = True
    cfg.pause_shader_profile = "pause_dim_vignette"
    stack = se.get_pause_shader_stack(cfg)
    assert len(stack) > 0


# ---- get_gameplay_shader_stack ----

def test_get_gameplay_shader_stack_empty_when_disabled():
    cfg = _Config()
    cfg.enable_gameplay_shaders = False
    cfg.gameplay_shader_profile = "gameplay_subtle_vignette"
    assert se.get_gameplay_shader_stack(cfg) == []


def test_get_gameplay_shader_stack_empty_when_profile_none():
    cfg = _Config()
    cfg.enable_gameplay_shaders = True
    cfg.gameplay_shader_profile = "none"
    assert se.get_gameplay_shader_stack(cfg) == []


def test_get_gameplay_shader_stack_nonempty_for_subtle_vignette():
    cfg = _Config()
    cfg.enable_gameplay_shaders = True
    cfg.gameplay_shader_profile = "gameplay_subtle_vignette"
    stack = se.get_gameplay_shader_stack(cfg)
    assert len(stack) == 1


def test_get_gameplay_shader_stack_nonempty_for_retro():
    cfg = _Config()
    cfg.enable_gameplay_shaders = True
    cfg.gameplay_shader_profile = "gameplay_retro"
    stack = se.get_gameplay_shader_stack(cfg)
    assert len(stack) == 2


# ---- stack apply() runs without raising ----

def test_menu_stack_apply_no_raise(surface_64x64):
    """Menu shader stack (menu_crt) apply chain runs without raising."""
    cfg = _Config()
    cfg.enable_menu_shaders = True
    cfg.menu_shader_profile = "menu_crt"
    stack = se.get_menu_shader_stack(cfg)
    ctx = {"time": 0.0}
    surf = surface_64x64
    for eff in stack:
        surf = eff.apply(surf, 0.016, ctx)
    assert surf.get_size() == (64, 64)


def test_pause_stack_apply_no_raise(surface_64x64):
    """Pause shader stack apply chain runs without raising."""
    cfg = _Config()
    cfg.enable_pause_shaders = True
    cfg.pause_shader_profile = "pause_dim_vignette"
    stack = se.get_pause_shader_stack(cfg)
    ctx = {"time": 0.0}
    surf = surface_64x64
    for eff in stack:
        surf = eff.apply(surf, 0.016, ctx)
    assert surf.get_size() == (64, 64)


def test_gameplay_stack_apply_no_raise(surface_64x64):
    """Gameplay shader stack apply chain runs without raising."""
    cfg = _Config()
    cfg.enable_gameplay_shaders = True
    cfg.gameplay_shader_profile = "gameplay_subtle_vignette"
    stack = se.get_gameplay_shader_stack(cfg)
    ctx = {"time": 0.0}
    surf = surface_64x64
    for eff in stack:
        surf = eff.apply(surf, 0.016, ctx)
    assert surf.get_size() == (64, 64)


# ---- registry and profiles ----

def test_shader_profiles_none_is_empty():
    assert se.SHADER_PROFILES["none"] == []


def test_shader_profiles_expected_keys():
    expected = {
        "none", "menu_crt", "menu_neon",
        "pause_dim_vignette",
        "gameplay_subtle_vignette", "gameplay_retro",
    }
    assert expected.issubset(se.SHADER_PROFILES.keys())


def test_effect_registry_has_all_profile_keys():
    """Every key referenced in SHADER_PROFILES exists in EFFECT_REGISTRY."""
    for profile_name, defs in se.SHADER_PROFILES.items():
        for d in defs:
            key = d[0] if isinstance(d, tuple) else d
            assert key in se.EFFECT_REGISTRY, f"profile {profile_name!r} uses key {key!r} not in registry"
