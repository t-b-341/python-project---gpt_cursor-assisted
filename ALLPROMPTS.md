You are an expert Python game developer helping refactor a Pygame project.

Repository context:
- The main game loop and a lot of logic live in game.py.
- There is a GameState dataclass in state.py that already stores some lists like enemies, player_bullets, enemy_projectiles, friendly_projectiles.
- There are still many global variables and module-level mutable state scattered across game.py (and possibly other modules) that track things like score, timers, active pickups, waves, etc.

Goal:
Refactor the project so that ALL core mutable game state is held inside the GameState object (in state.py), instead of as module-level globals or ad-hoc mutable structures.

Concrete tasks:
1. Scan game.py (and other relevant modules) for module-level mutable state that represents ongoing game state, such as:
   - lists of enemies, allies, projectiles, pickups
   - player stats, score, game timers
   - current wave, difficulty state, run/session info
   - any other “current game session” values that change over time
2. Add appropriate fields to GameState in state.py to hold these values.
   - Use type hints.
   - Use sensible defaults and field(default_factory=...) where appropriate.
3. Refactor game.py and other modules to:
   - Stop using these globals directly.
   - Instead, access and mutate them through a GameState instance.
   - Pass GameState explicitly into functions that need it rather than relying on globals.
4. Ensure that the main loop in game.py clearly constructs a single GameState instance at startup, and that this instance is passed down into all functions that operate on game state.
5. Do NOT change gameplay behavior or tuning; this should be a pure refactor.

Constraints:
- Keep the public behavior of the game identical.
- Do not introduce new features.
- Preserve compatibility with existing profiling and telemetry code.
- Keep the refactor incremental and readable: prefer small, clear changes over clever patterns.

Deliverables:
- Updated state.py with a richer GameState dataclass holding all mutable game state.
- Updated game.py and any other affected modules so that they no longer rely on global mutable state and instead operate on the GameState instance.
- Brief code comments where appropriate to clarify the intent of the new GameState fields.
X#------------------------------------------------------------------------------------------------------------------------------------------------------------X
You are an expert game engineer helping modularize a Pygame project.

Current state:
- game.py is still very large and contains:
  - The main loop
  - Input handling
  - Game state updates
  - Rendering logic
  - Menu / pause / high-scores / other screen logic in one place.
- There is already a GameState object in state.py, and many subsystems like rendering.py, enemies.py, telemetry.py, etc.

Goal:
Split game.py by responsibilities into:
1) "Screens" (e.g., menu, gameplay, pause, high scores)
2) "Systems" (e.g., input, movement, collision, spawning, AI, telemetry integration)

Concrete tasks:

1. Identify high-level game states / screens in game.py, such as:
   - Main menu
   - In-game / gameplay
   - Pause
   - High scores screen
   - Any other distinct UI/game screens

2. Create a screens/ package with modules like:
   - screens/menu.py
   - screens/gameplay.py
   - screens/pause.py
   - screens/high_scores.py
(Exact filenames can be adjusted to match existing state names.)

3. For each screen module:
   - Extract functions like: handle_events(state, events, controls), update(state, dt), render(state, screen).
   - Move the corresponding logic from game.py into the appropriate screen module.
   - Keep the signatures simple: they should operate on GameState and any shared objects like screen, controls, etc.

4. In game.py:
   - Replace the screen-specific inlined logic with a simple dispatcher that:
     - Tracks the current screen/state
     - Calls current_screen.handle_events(...)
     - Calls current_screen.update(...)
     - Calls current_screen.render(...)

5. Identify cross-cutting “system” logic that is not specific to a single screen, such as:
   - Movement updates
   - Collision detection that applies during gameplay
   - Enemy spawning / wave updates
   - Telemetry logging
   - Possibly AI logic
   Place those into a systems/ package, with modules like:
   - systems/movement_system.py
   - systems/collision_system.py
   - systems/spawn_system.py
   - systems/ai_system.py
   - systems/telemetry_system.py

6. In the gameplay screen module (screens/gameplay.py), orchestrate these systems:
   - Define a list of systems
   - In update(state, dt), iterate through them and call system.update(state, dt).

Constraints:
- Do not change gameplay behavior, keybinds, or visual output.
- No new features; this is purely a structural refactor.
- Reuse existing helper functions from rendering.py, enemies.py, etc. where it makes sense.
- Ensure imports are clean and there are no circular imports.

