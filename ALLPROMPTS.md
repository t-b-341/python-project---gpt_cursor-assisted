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
make teleporters be located in top left quadrant, and bottom right quadrant
create enemy classes: ambient, basic, large, super large. ambient is located stationary, and fires rockets every 6 seconds at player, one shot, with the ability for player to dodge out of the way of the rocket. place 3 ambient enemies at the start of each round, randomly, non-overlapping, on the map. basic enemies are the current smallest enemy size, large is the next larger size, with super large 4x the size of large, with super lodge firing rockets, and the ability to set off grenades that only damage the player and allies
Have enemies patrol outer area until player leaves main area
Add shield enemies in that reflect shots back at player, with extra damage, unless player flanks them
lower player health and armor amounts by 0.75x
give bosses 5x more health
add in a flamethrower-type enemy named flamethrower
change cooldown for ally drop to 3 seconds
make rockets purple
make ambient enemy purple
half alt r shield cooldown
at high score screen, add replay option to space/enter
when restarting at in-game menu screen, restart only back to wave 1, not game entirely
add "exit to main menu" screen which brings player to the start of the game


add in a title screen when the player starts the game with "GAME" centered, in large black text, with enter/space to start game, and esc to quit game
make enemies move in ways that aren't only to the player, but are also trying to dodge shots, and bait out grenades (getting into range, then getting back out of range of player grenades/bombs)
rremove control selection "aiming mode" screen which asks whether player is using keys or mouse, and set default to mouse
add "direct allies" control to control mapping menu with default being right click
introduce large enemy type with single laser
introduce super large enemy with triple laser
only two super large enemies on map at a time
only 10 large enemies on map at a time
20 limit to number of basic enemies 
3-5 ambient enemies per wave
increase map size 1.5x length x 1.5x width, without changing game resolution

when at the title screen, ask player if they are sure they want to exit the game




#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an AI pair programmer working inside Cursor.

Task: Scan the entire repo and identify everywhere that global variables, module-level state, or singleton-style Pygame resources are created or accessed.

Specifically find:
- globals in game.py (screen, clock, fonts, telemetry, difficulty, aiming mode, profile flags, config toggles)
- any other modules that rely on these globals (screens, systems, rendering.py, telemetry code)
- functions that implicitly depend on screen/clock/fonts without accepting parameters
- any code that initializes Pygame outside main()
- any module that performs drawing without receiving screen explicitly

Output a structured list:

1. List of globals and where they're declared.
2. List of functions/modules that implicitly depend on these globals.
3. List of modules that access screen/clock/fonts/telemetry/config through globals.
4. Recommendation: which items belong in AppContext vs. GameState vs. stay local.

DO NOT make any changes yet. Just produce the audit.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
Now create a new file named context.py (or the best location based on project layout) and define an AppContext dataclass.

AppContext must include:
- screen: pygame.Surface
- clock: pygame.time.Clock
- font, big_font, small_font: pygame.font.Font
- telemetry_client (if it exists)
- telemetry_enabled
- difficulty
- aiming_mode
- profile_enabled or equivalent
- any other application-wide configuration flags you identified in the audit

Rules:
- Only include true application-level resources (screen, fonts, clock, telemetry handles, global mode flags).
- Do NOT include dynamic game state (player, enemies, projectiles, score, wave_count, entity lists, etc.).

After writing the dataclass, output the complete file.


#------------------------------------------------------------------------------------------------------------------------------------------------------------
Now modify game.py to:

1. Import AppContext from context.py.
2. Remove the existing global variables related to screen, clock, fonts, telemetry, difficulty, aiming mode, etc.
3. In main(), after pygame.init() and resource initialization, construct a single AppContext instance.
4. Store all Pygame resources and config flags inside AppContext instead of globals.
5. Pass AppContext into whatever functions need it (initial screen, state initialization, main loop).

Requirements:
- Do not change gameplay behavior.
- Do not change GameState or entity state.
- Do not change frame rate or rendering logic.
- Keep main() as the entrypoint using if __name__ == "__main__".

When finished, show the updated game.py.
#---
fix laser enemy instakill issue; slow laser deployment time by 50x, and show an animation as the lasers come out to give the player time to react


#------------------------------------------------------------------------------------------------------------------------------------------------------------
Update the game loop inside game.py so that instead of referencing global screen/clock/fonts/etc., it uses AppContext:

- ctx.screen
- ctx.clock
- ctx.font, ctx.big_font, ctx.small_font
- ctx.telemetry_client
- ctx.difficulty, ctx.aiming_mode, etc.

Remove any leftover global references.

If any functions require screen/clock/fonts but currently receive no parameters, update their call sites to pass ctx or the specific resource.

Maintain 100% behavioral parity with the pre-refactor version.

When finished, show the updated loop.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
Now refactor modules outside game.py that relied on global screen/clock/font/telemetry/config values.

Steps:
1. For each screen class (menu, gameplay, pause, game over, etc.), update constructors or methods to accept AppContext.
2. For rendering.py (or equivalent), replace hidden globals with explicit ctx or parameters. If many functions use screen/font, accept ctx.
3. For any system (AI, collision, spawn, telemetry, UI) that uses global resources, update function signatures to receive ctx.
4. Fix all call sites so no module uses global screen/clock/font/telemetry.

Constraints:
- Do NOT change game rules, timing, physics, or entity logic.
- Keep function names and module boundaries the same unless required.
- If uncertain whether something belongs in ctx, prefer passing only the resource needed.

After completing the changes, output a diff summary across all files.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
Now perform cleanup:

1. Remove all global declarations in game.py and any other modules that referenced screen/clock/fonts/telemetry/config.
2. Delete unused variables that were only necessary before AppContext.
3. Ensure modules no longer rely on accessing global Pygame objects.
4. Search across the repo for any remaining screen / clock / font references not using ctx.
5. Ensure no module performs Pygame initialization outside main().

Finally, run a sanity check by reviewing:
- game.py
- context.py
- rendering helpers
- screens/
- systems/

