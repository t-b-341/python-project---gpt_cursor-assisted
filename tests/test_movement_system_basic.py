"""Basic tests for the movement system: player moves with input and is blocked by walls.

Uses minimal GameState and LevelState. No Pygame display; conftest sets SDL_VIDEODRIVER=dummy.
"""
from __future__ import annotations

import pygame
import pytest

from level_state import LevelState
from state import GameState
from systems.movement_system import update as movement_update


def _make_move_player(level: LevelState, width: int, height: int):
    """Minimal move_player that blocks on static_blocks and clamps to [0,width] x [0,height]."""

    def move_player(player_rect: pygame.Rect, move_x: int, move_y: int) -> None:
        block_rects = [b.get("rect", b) for b in level.static_blocks]
        for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
            if axis_dx == 0 and axis_dy == 0:
                continue
            player_rect.x += axis_dx
            player_rect.y += axis_dy
            hit = any(player_rect.colliderect(r) for r in block_rects)
            if hit:
                player_rect.x -= axis_dx
                player_rect.y -= axis_dy
            else:
                player_rect.x = max(0, min(player_rect.x, width - player_rect.w))
                player_rect.y = max(0, min(player_rect.y, height - player_rect.h))

    return move_player


def _make_clamp(width: int, height: int):
    def clamp(r: pygame.Rect) -> None:
        r.x = max(0, min(r.x, width - r.w))
        r.y = max(0, min(r.y, height - r.h))

    return clamp


@pytest.fixture
def screen_size():
    return 800, 600


@pytest.fixture
def level_empty(screen_size):
    w, h = screen_size
    return LevelState(
        static_blocks=[],
        trapezoid_blocks=[],
        triangle_blocks=[],
        destructible_blocks=[],
        moveable_blocks=[],
        giant_blocks=[],
        super_giant_blocks=[],
        hazard_obstacles=[],
    )


@pytest.fixture
def level_with_wall(screen_size):
    w, h = screen_size
    # Wall immediately to the right of player at (100,100) size 40x40 -> right edge 140.
    # Wall left edge at 141 so one step (e.g. 5 px) would overlap and get blocked.
    wall = pygame.Rect(141, 80, 40, 120)
    return LevelState(
        static_blocks=[{"rect": wall}],
        trapezoid_blocks=[],
        triangle_blocks=[],
        destructible_blocks=[],
        moveable_blocks=[],
        giant_blocks=[],
        super_giant_blocks=[],
        hazard_obstacles=[],
    )


@pytest.fixture
def game_state_empty(screen_size, level_empty):
    w, h = screen_size
    state = GameState()
    state.player_rect = pygame.Rect(100, 100, 40, 40)
    state.player_speed = 300
    state.move_input_x = 0
    state.move_input_y = 0
    state.is_jumping = False
    state.speed_mult = 1.0
    state.player_stat_multipliers = {"speed": 1.0}
    state.level = level_empty
    state.level_context = {
        "move_player": _make_move_player(level_empty, w, h),
        "clamp": _make_clamp(w, h),
        "width": w,
        "height": h,
    }
    return state


@pytest.fixture
def game_state_with_wall(screen_size, level_with_wall):
    w, h = screen_size
    state = GameState()
    state.player_rect = pygame.Rect(100, 100, 40, 40)
    state.player_speed = 300
    state.move_input_x = 0
    state.move_input_y = 0
    state.is_jumping = False
    state.speed_mult = 1.0
    state.player_stat_multipliers = {"speed": 1.0}
    state.level = level_with_wall
    state.level_context = {
        "move_player": _make_move_player(level_with_wall, w, h),
        "clamp": _make_clamp(w, h),
        "width": w,
        "height": h,
    }
    return state


class TestMovementNoGeometry:
    """Player moves as expected when there is no blocking geometry."""

    def test_player_moves_right(self, game_state_empty, screen_size):
        w, h = screen_size
        state = game_state_empty
        state.move_input_x = 1
        state.move_input_y = 0
        dt = 1.0 / 60.0
        x_before = state.player_rect.x

        movement_update(state, dt)

        assert state.player_rect.x > x_before
        assert state.player_rect.y == 100

    def test_player_moves_down(self, game_state_empty, screen_size):
        w, h = screen_size
        state = game_state_empty
        state.move_input_x = 0
        state.move_input_y = 1
        dt = 1.0 / 60.0
        y_before = state.player_rect.y

        movement_update(state, dt)

        assert state.player_rect.y > y_before
        assert state.player_rect.x == 100

    def test_player_stays_when_no_input(self, game_state_empty):
        state = game_state_empty
        state.move_input_x = 0
        state.move_input_y = 0
        dt = 0.016
        x_before, y_before = state.player_rect.x, state.player_rect.y

        movement_update(state, dt)

        assert state.player_rect.x == x_before
        assert state.player_rect.y == y_before


class TestMovementBlockedByWall:
    """Player is blocked when a wall is in the movement path."""

    def test_player_blocked_when_moving_into_wall(self, game_state_with_wall, screen_size):
        w, h = screen_size
        state = game_state_with_wall
        # Player at (100,100) right=140; wall at (141,80) so first step right hits it.
        state.move_input_x = 1
        state.move_input_y = 0
        dt = 1.0 / 60.0
        x_before = state.player_rect.x
        assert x_before == 100

        movement_update(state, dt)

        # Must be blocked: wall left is 141, player right must stay < 141 (or we revert to ~100)
        assert state.player_rect.right <= 141

    def test_player_can_still_move_parallel_to_wall(self, game_state_with_wall, screen_size):
        w, h = screen_size
        state = game_state_with_wall
        state.move_input_x = 0
        state.move_input_y = 1
        dt = 1.0 / 60.0
        y_before = state.player_rect.y

        movement_update(state, dt)

        assert state.player_rect.y > y_before
        assert state.player_rect.x == 100