Deliverables:
- A screens/ directory with separate modules for each major screen.
- A systems/ directory with clearly defined system modules.
- A simplified game.py that mainly:
  - Initializes pygame and GameState
  - Chooses the starting screen
  - Runs the loop by delegating to the current screen.

X------------------------------------------------------------------------------------------------------------------------------------------------------------X
You are an expert Python engineer specializing in telemetry and logging systems.

Current state:
- telemetry.py is a very large file that handles:
  - Database setup and schema
  - Event logging (shots, enemies, runs, etc.)
  - Possibly some analysis or querying
- The main game calls into telemetry.py to record various events.

Goal:
Refactor telemetry.py into a small, cohesive telemetry package with focused modules and a clean public interface.

Target structure (can be adjusted slightly if needed):
- telemetry/__init__.py
- telemetry/schema.py      (table definitions, schema creation/migration)
- telemetry/events.py      (event dataclasses or small value objects)
- telemetry/writer.py      (functions to log events to the DB)
- telemetry/reader.py      (optional: querying / analysis helpers, if present)

Concrete tasks:

1. Scan telemetry.py and categorize its contents into:
   - Schema / setup / connection handling
   - Event type definitions or constants
   - Functions that record events (log_shot, log_enemy_state, log_run, etc.)
   - Any querying / analysis code

2. Create a telemetry/ package and move code:
   - Put DB connection setup and table creation into telemetry/schema.py.
   - Put any event-specific small structures, enums, or dataclasses into telemetry/events.py.
   - Put all write-oriented functions into telemetry/writer.py.
   - Put any analysis / read-oriented helpers into telemetry/reader.py (if they exist).

3. In telemetry/__init__.py, expose a small, clean API for the rest of the game:
   For example:
   - init_telemetry(db_path: str) -> None
   - log_shot(state, bullet) -> None
   - log_enemy_state(state, enemy) -> None
   - end_run(state) -> None
   Internally these can call into schema.py, writer.py, etc.

4. Update all call sites in the game:
   - Replace direct imports from telemetry.py with imports from the new telemetry package API.
   - Ensure that gameplay code calls high-level telemetry functions and does not directly manipulate the DB or low-level details.

Constraints:
- Keep the database schema and actual logged data identical; this should NOT break existing telemetry files.
- Do not remove or change columns.
- No new gameplay behavior or logging behavior, only restructuring.
- Keep module responsibilities clear and avoid circular imports.

Deliverables:
- A telemetry/ package with schema.py, events.py, writer.py, reader.py (as needed), and __init__.py.
- Updated imports and calls across the project that use the new telemetry API.
- Minimal comments explaining the purpose of each module.


#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an expert game architect helping to introduce an Entity component to a Python/Pygame project.

Current state:
- There are separate concepts for player, enemies, allies, projectiles, etc.
- Logic for updating and drawing these entities is spread across several modules (e.g., enemies.py, maybe player logic in game.py, projectiles somewhere else).
- GameState currently holds lists like enemies, player_bullets, enemy_projectiles, friendly_projectiles.

Goal:
Introduce a common Entity base class (or small hierarchy) and unify core behavior patterns (update/draw/position/health) to make the code easier to maintain and extend.

Concrete tasks:

1. Create a new module, e.g., entities/base.py, with something like:

   - class Entity:
       - fields like x, y, hp, alive/active flag
       - basic methods: update(self, dt, state), draw(self, screen)

   You may use an abstract base class or simple base with default no-op methods.

2. Refactor existing entity-like classes (player, enemy, ally, projectile) to inherit from Entity where reasonable:
   - Ensure they implement or override update() and draw() as needed.
   - Reuse shared logic wherever possible (e.g., movement helpers, taking damage, marking dead).

3. Adjust GameState:
   - Option 1: Keep existing separate lists (enemies, projectiles, etc.) but ensure each list holds subclasses of Entity.
   - Option 2: Introduce a general entities list in addition to category lists.
   Choose the simplest approach that minimizes disruption but improves structure.

4. In the core gameplay update loop (likely in the gameplay screen or systems), introduce unified entity update logic:
   - E.g., for each entity in relevant lists: entity.update(dt, state).

5. Similarly, unify draw logic:
   - For each entity that needs drawing, call entity.draw(screen).

Constraints:
- Do NOT change gameplay behavior, difficulty, or visuals.
- Try not to change public function signatures that are widely used, unless necessary to support the Entity abstraction.
- Keep the base Entity minimal and focused; this is about structure, not a full ECS overhaul.