Output a final confirmation list of what was removed or updated.


#------------------------------------------------------------------------------------------------------------------------------------------------------------
Perform a non-destructive behavior review of the refactor.

Checklist:
- Does main() still run the game the same?
- Does pygame.init() only happen in one place?
- Does the window open the same size?
- Do all screens (main menu, gameplay, pause, game over) appear?
- Does drawing work (HUD, player, enemies, projectiles)?
- Does telemetry still initialize if enabled?
- Does quitting still work?
- Are no unexpected globals used anywhere?
- Are no modules importing game.py just to access state?

Make a report listing any behavioral discrepancies or follow-up fixes needed.

Do NOT change gameplay logic unless required to maintain parity.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an AI pair programmer working in this repo.

Goal: Move the control loading/saving helpers out of game.py into a dedicated module, to shrink game.py without changing behavior or performance.

Target functions in game.py:
- _key_name_to_code(name: str) -> int
- load_controls() -> dict[str, int]
- save_controls(controls: dict[str, int]) -> None

Steps:

1. Create a new module at the project root (same level as game.py) named controls_io.py (or reuse an existing controls-related module if there is one and it makes more sense).
2. Move the three functions above into controls_io.py.
3. Make sure imports are correct in controls_io.py:
   - It should import pygame (for key constants).
   - It should import json and os if they were previously used in these functions.
4. In game.py:
   - Remove the original definitions of _key_name_to_code, load_controls, save_controls.
   - Import them from controls_io.py using explicit imports, e.g.:
       from controls_io import _key_name_to_code, load_controls, save_controls
     or a similar clean pattern.
5. Update all call sites in game.py (and elsewhere, if any) to use the imported functions with the same names.
6. Do NOT change any logic inside the functions. Only move them and fix imports.

When you are done, show me:
- The new controls_io.py file.
- The updated imports and any changes in game.py.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an AI pair programmer working in this repo.

Goal: Move generic geometry/physics helper functions out of game.py into a dedicated utility module, to make game.py smaller without affecting performance.

In game.py, locate and move the following functions:

- clamp_rect_to_screen(r: pygame.Rect, width: int, height: int)
- vec_toward(ax, ay, bx, by) -> pygame.Vector2
- line_rect_intersection(start: pygame.Vector2, end: pygame.Vector2, rect: pygame.Rect) -> pygame.Vector2 | None
- can_move_rect(rect: pygame.Rect, dx: int, dy: int, other_rects: list[pygame.Rect]) -> bool
- rect_offscreen(r: pygame.Rect) -> bool
- filter_blocks_too_close_to_player(block_list: list[dict], player_center: pygame.Vector2, player_size: int) -> list[dict]

Steps:

1. Create a new module geometry_utils.py at the project root (same level as game.py).
2. Move the functions listed above into geometry_utils.py unchanged.
3. Add the necessary imports in geometry_utils.py:
   - import pygame
   - from typing import Optional, etc., if needed.
4. In game.py:
   - Remove the original definitions for these functions.
   - Import them from geometry_utils.py using explicit imports, for example:
       from geometry_utils import (
           clamp_rect_to_screen,
           vec_toward,
           line_rect_intersection,
           can_move_rect,
           rect_offscreen,
           filter_blocks_too_close_to_player,
       )
5. Update all call sites in game.py and any other modules to use the imported names exactly as before.
6. Do NOT change function behavior or signatures.

When finished, show:
- geometry_utils.py
- The updated import block in game.py.




#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an AI pair programmer working in this repo.

Goal: Move level/setup helper functions out of game.py into a dedicated module level_utils.py, to slim down game.py without affecting performance.

In game.py, locate the functions:

- filter_blocks_no_overlap(block_list: list[dict], all_other_blocks: list[list[dict]], player_rect: pygame.Rect) -> list[dict]
- clone_enemies_from_templates() -> list[dict]

Steps:

1. Create a new module level_utils.py in the project root.
2. Move these two functions into level_utils.py unchanged.
3. Add the minimal necessary imports in level_utils.py (e.g., pygame, typing, references to enemy templates or constants if required).
4. In game.py:
   - Remove the original definitions.
   - Import them at the top with:
       from level_utils import filter_blocks_no_overlap, clone_enemies_from_templates
5. Ensure all call sites (e.g. in main() / level context setup) use the imported functions and that no references are broken.
6. Do not modify the internal logic of these functions.

Show me:
- The new level_utils.py.
- The updated imports and relevant call sites in game.py.


#------------------------------------------------------------------------------------------------------------------------------------------------------------/
You are an AI pair programmer working in this repo.

Goal: Move the rotating paraboloid/trapezoid hazard system out of game.py into a dedicated hazards.py module. This should significantly shrink game.py without changing performance.

In game.py, identify:
- The global variable: hazard_obstacles = [...]  (the large list of hazard dicts under the comment "# Rotating paraboloid/trapezoid hazard system")
- The functions related to hazard behaviour, including at least:
  - check_point_in_hazard(...)
  - check_hazard_collision(hazard1: dict, hazard2: dict) -> bool
  - resolve_hazard_collision(hazard1: dict, hazard2: dict)
  - update_hazard_obstacles(dt: float, hazard_list: list, current_lvl: int, width: int, height: int)

Steps:

1. Create a new module hazards.py at the project root.
2. Move the hazard_obstacles definition and the hazard-related functions into hazards.py.
3. If hazard_obstacles currently depends on module-level WIDTH/HEIGHT constants from game.py, make hazards.py either:
   - Define WIDTH and HEIGHT in a similar way (only if they are truly static design-time values), OR
   - Refactor hazard_obstacles so WIDTH and HEIGHT usage is parameterized appropriately (e.g., created by a function that takes width/height). Prefer the simplest change that preserves behavior.
4. In game.py:
   - Remove the original hazard_obstacles list and the moved functions.
   - Import what you need from hazards.py, for example:
       from hazards import hazard_obstacles, update_hazard_obstacles, check_point_in_hazard
