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
1-25-26X#------------------------------------------------------------------------------------------------------------------------------------------------------------X
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


X#------------------------------------------------------------------------------------------------------------------------------------------------------------X
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
#------------------------------------------------------------------------------------------------------------------------------------------------------------/
You are an expert game engineer helping to refactor movement logic in a Python/Pygame project.

Current project structure (important pieces):
- game.py still contains much of the main game loop and a lot of movement logic.
- state.py defines a GameState object that holds enemies, bullets, allies, player state, etc.
- entities/ contains base entity and enemy wrappers.
- systems/movement_system.py already exists with an update(state, dt) stub (or minimal logic).
- systems/__init__.py defines GAMEPLAY_SYSTEMS that includes movement_system.update(state, dt) in the main gameplay update.

Goal:
Extract ALL per-frame movement logic from game.py (and any other scattered places, if applicable) and centralize it into systems/movement_system.update(state, dt), so that movement becomes a cohesive system operating on GameState.

Concrete tasks:

1. Identify ALL movement-related logic in game.py (and related modules where appropriate), including but not limited to:
   - Player position updates based on input and velocity.
   - Enemy position updates (chasing player, pathing, drifting, etc.).
   - Projectile / bullet movement for player, enemy, and allied projectiles.
   - Ally movement / orbiting / AI-driven motion if present.
   - Any rect / Vector2 operations that advance positions over time.

2. For each movement chunk:
   - Move that logic into systems/movement_system.py inside update(state, dt).
   - Organize it into small helper functions inside movement_system.py when helpful, for example:
     - _update_player(state, dt)
     - _update_enemies(state, dt)
     - _update_projectiles(state, dt)
     - _update_allies(state, dt)
   - Make each helper operate purely on GameState and any necessary constants; do NOT rely on globals.

3. In game.py (and any other call sites):
   - Remove or simplify the in-place movement code.
   - Ensure the main gameplay loop no longer directly updates positions; instead it just calls movement_system.update(state, dt) via the existing GAMEPLAY_SYSTEMS mechanism.

4. If any movement helpers in other modules (e.g., enemies.py or entities/base.py) are already responsible for moving things:
   - Reuse them from movement_system.update when appropriate.
   - Do NOT duplicate behavior; call the existing logic once, from a clearly defined place.

5. Make sure that:
   - Player, enemies, bullets, allies, and any other moving entities still move exactly as before.
   - Clamp-to-screen or bounds operations remain correct and are still applied (either inside movement_system or via helpers it calls).
   - No visual/gameplay behavior changes; only the location/structure of the code changes.

Constraints:
- Do NOT change the existing gameplay tuning, speeds, trajectories, or behavior.
- Do NOT change the public GameState interface or the GAMEPLAY_SYSTEMS contract.
- Avoid circular imports; if needed, prefer importing entities or helpers inside functions rather than at the top level.

Deliverables:
- A fully implemented systems/movement_system.update(state, dt) that performs all per-frame movement.
- A slimmer game.py where movement logic has been removed and delegated to the movement system.
- Clear, readable helper functions within movement_system.py where appropriate.

#------------------------------------------------------------------------------------------------------------------------------------------------------------/
You are an expert game engineer helping to refactor collision and damage logic in a Python/Pygame project.

Current project structure (important pieces):
- game.py still contains much of the collision handling and damage application logic.
- state.py defines GameState, which includes enemies, bullets/projectiles, player state, pickups, allies, shields/overshields, score, etc.
- entities/ defines base Entity and enemy wrappers (and may later handle more behavior).
- systems/collision_system.py already exists with an update(state, dt) stub (or minimal logic).
- systems/__init__.py defines GAMEPLAY_SYSTEMS that includes collision_system.update(state, dt) in the main gameplay update.

Goal:
Extract ALL collision and damage logic from game.py (and any other scattered locations) and centralize it into systems/collision_system.update(state, dt), so that collision handling is a cohesive system operating on GameState.

Concrete tasks:

