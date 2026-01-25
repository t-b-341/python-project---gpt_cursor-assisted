# All improvement suggestions and TODO items have been moved to GAME_IMPROVEMENTS.md
# See that file for the complete list of planned features and fixes.
#
# Original improvement comments have been extracted to GAME_IMPROVEMENTS.md
#--------------------------------------------------------------------------------------------------------------------------
#change enemy bullet colors
#enemy movement
#enemy respawn timer
#survival timer, waves, multiple levels
#movement direction overwrites to most recent move direction
#player path prediction
#different shapes for shots (circle, squares, etc., like 2hu)
#--------------------------------------------------------
#add boost mechanic using shift, and slow down mechanic using ctrl
#add a control mapping system, so the player can map the keys to the actions
#add a pickup for boost
#add a pickup for more firing speed
#add a pickup for enemies spawn more often, that enemies can pick up, and that you have to shoot to destroy the pickup
#--------------------------------------------------------
#make pickups bigger, add in another pickup that increases the player's max health 
#add a pickup that increases the player's speed
#add a pickup that increases the player's firing rate
#add a pickup that increases the player's bullet size
#add a pickup that increases the player's bullet speed
#add a pickup that increases the player's bullet damage
#add a pickup that increases the player's bullet knockback
#add a pickup that increases the player's bullet penetration
#add a pickup that increases the player's bullet explosion radius
#randomize the pickups, so that the player never knows what they will get
#--------------------------------------------------------
#make pickup that increases the shot size to 10x regular size, and another pickup that increase the shot beams to 3 beams
#--------------------------------------------------------
#add a pickup that bounces shots around on the walls
#add an enemy that shoots shots that bounce around on the walls
#stack pickups so that the player can get a combo of pickups
#add in more squares and rectangles that can be moved around, but have health bars that enemies can shoot at to destroy them
#--------------------------------------------------------
#add a pickup timer, and effects around the pickup, and an effect when the player picks up the pickup
#add a pickup that functions like a rocket launcher with a longer rate of fire, but the shots do more damage with an area of effect
#--------------------------------------------------------
#add a map to key 1 for the basic fire, then key 2 for the rocket launcher, then key 3 for the triple shot, then key 4 for the bouncing bullets, then key 5 for the giant bullets
#--------------------------------------------------------
#make the map bigger, and add in more geometry, with areas of health recovery, and overshields (extra health bar that can be used to block damage)
#--------------------------------------------------------
#add a pickup that increases the player's overshield
#FUTURE
#SMALL FEATURES TO ADD; integrate C++ for the physics and collision detection?
#multiple levels, with different themes and enemies, and pickups, and powerups
#more weapons; start with basic weapons (weapon 1 = peashooter, weapon 2 = rocket launcher, weapon 3 = triple shot, weapon 4 = bouncing bullets, weapon 5 = giant bullets)
#pick up weapons as levels progress, and as the player kills enemies, then enemies drop the weapons they use (so there's an enemy that does peashooters, and another that does rocket launchers, etc.)
#final boss, with a unique weapon that the player has to defeat (combo of all weapons), multiple phases, and a unique weapon for each phase
#add a special pickup that adds a laser beam weapon that the player can use to destroy enemies from a distance, that's a long ray, but doesn't cut through solid blocks, but breaks temporary barriers
#continue? after game is done, to add an endurance mode for postgame
#add a score counter and survival wave amount/time survived
#add a difficulty selector, so the player can choose the difficulty of the game, which impacts enemy spawns (more, harder enemies, fewer pickups?)
#by end of game it's a bullet hell with the player having all their tools
#add space bar to jump in direction of movement?
#--------------------------------------------------------
#add friendly AI, about 1-2 per every 3-5 enemies that move independently, and attack the enemies, and help the player, with a health bar and various spawn classes and behavior patterns
#--------------------------------------------------------
#make the friendly AI move, and make the enemy AI focus on the player, and the friendly, and move in response to the player and the friendly's bullets, and position
#--------------------------------------------------------
#make weapons drop in the center of the screen, and the player has to pick them up to use them, adding one with each level completed
#make each level 3 waves, increasing in difficulty, with the last wave being the boss
#make 3 different levels, with the final level being a boss with 10,000 health
#--------------------------------------------------------
#make the rockets shot size bigger
#--------------------------------------------------------
#add a shield for use with left alt key that lasts 2 seconds, and takes 10-15 seconds to recharge
#--------------------------------------------------------
#make the player turn red while the shield is active, and a text displays in the hud SHIELD ACTIVU (spelled like that)
#--------------------------------------------------------
#Game; add enemy with shield that is a line across the front of the enemy, which the player must flank to damage; 
#add one shield enemy with reflective shield, which takes damage done to the shield and fires back at the player; enemy does not fire, enemy turns at speed player can flank 
#Game; controls; add in arrows for shooting, and an option to choose between mouse and arrow keys
#Game; classes to play as, custom mod setting to change enemy spawn amount, custom wave builder
#;enable or disable stats and any UI elements like health; take away health bars for destructible blocks, add in texture that shows block is breakable, give texture to unbreakable blocks; 
#clean up UI
#Game.py; change aiming mechanic
#Arrow keys: Add it as an option in the menu to use either mouse or arrow aiming
#Game.py; large shapes that bounce around the map, destroying what's in their path, and the enemies avoid them
#--------------------------------------------------------
#add a health bar for the player
#make the metrics optional in the menu
#--------------------------------------------------------
#put the health bar on the bottom of the screen
#--------------------------------------------------------
#start game fullscreen
#--------------------------------------------------------
#in telemetry.py, track the player's position and velocity, and the enemy's position and velocity, and which enemy types spawned that wave; do the wave's tracking for the enemies as its own table
#--------------------------------------------------------
#add more enemies, and friendly ai, and give the ai more health (50-100), with their bar being full and green at the beginning of the waves
#--------------------------------------------------------
#add in more moveable blocks
#add in moveable blocks that can be destroyed by the player's, and enemy's bullets
#--------------------------------------------------------
#make only one health area, and have it move around the map, and the player has to move to it to heal
#add a pickup that increases the player's health regeneration rate
#add in more geometry (moveable blocks, unmovable blocks, destructible blocks, indestructible blocks) to fill up the map more
#once there are 5 enemies remaining, have them move towards the player, and the player has to move to avoid them, and the player has to shoot them to kill them
#--------------------------------------------------------
#add in trapezoids that hang off the top, bottom, and sides of the screen, that are unmovable, and indestructible
#--------------------------------------------------------
#let the enemies move the blocks out of the way as well, to chase the player
#--------------------------------------------------------
#take the moveable, indestructible geometry, and leave only the destructible, movable geometry, and the unmovable, destructible, and unmovable, destructible geometry. 
#outside/border: create spaces between trapezoids, creating 3 total on left side, 2 on right, next to each other, with 5 trapezoids with 2 triangles each on top of them on top, and then a line of triangles across the bottom
#
#read the supporting files of game_physics, and optimize them with game.py, telemetry.py, and visualize.py, and then optimize game.py, telemetry.py, and visualize.py amongst each other, given the new updates in game.py
#--------------------------------------------------------
#is there a way to utilize the GPU for processing as well?
#--------------------------------------------------------
#I have an NVIDIA GPU, a 4080 super, so CUDA cores should be available; 
#--------------------------------------------------------
#GPU acceleration status:
# - game.py: ✅ IMPLEMENTED - Uses GPU for bullet updates (50+ bullets) via gpu_physics module
# - telemetry.py: ✅ IMPLEMENTED - GPU support added for batch event processing (when CUDA available)
# - visualize.py: ✅ IMPLEMENTED - GPU support added for data processing operations (when CUDA available)
# ✅ CUDA 12.9 CONFIGURED - GPU acceleration is active (RTX 4080 SUPER detected)
#    Falls back to CPU JIT (2-5x speedup) if CUDA becomes unavailable.
#--------------------------------------------------------
#fix the health bars for the friendly ai, and make their health bars full and green at the beginning of the waves
#--------------------------------------------------------
#change all enemies to have no more than 300 health each. The enemies can have health lower than that.
#--------------------------------------------------------
#I'm still encountering frame rate issues. Let's add a feature where at the beginning ofhe game, you ask if the user wants to run telemetry and write to game_telemetry.db.
#isualize.py: update the charts to be the most recent run
#--------------------------------------------------------
#set default telemetry to disabled in the menu
#--------------------------------------------------------
#add a high score board after each death, and the ability to type in a name
#verify all code in repo is working correctly, and all features are implemented correctly, and all code is optimized for performance
#--------------------------------------------------------
#increase player base health to 250
#--------------------------------------------------------
#health pickups are worth 100 health
#--------------------------------------------------------
#add a beam that fires in a sine wave pattern, and the beam is a line that is 10 pixels wide, and 1000 pixels long, and the beam is fired from the player's position, and the beam is fired in a sine wave pattern, and the beam is fired in a cosine wave pattern, and the beam is fired in a tangent wave pattern, and the beam is fired in a cotangent wave pattern, and the beam is fired in a secant wave pattern, and the beam is fired in a cosecant wave pattern, and the beam is fired in a arcsecant wave pattern, and the beam is fired in a arccosecant wave pattern, and the beam is fired in a arcsecant wave pattern, and the beam is fired in a arccosecant wave pattern
#--------------------------------------------------------
#add a rotating paraboloid that slowly rotates around the stage, that is 500 pixels wide, and 500 pixels tall, and is a hazard that does damage to the player, and the player has to avoid it
#--------------------------------------------------------
#add in two more paraboloids with collision physics, so that they'll bounce off each other, and that do damage to the player at 10 damage/second
#--------------------------------------------------------
#make the paraboloids half size, add another one, and have them start at the corners of the map
#on the second level, turn the paraboloids into trapezoids that do the same function as the paraboloid
#make it so that the player can "bully" the obstacles by shooting them and they move in response to being shot, and make the obstacles kill the enemies when they collide with the hazard
#--------------------------------------------------------
#add in a pickup that randomizes, with an on screen element on the HUD, how much base damage is multiplied by
#add in a beam selection option in the pre-game menu (useful for testing beams)
#make it so that the player cannot fly through the hazards (paraboloid, trapezoids, and all future hazards)
#--------------------------------------------------------
#beam selection controls don't work
#make shots from players move the hazards
#make damage done to enemies displayed over their health bar as an integer
#--------------------------------------------------------
#make it so that after the player damages an enemy, the damage given number goes away after 2 seconds
#make it so I cannot fly through allies
#make it so that allies disappear after dying
#change beam selections to only be sine beam (instead of the other trig functions), and change beam selection to include rockets, bounce beam, etc., for ease of testing
#--------------------------------------------------------
#make aoe bigger for rocket beam
#make a weapon name document for reference, with enemy names
#spawn with wave_beam in slot 2, in addition to basic
#--------------------------------------------------------
#make wave beam a solid line rather than dots, and turn the beam lime green
#--------------------------------------------------------
#make wave beam an undulating wave, with a period of 1 second, and a amplitude of 10 pixels
#--------------------------------------------------------
#make the wave beam have a period of 0.5 seconds, and a amplitude of 7 pixels
#--------------------------------------------------------
#when player collects a pickup, automatically switch to that weapon, and display the weapon name on the screen
#--------------------------------------------------------
#take away wave beam as a starting weapon, leave it as only a pickup, leaving the player only with the basic beam and the other weapons as pickups
#--------------------------------------------------------
#make the weapon pickup messages display for 3 seconds, and then fade out
#--------------------------------------------------------
#make hazards move 3x faster
#--------------------------------------------------------
#give destructible obstacles 10x more health
#--------------------------------------------------------
#give allies 10x more health
#make the default telemetry selection to be disabled, but still able to be enabled
#--------------------------------------------------------
#select telemetry, and select metrics, as two different options in the menu that can be selected independently, with disabled as the default for both
#--------------------------------------------------------
#metrics menu: show and hide, independent from telemetry
#telemetry menu:  enable and disable, independent from metrics
#-------------------------------------------------------- 1-23-26--------------------------------------------------------------------------------------
#make all blocks moveable, and indestructible, and the player can push them around
#--------------------------------------------------------
#add destructible, moveable blocks back in. Make blocks 50% of all blocks, and the other 50% be indestructible, moveable blocks
#--------------------------------------------------------
#add texture into indestructible, moveable blocks that makes it looks like a silver wall
#add texture into destructible, moveable blocks that makes it looks like a cracked brick wall
#--------------------------------------------------------
#fix issue where allies do not disappear after dying - FIXED: Added cleanup checks and hazard collision handling
#--------------------------------------------------------
#fix issue where wave beams get stuck displayed after beam switched - FIXED: Added beam clearing when switching weapons
#--------------------------------------------------------
#make bouncing bullets projectiles twice the size, and projectiles orange - FIXED: Added 2x size multiplier and orange color
#--------------------------------------------------------
#make player stick out more on map by making player 10% larger, and have a highlight around the player - FIXED: Increased size to 28x28 and added glowing highlight
#--------------------------------------------------------
#make player's model a circle - FIXED: Changed from rectangle to circle with circular highlight
#--------------------------------------------------------
#in menu, set default beam selection to basic - FIXED: Changed default selection to index 6 (basic)
#--------------------------------------------------------
#allow the player to start in endurance mode 
#fix endurance mode crash when game starts
#-------------------------------------------------------
#do not drop the basic beam as a pickup weapon 
#game; Make a placeholder text for each drop saying whether it's health, or which weapon it is 
#game; Change shape of healing pattern with each stage between triangles and rectangles 
#--------------------------------------------------------
#increase enemy and ally movement speed by 110% 
#increase enemy and ally health by 110%  
#increase enemy and ally damage by 110%  
#increase enemy and ally fire rate by 110%
#--------------------------------------------------------
#add in a grenade to use with e with an aoe of a radius that is 10x the player space that kills enemies and does damage to destructible obstacles
#game; fix ally collision to prevent player position and allies from being in the same spot
#game; enemy type - spawner - spawns enemies during round
#game; make wave beam second to last dropped, giant beam last
#game; make beam selector harder to access (testing mode? if yes, display beam selection)
#game; make an enemy that predicts and shoots ahead of player's location; dark maroon rhomboid
#game; lower blocks amount, and make them bigger
#Game; add controls at bottom of screen (wasd to move, mouse + click to aim and shoot) or (wasd to move, arrow keys to aim and shoot), grenade, and which weapon is mapped to which weapon slot with first letter of weapon name
#--------------------------------------------------------/
#make player clone (maroon enemy) have 2000 health, and move 3x standard speed
#add another block size - giant, super giant, which cannot be moved
#make it so that player spawn and block spawn cannot overlap, player spawn takes priority
#make lives 3 per wave, resetting at the beginning of each wave
#--------------------------------------------------------/
#prevent blocks from spawning within a radius of 10x the player size, from the player
#--------------------------------------------------------/
#create enemy classes; pawn = basic beam, basic movement speed
#create enemy classes; queen = maroon, "player copy"
#prevent enemies and allies from spawning where blocks are
#when game launches in command line, print "welcome to my game! :D"
#give maroon enemy name "queen", and allow it to use grenades and shield as well as it gets damage done to it after 300-500 damage, for 5 seconds, and player gets close (grenade), and destroys destructible cover to lower ability for player to hide
#prevent allies or enemies from spawning in health block
#--------------------------------------------------------/
#make health block be in a different spot from the boss spawn point
#add in suicide enemy that goes towards player and detonates themselves with grenade, and disappears after detonating, and damages player if in range of grenade; when enemy dies, the enemy despawns
#update WEAPON_AND_ENEMY_REFERNCE.md to reflect most recent weapons, their spawn order, enemies with their names, and their behavior patterns
#make enemies prioritize player damage, unless player is over half the map away from them, then prioritize allies closeby
#--------------------------------------------------------/
#make a list of all pickups, and their effects, and their spawn order
#game; add side quests, and goal tracking; complete wave without getting hit, get a bonus 10,000 points
#prevent boxes from overlapping with allies, on other boxes, or player, on spawn
#when metrics are disabled, disable all hud information; when selecting options (HUD: enable, disable)
#create custom character profile creator
#--------------------------------------------------------/
#character profile premade and custom character profile do not allow for right to continue to next menu 
# --------------------------------------------------------/
#make character profile option yes or no, and if yes, allow player to select premade, or make a profile, prior to start of game
#replace metrics selection with HUD, which toggles HUD dynamics on or off, and can be changed
#fix text overlap in "ready to start" menu with weapon basic, and other text
#test mode menu: puts enemy name over the enemy health bar
#make custom stats able to be updated
#make custom stats able to select to next menu by enter, and right arrow
#fix text overlap in "select player class" menu
#increase rate of fire for all enemies
#game; rename enemy with shield to "shield enemy"
#fix triple shot beam to include two more beams, offset by an equal arc on each side of center beam, and increase beam shot size to 3x current size, and turn purple
#verify when health = zero, enemies and allies die and disappear from map
#after each enemy dies, put in bottom right corner a text feed that updates "(enemy type) defeated!"
#--------------------------------------------------------/
#change hud and telemetry to two different pages, rather than sharing the same page
#change triple shot to basic beam, with three beams in total, offset by an equal arc
#delete second HUD menu on options menu
#--------------------------------------------------------/
#prevent any blocks from overlapping with each other
#make health bar and HP amount above the control information at bottom of screen in-game
#increase "queen" rate of fire, and raise health to 5000, and give shield like "shield enemy" that activates and deactivates at rates of 10-20 seconds each phase, enabled for 5-10 seconds
#increase base enemy spawn amount by 3x
#make an enemy "patrol" that patrols the outside border of the map, with the wave beam
#if enemies haven't moved for 5 seconds, have them change direction away from an object they are stuck on
#fix game slowdown when many shots are on screen
#change queen shoot cooldown to 0.2s, and update in WEAPON_AND_ENEMY_REFERENCE.md
#--------------------------------------------------------/
#make it so that the health box and other objects do not overlap with each other
#give player 3x health, 1.5x movement speed
#remove giant and super giant labels from obstacles
#--------------------------------------------------------/
#game; change queen shot cooldown to 1 second, and update in WEAPON_AND_ENEMY_REFERENCE.md
#--------------------------------------------------------/
#make it so that the health box does not overlap with other objects
#--------------------------------------------------------
#make it so that enemies cannot go through other objects, and must go around
#make bomb do more damage
#make it so that the health box does not overlap with other objects
#--------------------------------------------------------
#increase player health by 10x
#--------------------------------------------------------
#make it so that player is immune to player bomb damage
#make a status bar at the bottom of the screen that shows player bomb readiness status with a progress bar that is red when not ready, and purple when ready and says "BOMB" in it
#add a missile that seeks enemies and explodes on contact with "r" key
#--------------------------------------------------------/
#update controls.json with new controls 
#make suicide enemies blow up when closer to player, not at beginning of wave
#when player dies, keep enemy state on screen and allow player to continue next life from death point
#make suicide enemy twice as big, and 0.75x current movement speed
#make "tab" key create an overshield the amount of the player's health that is an orange bar that stacks on top of the player's health, and recharges every 45 seconds, with a progress bar on the bottom
#put shield recharge bar on the bottom
#make a recharge bar for the missile, place on bottom
#--------------------------------------------------------/
#when wave starts, start with overshield charged 
#jump = spacebar, add to json file controls listing
#--------------------------------------------------------/
#change "jump" name to "dash" in game and controls
#--------------------------------------------------------/
#new control: "ally_drop" key, "q": drop an ally behind you that regenerates every 30 seconds, that distracts all enemies chasing you
#set to show HUD by default
#game; fix overshield bar and health bar overlay, and amount shown in health and overshield, show bars full, with health and overshield amounts full
#--------------------------------------------------------
#start with shield, overshield, and drop ally charged at beginning of round, and add a "ALLY DROP" progress bar that is purple when charged
#--------------------------------------------------------/ 1-24-26--------------------------------------------------------------------------------------
#GPT prompt to profile game.py;
#"This repository contains a game.py file that launches the game immediately on import.
#I want you to automatically create, run, and collect profiling results for this game using cProfile, without modifying game.py itself.
#Your tasks:
#Inspect game.py to detect how the game starts (it runs on import).
#Create a new file called profile_game.py that:
#Executes game.py in a controlled way using the runpy module:
#runpy.run_module("game", run_name="__main__")
#Wraps this module execution inside a cProfile.Profile() context.
#Automatically stops profiling after ~10 seconds to avoid infinite loops.
#Saves human-readable results to profiling_results.txt sorted by cumulative time (limit to top 150 lines).
#Saves the raw stats to profiling_results.prof for SnakeViz.
#After creating the script, automatically run it using:
#python profile_game.py
#If any error occurs (import errors, missing modules, runpy issues), fix the script automatically and retry up to 3 times.
#At the end, verify both profiling files exist.
#Output for me:
#the first 60 lines of profiling_results.txt
#the detected startup mechanism of the game
#the top ~10 slowest functions summarised.
#Perform all steps automatically with no follow-up questions unless game.py is missing."**
#--------------------------------------------------------
#GPT prompt post_profiling;
# You are working in a Python repo that uses Pygame with a large monolithic file `game.py` (~7,000+ lines).
# The game is fully playable. Do NOT refactor the entire file or change core logic.