5. Ensure all call sites in game.py and systems still work:
   - The level context that passes "hazard_obstacles" into gameplay.
   - Any calls to update_hazard_obstacles or check_point_in_hazard.
6. Keep hazard behavior identical; only the location of code should change.

When done, show:
- hazards.py
- Updated imports and usage in game.py.


////-----------------------------------------------------------------------------------------------------------------------------------------------------------/
END 1-25-26
You are an AI pair programmer working in this repo.

Goal: Move pickup/weapon spawning and pickup visual effect helpers out of game.py into a dedicated pickups.py module.

In game.py, locate these functions:

- spawn_pickup(pickup_type: str)
- spawn_weapon_in_center(weapon_type: str, state: GameState, width: int, height: int)
- spawn_weapon_drop(enemy: dict, state: GameState)
- create_pickup_collection_effect(x: int, y: int, color: tuple[int, int, int], state: GameState)
- update_pickup_effects(dt: float, state: GameState)

Steps:

1. Create pickups.py in the project root.
2. Move the functions listed above into pickups.py without changing their internal logic.
3. Add the necessary imports in pickups.py:
   - typing, pygame, GameState, any weapon or pickup constants, etc.
4. In game.py:
   - Remove the original function definitions.
   - Import the functions from pickups.py, e.g.:
       from pickups import (
           spawn_pickup,
           spawn_weapon_in_center,
           spawn_weapon_drop,
           create_pickup_collection_effect,
           update_pickup_effects,
       )
5. Fix all call sites in game.py (and elsewhere) to use the imported names.

Behavior must remain identical.

Afterward, show:
- pickups.py
- Updated import section and any changed call sites in game.py.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an AI pair programmer working in this repo.

Goal: Move projectile spawning logic out of game.py into a dedicated projectiles_spawning.py module, to shrink game.py.

In game.py, identify and move the following functions:

- spawn_player_bullet_and_log(state: GameState, ctx: AppContext)
- spawn_enemy_projectile(enemy: dict, state: GameState, telemetry_client=None, telemetry_enabled: bool = False)
- spawn_enemy_projectile_predictive(enemy: dict, direction: pygame.Vector2, state: GameState)
- spawn_boss_projectile(boss: dict, direction: pygame.Vector2, state: GameState)
- spawn_ally_missile(friendly: dict, target_enemy: dict, state: GameState) -> None

Steps:

1. Create projectiles_spawning.py at the project root.
2. Move these functions into projectiles_spawning.py unchanged.
3. Add required imports in projectiles_spawning.py:
   - pygame, typing, GameState, AppContext, any projectile-related constants, Telemetry if needed.
4. In game.py:
   - Remove the original definitions.
   - Import the functions from projectiles_spawning.py with explicit imports, such as:
       from projectiles_spawning import (
           spawn_player_bullet_and_log,
           spawn_enemy_projectile,
           spawn_enemy_projectile_predictive,
           spawn_boss_projectile,
           spawn_ally_missile,
       )
5. Update all call sites in game.py (and any other modules) to use the imported functions.

Ensure no gameplay change; only the module structure changes.

Show:
- projectiles_spawning.py
- Updated imports and relevant call sites in game.py.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an AI pair programmer working in this repo.

Goal: Move scoring and enemy kill helper logic out of game.py into a scoring.py module, to reduce game.py size.

In game.py, locate:

- calculate_kill_score(wave_num: int, run_time: float) -> int
- kill_enemy(enemy: dict, state: GameState, width: int, height: int) -> None

Steps:

1. Create scoring.py at the project root.
2. Move these functions into scoring.py unchanged.
3. Add required imports in scoring.py:
   - typing, pygame, GameState, any enemy/projectile utilities used inside kill_enemy.
4. In game.py:
   - Remove the original definitions.
   - Import them from scoring.py:
       from scoring import calculate_kill_score, kill_enemy
5. Fix all call sites in game.py (or other modules) to use the imported functions.

Do not alter behavior; only relocate the code.

When done, show:
- scoring.py
- Updated imports and relevant call sites in game.py.

#------------------------------------------------------------------------------------------------------------------------------------------------------------
You are an AI pair programmer working in this repo.

Goal: Move the player death/reset logic out of game.py into a respawn.py module, to shrink game.py without affecting performance.

In game.py, locate:

- reset_after_death(state: GameState, width: int, height: int)

Steps:

1. Create respawn.py in the project root.
2. Move reset_after_death into respawn.py unchanged.
3. Add any imports needed in respawn.py:
   - pygame, GameState, clamp_rect_to_screen (from geometry_utils), etc.
4. In game.py:
   - Remove the original definition.
   - Import it from respawn.py:
       from respawn import reset_after_death
5. Update all call sites to use the imported function.

Behavior must remain identical.

Show:
- respawn.py
- Updated import and call sites in game.py.

1-26-26#--------------------------------------------------------------------------------------------------------------------------------------------------------
1) You are working in my Pygame project.

I want to introduce a LevelState dataclass to hold all level geometry instead of relying on global variables in game.py.

STEP 1 — Create LevelState
1. Create a new dataclass LevelState in a new file level_state.py (or define it in state.py if that fits better).
2. It should contain the following fields:
   - static_blocks
   - trapezoid_blocks
   - triangle_blocks
   - destructible_blocks
   - moveable_blocks
   - giant_blocks
   - super_giant_blocks
   - hazard_obstacles
   - moving_health_zone (Optional[…])
3. Use broad type hints (like list[Any] or list[pygame.Rect]) that match current usage.

STEP 2 — Attach LevelState to GameState
4. Add a field on GameState: level: LevelState | None = None.
5. Initialize game_state.level when GameState is created in game.py.

STEP 3 — Build LevelState in game.py
6. Find the section in game.py where all blocks are currently created and stored in globals.
7. Instead of assigning to module-level globals, construct a LevelState instance and assign it to game_state.level.
8. Behavior must remain identical.

STEP 4 — Cleanup
9. Remove unused geometry globals after functionality is replaced.
10. Keep temporary globals only if other modules still depend on them; we will refactor those in later steps.

