"""Player vs pickups: collection and effect application."""
from __future__ import annotations


def handle_pickup_player_collisions(state, ctx: dict) -> None:
    """Collect pickups that overlap the player; run collection effect and apply effect."""
    player = state.player_rect
    create_effect = ctx.get("create_pickup_collection_effect")
    apply_effect = ctx.get("apply_pickup_effect")
    if not player or not apply_effect:
        return
    for pickup in state.pickups[:]:
        if player.colliderect(pickup["rect"]):
            if create_effect:
                create_effect(pickup["rect"].centerx, pickup["rect"].centery, pickup["color"], state)
            apply_effect(pickup["type"], state)
            state.pickups.remove(pickup)
