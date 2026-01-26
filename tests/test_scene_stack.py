"""Tests that the SceneStack and scene transitions behave as expected."""
from __future__ import annotations

import pytest

from constants import STATE_PLAYING, STATE_PAUSED, STATE_HIGH_SCORES, STATE_NAME_INPUT
from scenes import SceneStack, GameplayScene, PauseScene, HighScoreScene, NameInputScene, ShaderTestScene


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