# CONTEXT:
# I recently ran a cProfile performance pass.
# The clear bottleneck is rendering: Surface.blit, pygame.draw.polygon, pygame.draw.rect,
# pygame.draw.line, pygame.draw.circle, Surface.fill, and pygame.display.flip dominate runtime.
# Physics, AI, collision, and telemetry are relatively cheap.

# GOAL:
# Perform a minimal, safe optimization pass that reduces rendering overhead by:
# 1. Reducing the number of draw calls per frame.
# 2. Caching static or rarely-changing geometry into pre-rendered surfaces.
# 3. Keeping visual output and gameplay behavior effectively the same.

# HARD CONSTRAINTS (very important):
# - Do NOT restructure the file or split systems apart.
# - Do NOT rename major systems.
# - Do NOT change game rules, input, enemy logic, ally logic, or telemetry behavior.
# - Do NOT modify database schema or telemetry.py logic.
# - Do NOT introduce new external dependencies.
# - Do NOT perform large-scale refactors or move big code blocks around.
# - Preserve all existing comments and TODOs where possible.

# FOCUS AREAS TO OPTIMIZE (from profiling results):
# - update_hazard_obstacles
# - draw_cracked_brick_wall_texture
# - draw_silver_wall_texture
# - generate_paraboloid_points
# - draw_projectile
# - draw_health_bar
# - render_hud_text
# - Any hot loops doing thousands of polygon/rect/line/blit calls per frame.