1. Identify ALL collision-related logic in game.py, including but not limited to:
   - Player bullets hitting enemies (damage, kills, score multipliers, on-hit effects).
   - Enemy projectiles hitting the player (damage, shields/overshields).
   - Enemies colliding with the player (contact damage, knockback, death, etc.).
   - Allies colliding with enemies or projectiles, if applicable.
   - Pickups colliding with the player (health, overshield, XP, currency, etc.).
   - Any collision checks using rect.colliderect, distance thresholds, or hitbox overlap logic.

2. For each collision/interaction case:
   - Move the logic into systems/collision_system.py within update(state, dt).
   - Organize the code into helper functions for clarity, e.g.:
     - _handle_player_bullet_enemy_collisions(state)
     - _handle_enemy_projectile_player_collisions(state)
     - _handle_enemy_player_collisions(state)
     - _handle_pickup_player_collisions(state)
   - Ensure these helpers:
     - Work entirely through GameState.
     - Mutate state (HP, score, lists of entities, etc.) in the same way as the original game.py code did.

3. In game.py:
   - Remove the inlined collision/damage logic.
   - Ensure that collision handling happens only via collision_system.update(state, dt), invoked through the GAMEPLAY_SYSTEMS loop.

4. Preserve all side effects:
   - Enemy HP / death behavior, including removal from state lists and any death effects.
   - Player HP, shield/overshield depletion, game-over triggers, etc.
   - Score, multipliers, combo counters, streaks.
   - Telemetry calls related to collisions (e.g., logging hits or deaths). If telemetry hooks were embedded in collision logic, move those calls into collision_system.py or into telemetry_system.py via clearly defined hooks, keeping behavior identical.

5. Make sure:
   - Collision outcomes remain exactly the same (no tuning or behavior changes).
   - Order of operations (e.g., which collisions are processed first) remains the same unless it’s provably irrelevant.
   - No new bugs are introduced due to entity removal while iterating; use safe iteration patterns (e.g., iterate over a copy or collect to-remove indices first).

Constraints:
- Do NOT change gameplay behavior, damage values, or outcomes.
- Avoid circular imports; access only what you need via GameState and any existing helper modules (e.g., enemies.py, entities/base.py).
- Maintain clarity: prioritize simple, readable helper functions over clever one-liners.

Deliverables:
- A fully implemented systems/collision_system.update(state, dt) that handles all runtime collisions and associated effects.
- A slimmer game.py where collision logic has been removed and is now delegated to the collision system.
- Well-structured collision helpers inside collision_system.py with descriptive names.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an expert game engineer helping to refactor spawn and wave logic in a Python/Pygame project.

Current project structure (important pieces):
- game.py still contains much of the logic for:
  - spawning enemies
  - managing waves / phases
  - spawning bosses or special enemies
  - scaling difficulty over time
- state.py defines GameState, which includes lists of enemies and other runtime data such as wave counters, timers, difficulty multipliers, etc.
- There is a systems/spawn_system.py module with an update(state, dt) stub (or minimal logic).
- systems/__init__.py defines GAMEPLAY_SYSTEMS that includes spawn_system.update(state, dt) in the main gameplay update loop.

Goal:
Extract ALL spawn / wave / boss / difficulty-scaling logic from game.py (and any other scattered places) and centralize it into systems/spawn_system.update(state, dt) so that spawning and progression become a cohesive system operating on GameState.

Concrete tasks:

1. Identify ALL logic in game.py that is responsible for:
   - Spawning regular enemies and/or special enemy types over time.
   - Managing wave numbers, wave timers, or progression milestones.
   - Spawning bosses or mini-bosses.
   - Scaling difficulty based on time, wave number, score, or other metrics.
   - Any helper functions used exclusively for spawning or wave management.

2. Move this logic into systems/spawn_system.py:
   - Implement update(state, dt) as the single entry point called each frame.
   - Inside this module, create small helpers as needed, for example:
     - _update_wave_timers(state, dt)
     - _spawn_regular_enemies_if_needed(state)
     - _spawn_bosses_if_needed(state)
     - _update_difficulty_scaling(state, dt)
   - Ensure that all changes to the lists of enemies, waves, and difficulty variables are made through GameState.

