"""
Central registry defining the order in which gameplay simulation systems are run each frame.

Convention: each system exposes update(state, dt). Context (e.g. level geometry, callables)
is provided via state.level_context so systems stay stateless and order is explicit here.

Update order is significant:
  1. movement — applies player/enemy/bullet motion; must run before collision so positions are current.
  2. collision — resolves hits, damage, pickups, teleporters; must run after movement, before spawn so
     spawn can see latest kills and before AI so AI sees current projectile/entity positions.
  3. spawn — wave timers, spawner minions, next-wave triggers; runs after collision so “enemies
     cleared” and spawn decisions use up-to-date state.
  4. ai — enemy and friendly AI (shooting, targeting); runs last so it sees final positions and
     spawn state for the step.

Telemetry is not part of the fixed-step simulation; it is driven from the main loop (position
sampling, tick/flush). Systems that need to log do so via callbacks in level_context or app context.
"""
from __future__ import annotations

from .movement_system import update as movement_update
from .collision_system import update as collision_update
from .spawn_system import update as spawn_update
from .ai_system import update as ai_update

# Ordered list of systems run each fixed-step simulation tick. Do not reorder without
# considering movement → collision → spawn → ai dependencies above.
SIMULATION_SYSTEMS = [
    movement_update,
    collision_update,
    spawn_update,
    ai_update,
]
