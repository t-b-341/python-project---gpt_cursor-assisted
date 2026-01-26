"""
Tests for audio_system: volume/mute setters and robustness of play_sfx/play_music
when assets are missing.
"""
from __future__ import annotations

import pytest

import pygame

from systems import audio_system


@pytest.fixture(autouse=True)
def _setup():
    """Pygame and mixer init so volume/music calls are safe."""
    if not pygame.get_init():
        pygame.init()
    audio_system.init_mixer()


def test_volume_setters_reflect_state():
    """Set SFX and music volume; getters reflect the updated state."""
    audio_system.set_sfx_volume(0.5)
    assert audio_system.get_sfx_volume() == 0.5
    audio_system.set_music_volume(0.3)
    assert audio_system.get_music_volume() == 0.3


def test_mute_setters_reflect_state():
    """Toggle mute; is_muted_sfx / is_muted_music reflect state."""
    audio_system.set_muted(sfx=True, music=False)
    assert audio_system.is_muted_sfx() is True
    assert audio_system.is_muted_music() is False
    audio_system.set_muted(sfx=False, music=True)
    assert audio_system.is_muted_sfx() is False
    assert audio_system.is_muted_music() is True
    audio_system.unmute_all()
    assert audio_system.is_muted_sfx() is False
    assert audio_system.is_muted_music() is False


def test_play_sfx_nonexistent_does_not_raise():
    """play_sfx with nonexistent sound does not raise (muted or unmuted)."""
    audio_system.set_muted(sfx=False)
    audio_system.play_sfx("nonexistent_test_sound")
    audio_system.set_muted(sfx=True)
    audio_system.play_sfx("nonexistent_test_sound")


def test_play_music_nonexistent_does_not_raise():
    """play_music with nonexistent track does not raise."""
    audio_system.play_music("nonexistent_test_music", loop=True)
    audio_system.play_music("nonexistent_test_music", loop=False)


def test_play_music_nonexistent_handles_loop_args():
    """play_music with missing path accepts loop=True and loop=False without crashing."""
    r1 = audio_system.play_music("nonexistent_test_music", loop=True)
    r2 = audio_system.play_music("nonexistent_test_music", loop=False)
    assert r1 is False
    assert r2 is False