3. In game.py:
   - Remove or simplify the spawn / wave / boss logic so that the gameplay loop no longer directly spawns enemies.
   - Verify that spawning is invoked solely via spawn_system.update(state, dt), as part of the GAMEPLAY_SYSTEMS list.

4. Reuse existing helpers where appropriate:
   - If enemies.py or other modules have helper functions for constructing enemy objects, use those from spawn_system.py instead of duplicating logic.
   - Keep all enemy-creation behavior (types, starting positions, stats) identical to the original implementation.

5. Preserve ALL gameplay behavior and progression:
   - Wave timing, wave sizes, and enemy types must remain the same.
   - Boss / special enemy appearances and conditions should remain unchanged.
   - Difficulty scaling over time (health, count, speed, etc.) must produce the same outcomes as before.

Constraints:
- Do NOT change gameplay balance, timers, or difficulty.
- Avoid circular imports; prefer importing enemy factory functions or config modules in spawn_system.py instead of reaching back into game.py.
- Keep the code in spawn_system.py cohesive and readable, with clearly named helpers.

Deliverables:
- A fully implemented systems/spawn_system.update(state, dt) that handles all enemy/boss spawning, wave management, and difficulty scaling.
- A slimmer game.py where spawn-related logic has been removed and is now delegated to the spawn system.
- Clear internal helpers inside spawn_system.py with descriptive names and docstrings/comments where appropriate.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an expert game AI engineer helping to refactor AI and decision-making logic in a Python/Pygame project.

Current project structure (important pieces):
- game.py currently contains various logic that determines HOW enemies (and possibly allies or special entities) behave, including:
  - Target selection (e.g., chasing the player, moving toward a point).
  - Behavior modes (e.g., aggressive, strafing, fleeing, orbiting).
  - Special attack patterns or movement patterns driven by AI decisions.
- state.py defines GameState, which includes:
  - Player position / state.
  - Lists of enemies, allies, projectiles, and other entities.
  - Difficulty or phase information that may influence AI behavior.
- There is a systems/ai_system.py module with an update(state, dt) stub (or minimal logic).
- systems/__init__.py defines GAMEPLAY_SYSTEMS that includes ai_system.update(state, dt) in the main gameplay update loop (or it can be added if not already).

Goal:
Extract ALL AI / behavior / decision-making logic from game.py (and any other scattered places) and centralize it into systems/ai_system.update(state, dt), so that entities’ decisions are handled in a cohesive system operating on GameState.

Concrete tasks:

1. Identify ALL AI-related logic in game.py (and related modules), including:
   - Code that decides where enemies should move (toward the player, to certain waypoints, in patterns).
   - Code that chooses whether an enemy should shoot, charge, dodge, or perform some special action.
   - Logic that switches enemy states or behavior modes over time or based on health/wave.
   - Ally or drone behavior, if any (following player, attacking enemies, healing, etc.).

2. Move this decision-making code into systems/ai_system.py:
   - Implement update(state, dt) as the single entry point.
   - Inside ai_system.py, create helpers such as:
     - _update_enemy_ai(state, dt)
     - _update_ally_ai(state, dt)
     - _choose_enemy_targets(state)
     - _update_enemy_behavior_modes(state, dt)
   - Keep the AI logic focused on *decisions* (what entities intend to do: move direction, shoot flags, behavior state), not on the low-level integration of physics or collisions.

3. Coordinate with other systems:
   - If movement_system.update(state, dt) handles the actual movement, AI should set intent (direction, velocity, behavior flags) that movement_system then applies.
   - If spawn_system.update(state, dt) handles creating enemies, AI should not create entities; it should only control existing ones.
   - If telemetry_system or collision_system care about AI state, ensure they still get the same state changes via GameState.

4. In game.py:
   - Remove or simplify direct AI logic (e.g., inline “chase player” movement, shoot-if-close-enough logic).
   - Verify that AI behavior is invoked solely via ai_system.update(state, dt) (through the GAMEPLAY_SYSTEMS list).

