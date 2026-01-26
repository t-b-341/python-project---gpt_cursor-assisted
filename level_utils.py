"""Level/setup helper functions. Used by game.py for block filtering and enemy cloning."""
from __future__ import annotations

import pygame

from config_enemies import ENEMY_TEMPLATES
from enemies import make_enemy_from_template


def filter_blocks_no_overlap(block_list: list[dict], all_other_blocks: list[list[dict]], player_rect: pygame.Rect) -> list[dict]:
    """Filter blocks to remove those too close to player and overlapping with other blocks."""
    filtered = []
    player_center = pygame.Vector2(player_rect.center)
    player_size = max(player_rect.w, player_rect.h)  # Use larger dimension (28)
    min_block_distance = player_size * 10  # 10x player size = 280 pixels

    for block in block_list:
        block_rect = block["rect"]
        block_center = pygame.Vector2(block_rect.center)

        # Check distance from player
        if block_center.distance_to(player_center) < min_block_distance:
            continue

        # Check collision with player
        if block_rect.colliderect(player_rect):
            continue

        # Check collision with other blocks
        overlaps = False
        for other_block_list in all_other_blocks:
            for other_block in other_block_list:
                if block_rect.colliderect(other_block["rect"]):
                    overlaps = True
                    break
            if overlaps:
                break

        # Check collision with other blocks in same list (prevent self-overlap)
        if not overlaps:
            for other_block in block_list:
                if other_block is not block and block_rect.colliderect(other_block["rect"]):
                    overlaps = True
                    break

        if not overlaps:
            filtered.append(block)

    return filtered


def clone_enemies_from_templates() -> list[dict]:
    # Kept for compatibility but waves use start_wave() instead.
    return [make_enemy_from_template(t, 1.0, 1.0) for t in ENEMY_TEMPLATES]