Make sure imports resolve and the game still runs.

2) We have introduced a LevelState and attached it to GameState as game_state.level. Now I want to remove remaining module-level geometry globals in the systems.

STEP 1 — Update movement_system
1. Open systems/movement_system.py.
2. Replace any references to trapezoid_blocks, triangle_blocks, destructible_blocks, moveable_blocks, giant_blocks, super_giant_blocks, hazard_obstacles, moving_health_zone, etc. with references to game_state.level.<field>.
3. If the main update function does not receive game_state yet, modify its signature and update all call sites so it does.

STEP 2 — Update collision_system
4. Open systems/collision_system.py.
5. Replace all references to block/hazard globals with game_state.level.<field>.
6. Update function signatures and call sites in game.py as needed so collision_system has access to GameState.

STEP 3 — Cleanup
7. Remove any now-unused module-level geometry variables from game.py and the systems modules.
8. Behavior must remain identical.

Add a short comment like “# Uses LevelState instead of module-level globals”. Ensure the game still runs and all tests still pass.

3) I want to move gameplay input-handling logic out of game.py into systems/input_system.py to simplify the main loop.

STEP 1 — Create input_system
1. Create systems/input_system.py.
2. Define:
   def handle_gameplay_input(events, game_state, ctx) -> None:
3. Move gameplay-only input parsing from game.py into this function, including:
   - move_input_x / move_input_y
   - jumping
   - firing weapons
   - switching weapons
   - toggling aim mode
   - any other gameplay-specific key/mouse controls

STEP 2 — Use it in game.py
4. In game.py’s main loop:
   - After events = pygame.event.get()
   - After screen handlers process non-gameplay states
   - If the current state is gameplay, call:
       handle_gameplay_input(events, game_state, ctx)

STEP 3 — Keep screen logic intact
5. Do NOT modify the pause, high-score, name-input, or menu screen logic.
6. Only factor out gameplay input.

Behavior and controls must remain identical.

4) I want to move the large manual reset blocks in game.py into methods of GameState.

STEP 1 — Add methods to GameState
1. In state.py, add methods like:
     def reset_run(self, ctx=None) -> None:
         """Reset the game state for a brand new run."""
     def reset_wave(self, wave: int = 1) -> None:
         """Reset wave-related fields, starting at the given wave."""
2. Move run-reset logic from game.py into reset_run:
   - clear enemies/friendlies
   - clear bullets/projectiles
   - reset HP, lives, score
   - reset run_time, survival timers, wave timers
   - reset or initialize any run-specific properties
3. Move wave-specific reset logic into reset_wave (if there is any; otherwise keep it simple and focused).

STEP 2 — Replace inline logic in game.py
4. In game.py, find where a new run or restart is triggered (after death, menu selection, etc.).
5. Replace the large manual reset blocks with:
     game_state.reset_run(ctx)
     game_state.reset_wave(1)
   or whatever combination matches current behavior.

STEP 3 — Preserve behavior
6. Behavior must remain identical:
   - New runs start with the same conditions as before.
   - Waves/score/health are reset the same way.
7. Keep imports clean and avoid circular dependencies; use type hints with string annotations if needed.

5) I want to expand pytest coverage of the refactored systems.

STEP 1 — Movement tests
1. Create tests/test_movement_system_basic.py.
2. Write tests that:
   - Construct a minimal GameState and LevelState, including a player rect and a simple static block.
   - Set move_input_x / move_input_y on GameState.
   - Call movement_system.update(game_state, dt, ctx) (or the appropriate signature).
   - Assert:
       - The player moves as expected when there is no blocking geometry.
       - The player is blocked correctly when a wall is in the movement path.

STEP 2 — Spawn tests
3. Create tests/test_spawn_system_basic.py.
4. Write tests that:
   - Initialize GameState at wave 1 with no enemies.
   - Call spawn_system.update(game_state, dt, ctx) with a dt that should trigger a spawn.
   - Assert that enemies are spawned according to the early wave rules.
   - Optionally, test wave advancement conditions if they are deterministic.

Constraints:
- Make tests deterministic (seed randomness if needed).
- Do not require an actual Pygame display window.
- All existing tests must still pass.

6) I want to centralize difficulty, player class, weapon mode, and options toggles into a GameConfig dataclass.

STEP 1 — Create GameConfig
1. Create config/game_config.py (or place it near constants.py).
2. Define a GameConfig dataclass with fields like:
   - difficulty
   - player_class
   - weapon_mode
   - enable_telemetry
   - show_metrics
   - aim_mode
   - any other toggles or scalar config values that are currently scattered around

STEP 2 — Initialize in game.py
3. In game.py, after parsing options or setting defaults, construct a GameConfig instance.
4. Attach it to AppContext, e.g. ctx.config = GameConfig(...).

STEP 3 — Update systems to use GameConfig
5. Replace direct references to separate flags (difficulty, aim mode, telemetry toggle, etc.) with references to ctx.config.<field>.
6. Keep behavior exactly the same; this is a structural cleanup only.

STEP 4 — Cleanup duplicates
7. Remove redundant flags in AppContext and GameState that are now clearly config values.
8. Avoid introducing circular imports; use string annotations or local imports if needed.

7) I want clearer management of whether the game uses the C physics extension or the Python fallback.

STEP 1 — Improve import logic
1. In game.py, wrap the C-extension import in a helper function.
2. That helper should:
   - Accept a force_python: bool = False argument.
   - If force_python is True, skip the C import and return the Python implementation.
   - Otherwise, try importing game_physics:
       - On success: mark ctx.using_c_physics = True and print "Using C-accelerated physics module."
       - On failure: mark ctx.using_c_physics = False and print "C-accelerated physics unavailable; using Python fallback."

STEP 2 — Add optional override
3. Add a command-line flag like --python-physics or an environment variable USE_PYTHON_PHYSICS=1.
4. Use this override to set force_python for the helper function.