# ALLOWED STRATEGIES:
# 1. Pre-render static geometry/textures:
#    - Create one or more cached pygame.Surface objects at startup or when level layout changes.
#    - Draw static terrain, walls, cracked textures, silver walls, and hazard patterns ONCE.
#    - During each frame, blit these cached surfaces instead of redrawing all shapes.
#
# 2. Reduce redundant draw calls:
#    - If many tiny shapes are drawn per frame but rarely change, merge them into fewer surfaces.
#    - Convert repeated polygon/rect/line drawing into pre-batched surfaces.
#    - Look for predictable static geometry and combine it.
#
# 3. Cache text rendering:
#    - Cache rendered font surfaces for HUD elements that don't change every frame.
#    - Only re-render text when its underlying value changes.
#
# 4. Keep gameplay identical:
#    - Do not change hitboxes, positions, or logic.
#    - Do not alter gameplay behavior; only optimize draws.

# IMPLEMENTATION GUIDELINES:
# - Add small helper functions or cached surfaces near relevant drawing code.
# - If needed, add a small initialization step (e.g., init_cached_surfaces()) called during setup.
# - Keep modifications localized; avoid touching unrelated systems.
# - Globals for cached surfaces are allowed but should be clearly named.

# VALIDATION STEPS:
# 1. After changes, run the game:
#    - Ensure it launches without errors.
#    - Ensure menus, HUD, enemies, and terrain render correctly.
# 2. Optionally re-run the profiler (profile_game.py):
#    - Confirm cumulative time for rendering calls decreases.

