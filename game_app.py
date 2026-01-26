"""
GameApp: owns the main loop, GameState, AppContext, and SceneStack.
game.py remains the thin entrypoint that creates GameApp() and calls app.run().
"""
from __future__ import annotations


class GameApp:
    """Owns game state, context/config, scene stack, and the Pygame main loop."""

    def __init__(self) -> None:
        # Import here to avoid circular import (game imports GameApp, GameApp uses game)
        import game as game_module
        r = game_module._create_app()
        self.ctx = r.ctx
        self.game_state = r.game_state
        self.scene_stack = r.scene_stack
        self.fps = r.fps
        self.fixed_dt = r.fixed_dt
        self.max_sim_steps = r.max_sim_steps
        self.update_simulation = r.update_simulation
        self.sync_scene_stack = r.sync_scene_stack
        self.simulation_accumulator = r.simulation_accumulator

    def run(self) -> None:
        """Run the main loop (event handling, update, render)."""
        import game as game_module
        game_module._run_loop(self)