STEP 3 — Centralize physics access
5. Ensure the main game gets a single physics module/namespace from this helper.
6. Other systems that need physics functions should use this provided module rather than directly importing game_physics.

Behavior should remain identical apart from clearer console messages and the ability to force Python mode.

8) I want to refactor and clean up the rendering pipeline to make UI/gameplay rendering more maintainable without changing visuals.

STEP 1 — Identify rendering responsibilities
1. In rendering.py and screens/gameplay.py, identify all rendering responsibilities:
   - background drawing
   - entity drawing (player, enemies, friendlies)
   - projectiles/particles
   - HUD elements (health, score, wave, etc.)
   - overlays (damage flashes, wave alerts, pause overlays, etc.)

STEP 2 — Introduce RenderContext
2. In rendering.py, create a RenderContext dataclass with fields like:
   - screen surface
   - fonts
   - common colors / theme
   - any scaling factors or layout constants
3. Make render functions accept a RenderContext rather than repeatedly looking up fonts/surfaces.

STEP 3 — Modularize gameplay rendering
4. In gameplay.py (or rendering.py, depending on current structure), split the main gameplay render function into smaller functions:
   - render_background(game_state, ctx, render_ctx)
   - render_entities(game_state, ctx, render_ctx)
   - render_projectiles(game_state, ctx, render_ctx)
   - render_hud(game_state, ctx, render_ctx)
   - render_overlays(game_state, ctx, render_ctx)
5. Have the main gameplay render call these in order.

STEP 4 — Screen rendering consistency
6. Ensure pause, name input, and high-score screens also receive a RenderContext (or something equivalent).
7. Try to align their function signatures so they are consistent across screens.

STEP 5 — Do NOT change visuals
8. The on-screen output should remain visually identical.
9. Only reorganize code, extract helpers, and improve structure.

STEP 6 — Cleanup
10. Remove any now-unused helper functions or duplicate draw calls.
11. Add brief comments explaining which part of the frame each render function is responsible for.

9) I want to organize all assets (images, sounds, fonts, etc.) under a clear structure and centralize asset loading.

STEP 1 — Directory structure
1. Under the project root, ensure we have a clear asset folder layout, for example:
   - assets/images/
   - assets/sfx/
   - assets/music/
   - assets/fonts/
   - assets/data/ (for JSON/config files if needed)
2. Move existing asset files into these directories where appropriate (update .gitignore if needed).

STEP 2 — Asset manager module
3. Create a module, e.g. asset_manager.py.
4. Implement functions or a class to:
   - Resolve file paths for assets (using a base assets directory).
   - Load and cache images (pygame.image.load + convert/convert_alpha).
   - Load and cache sounds/music.
   - Load and cache fonts.
5. Expose simple functions such as:
   - get_image("player")
   - get_sound("enemy_death")
   - get_font("main", size)

STEP 3 — Replace scattered loads
6. Find direct calls to pygame.image.load, mixer.Sound, font loading, etc. scattered across the code.
7. Replace them with calls to asset_manager functions.
8. Keep behavior identical (same assets, same sizes, same paths from the user’s perspective).

STEP 4 — Error handling
9. Implement graceful handling for missing assets (e.g., print a clear error, maybe use a placeholder).
10. Avoid crashing with obscure tracebacks when an asset path is wrong.

STEP 5 — Future-friendly
11. Optionally, allow some assets to be configured via data files in assets/data/, but do NOT overcomplicate this yet.
12. Keep the focus on getting all loading logic centralized and consistent.

10) I want to centralize audio handling (sound effects and music) into a simple sound manager, instead of having sound calls scattered around.

STEP 1 — Create audio_system or sound_manager
1. Create a new module, e.g. systems/audio_system.py or sound_manager.py.
2. Implement:
   - Initialization of pygame.mixer (if not already done centrally).
   - A registry of sound effects and music tracks.
   - Functions like:
       play_sfx(name: str)
       play_music(name: str, loop: bool = True)
       stop_music()

STEP 2 — Volume and muting controls
3. Store global SFX and music volume in either GameConfig or AppContext.
4. Add functions:
   - set_sfx_volume(value: float)
   - set_music_volume(value: float)
   - mute/unmute helpers if useful.
5. Make sure changing volume affects all relevant channels.

STEP 3 — Replace scattered audio calls
6. Find direct uses of pygame.mixer.Sound(...).play() and music calls in game.py and other modules.
7. Replace them with calls to the audio system (play_sfx, play_music, stop_music, etc.).
8. Keep which sound plays when exactly the same.

STEP 4 — Integrate with options/screens
9. Optionally, if there is an options menu or config, wire volume/mute toggles into GameConfig and have the audio system respect those values.
10. Do not change gameplay logic — only consolidate audio behavior.

Behavior must remain effectively identical to the player, just managed in one place.

11) I want to perform a global cleanup pass to improve consistency without changing game behavior.

STEP 1 — Import hygiene
1. Remove unused imports in all modules.
2. Replace any wildcard imports with explicit imports.
3. Group imports in each file as:
   - standard library
   - third-party (pygame, numpy, sqlite3, etc.)
   - internal modules (systems, entities, telemetry, etc.)

STEP 2 — Naming consistency
4. Ensure the following conventions:
   - snake_case for functions and variables
   - PascalCase for classes
   - ALL_CAPS for constants
5. Rename only when reasonably safe; if a rename requires touching many files, keep it focused and cohesive per commit.

STEP 3 — File structure clarity
6. In each directory (systems/, entities/, screens/, telemetry/, etc.), ensure file names match their purpose.
7. Note any modules that appear unused or redundant; either remove them or mark them clearly.

STEP 4 — Documentation comments
8. At the top of key modules (especially in systems/ and entities/), add a short comment summarizing their purpose.
9. Update any existing docstrings that have become stale after refactors.

STEP 5 — No behavior changes
10. Do NOT change gameplay logic, AI, physics, or rendering behavior.
11. The game should run exactly as before; this is strictly cleanup and consistency.