Deliverables:
- New entities/base.py (and possibly entities/player.py, entities/enemy.py, etc., if you decide to reorganize).
- Updated entity classes inheriting from Entity.
- Updated GameState and game loop code that use the unified entity pattern for update/draw.

#------------------------------------------------------------------------------------------------------------------------------------------------------------

You are acting as a repository hygiene and tooling expert for a Python game project.

Current state:
- The repo contains build artifacts, compiled extension outputs, profiling files, and __pycache__ folders, e.g.:
  - build/lib.win-amd64-cpython-312/...
  - build/temp.win-amd64-...
  - profiling_results.prof
  - profiling_results.txt
  - __pycache__/ directories
  - Possibly *.pyd or *.so files from the C extension build
  - Possibly *.db files depending on how telemetry/high scores are stored

Goal:
Ensure that only source and intentionally-versioned assets are tracked in Git, and that all build/runtime artifacts are ignored via .gitignore.

Concrete tasks:

1. Inspect the current repository contents for:
   - build/ and dist/ directories
   - __pycache__/ directories and *.pyc files
   - profiling *.prof files and profiling_results*.txt
   - compiled extension binaries (*.pyd, *.so, *.dll) that are generated from setup.py
   - telemetry or runtime-generated SQLite databases (*.db)

2. Update .gitignore to exclude:
   - __pycache__/
   - *.pyc
   - build/
   - dist/
   - *.egg-info/
   - *.prof
   - profiling_results*.txt
   - Compiled extension binaries (e.g. *.pyd, *.so) if they are build artifacts
   - Any runtime-generated *.db files that should not be versioned (leave in only specific DB files if they are meant to be shipped as initial data)

3. Remove tracked files that should be ignored:
   - For any currently tracked build artifacts or caches, update the Git index to stop tracking them (but don’t delete generated files needed for local runs):
     - e.g., git rm --cached path/to/file-or-directory

4. Ensure the repo remains buildable:
   - The source and setup.py should still allow rebuilding the extension when needed.
   - The game should still run after a fresh clone followed by appropriate install/build commands.

Constraints:
- Do not remove any essential asset files (images, sounds, fonts, configs).
- If any *.db file is truly required (e.g., a default high-scores DB or baseline telemetry schema), do NOT ignore that specific file; instead, only ignore the dynamic/runtime ones or use a naming pattern.

Deliverables:
- Updated .gitignore with appropriate ignore rules for Python, Pygame, and C-extension build artifacts.
- A clean repository tree without extraneous build/cache/profiling files tracked in Git.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are a Python testing expert helping add a minimal but useful test suite to a Pygame-based game project.

Current state:
- There is no (or almost no) automated testing.
- Core game logic includes:
  - Enemy movement and AI behavior
  - Projectile motion and collision logic
  - Wave/spawn logic
  - Telemetry DB setup and basic logging

Goal:
Introduce a very small set of tests (e.g., using pytest) that provide guardrails for future refactors, focusing on pure logic that does not depend on Pygame’s display.

Concrete tasks:

1. Add a tests/ directory at the repository root with an empty __init__.py if needed.

2. Create a small number of focused test modules, for example:
   - tests/test_enemy_behavior.py
   - tests/test_projectiles.py
   - tests/test_spawn_logic.py
   - tests/test_telemetry_init.py

3. Identify pure functions or small units of logic that are deterministic and do not require a graphical display, such as:
   - Functions that compute enemy movement toward the player.
   - Functions that update projectile positions based on velocity and dt.
   - Functions that decide when to spawn new enemies or waves.
   - Telemetry initialization that creates the necessary tables in an in-memory or temporary DB.

4. Write tests that:
   - Instantiate minimal GameState and entities as needed.
   - Call the logic functions (e.g., move_enemy_towards_player, update_projectile, spawn_wave_if_needed).
   - Assert simple, meaningful conditions (e.g., enemy.x moves closer to player.x, new projectiles are spawned under certain conditions, telemetry creates required tables without error).

5. Add a basic test configuration:
   - Optionally include a pytest.ini or pyproject.toml section if useful.
   - Ensure tests can run via `pytest` from the repo root without needing the full graphical game environment.

Constraints:
- Do not overcomplicate the test setup; the goal is 5–15 tests that cover critical logic paths.
- Avoid tests that require opening a Pygame window or running the full main loop.
- Keep tests fast and deterministic.

Deliverables:
- A tests/ directory with a small set of meaningful unit tests.
- The ability to run `pytest` successfully from the project root and have all tests pass.