5. Maintain existing behavior and difficulty:
   - Enemies must still behave as before: chase, shoot, dodge, etc., at the same times and conditions.
   - Ally behaviors should remain the same where they existed.
   - Do NOT alter tuning (distances, trigger thresholds, probabilities) unless necessary for correctness; copy those values as-is into ai_system.py.

6. Keep the design extendable:
   - Organize AI code so that it’s easy to add new enemy types or behaviors later (e.g., by branching on enemy type or using small strategy functions).
   - Avoid excessive coupling to a specific enemy implementation: use helpers or type checks judiciously.

Constraints:
- Do NOT change how the game “feels” from the player’s perspective; AI should behave identically after the refactor.
- Avoid introducing circular imports; work through GameState and any dedicated config or helper modules (like enemies.py).
- Prefer clear, small helper functions over overly generic abstractions.

Deliverables:
- A fully implemented systems/ai_system.update(state, dt) that handles all runtime AI decisions for enemies (and allies, if present).
- A slimmer game.py where AI logic has been removed and is now delegated to the AI system.
- AI logic that is clearly structured and easy to extend in systems/ai_system.py.

#------------------------------------------------------------------------------------------------------------------------------------------------------------/
You are an expert Python/Pygame engineer helping refactor UI and HUD rendering logic.

Current project structure (important pieces):
- game.py still contains HUD/UI drawing code, including:
  - Score, multipliers, wave info, timers
  - Player health / shield bars
  - Ammo, abilities, cooldown indicators
  - Status text, announcements, popups
  - Boss HP bars or alerts
- rendering.py contains some helper functions but not a complete UI system.
- systems/ exists, but currently lacks a ui/hud module.
- screens/gameplay.py calls into rendering logic directly.

Goal:
Move ALL user interface and HUD rendering logic into a dedicated system module:
    systems/ui_system.py   (or hud_system.py)
and unify it into clean, reusable functions.

Concrete tasks:

1. Identify ALL UI/HUD code paths in game.py and related modules, including:
   - Drawing the player’s HP bar, shield bar, overshield bar.
   - Score display, multiplier, combo UI.
   - Wave or stage announcements.
   - Ammo counts, gadget cooldown meter, ability icons.
   - Boss HP bars or boss warnings.
   - Any UI text (e.g., “Paused”, “New Wave”, “Game Over” overlays).

2. Create systems/ui_system.py with a public function:
       def render(state, screen, ctx) -> None
   (or update/render as needed)
   The system should:
   - Use constants from constants.py / config modules.
   - Use pygame font rendering, shapes, blits, etc.
   - Draw ALL HUD/UI elements on top of the gameplay scene.

3. Move all HUD/UI code out of game.py and screens/gameplay.py.
   In screens/gameplay.py:
   - Gameplay screen should only call ui_system.render(state, screen, ctx)
   - Remove all inline UI drawing.

4. If rendering.py already contains helper functions:
   - Reuse them inside ui_system.py
   - Optionally move UI-specific helpers from rendering.py → ui_system.py for clarity.

5. Maintain the EXACT current visual layout:
   - Same font sizes
   - Same colors
   - Same placement (x,y)
   - Same bars, text, and indicators
   - Same conditional logic (only show certain UI elements in certain states)

6. Keep UI logic separate from game logic:
   - UI should read state but NOT modify it.
   - Any game logic triggered by UI input stays in screen modules.

Constraints:
- Do not change any gameplay behavior or UI appearance.
- Avoid circular imports by limiting ui_system.py dependencies to:
     - pygame
     - constants.py
     - rendering helpers
     - GameState
- Keep ui_system.py easy to extend for future UI additions.

Deliverables:
- A systems/ui_system.py module containing all HUD/UI rendering.
- Updated screens/gameplay.py that delegates UI drawing to this system.
- A slimmer game.py/rendering.py after removing UI/HUD-specific drawing code.


#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are acting as a senior software engineer performing a global cleanup/refactoring pass on the entire Python/Pygame game project.

