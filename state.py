"""Game state container for core game lists."""
from dataclasses import dataclass, field


@dataclass
class GameState:
    """Container for core game lists and state.
    
    This is a first-step refactoring to group related game data.
    Only a subset of global lists are included initially.
    """
    enemies: list = field(default_factory=list)
    player_bullets: list = field(default_factory=list)
    enemy_projectiles: list = field(default_factory=list)
    friendly_projectiles: list = field(default_factory=list)
