You are Cursor working on my existing Pygame project (game.py / game_app.py, scenes/, screens/, shader_effects/, telemetry/, etc.).

GOAL (high level)
- Make the architecture cleaner and more maintainable WITHOUT breaking behavior:
  - Tame and decompose game.py (event handling, main loop, initialization, level geometry).
  - Finish the migration to the SceneStack-based scene system (scenes/), and retire legacy screens/ use.
  - Centralize telemetry and GPU capability detection behind small APIs.
  - Replace ad-hoc print debugging with logging.
  - Add focused tests for scene transitions and shader registry.
  - Improve packaging/entrypoint ergonomics for running and building the game.

GLOBAL RULES
- Preserve existing behavior. If something might be behavior-breaking, keep it behind a flag or TODO and stay conservative.
- Prefer small, focused refactors inside each step, but keep working through this prompt in order.
- Reuse existing types and helpers (GameState, UiState, Scene, SceneTransition, SceneStack, AppContext, etc.) instead of inventing new patterns.
- Keep names and file locations that already exist when possible; if you create new files, keep them in sensible folders (config/, telemetry/, etc.).
- Use existing style and formatting (black/PEP8-ish); keep type hints where already used.
- After major changes, run the test suite and basic game start to ensure nothing is obviously broken.

================================================================================
STEP 1 – Split event handling in game.py into composable helpers
================================================================================

1. Open game.py.

2. Locate the large `_handle_events(...)` function. It currently:
   - Iterates over `pygame.event.get()`
   - Handles QUIT / window events
   - Delegates some input to the current scene / SceneStack
   - Handles legacy `game_state.current_screen` / STATE_* logic
   - Handles pause/menu/high-score/name-input, shader toggles, control-remap logic, etc.

3. Refactor `_handle_events(...)` into three helpers, all in game.py:

   - `def handle_global_events(events, ctx, game_state, ui_state, scene_stack, screen_ctx) -> bool:`
     - Purpose: handle events that apply globally, regardless of which scene is active.
     - Responsibilities:
       - Handle `pygame.QUIT` and any global kill-switch events. Return `False` if we should stop running, `True` otherwise.
       - Handle window close, maybe alt+F4 or platform-specific quit events if present.
       - Keep this function PURELY about “does the game keep running?” and truly global shortcuts (if any exist).

   - `def handle_scene_events(events, ctx, game_state, ui_state, scene_stack, screen_ctx, previous_game_state) -> "SceneTransition | None":`
     - Purpose: delegate events to the active scene / SceneStack in the modern system.
     - Responsibilities:
       - Retrieve the current scene from the scene stack.
       - If a scene exists and supports it, call `scene.handle_input_transition(...)` (or whatever the current scene API is) passing:
         - ctx, game_state, ui_state (and any other arguments it expects).
       - Collect and return a `SceneTransition` object (or None) describing what should happen (push, pop, quit, replace, none).
       - Do NOT handle legacy `game_state.current_screen` states here.

   - `def handle_legacy_state_events(events, ctx, game_state, ui_state, screen_ctx) -> None:`
     - Purpose: temporarily house legacy input code that still uses `game_state.current_screen`, `STATE_CONTROLS`, `STATE_NAME_INPUT`, etc.
     - Responsibilities:
       - Move the legacy input handling that is conditional on `game_state.current_screen` or STATE_* constants into this function.
       - Keep behavior identical, just extracted out of `_handle_events`.
       - Add a clear comment at the top like:
         - `# TODO: This function contains legacy screen-based input handling. Once all screens are migrated to scenes, this should be removed.`

4. Rewire `_handle_events(...)` into a thin coordinator using these helpers:

   - Signature should stay the same as before so the rest of the code doesn’t break.
   - Inside `_handle_events(...)`:
     - Call `handle_global_events`. If it returns `False`, propagate that up (game loop should stop).
     - Call `handle_scene_events` and capture any returned `SceneTransition`.
     - Call `handle_legacy_state_events` for now (until screens are fully migrated).
     - Return:
       - The “running” boolean, and
       - The `SceneTransition` (if this is how it previously worked), or whatever the previous interface was.
     - Match the previous calling code so the loop logic doesn’t change.

5. Make sure `_handle_events` has a docstring explaining this structure and the migration path.

================================================================================
STEP 2 – Finish migration to SceneStack-based scenes and retire legacy screens
================================================================================

Goal: Make `scenes/` the single source of truth for menus, gameplay, pause, and other UI; minimize and eventually remove `screens/` from game flow.