Goal:
Improve maintainability without changing gameplay logic or behavior.

Perform the following cleanup actions across ALL modules in the repository:

1. **Remove unused imports**
   - Use static analysis to detect unused imports.
   - Delete them unless they are needed for type hints or future hooks.

2. **Remove dead code**
   - Identify functions or classes that are never referenced.
   - Identify leftover helper functions in game.py that are now redundant due to systems.
   - Remove commented-out blocks that are no longer relevant.
   - Remove leftover stub code (e.g., pass blocks for logic that no longer exists).
   - Be cautious: keep anything that is still referenced.

3. **Fix inconsistent naming**
   - If variables or functions violate snake_case for Python, convert them.
   - If some modules/functions still use old names after refactors, align them to the current structure.

4. **Improve type hints**
   - Add appropriate return types, argument types, and dataclass types.
   - Ensure GameState fields are properly annotated.
   - Improve entity type hints (player, enemies, projectiles, pickups).

5. **Improve formatting**
   - Apply PEP8 line widths.
   - Fix spacing, blank lines, and wrapping.
   - Normalize import order (stdlib → third-party → local modules).
   - Fix long dict/list literals using multiline formatting where helpful.

6. **Fix docstrings & comments**
   - Update any outdated docstrings referencing old behavior that was moved.
   - Remove misleading or obsolete comments.
   - Add lightweight docstrings to system update functions for readability.

7. **Clean up TODOs**
   - If TODO comments refer to code that has already moved, clean them.
   - Otherwise, leave valid TODOs intact but clarify them if vague.

8. **Ensure no circular imports**
   - After cleanup, verify imports are stable.
   - If a circular dependency appears, fix by:
       - moving imports inside functions
       - restructuring module usage
       - using forward references in type hints

9. **Preserve behavior exactly**
   VERY IMPORTANT:
   - Do NOT change gameplay logic.
   - Do NOT change timings, math values, tuning, or UI geometry.
   - Do NOT remove calls required for telemetry or profiling.
   - Do NOT break compatibility with the systems architecture.

Deliverables:
- A cleaned, consistent, maintainable codebase.
- No functional differences in gameplay or visuals.
- Better type hints and formatting throughout the repo.
- Smaller and more readable modules.


////#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an expert Python/Pygame rendering engineer helping to clean up and structure the rendering pipeline for a 2D game.

Current project structure (important pieces):
- game.py still orchestrates some rendering responsibilities.
- rendering.py contains various drawing helpers (background, entities, effects, etc.), but is not yet a fully cohesive rendering pipeline.
- systems/ now exists and includes gameplay-related systems (movement, collision, spawn, AI, UI/HUD, telemetry).
- screens/ includes gameplay.py and other screens, some of which still call rendering functions directly.
- A ui_system (or hud_system) is responsible for HUD/UI drawing (or will be, after a previous refactor).
- entities/ defines base Entity classes and wrappers that may implement draw(screen, state).

Goal:
Refactor and clean up the rendering pipeline so that:
- All world/gameplay rendering (background, entities, projectiles, effects) is handled in a small number of clearly defined functions, ideally through a rendering system or central module.
- Draw order, layering, and surface usage are explicit and consistent.
- Screens and systems delegate rendering work instead of hand-drawing ad hoc.

Concrete tasks:

1. **Establish a clear rendering entry point**
   - Choose a single, central function to handle the main gameplay rendering, for example:
       rendering.render_gameplay(state, screen, ctx)
   - This function should:
       - Clear the screen (fill background or draw background image).
       - Draw the world (map, background elements).
       - Draw entities and projectiles in the correct order.
       - Defer HUD/UI rendering to the existing ui_system/hud_system.

2. **Consolidate world rendering logic**
   - Search game.py, screens/gameplay.py, and rendering.py for any code that:
       - Fills the screen with a color or background.
       - Draws enemies, player, allies, bullets/projectiles, pickups, and effects directly.
   - Move or redirect this logic into rendering.py (or a dedicated systems/rendering_system.py if that aligns better with the current architecture).
   - Ensure entities that already implement draw(screen, state) are called via a unified loop that respects draw order.