# DELIVERABLES:
# - Updated `game.py` with localized render optimizations.
# - A short explanation describing:
#   - What was optimized.
#   - Where caching or batching was applied.
#   - Any trade-offs or notes for future improvements.

# Reminder: This is a SURGICAL optimization pass focused ONLY on rendering.
# Avoid touching anything outside the draw/render systems.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------/
#GPT verification post-rendering optimization;
# VERIFY RENDERING OPTIMIZATION CHANGES
#
# You are verifying the recent rendering optimization changes made to `game.py`.
# Do NOT make additional refactors or broad changes.
# Do NOT rewrite large sections of code.
# Only confirm correctness and fix local issues caused specifically by the optimization pass.
#
# WHAT TO VERIFY:
# 1. The game starts without errors.
# 2. The cached surfaces, pre-rendered textures, and batched draw calls work correctly.
# 3. The following must render as before:
#    - Player, enemies, allies
#    - Projectiles
#    - Static geometry (walls, cracked texture, silver texture)
#    - Hazards and obstacle visuals
#    - Health bars, HUD text, menus
# 4. The visual output must match the original behavior:
#    - No missing graphics
#    - No invisible terrain
#    - No duplicated drawing
#    - No flickering, overdraw, or weird artifacts
# 5. Cached surfaces should update correctly IF level geometry changes.
#
# FIX SCOPE:
# - If there are errors, missing textures, or incorrect visuals from the caching changes:
#   * Fix ONLY those problems in the smallest, most localized way possible.
# - Do NOT rewrite logic unrelated to rendering.
# - Do NOT alter core gameplay, physics, AI, or telemetry.
# - Keep modifications minimal and safe.
#
# OPTIONAL (if safe to perform):
# - Briefly run the profiling script (`python profile_game.py`) to ensure render times have improved.
# - Show me the top 40 lines of the new profiling output if the script was re-run successfully.
#
# FINAL OUTPUT REQUIREMENTS:
# - Summarize what visual issues (if any) were found.
# - Summarize what local fixes you applied (if any).
# - Confirm the game now renders correctly with the cached surfaces and optimizations.
#
# AGAIN, DO NOT perform large refactors. Only verify and fix local issues from the render optimization.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------/
#GPT prompt to add a main entry point to game.py;
# ADD A MAIN ENTRY POINT TO game.py
#
# GOAL:
# Wrap the current top-level startup and main game loop in game.py into a function called main(),
# and add the standard Python entry guard:
#
#     if __name__ == "__main__":
#         main()
#
# This will make profiling, testing, and future tools easier.
#
# VERY IMPORTANT CONSTRAINTS:
# - Do NOT change gameplay behavior.
# - Do NOT restructure the entire file.
# - Do NOT move large blocks of code into other modules.
# - Do NOT rename any existing functions or classes.
# - Do NOT modify telemetry, physics, AI, enemy logic, ally logic, or the event loop.
# - Keep all globals, constants, and initialization the same.
# - Only encapsulate the existing top-level “game startup + main loop” code inside main().
#
# IMPLEMENTATION DETAILS:
# 1. Locate the section of game.py that runs immediately on import:
#    - pygame.init()
#    - screen/display setup
#    - creating the clock
#    - creating player/enemy states
#    - the main while-loop (“while running:”)
#    - the try/except/finally cleanup
#
# 2. Wrap ALL of that import-time code inside:
#        def main():
#            <original code>
#
# 3. Add this block at the bottom of game.py:
#
#        if __name__ == "__main__":
#            main()
#
# 4. Do NOT modify any logic within the loop.
# 5. Do NOT create new modules or move code outside game.py.
#
# AFTER APPLYING CHANGES:
# - Run `python game.py` to confirm the game still starts, plays, and exits normally.
# - Ensure no visual, gameplay, or physics differences from before.
#
# OUTPUT:
# - Summarize which lines were wrapped into main(), and confirm behavior is unchanged.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#GPT prompt to extract constants into constants.py; # EXTRACT CONSTANTS INTO constants.py
#
# GOAL:
# Create a new file named constants.py and move ONLY simple constant definitions
# out of game.py into that file. Then import them back into game.py.
#
# WHAT COUNTS AS A CONSTANT:
# - All-caps variable names (e.g., SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_MAX_HEALTH)
# - Color tuples (e.g., RED = (255,0,0))
# - Static numbers used for tuning (e.g., BASE_SPEED = 5.0)
# - Difficulty multipliers
# - Weapon base properties if they are defined as immutable data
#
# WHAT MUST *NOT* BE MOVED:
# - Anything that changes at runtime
# - Anything that depends on pygame being initialized (Surfaces, Rects, fonts)
# - Anything that is modified inside the game loop
# - Anything that is a list/dict that the game mutates (unless it is a pure config dict)
#
# SPECIFIC TASKS:
# 1. Create constants.py
# 2. Move the simple constant assignments from game.py into constants.py
# 3. In game.py, import the constants:
#        from constants import *
#    (using wildcard import is fine for constants)
# 4. Do NOT modify game logic.
# 5. Do NOT change behavior.
# 6. Do NOT move functions, classes, or any runtime objects.
#
# ALLOWED MOVES:
# - Screen dimensions
# - Color values
# - Weapon base values that do not change
# - Character base stats that do not change
# - Tuning values (enemy spawn rate multipliers, difficulty constants)
# - Physics constants (gravity, dash cooldown, etc.)
#
# AFTER EXTRACTION:
# - Confirm that python game.py still launches and behaves normally.
# - Summarize which constants were moved.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------/
# TASK: FINISH CONFIG EXTRACTION FROM game.py
#
# GOAL:
# Move remaining pure configuration data and tuning values out of game.py into:
#   - constants.py      (global tuning values, base constants)
#   - config_weapons.py (weapon definitions, if helpful)
#   - config_enemies.py (enemy base definitions, if helpful)
#
# WHAT TO MOVE:
# - Pure data that does NOT change at runtime:
#   * Difficulty multipliers
#   * Base health/shield values for player classes
#   * Base damage, cooldown, ammo capacity per weapon
#   * Enemy base HP, speed, damage, score value, etc.
#   * Spawn rate multipliers (e.g., EASY/HARD modifiers)
# - Data that is *used* by the game but not modified by it.
#
# WHAT MUST NOT BE MOVED:
# - Any variable that is mutated during the game.
# - Lists/dicts that are appended to, popped from, or modified dynamically.
# - Any object that depends on pygame initialization (Surfaces, Rects, fonts).
#
# FILE STRUCTURE:
# - constants.py: shared tuning constants, global scalar values, simple dicts.
# - config_weapons.py: weapon definitions as dicts or dataclasses.
# - config_enemies.py: enemy archetypes as dicts or dataclasses.
#
# IMPLEMENTATION:
# 1) Create config_weapons.py and config_enemies.py if they do not exist.
# 2) Move appropriate config blocks out of game.py into those files.
# 3) In game.py, replace the moved definitions with imports:
#       from constants import *
#       from config_weapons import WEAPONS  # or similar
#       from config_enemies import ENEMIES  # or similar
# 4) Keep the data structures identical so existing code can still index them.
#
# CONSTRAINTS:
# - Do NOT change game logic or behavior.
# - Do NOT rename keys or reorganize the structure of config dicts unless absolutely necessary.
# - Do NOT move any runtime state out of game.py.
#
# AFTER CHANGES:
# - Run `python game.py` and confirm the game still behaves exactly the same.
# - Summarize which config blocks were moved and to which files.
#--------------------------------------------------------------------------------------------------------------------
#enemies prioritize player over allies
#--------------------------------------------------------------------------------------------------------------------
#fix issue where bullets and damage stay on screen after enemies have died
#--------------------------------------------------------------------------------------------------------------------
#GPT;
# TASK: EXTRACT RENDER HELPERS INTO rendering.py
#
# GOAL:
# Move pure drawing / rendering helper functions out of game.py into a new module
# named rendering.py, then import and use them from game.py.
#
# CANDIDATE FUNCTIONS TO MOVE:
# - draw_silver_wall_texture(...)
# - draw_cracked_brick_wall_texture(...)
# - draw_projectile(...)
# - draw_health_bar(...)
# - draw_centered_text(...)
# - render_hud_text(...)
# - Any other small helpers that ONLY deal with drawing on a surface.
#
# WHAT MUST STAY:
# - The main game loop and orchestration stay in game.py.
# - Functions that directly mix logic and drawing should stay in game.py for now.
#
# IMPLEMENTATION:
# 1) Create rendering.py.
# 2) Move the identified drawing helper functions from game.py into rendering.py.
# 3) Ensure rendering.py has the minimal imports it needs (e.g., pygame, typing).
# 4) In game.py, import the moved functions:
#       from rendering import (
#           draw_silver_wall_texture,
#           draw_cracked_brick_wall_texture,
#           draw_projectile,
#           draw_health_bar,
#           draw_centered_text,
#           render_hud_text,
#       )
# 5) Update call sites in game.py only as needed to reference the imported names.
#    The function signatures and behaviors should remain the same.
#
# CONSTRAINTS:
# - Do NOT change what these functions draw or how they behave.
# - Do NOT introduce new dependencies beyond pygame/typing/whatever they already used.
# - Do NOT refactor game logic; this is a pure “move helpers out” step.
#
# AFTER CHANGES:
# - Run `python game.py` to confirm the game still renders as before (HUD, walls,
#   projectiles, health bars, etc.).
# - Summarize which functions were moved into rendering.py.
#--------------------------------------------------------------------------------------------------------------------
# TASK: EXTRACT ENEMY/ALLY BEHAVIOR HELPERS
#
# GOAL:
# Move enemy- and ally-related helper functions out of game.py into:
#   - enemies.py  (enemy movement, targeting, behavior helpers)
#   - allies.py   (ally movement/behavior helpers)  [optional but preferred]
#
# CANDIDATE FUNCTIONS TO MOVE (EXAMPLES):
# - move_enemy_with_push_cached(...)
# - find_nearest_threat(...)
# - find_nearest_enemy(...)
# - any small, reusable functions that operate on enemy or ally data structures
#   but do not directly depend on the main loop.
#
# IMPLEMENTATION:
# 1) Create enemies.py (and allies.py if there are clear ally-specific helpers).
# 2) Move enemy-related helpers into enemies.py.
# 3) Move ally-related helpers into allies.py.
# 4) In game.py, import them:
#       from enemies import move_enemy_with_push_cached, find_nearest_threat, find_nearest_enemy
#       from allies import update_friendly_ai   # or whichever functions exist
# 5) Keep function signatures the same so existing call sites in game.py work
#    without major changes.
#
# CONSTRAINTS:
# - Do NOT change the logic of enemy or ally behavior in this step.
# - Do NOT change data formats of enemies/allies (dict structure, etc.).
# - Do NOT move the main update loop; only helpers.
# - Keep imports minimal in enemies.py/allies.py (only what they need).
#
# AFTER CHANGES:
# - Run `python game.py` to confirm that enemy and ally behavior matches the
#   previous version (movement, targeting, interactions).
# - Summarize which functions were moved into enemies.py/allies.py.