12) I want to improve the game loop timing model to be more robust and deterministic, ideally moving toward a fixed-step simulation.

STEP 1 — Analyze current timing
1. Look at how dt is currently computed in game.py (likely via clock.tick(FPS) / 1000.0).
2. Confirm how dt is passed into systems (movement, AI, collision, spawn, etc.).

STEP 2 — Introduce a fixed-step model
3. Implement a fixed-step simulation pattern in game.py, for example:
   - Define a FIXED_DT (e.g., 1.0 / 60.0).
   - Maintain an accumulator variable.
   - Each frame:
       dt = clock.tick(FPS) / 1000.0
       accumulator += dt
       while accumulator >= FIXED_DT:
           update(FIXED_DT)
           accumulator -= FIXED_DT
       render(interpolation_factor)
4. Extract the existing update calls into an update_simulation(fixed_dt, game_state, ctx) function.

STEP 3 — Adjust systems to use fixed dt
5. Ensure movement_system, ai_system, collision_system, spawn_system, etc., consistently take a fixed dt (FIXED_DT).
6. Avoid mixing variable dt and fixed dt in the same logic path.

STEP 4 — Rendering interpolation (optional)
7. Optionally, pass an interpolation factor to rendering code:
   - interpolation = accumulator / FIXED_DT
   - Use it for smoothing positions if desired (but this can be a later enhancement).

STEP 5 — Preserve behavior as much as possible
8. Try to keep gameplay feel similar to the current behavior, but with more stable motion under varying FPS.
9. Update or add tests if needed to account for fixed-step timing.

The goal is to make simulation more deterministic and robust against frame spikes.

13) I want to move toward a lightweight ECS-style architecture to simplify adding new enemy and projectile types.

STEP 1 — Inventory current entities
1. Inspect entities (player, enemies, friendlies, projectiles) and see how they are stored in GameState.
2. Note where logic branches on types (enemy types, projectile types) via if/elif chains.

STEP 2 — Define simple components
3. Introduce a minimal set of components in a new module (e.g., ecs_components.py), such as:
   - PositionComponent
   - VelocityComponent
   - HealthComponent
   - SpriteComponent or RenderComponent
   - AIComponent (with flags or behavior identifiers)
   - ColliderComponent
4. These can be simple dataclasses or lightweight classes.

STEP 3 — Entity registry in GameState
5. Add an entity registry to GameState, something like:
   - entities: dict[int, dict[type, Any]]
   where each entity id maps to a dict of components.
6. Provide helper functions:
   - create_entity(components: list[Any]) -> entity_id
   - get_entities_with(*component_types) -> iterable of entity_ids

STEP 4 — Adapt systems gradually
7. Modify one system at a time (e.g., movement_system) to:
   - Iterate over entities with PositionComponent and VelocityComponent.
   - Update positions based on velocity and dt.
8. Next, adapt collision_system to operate on entities with PositionComponent + ColliderComponent.
9. Avoid rewriting everything at once; keep compatibility with existing lists while migrating.

STEP 5 — Reduce type-specific branching
10. Where there are big chains like “if enemy_type == X”, move toward data-driven behavior via components or small strategy objects.
11. Keep behavior identical for now; focus on structural changes.

STEP 6 — Clean up once stable
12. After systems are reliably using the ECS structures, remove redundant per-type lists and logic.
13. Maintain and/or expand tests to ensure that behavior doesn’t regress.

This should remain a “lite” ECS layer appropriate for this project, not an over-engineered full engine.

1) We have just completed a large multi-step refactor (prompts 1–13).  
Now we must perform a STABILIZATION PASS across the project.

Goal:
Identify and fix breakages, inconsistencies, missing imports, outdated references, and logic mismatches introduced by the refactor. No new features. No architectural changes. Strictly stabilization.

Constraints:
- DO NOT introduce new behavior.
- DO NOT modify gameplay logic, physics, AI, or spawn behavior.
- DO NOT change public APIs.
- DO NOT add or remove entire systems.
- Keep all visual, auditory, and gameplay behavior identical to pre-refactor.
- Prefer minimal diffs that correct concrete errors.

Tasks:

1. **Static “sanity scan”**
   - Search for broken imports, missing modules, and references to removed globals.
   - Fix import paths, rename variables for consistency, and remove stale references.

2. **Runtime error audit**
   - Add temporary lightweight try/print wrappers only where absolutely needed to locate failing code paths.
   - Identify missing attributes, NameErrors, uninitialized fields, or any incorrect level geometry references from the new LevelState structure.

3. **Signature & call-site alignment**
   - Ensure all systems (movement, collision, ai, spawn, ui, telemetry) have updated function signatures matching the refactor (dt, game_state, ctx).
   - Update all call sites accordingly.

4. **Game loop stabilization**
   - Ensure game.py’s main loop correctly:
       - Obtains events
       - Delegates gameplay input to the new input_system
       - Calls update functions in the intended order
       - Renders screens correctly
   - Fix any mismatched screen handler calls or missing parameters.

5. **State initialization consistency**
   - Verify GameState fields are fully initialized:
       - level (LevelState)
       - config (GameConfig)
       - telem writer (if enabled)
       - movement/firing flags
       - timers, counters, wave variables
   - Fix missing initialization lines.

6. **Remove any accidental leftover globals**
   - If any geometry globals or outdated constants remain:
       - Replace them with game_state.level fields.
       - Only remove globals that are truly unused.

7. **Test environment stabilization**
   - Ensure all existing pytest tests run without errors.
   - Update tests only if the refactor changed module paths or initialization patterns.
   - Do NOT alter test logic or expected behavior.

8. **Minimal documentation updates**
   - At the top of any file where the refactor changed imports or structure, add a 1-2 line comment clarifying the new arrangement (LevelState, input_system, systems registry, etc.).

After completing the above, present all diffs for review.
Keep diffs focused, minimal, and strictly corrective.

This is a stabilization sweep — no new features, no redesigns. Only ensure the refactored codebase builds, runs, and behaves exactly the same as before.