3. **Make draw order explicit and consistent**
   - Define a clear draw order for gameplay elements, such as:
       1) Background / world
       2) Terrain / static obstacles
       3) Pickups / items
       4) Enemies / allies / player
       5) Projectiles / effects
       6) Overlays (e.g., warning circles, targeting indicators)
       7) HUD/UI (done by ui_system)
   - Implement this ordering in the central rendering entry point.
   - Avoid sprinkling blits in random places; everything should go through the central pipeline.

4. **Clean up surfaces, scaling, and camera usage (if present)**
   - If the game uses an off-screen surface (e.g., a world surface scaled to the window), centralize:
       - Creation of this surface
       - All drawing to that surface
       - The final blit from the surface to the main screen
   - If there is a camera or viewport:
       - Ensure camera transforms (offsets) are applied in a consistent way when drawing entities.
       - Isolate camera logic in one place (e.g., rendering.py or a small camera helper module), not spread throughout the code.

5. **Remove duplicate or unused rendering helpers**
   - In rendering.py and other modules, look for:
       - Functions that are no longer used since the new systems/screens refactor.
       - Functions that duplicate behavior with small differences.
   - Remove dead code and consolidate similar helpers into one canonical implementation where safe.

6. **Coordinate with UI/HUD system**
   - Ensure that gameplay rendering and HUD rendering are clearly separated:
       - World and entities: handled by rendering.py or a rendering system.
       - UI/HUD overlays: handled by ui_system/hud_system, called AFTER world rendering.
   - Screens/gameplay.py should:
       - Call the core rendering function for the world.
       - Then call ui_system.render(state, screen, ctx) (or equivalent).

7. **Make sure rendering is side-effect free (game logic wise)**
   - Ensure rendering functions do NOT modify game logic state (HP, score, timers, etc.).
   - Rendering may read from GameState and context, but must not change them.
   - Any leftover logic in rendering helpers that mutates state should be moved into a proper system (e.g., AI, movement, collision).

8. **Preserve visual output exactly**
   VERY IMPORTANT:
   - Do NOT change visual placement, colors, fonts, or effects unless necessary for consistency.
   - The game should look identical before and after this refactor: same draw order, same UI layout, same styling.
   - Maintain any intentional layering quirks (e.g., certain effects always in front of certain entities) by preserving their effective order.

9. **Apply light cleanup**
   - While touching rendering code, also:
       - Remove unused imports.
       - Add/clarify type hints for major functions (e.g., state: GameState, screen: pygame.Surface).
       - Improve formatting and naming for readability.

Deliverables:
- A clear, centralized rendering pipeline with:
   - One main entry for gameplay/world rendering.
   - Distinct, explicit draw order.
   - Clean separation between world rendering and HUD/UI rendering.
- Screens/gameplay.py and game.py simplified to delegate rendering instead of doing it directly.
- No change in actual visuals or gameplay behavior.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
ai behavior; make it so that enemies don't get stuck on walls
fix texts overlapping when beams are picked up
highlight enemies when there are five or less in a wave
make it so that multiple ally ai can be laid down without deleting the previous ally, and that ally can follow player
remove wave beam
take out beams and replace with ally direction commands where mouse location + click determines which direction the allies will go towards
increase all enemy hp amount x10
make armor drain at 10 hp per second
make walls prevent missiles from going through them
increase enemy rate of fire by 5x


#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an expert Python data viz engineer helping to modularize visualize.py in a Pygame/SQLite telemetry project.

Current state:
- visualize.py is ~1500 lines and currently does ALL of the following:
  - CLI / argument parsing and main()
  - SQLite connection and query helpers
  - Utility functions like table_exists, read_df, safe_numeric, no_data
  - A Page dataclass and a long list of Page(...) definitions
  - ~30+ draw_* functions, each rendering a specific plot
  - A “save all plots to PNGs” function
  - A Matplotlib “single popup, page-through-plots” viewer with keyboard controls