#--------------------------------------------------------------------------------------------------------------------
# TASK: INTRODUCE A BASIC GameState CONTAINER (FIRST STEP ONLY)
#
# GOAL:
# Define a GameState dataclass to group some core game lists (enemies,
# projectiles, allies, etc.) and start using it in a limited, gentle way,
# WITHOUT rewriting the whole game.
#
# SCOPE OF THIS STEP:
# - Create GameState in a new file state.py.
# - Use GameState for a small subset of global lists (for example:
#   enemies, player_bullets, enemy_projectiles, friendly_projectiles).
# - Update a LIMITED number of functions to accept a GameState instance
#   instead of reading/modifying those globals directly.
#
# IMPLEMENTATION:
# 1) Create state.py with something like:
#       from dataclasses import dataclass, field
#
#       @dataclass
#       class GameState:
#           enemies: list = field(default_factory=list)
#           player_bullets: list = field(default_factory=list)
#           enemy_projectiles: list = field(default_factory=list)
#           friendly_projectiles: list = field(default_factory=list)
#           # (Optionally add more fields later; keep this minimal at first.)
#
# 2) In game.py:
#    - Import GameState: from state import GameState
#    - In main(), create a GameState instance:
#          state = GameState()
#    - Replace the corresponding global lists with fields on state, for example:
#          # Instead of: enemies = []
#          # Use:       state.enemies
#
# 3) Update a small number of functions that operate heavily on these lists
#    (e.g., projectile update / spawn functions, basic enemy update) so they
#    accept a `state` parameter instead of relying on global variables.
#
# 4) Keep all other globals as-is for now. This is a FIRST STEP ONLY.
#
# CONSTRAINTS:
# - Do NOT attempt to move ALL globals into GameState in one pass.
# - Do NOT change game behavior or data formats.
# - Do NOT refactor unrelated systems while doing this.
#
# AFTER CHANGES:
# - Run `python game.py` and verify gameplay is unchanged.
# - Summarize:
#   * What fields were added to GameState.
#   * Which functions were updated to use the GameState instance.

#--------------------------------------------------------------------------------------------------------------------
# (Improvement comments moved to GAME_IMPROVEMENTS.md)

#--------------------------------------------------------------------------------------------------------------------
# (Improvement comments moved to GAME_IMPROVEMENTS.md)

#--------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------