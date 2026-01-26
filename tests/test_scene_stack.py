"""Tests that the SceneStack and scene transitions behave as expected."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from constants import STATE_PLAYING, STATE_PAUSED, STATE_HIGH_SCORES, STATE_NAME_INPUT
from scenes import SceneStack, GameplayScene, PauseScene, HighScoreScene, NameInputScene, ShaderTestScene
from scenes.shader_test import SHADER_TEST_STATE_ID


def test_scene_stack_push_pop_current():
    s = SceneStack()
    assert s.current() is None
    assert len(s) == 0

    g = GameplayScene(STATE_PLAYING)
    s.push(g)
    assert s.current() is g
    assert len(s) == 1
    assert s.current().state_id() == STATE_PLAYING

    p = PauseScene()
    s.push(p)
    assert s.current() is p
    assert len(s) == 2
    assert s.current().state_id() == STATE_PAUSED

    popped = s.pop()
    assert popped is p
    assert s.current() is g
    assert s.current().state_id() == STATE_PLAYING

    s.pop()
    assert s.current() is None
    assert s.pop() is None


def test_scene_stack_clear():
    s = SceneStack()
    s.push(GameplayScene(STATE_PLAYING))
    s.push(PauseScene())
    s.clear()
    assert s.current() is None
    assert len(s) == 0


def test_scene_handle_input_return_shape():
    """Scenes' handle_input return dicts with expected keys for the loop."""
    p = PauseScene()
    out = p.handle_input([], None, {})
    assert isinstance(out, dict)
    assert "screen" in out
    assert "quit" in out
    # replay/restart used by high scores / pause
    assert "restart" in out or "replay" in out or "screen" in out

    g = GameplayScene(STATE_PLAYING)
    out = g.handle_input([], None, {})
    assert "screen" in out and "quit" in out

    sh = ShaderTestScene()
    out = sh.handle_input([], None, {})
    assert isinstance(out, dict)
    assert "screen" in out and "quit" in out and "pop" in out


def test_shader_test_scene_state_id_and_stack():
    """ShaderTestScene has state_id SHADER_TEST and works on the stack like other scenes."""
    s = SceneStack()
    g = GameplayScene(STATE_PLAYING)
    s.push(g)
    sh = ShaderTestScene()
    s.push(sh)
    assert s.current() is sh
    assert s.current().state_id() == SHADER_TEST_STATE_ID
    assert len(s) == 2
    popped = s.pop()
    assert popped is sh
    assert s.current() is g
    assert s.current().state_id() == STATE_PLAYING


def test_shader_test_scene_render_no_crash():
    """ShaderTestScene.render() runs without raising (fallback path or GL path)."""
    sh = ShaderTestScene()
    render_ctx = MagicMock()
    render_ctx.screen = MagicMock()
    render_ctx.font = MagicMock()
    render_ctx.font.render.return_value.get_rect.return_value = MagicMock()
    render_ctx.big_font = MagicMock()
    render_ctx.big_font.render.return_value.get_rect.return_value = MagicMock()
    render_ctx.width = 800
    render_ctx.height = 600
    sh.render(render_ctx, None, {})