1. Inspect the following:
   - `scenes/gameplay.py`, `scenes/pause.py`, `scenes/title.py`, `scenes/high_scores.py`, `scenes/name_input.py`, `scenes/shader_test.py`, `scenes/shader_settings.py` (or similarly named).
   - `screens/gameplay.py`, `screens/pause.py`, `screens/high_scores.py`, `screens/name_input.py`, etc.
   - The constants / enums representing states: `STATE_MENU`, `STATE_TITLE`, `STATE_PAUSED`, `STATE_HIGH_SCORES`, `STATE_NAME_INPUT`, etc.

2. For each “legacy screen” state that’s still used in `game_state.current_screen` logic:
   - Confirm there exists a corresponding scene class in `scenes/` **or** create one by migrating logic from the associated `screens/` module.

3. Migration for each screen → scene:
   - If the scene file already exists:
     - Verify it fully handles:
       - Input
       - Update
       - Render
     - Move any remaining logic from the corresponding `screens/` module into the scene.
   - If a scene file does NOT exist:
     - Create a new scene in `scenes/` with a `Scene`-like base class or whatever pattern is already used.
     - Port code from the matching `screens` module, preserving behavior.

   - For each scene:
     - Ensure it exposes a consistent API:
       - `handle_input_transition(...)` (or whatever the current standard is).
       - `update(...)`
       - `render(...)`
       - `enter(...)` / `exit(...)` if the stack model uses them.

4. Open `_apply_scene_transition(...)` in game.py:
   - Ensure all pushes/pops/replacements use the SceneStack and the scene classes in `scenes/`.
   - Remove / reduce any code branches that set `game_state.current_screen` to “pseudo screens” when we can express them as Scenes instead.
   - For transitions like:
     - Pause
     - High scores
     - Name input
     - Shader test / shader settings
     - Title/menu
     - Victory/defeat
     - Make them all map explicitly to `SceneTransition` objects that push/pop/replace Scenes.

5. Once scenes are fully handling these responsibilities:
   - Gradually remove logic that depends on `game_state.current_screen` for high-level flow.
   - Keep `game_state.current_screen` only if it is genuinely needed for lower-level logic, or mark it as deprecated and add TODOs.

6. After all this, if `screens/` is no longer referenced anywhere in game flow:
   - Either:
     - Delete the `screens/` package entirely, **or**
     - Move it to a `legacy/` folder and mark it as deprecated, making sure nothing imports it at runtime.

7. Run the test suite and also manually:
   - Launch the game.
   - Navigate title → start game → pause → resume → high scores → name entry → shader test/settings (if applicable).
   - Ensure all transitions still work as before.

================================================================================
STEP 3 – Slim down main() and the run loop via GameApp
================================================================================

Goal: Move main loop plumbing and coordination into a “GameApp”-like object rather than having everything live in `game.py`.

1. Open `game_app.py` (or the existing file that holds the app/game wrapper logic).

2. Inspect the current contents; if there is already a `GameApp` or similar class, enhance it. If not, create one that encapsulates:

   - `ctx` (AppContext)
   - `game_state`
   - `ui_state`
   - `scene_stack`
   - `screen_ctx` / rendering context
   - Clock and timing (pygame.time.Clock or equivalent)
   - Telemetry writer / config, if appropriate.

3. Move the core loop logic currently in game.py’s `_run_loop(...)` into methods on the GameApp-like class. For example:

   - `def process_events(self) -> bool:` – calls `_handle_events` (or the refactored version), returns whether to keep running.
   - `def update(self, dt: float) -> None:` – runs simulation (systems, enemy AI, bullet updates, etc.).
   - `def render(self) -> None:` – clears screen, draws game/menus/shaders, flips display.

   Keep the existing logic and behavior, just refactor the location and structure.

4. Refactor game.py’s `_run_loop(...)` to become a thin wrapper that delegates to the GameApp instance, or better, move it entirely into `GameApp.run()`:

   - `def run(self) -> None:` – contains the game loop:
     - `clock = pygame.time.Clock()`
     - `while running:`
       - `dt = clock.tick(target_fps) / 1000.0`
       - `running = self.process_events()`
       - `self.update(dt)`
       - `self.render()`

5. Refactor `main()` in game.py so it:
   - Initializes Pygame and any global settings (or delegate that into GameApp if more appropriate).
   - Builds the `AppContext` and initial `GameState` / `UiState`.
   - Constructs a `GameApp(...)` instance with these objects.
   - Calls `app.run()`.

   Example structure (adapt to fit existing patterns):

   ```python
   def main() -> None:
       pygame.init()
       ctx = create_app_context()  # existing helper, if present
       game_state, ui_state, scene_stack, screen_ctx = bootstrap_game_state_and_scenes(ctx)
       app = GameApp(ctx, game_state, ui_state, scene_stack, screen_ctx)
       app.run()