Goal:
Refactor visualize.py into a small entrypoint plus a telemetry_viz package, without changing behavior or output.

Target structure (can be adjusted slightly if needed for simplicity):

- visualize.py                 # tiny: CLI and main()
- telemetry_viz/
    __init__.py
    core.py                    # Page dataclass, pages list/registry
    db_utils.py                # safe_numeric, table_exists, read_df, no_data, GPU helpers
    viewer.py                  # save_pngs, run_single_popup, key handlers, figure setup
    plots_player.py            # movement path/heatmap, velocity, player positions
    plots_damage.py            # damage taken/dealt, heatmaps, death locations
    plots_waves.py             # wave progression, difficulty, survival per wave
    plots_meta.py              # accuracy over runs, damage over runs, performance summary
    plots_misc.py              # bullet shape distribution, zone effectiveness, etc.

Concrete tasks:

1. Create the telemetry_viz/ package and move shared helpers:
   - Move safe_numeric, table_exists, read_df, and no_data out of visualize.py into telemetry_viz/db_utils.py.
   - Update all draw_* functions to import these helpers from telemetry_viz.db_utils.

2. Extract Page and the pages list:
   - Move the Page dataclass and the pages = [Page(...), ...] registry into telemetry_viz/core.py.
   - Make core.py responsible for importing the various draw_* functions from the plot modules and constructing the pages list.

3. Extract viewer logic:
   - Move save_pngs(), run_single_popup(), and any associated helper functions (e.g., key event handlers, figure creation) into telemetry_viz/viewer.py.
   - viewer.py should:
     - Accept (conn, run_id, pages) and handle saving PNGs and the interactive viewer.
     - Not perform argument parsing or DB path resolution.

4. Group draw_* functions into themed modules:
   - Create telemetry_viz/plots_player.py, plots_damage.py, plots_waves.py, plots_meta.py, plots_misc.py.
   - Move the draw_* functions into these modules based on their semantics (player movement, damage, waves, cross-run stats, misc).
   - Ensure each draw_* keeps the same signature: draw_X(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool.

5. Slim down visualize.py:
   - Leave visualize.py as the CLI entry point that:
     - Parses arguments.
     - Opens the SQLite DB.
     - Determines run_id.
     - Imports pages from telemetry_viz.core.
     - Calls save_pngs and optionally run_single_popup from telemetry_viz.viewer.
   - Do not keep any draw_* functions, helpers, or Page definitions in visualize.py.

6. Preserve behavior and output:
   - All plots must still be generated with the same filenames and contents.
   - The interactive page-through viewer should behave identically (same keys, same order).
   - The default list and ordering of Page entries must remain the same.

Constraints:
- Do NOT change plot logic, queries, or JDBC/SQLite behavior; only move code.
- Avoid circular imports by:
  - Having plot modules import db_utils and common helpers.
  - Having core.py import draw_* from plot modules and build the pages list.
  - Having viewer.py import Page (and possibly pages) from core.py.
- Ensure that running `python visualize.py ...` works exactly as before, just with a smaller entry file and a structured telemetry_viz package.

Deliverables:
- New telemetry_viz package with core.py, db_utils.py, viewer.py, and several plots_*.py modules.
- Updated visualize.py that is short, clear, and only orchestrates CLI → DB → telemetry_viz.
- No change in observable behavior, plot ordering, filenames, or viewer controls.

ask if the player would prefer to see data from all runs, or just most recent run, then display what player states they would like to see in visualize.py

#------------------------------------------------------------------------------------------------------------------------------------------------------------/
change all enemies to same color, and make allies follow player around map
increase ally movement speed to 2x current speed
add in an ally type that fires missiles, at one 3 shot burst every 7 seconds, and moves around and can be guided like other ally
right click to change ally movement direction and focus, where player can guide allies. if player doesn't click, allies function as normal
add in teleporter from one half of map to another half of map, treat teleporters like health area spawn, where nothing can overlap with teleporter, except for player
make teleport points green rhomboids with purple border, approximately 1.5x the size of the player


#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