PHASE 1: 
We are now in PHASE 1: FEEL & GAMEPLAY TUNING.

Assume the Phase 0 stabilization pass is complete: tests pass, the game runs, and behavior matches pre-refactor. Now I want to focus on “feel”: movement, weapons, difficulty pacing, and visual/audio feedback (“juice”). This is a targeted polish phase, not another massive refactor.

Overall Goal:
Improve the FEEL of the game: responsiveness, weapon impact, difficulty curve, and feedback effects, while keeping the core design intact.

Global Constraints:
- DO NOT introduce new game modes or major mechanics.
- DO NOT remove existing weapons, enemies, or waves.
- Prefer making existing systems feel better rather than adding completely new ones.
- Any new effects should be configurable and easy to tone down or disable.
- Keep code changes scoped and incremental: if a step becomes too large, propose to split it.

PHASE 1 TASKS:

1. Centralize “feel” tuning into GameConfig
   - In the GameConfig (or equivalent config structure), ensure we have fields for:
     - player movement: base speed, optional acceleration/deceleration
     - jump parameters (if applicable)
     - weapon fire rates (per weapon)
     - weapon damage (per weapon)
     - knockback / recoil magnitudes (if used)
   - Confirm all these values are used by systems (movement_system, projectile/weapon logic) instead of hard-coded constants.
   - Keep default values so that feel is initially close to pre-phase behavior.

2. Movement responsiveness tuning hooks
   - In movement_system:
     - Make sure movement uses the GameConfig values.
     - Optionally allow a very small smoothing or acceleration factor to adjust “snappiness.”
   - Add very small, well-commented tuning constants to control:
     - Input dead zones (if needed).
     - Max velocity or clamp behavior.
   - Do not radically change movement yet; just expose the hooks and ensure they are easy to tweak in one place.

3. Weapon feel tuning hooks
   - Ensure weapon/projectile creation code uses:
     - Fire rate from config
     - Damage from config
     - Optional spread/recoil from config if present
   - If there are magic numbers for cooldowns / bullet speed, move them into config.
   - Make sure nothing is hardcoded in multiple places — centralize per-weapon properties.

4. Difficulty curve and pacing via config
   - Identify where wave spawn rates, enemy counts, and enemy health/damage are defined (spawn_system, enemy config, etc.).
   - Expose key parameters in GameConfig or enemy config:
     - base_enemy_health_per_wave
     - base_spawn_rate_per_wave
     - difficulty multipliers for different difficulty levels.
   - Make early waves slightly tunable without editing core logic.

5. Add “juice” (visual feedback) in a controlled way
   - Player hits on enemies:
     - Add a small, time-limited “damage flash” for enemies (e.g., tint or brightness boost) that is triggered when they take damage.
   - Player takes damage:
     - Add a brief screen flash or vignette overlay to indicate damage.
   - Wave transitions:
     - Add a small HUD banner or text that appears briefly on wave start or wave clear.
   - Ensure all these effects:
     - Are driven by timers/flags in GameState or a small FX manager.
     - Have magnitudes/durations configurable from config.
     - Degrade gracefully if disabled.

6. Audio “juice” integration with audio system
   - Hook existing audio calls into the new sound manager / audio system (if present).
   - Add distinct SFX for:
     - Enemy death (if not already)
     - Player hit
     - Wave start / wave cleared
     - Big events (boss spawn, etc.)
   - Use volume and mute toggles from config/AppContext; do not hardcode volumes.

7. Manual testing scaffold (for me, the human)
   - Ensure there are easy-to-find constants or config entries for:
     - “casual” feel profile
     - “arcade” feel profile
   - Optionally add comments or a small document block at the top of the config file explaining which values to tweak for:
     - More floaty vs tight movement
     - Faster vs slower weapons
     - Easier vs harder early waves

Throughout this phase:
- Prefer small, testable changes.
- Make sure tests still pass.
- Avoid touching unrelated systems like telemetry schema or ECS architecture.

At the end, present diffs grouped logically (movement config, weapons config, FX/juice additions) so I can review them in chunks.

phase 2: 
We are now in PHASE 2: TELEMETRY, ANALYTICS, AND PERFORMANCE.

Phase 1 improved the FEEL of the game. Now I want to:
- Use telemetry to understand difficulty and player experience.
- Add visualizations for death hotspots and pressure.
- Add lightweight performance instrumentation and perform a SMALL optimization pass.

Overall Goal:
Make the game “observable”: understand difficulty curves, death patterns, and performance behavior via telemetry and profiling, then make modest, safe improvements.

Global Constraints:
- Do NOT change core mechanics or enemy/weapon behavior solely for performance.
- Do NOT redesign telemetry schema; extend it minimally.
- Do NOT introduce heavy dependencies (keep it Python + matplotlib/numpy-level complexity).
- Keep new telemetry optional and cheap at runtime.

PHASE 2 TASKS:

1. Ensure telemetry logs key difficulty-related metrics
   - Confirm or add logging for:
     - Player health over time (HP vs run_time).
     - Enemies alive over time (count vs run_time).
     - Player position over time.
     - Death events (run_id, run_time, player_x, player_y, wave_number).
   - If any of these are missing in the telemetry writer, add them with minimal schema changes.

2. Add visualizations for deaths and hotspots
   - In telemetry_viz:
     - Add a new page that shows a scatter plot of death positions over the playfield for:
       - A single run.
       - Optionally all runs combined (if requested).
     - Color or shape can indicate wave_number or difficulty.
   - Make sure axes match the in-game coordinate system so I can interpret positions.

3. Add time-series difficulty plots
   - Add a page that, for a single run, plots over time:
     - enemies_alive
     - player_health
     - damage_taken (or cumulative damage)
   - Optionally overlay wave markers (e.g., vertical lines or labels when waves start).

4. Pressure score telemetry (if a pressure metric exists or is easy to add)
   - If Phase 1 or later plans introduced a “pressure_score” (based on enemy count, bullets near player, recent damage, etc.):
     - Log pressure_score over time in telemetry.
     - Add a plot showing pressure_score vs time, alongside enemies_alive and player_health.
   - If not yet implemented, keep this step as a stub or optional extension, NOT a major new system.

5. Lightweight performance instrumentation
   - Add simple timing instrumentation in a DEBUG or DEV mode:
     - Frame time (per frame).
     - Optional per-system timings: movement, AI, collision, spawn, rendering.
   - Store these metrics either:
     - In a small in-memory structure for real-time debug display, and/or
     - In a separate log/telemetry table for offline inspection.
   - Overhead should be minimal and disabled in normal play if desired.

6. Profiling support & micro-optimizations
   - Ensure profile_game.py (or equivalent profiling script) is up to date with the new architecture (systems registry, GameState, etc.).
   - Run a profiling session (conceptually) and:
     - Identify the top hotspots.
     - Apply 1–3 safe micro-optimizations where obvious, such as:
       - Reducing repeated attribute lookups inside hot loops.
       - Avoiding unnecessary list traversals.
       - Caching constant lookups in local variables in tight sections.
   - Keep these optimizations small and well-commented.

7. Documentation for telemetry usage
   - In a telemetry README or comment block:
     - Document how to:
       - Run the game with telemetry enabled.
       - Run the visualizer.
       - Interpret key plots (deaths, difficulty over time, performance metrics).
   - This is just enough documentation for me (the human) to replicate tuning workflows later.

Throughout this phase:
- Focus on observability and clarity, not radical design changes.
- Do not break existing telemetry consumers (visualize.py, existing plots).
- Keep tests passing and avoid schema changes that require DB migration logic unless absolutely necessary.


phase 3:
We are now in PHASE 3: ENGINE ARCHITECTURE.

Phase 1 tuned feel, Phase 2 added telemetry and perf insight. Now I want to strengthen the engine architecture itself by:
- Formalizing a systems registry for updates.
- Making enemies and projectiles more data-driven.
- Introducing a simple scene/stack system for screens and gameplay.

Overall Goal:
Make the game’s architecture more engine-like and extensible, without changing visible behavior.

Global Constraints:
- Preserve gameplay: NO gameplay changes, NO new types beyond what’s required to demo architecture.
- Keep refactors incremental and well-structured.
- Do not introduce circular imports; use modules and type hints carefully.
- All changes should be backward-compatible with tests and existing flows.

PHASE 3 TASKS:

1. Systems registry and central update pipeline
   - Introduce a small “System” abstraction or pattern:
     - A base class, Protocol, or convention: system.update(game_state, ctx, dt).
   - Create a systems registry (e.g., in systems/registry.py) that defines the ordered list of systems:
     - movement_system
     - ai_system
     - collision_system
     - spawn_system
     - telemetry_system
     - (any others currently called from the main loop)
   - Replace hardcoded sequential calls in game.py’s update logic with:
     - for system in systems_registry: system.update(game_state, ctx, dt)
   - Preserve the current update order exactly.
   - Add comments documenting why the order is what it is.

2. Data-driven enemy and projectile definitions
   - Create a data definition layer for enemies and projectiles:
     - Either Python dataclasses in config/enemy_defs.py and config/projectile_defs.py, or JSON files in assets/data/ loaded into structured objects.
   - Each enemy definition should define:
     - type_id
     - base_health
     - move_speed
     - sprite_id or asset key
     - score_value
     - behavior flags or tags (e.g., “flying”, “suicider”).
   - Each projectile definition should define:
     - type_id
     - speed
     - damage
     - lifetime
     - sprite_id or asset key
     - flags like “piercing”, “explosive”.
   - Add helper functions like get_enemy_def(type_id) and get_projectile_def(type_id) with caching for performance.
   - Update spawn_system and projectile creation logic to use these definitions instead of hardcoded constants.
   - Ensure that current enemy and projectile behavior/stats are encoded into these definitions so gameplay remains the same.

3. Scene / state stack for screens and gameplay
   - Define a Scene base class or Protocol (e.g., scenes/base.py) with methods:
     - handle_input(events, game_state, ctx) -> None
     - update(dt, game_state, ctx) -> None
     - render(render_ctx, game_state, ctx) -> None
     - Optional on_enter/on_exit hooks.
   - Implement concrete scene classes for:
     - GameplayScene
     - PauseScene
     - HighScoreScene
     - NameInputScene
     (and optionally MainMenuScene if desired later, but not required now).
   - Wrap existing screen logic in these scenes or adapt existing screen handlers to these interfaces.
   - Implement a SceneStack:
     - push(scene)
     - pop()
     - current() -> scene
     - The game loop should:
         - delegate input to the current scene
         - call current_scene.update(dt, game_state, ctx)
         - call current_scene.render(render_ctx, game_state, ctx)
   - Replace the old state-constant + screen handler mapping with the SceneStack mechanism.
   - Keep current flows intact:
     - gameplay → pause → resume
     - gameplay → death → high score → name input → back to menu/gameplay.

4. Consistency and glue
   - Ensure:
     - Systems registry, data-driven enemy/projectile definitions, and scenes stack all coexist cleanly.
     - No circular imports between scenes, systems, and GameState/AppContext.
   - Update imports and adjust module responsibilities if some code now belongs more naturally in a different module (e.g., move screen-specific logic into scenes/).

5. Tests and documentation
   - Update or add tests to:
     - Verify the systems registry calls systems in the expected order.
     - Verify that data-driven enemy/projectile definitions are loaded correctly and match expected defaults.
     - Verify that the SceneStack transitions behave as expected (push/popup patterns).
   - Add brief documentation (or comments) summarizing:
     - “How systems are registered and updated.”
     - “How enemy/projectile definitions are structured and extended.”
     - “How scenes and the scene stack manage screens and gameplay.”

Throughout this phase:
- Prioritize clarity and modularity over cleverness.
- Make sure all existing features remain intact and tests continue to pass.
- If a subtask grows too large, break it into smaller, clearly described steps before applying changes.



#------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------
