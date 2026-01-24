#FEATURES TO ADD
#--------------------------------------------------------
#change player bullet color
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





import math
import warnings

# Suppress pygame's pkg_resources deprecation warning
# This is a pygame internal issue, not our code
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
import random
import json
import os

import pygame
import sqlite3
from datetime import datetime, timezone

# Try to import C extension for performance, fallback to Python if not available
# Note: game_physics module is built from game_physics.c - see BUILD_INSTRUCTIONS.md
try:
    import game_physics  # type: ignore
    USE_C_EXTENSION = True
except ImportError:
    USE_C_EXTENSION = False
    print("Note: C extension not available, using Python fallback (slower)")

# GPU acceleration (optional - falls back to CPU if unavailable)
try:
    from gpu_physics import update_bullets_batch, check_collisions_batch, CUDA_AVAILABLE
    USE_GPU = CUDA_AVAILABLE
    if USE_GPU:
        print("GPU acceleration enabled (CUDA)")
    else:
        print("GPU acceleration available but CUDA not detected (using CPU fallback)")
except ImportError:
    USE_GPU = False
    print("Note: GPU acceleration not available. Install with: pip install numba")

from telemetry import (
    Telemetry,
    EnemySpawnEvent,
    PlayerPosEvent,
    ShotEvent,
    EnemyHitEvent,
    PlayerDamageEvent,
    PlayerDeathEvent,
    WaveEvent,
    WaveEnemyTypeEvent,
    EnemyPositionEvent,
    PlayerVelocityEvent,
    BulletMetadataEvent,
    PlayerActionEvent,
    ZoneVisitEvent,
    FriendlyAISpawnEvent,
    FriendlyAIPositionEvent,
    FriendlyAIShotEvent,
    FriendlyAIDeathEvent,
)

# ----------------------------
# Controls (remappable) - module level constants
# ----------------------------
CONTROLS_PATH = "controls.json"
DEFAULT_CONTROLS = {
    "move_left": "a",
    "move_right": "d",
    "move_up": "w",
    "move_down": "s",
    "boost": "left shift",
    "slow": "left ctrl",
    "dash": "space",
    "ally_drop": "q",
}

# Placeholder WIDTH/HEIGHT for module-level initialization
# Will be updated in main() after pygame.display.init()
WIDTH = 1920  # Default placeholder
HEIGHT = 1080  # Default placeholder

# ----------------------------
# Rendering cache for performance optimization
# ----------------------------
# Cache for pre-rendered wall textures (key: (width, height, crack_level), value: Surface)
_wall_texture_cache = {}
# Cache for pre-rendered static block surfaces
_cached_trapezoid_surfaces = {}
_cached_triangle_surfaces = {}
# Cache for HUD text surfaces (key: (text, color), value: Surface)
_hud_text_cache = {}
# Cache for health bar surfaces (key: (width, height, hp_ratio), value: Surface)
_health_bar_cache = {}


def main():
    """Main entry point for the game."""
    global screen, clock, font, big_font, small_font, WIDTH, HEIGHT
    global running, state, player, enemies, player_bullets, enemy_projectiles
    global telemetry, telemetry_enabled, run_id, run_time, survival_time
    global player_hp, player_max_hp, player_speed, player_bullet_damage
    global player_time_since_shot, shots_fired, hits, damage_taken, damage_dealt
    global enemies_spawned, enemies_killed, deaths, wave_number, time_to_next_wave
    global wave_active, score, lives, current_level, max_level, wave_in_level
    global current_weapon_mode, previous_weapon_mode, unlocked_weapons
    global overshield, overshield_recharge_timer, shield_active, shield_duration_remaining
    global shield_cooldown_remaining, shield_recharge_timer, grenade_time_since_used
    global missile_time_since_used, jump_cooldown_timer, jump_timer, is_jumping
    global jump_velocity, laser_beams, wave_beams, laser_time_since_shot
    global player_current_zones, previous_boost_state, previous_slow_state
    global ally_drop_timer, dropped_ally, friendly_ai, friendly_projectiles
    global fire_rate_buff_t, pos_timer
    global run_started_at, run_ended_at, continue_blink_t, player_name_input
    global name_input_active, final_score_for_high_score
    global survival_time, wave_beam_time_since_shot, wave_active
    global menu_section, difficulty_selected, aiming_mode_selected, use_character_profile_selected
    global character_profile_selected, custom_profile_stat_selected, player_class_selected
    global ui_show_metrics_selected, beam_selection_selected, endurance_mode_selected
    global previous_game_state, pause_selected, difficulty, aiming_mode, use_character_profile
    global player_class, custom_profile_stats, custom_profile_stats_keys, testing_mode
    global weapon_selection_options, current_weapon_mode, unlocked_weapons, wave_beam_pattern_index
    global beam_selection_pattern, ui_show_metrics, ui_show_hud, player_shoot_cooldown
    global pickups, damage_numbers, weapon_pickup_messages, trapezoid_blocks, triangle_blocks
    global destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks
    global hazard_obstacles, moving_health_zone, ui_show_health_bars, ui_show_player_health_bar
    global _cached_trapezoid_surfaces, _cached_triangle_surfaces
    global last_horizontal_key, last_vertical_key, last_move_velocity, boost_meter, boost_meter_max
    global boost_drain_per_s, boost_regen_per_s, boost_speed_mult, player_bullet_shape_index
    global blocks, player_bullets, enemy_projectiles, friendly_ai, friendly_projectiles
    global grenade_explosions, missiles, friendly_ai_templates, overshield_max, grenade_cooldown, missile_cooldown, ally_drop_cooldown
    
    pygame.init()

    # Welcome message when game launches
    print("welcome to my game! :D")

    # ----------------------------
    # Window / timing
    # ----------------------------
    # Start in fullscreen mode
    pygame.display.init()
    screen_info = pygame.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mouse Aim Shooter + Telemetry (SQLite)")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 56)
    small_font = pygame.font.SysFont(None, 20)

    # Initialize player and other game state variables that depend on WIDTH/HEIGHT
    player = pygame.Rect((WIDTH - 28) // 2, (HEIGHT - 28) // 2, 28, 28)
    
    # Initialize pygame mouse visibility
    pygame.mouse.set_visible(True)
    
    # Load controls from file (now that pygame is initialized)
    # This must happen after pygame.init() to avoid warnings
    global controls
    if not controls:  # Only load if not already loaded
        controls = load_controls()
    
    # Filter blocks to prevent overlaps (moved from module level)
    global destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks
    destructible_blocks = filter_blocks_no_overlap(destructible_blocks, [moveable_destructible_blocks, giant_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], player)
    moveable_destructible_blocks = filter_blocks_no_overlap(moveable_destructible_blocks, [destructible_blocks, giant_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], player)
    giant_blocks = filter_blocks_no_overlap(giant_blocks, [destructible_blocks, moveable_destructible_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], player)
    super_giant_blocks = filter_blocks_no_overlap(super_giant_blocks, [destructible_blocks, moveable_destructible_blocks, giant_blocks, trapezoid_blocks, triangle_blocks], player)

    # ----------------------------
    # Start run + log initial spawns
    # ----------------------------
    run_id = None  # Will be set when game starts
    # Don't start wave automatically - wait for menu selection

    # ----------------------------
    # Main loop with safe shutdown
    # ----------------------------
    # Note: telemetry_enabled and telemetry are module-level variables,
    # so we can modify them directly without global declaration in the main loop
    # Initialize high scores database
    init_high_scores_db()

    # Main loop with safe shutdown
    running = True
    FPS = 60
    
    try:
        while running:
            dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
            run_time += dt
            survival_time += dt
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle keyboard events
                if event.type == pygame.KEYDOWN:
                    # ESC key handling
                    if event.key == pygame.K_ESCAPE:
                        if state == STATE_PLAYING or state == STATE_ENDURANCE:
                            previous_game_state = state
                            state = STATE_PAUSED
                            pause_selected = 0
                        elif state == STATE_PAUSED:
                            state = previous_game_state if previous_game_state else STATE_PLAYING
                        elif state == STATE_CONTINUE:
                            running = False
                        elif state == STATE_CONTROLS:
                            state = STATE_PAUSED
                        elif state == STATE_MENU:
                            running = False
                        elif state == STATE_VICTORY or state == STATE_GAME_OVER or state == STATE_HIGH_SCORES:
                            running = False
                        elif state == STATE_NAME_INPUT:
                            if player_name_input.strip():
                                save_high_score(
                                    player_name_input.strip(),
                                    final_score_for_high_score,
                                    wave_number - 1,
                                    survival_time,
                                    enemies_killed,
                                    difficulty
                                )
                            state = STATE_HIGH_SCORES
                            name_input_active = False
                    
                    # P key for pause
                    if event.key == pygame.K_p:
                        if state == STATE_PLAYING or state == STATE_ENDURANCE:
                            previous_game_state = state
                            state = STATE_PAUSED
                            pause_selected = 0
                        elif state == STATE_PAUSED:
                            state = previous_game_state if previous_game_state else STATE_PLAYING
                    
                    # Pause menu navigation
                    if state == STATE_PAUSED:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            pause_selected = (pause_selected - 1) % len(pause_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            pause_selected = (pause_selected + 1) % len(pause_options)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            choice = pause_options[pause_selected]
                            if choice == "Continue":
                                state = previous_game_state if previous_game_state else STATE_PLAYING
                            elif choice == "Quit":
                                running = False
                    
                    # Menu navigation
                    if state == STATE_MENU:
                        if menu_section == 0:  # Difficulty selection
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                difficulty_selected = (difficulty_selected - 1) % len(difficulty_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                difficulty_selected = (difficulty_selected + 1) % len(difficulty_options)
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                difficulty = difficulty_options[difficulty_selected]
                                menu_section = 1  # Go to aiming mode
                        elif menu_section == 1:  # Aiming mode
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                aiming_mode_selected = (aiming_mode_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                aiming_mode_selected = (aiming_mode_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 0  # Go back
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                aiming_mode = AIM_MOUSE if aiming_mode_selected == 0 else AIM_ARROWS
                                menu_section = 1.5  # Go to character profile yes/no
                        elif menu_section == 1.5:  # Character profile yes/no
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                use_character_profile_selected = (use_character_profile_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                use_character_profile_selected = (use_character_profile_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 1  # Go back
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                use_character_profile = use_character_profile_selected == 1
                                if use_character_profile:
                                    menu_section = 2  # Go to profile selection
                                else:
                                    menu_section = 3  # Skip to options
                        elif menu_section == 2:  # Character profile selection
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                character_profile_selected = (character_profile_selected - 1) % len(character_profile_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                character_profile_selected = (character_profile_selected + 1) % len(character_profile_options)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 1.5  # Go back
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                if character_profile_selected == 0:
                                    menu_section = 7  # Go to class selection
                                elif character_profile_selected == 1:
                                    menu_section = 6  # Go to custom profile creator
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                if character_profile_selected == 0:
                                    menu_section = 7  # Go to class selection
                                elif character_profile_selected == 1:
                                    menu_section = 6  # Go to custom profile creator
                        elif menu_section == 6:  # Custom profile creator
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                custom_profile_stat_selected = (custom_profile_stat_selected - 1) % len(custom_profile_stats_list)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                custom_profile_stat_selected = (custom_profile_stat_selected + 1) % len(custom_profile_stats_list)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                                custom_profile_stats[stat_key] = max(0.5, custom_profile_stats[stat_key] - 0.1)
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                menu_section = 3  # Continue to options
                            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                                stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                                custom_profile_stats[stat_key] = min(3.0, custom_profile_stats[stat_key] + 0.1)
                            elif event.key == pygame.K_MINUS:
                                stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                                custom_profile_stats[stat_key] = max(0.5, custom_profile_stats[stat_key] - 0.1)
                        elif menu_section == 7:  # Class selection
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                player_class_selected = (player_class_selected - 1) % len(player_class_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                player_class_selected = (player_class_selected + 1) % len(player_class_options)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 2  # Go back
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                player_class = player_class_options[player_class_selected]
                                menu_section = 3  # Go to options
                        elif menu_section == 3:  # HUD options
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                ui_show_metrics_selected = (ui_show_metrics_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                ui_show_metrics_selected = (ui_show_metrics_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                if use_character_profile:
                                    menu_section = 7 if character_profile_selected == 0 else 6
                                else:
                                    menu_section = 1.5
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                ui_show_metrics = ui_show_metrics_selected == 0
                                ui_show_hud = ui_show_metrics
                                if testing_mode:
                                    menu_section = 4  # Go to weapon selection
                                else:
                                    menu_section = 5  # Go to start
                        elif menu_section == 4:  # Weapon selection (testing mode)
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                beam_selection_selected = (beam_selection_selected - 1) % len(weapon_selection_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                beam_selection_selected = (beam_selection_selected + 1) % len(weapon_selection_options)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 3  # Go back
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                selected_weapon = weapon_selection_options[beam_selection_selected]
                                unlocked_weapons.add(selected_weapon)
                                if current_weapon_mode == "wave_beam" and selected_weapon != "wave_beam":
                                    wave_beams.clear()
                                if current_weapon_mode == "laser" and selected_weapon != "laser":
                                    laser_beams.clear()
                                current_weapon_mode = selected_weapon
                                if selected_weapon == "wave_beam":
                                    wave_beam_pattern_index = 0
                                    beam_selection_pattern = "sine"
                                else:
                                    beam_selection_pattern = selected_weapon
                                menu_section = 5  # Go to start
                        elif menu_section == 5:  # Start game
                            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                if testing_mode:
                                    menu_section = 4
                                else:
                                    menu_section = 3
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                # Initialize game
                                if telemetry_enabled:
                                    telemetry = Telemetry(db_path="game_telemetry.db", flush_interval_s=0.5, max_buffer=700)
                                else:
                                    class NoOpTelemetry:
                                        def __getattr__(self, name):
                                            return lambda *args, **kwargs: None
                                    telemetry = NoOpTelemetry()
                                
                                # Apply class stats
                                stats = player_class_stats[player_class]
                                player_max_hp = int(1000 * stats["hp_mult"])
                                player_hp = player_max_hp
                                player_speed = int(300 * stats["speed_mult"])
                                player_bullet_damage = int(20 * stats["damage_mult"])
                                player_shoot_cooldown = 0.12 / stats["firerate_mult"]
                                
                                # Set state
                                if endurance_mode_selected == 1:
                                    state = STATE_ENDURANCE
                                    lives = 999
                                    previous_game_state = STATE_ENDURANCE
                                else:
                                    state = STATE_PLAYING
                                    previous_game_state = STATE_PLAYING
                                
                                run_id = telemetry.start_run(run_started_at, player_max_hp) if telemetry_enabled else None
                                start_wave(wave_number)
                    
                    # Controls rebinding
                    if state == STATE_CONTROLS and controls_rebinding:
                        if event.key != pygame.K_ESCAPE:
                            action = controls_actions[controls_selected]
                            controls[action] = event.key
                            save_controls(controls)
                            controls_rebinding = False
                        else:
                            controls_rebinding = False
                    
                    # Shield activation (Left Alt)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_LALT:
                        if shield_cooldown_remaining <= 0.0 and not shield_active:
                            shield_active = True
                            shield_duration_remaining = shield_duration
                            shield_cooldown = random.uniform(10.0, 15.0)
                            shield_recharge_cooldown = shield_cooldown
                            shield_recharge_timer = 0.0
                            shield_cooldown_remaining = 0.0
                    
                    # Overshield activation (Tab)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_TAB:
                        if overshield_recharge_timer >= overshield_recharge_cooldown:
                            overshield = player_max_hp
                            overshield_max = max(overshield_max, player_max_hp)
                            overshield_recharge_timer = 0.0
                    
                    # Grenade (E key)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_e:
                        if grenade_time_since_used >= grenade_cooldown:
                            grenade_radius = player.w * 10  # 10x player size
                            grenade_explosions.append({
                                "x": player.centerx,
                                "y": player.centery,
                                "radius": 0,
                                "max_radius": grenade_radius,
                                "timer": 0.3,  # Explosion duration
                                "damage": grenade_damage
                            })
                            grenade_time_since_used = 0.0
                    
                    # Missile (R key)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_r:
                        if missile_time_since_used >= missile_cooldown:
                            # Find nearest enemy as target
                            target_enemy = None
                            min_dist = float("inf")
                            for enemy in enemies:
                                dist = (pygame.Vector2(enemy["rect"].center) - pygame.Vector2(player.center)).length_squared()
                                if dist < min_dist:
                                    min_dist = dist
                                    target_enemy = enemy
                            
                            if target_enemy:
                                missile_rect = pygame.Rect(player.centerx - 8, player.centery - 8, 16, 16)
                                missiles.append({
                                    "rect": missile_rect,
                                    "vel": pygame.Vector2(0, 0),
                                    "target_enemy": target_enemy,
                                    "speed": 500,
                                    "damage": missile_damage,
                                    "explosion_radius": 150
                                })
                                missile_time_since_used = 0.0
                    
                    # Ally drop (Q key)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == controls.get("ally_drop", pygame.K_q):
                        if ally_drop_timer >= ally_drop_cooldown:
                            if dropped_ally and dropped_ally in friendly_ai:
                                friendly_ai.remove(dropped_ally)
                            
                            # Find tank template
                            tank_template = None
                            for tmpl in friendly_ai_templates:
                                if tmpl.get("type") == "tank":
                                    tank_template = tmpl
                                    break
                            
                            if tank_template:
                                player_center = pygame.Vector2(player.center)
                                if last_move_velocity.length_squared() > 0:
                                    spawn_dir = -last_move_velocity.normalize()
                                else:
                                    spawn_dir = pygame.Vector2(0, 1)
                                
                                spawn_pos = player_center + spawn_dir * 60  # Spawn 60 pixels behind player
                                friendly = make_friendly_from_template(tank_template, 1.0, 1.0)
                                friendly["rect"].center = (int(spawn_pos.x), int(spawn_pos.y))
                                friendly_ai.append(friendly)
                                dropped_ally = friendly
                            
                            ally_drop_timer = 0.0
                    
                    # Weapon switching (keys 1-6)
                    if state == STATE_PLAYING or state == STATE_ENDURANCE:
                        if event.key == pygame.K_1 and "basic" in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            current_weapon_mode = "basic"
                        elif event.key == pygame.K_2 and "rocket" in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            if previous_weapon_mode == "wave_beam":
                                wave_beams.clear()
                            if previous_weapon_mode == "laser":
                                laser_beams.clear()
                            current_weapon_mode = "rocket"
                        elif event.key == pygame.K_3 and "triple" in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            if previous_weapon_mode == "wave_beam":
                                wave_beams.clear()
                            if previous_weapon_mode == "laser":
                                laser_beams.clear()
                            current_weapon_mode = "triple"
                        elif event.key == pygame.K_4 and "bouncing" in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            if previous_weapon_mode == "wave_beam":
                                wave_beams.clear()
                            if previous_weapon_mode == "laser":
                                laser_beams.clear()
                            current_weapon_mode = "bouncing"
                        elif event.key == pygame.K_5 and "giant" in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            if previous_weapon_mode == "wave_beam":
                                wave_beams.clear()
                            if previous_weapon_mode == "laser":
                                laser_beams.clear()
                            current_weapon_mode = "giant"
                        elif event.key == pygame.K_6 and "laser" in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            if previous_weapon_mode == "wave_beam":
                                wave_beams.clear()
                            current_weapon_mode = "laser"
                        elif event.key == pygame.K_7 and "wave_beam" in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            if previous_weapon_mode == "laser":
                                laser_beams.clear()
                            current_weapon_mode = "wave_beam"
                            wave_beam_pattern_index = 0
                            beam_selection_pattern = "sine"
            
            # Game state updates (only when playing)
            if state == STATE_PLAYING or state == STATE_ENDURANCE:
                # Update timers
                player_time_since_shot += dt
                laser_time_since_shot += dt
                wave_beam_time_since_shot += dt
                grenade_time_since_used += dt
                missile_time_since_used += dt
                jump_cooldown_timer += dt
                jump_timer += dt
                overshield_recharge_timer += dt
                shield_duration_remaining -= dt
                shield_cooldown_remaining -= dt
                shield_recharge_timer += dt
                ally_drop_timer += dt
                fire_rate_buff_t += dt
                pos_timer += dt
                continue_blink_t += dt
                
                # Update shield
                if shield_active:
                    if shield_duration_remaining <= 0.0:
                        shield_active = False
                        shield_cooldown_remaining = shield_cooldown
                        shield_recharge_timer = 0.0
                
                # Update jump/dash
                if is_jumping:
                    jump_timer += dt
                    if jump_timer >= jump_duration:
                        is_jumping = False
                        jump_velocity = pygame.Vector2(0, 0)
                
                # Update hazard obstacles
                update_hazard_obstacles(dt)
                
                # Update pickup effects
                update_pickup_effects(dt)
                
                # Player movement and input handling
                keys = pygame.key.get_pressed()
                
                # Get movement input
                move_x = 0
                move_y = 0
                
                # Handle movement keys
                if keys[controls.get("move_left", pygame.K_a)]:
                    move_x = -1
                    last_horizontal_key = controls.get("move_left", pygame.K_a)
                elif keys[controls.get("move_right", pygame.K_d)]:
                    move_x = 1
                    last_horizontal_key = controls.get("move_right", pygame.K_d)
                
                if keys[controls.get("move_up", pygame.K_w)]:
                    move_y = -1
                    last_vertical_key = controls.get("move_up", pygame.K_w)
                elif keys[controls.get("move_down", pygame.K_s)]:
                    move_y = 1
                    last_vertical_key = controls.get("move_down", pygame.K_s)
                
                # Boost/slow mechanics
                is_boosting = keys[controls.get("boost", pygame.K_LSHIFT)] and boost_meter > 0
                is_slowing = keys[controls.get("slow", pygame.K_LCTRL)]
                
                if is_boosting:
                    boost_meter = max(0, boost_meter - boost_drain_per_s * dt)
                    speed_mult = boost_speed_mult
                    previous_boost_state = True
                else:
                    boost_meter = min(boost_meter_max, boost_meter + boost_regen_per_s * dt)
                    speed_mult = 1.0
                    previous_boost_state = False
                
                if is_slowing:
                    speed_mult *= slow_speed_mult
                    previous_slow_state = True
                else:
                    previous_slow_state = False
                
                # Apply fire rate buff
                effective_fire_rate = player_shoot_cooldown
                if fire_rate_buff_t < fire_rate_buff_duration:
                    effective_fire_rate *= fire_rate_mult
                
                # Calculate movement
                if move_x != 0 or move_y != 0:
                    move_dir = pygame.Vector2(move_x, move_y).normalize()
                    move_speed = player_speed * speed_mult * player_stat_multipliers["speed"]
                    
                    # Apply jump/dash velocity
                    if is_jumping:
                        move_speed += jump_velocity.length()
                    
                    move_amount = move_speed * dt
                    move_vec = move_dir * move_amount
                    
                    last_move_velocity = move_dir * move_speed
                    
                    # Move player with collision
                    move_player_with_push(player, int(move_vec.x), int(move_vec.y), blocks)
                    clamp_rect_to_screen(player)
                else:
                    last_move_velocity = pygame.Vector2(0, 0)
                
                # Update jump/dash
                if is_jumping:
                    player.x += int(jump_velocity.x * dt)
                    player.y += int(jump_velocity.y * dt)
                    clamp_rect_to_screen(player)
                
                # Player shooting
                mouse_buttons = pygame.mouse.get_pressed()
                shoot_input = mouse_buttons[0] or (aiming_mode == AIM_ARROWS and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]))
                
                if shoot_input and player_time_since_shot >= effective_fire_rate:
                    spawn_player_bullet_and_log()
                    player_time_since_shot = 0.0
                
                # Laser beam weapon
                if current_weapon_mode == "laser" and laser_time_since_shot >= laser_cooldown:
                    if aiming_mode == AIM_ARROWS:
                        keys = pygame.key.get_pressed()
                        dx = (1 if keys[pygame.K_RIGHT] else 0) - (1 if keys[pygame.K_LEFT] else 0)
                        dy = (1 if keys[pygame.K_DOWN] else 0) - (1 if keys[pygame.K_UP] else 0)
                        if dx == 0 and dy == 0:
                            if last_move_velocity.length_squared() > 0:
                                direction = last_move_velocity.normalize()
                            else:
                                direction = pygame.Vector2(1, 0)
                        else:
                            direction = pygame.Vector2(dx, dy).normalize()
                    else:
                        mx, my = pygame.mouse.get_pos()
                        direction = vec_toward(player.centerx, player.centery, mx, my)
                    
                    end_pos = pygame.Vector2(player.center) + direction * laser_length
                    laser_beams.append({
                        "start": pygame.Vector2(player.center),
                        "end": end_pos,
                        "color": (255, 50, 50),
                        "width": 5,
                        "damage": laser_damage,
                        "timer": 0.1
                    })
                    laser_time_since_shot = 0.0
                
                # Wave beam weapon
                if current_weapon_mode == "wave_beam" and wave_beam_time_since_shot >= wave_beam_cooldown:
                    if aiming_mode == AIM_ARROWS:
                        keys = pygame.key.get_pressed()
                        dx = (1 if keys[pygame.K_RIGHT] else 0) - (1 if keys[pygame.K_LEFT] else 0)
                        dy = (1 if keys[pygame.K_DOWN] else 0) - (1 if keys[pygame.K_UP] else 0)
                        if dx == 0 and dy == 0:
                            if last_move_velocity.length_squared() > 0:
                                direction = last_move_velocity.normalize()
                            else:
                                direction = pygame.Vector2(1, 0)
                        else:
                            direction = pygame.Vector2(dx, dy).normalize()
                    else:
                        mx, my = pygame.mouse.get_pos()
                        direction = vec_toward(player.centerx, player.centery, mx, my)
                    
                    pattern = wave_beam_patterns[wave_beam_pattern_index % len(wave_beam_patterns)]
                    points = generate_wave_beam_points(
                        pygame.Vector2(player.center),
                        direction,
                        pattern,
                        wave_beam_length,
                        amplitude=50.0,
                        frequency=0.02,
                        time_offset=run_time
                    )
                    wave_beams.append({
                        "points": points,
                        "color": (50, 255, 50),
                        "width": wave_beam_width,
                        "damage": wave_beam_damage,
                        "timer": 0.2
                    })
                    wave_beam_time_since_shot = 0.0
                
                # Update laser beams
                for beam in laser_beams[:]:
                    beam["timer"] -= dt
                    if beam["timer"] <= 0:
                        laser_beams.remove(beam)
                    else:
                        # Check collision with enemies
                        for enemy in enemies[:]:
                            if line_rect_intersection(beam["start"], beam["end"], enemy["rect"]):
                                enemy["hp"] -= beam["damage"] * dt * 60  # Damage per frame
                                if enemy["hp"] <= 0:
                                    kill_enemy(enemy)
                
                # Update wave beams
                for beam in wave_beams[:]:
                    beam["timer"] -= dt
                    if beam["timer"] <= 0:
                        wave_beams.remove(beam)
                    else:
                        # Check collision with enemies
                        for enemy in enemies[:]:
                            hit_pos, dist = check_wave_beam_collision(beam["points"], enemy["rect"], wave_beam_width)
                            if hit_pos:
                                enemy["hp"] -= beam["damage"] * dt * 60
                                if enemy["hp"] <= 0:
                                    kill_enemy(enemy)
                
                # Enemy updates
                for enemy in enemies[:]:
                    if enemy.get("hp", 1) <= 0:
                        kill_enemy(enemy)
                        continue
                    
                    # Enemy AI: find target and move towards it
                    enemy_pos = pygame.Vector2(enemy["rect"].center)
                    target_info = find_nearest_threat(enemy_pos)
                    
                    if target_info:
                        target_pos, target_type = target_info
                        direction = vec_toward(enemy_pos.x, enemy_pos.y, target_pos.x, target_pos.y)
                        enemy_speed = enemy.get("speed", 80) * dt
                        
                        # Dodge bullets if in range
                        dodge_threats = find_threats_in_dodge_range(enemy_pos, 200.0)
                        if dodge_threats:
                            # Try to dodge by moving perpendicular
                            dodge_dir = pygame.Vector2(-direction.y, direction.x)  # Perpendicular
                            if random.random() < 0.5:
                                dodge_dir = -dodge_dir
                            direction = (direction + dodge_dir * 0.5).normalize()
                        
                        move_x = int(direction.x * enemy_speed)
                        move_y = int(direction.y * enemy_speed)
                        move_enemy_with_push(enemy["rect"], move_x, move_y, blocks)
                    
                    # Enemy shooting
                    enemy["shoot_cooldown"] = enemy.get("shoot_cooldown", 999.0) + dt
                    if enemy["shoot_cooldown"] >= enemy.get("shoot_cooldown_time", 1.0):
                        if target_info:
                            target_pos, target_type = target_info
                            if enemy.get("is_predictive", False):
                                spawn_enemy_projectile_predictive(enemy, direction)
                            else:
                                spawn_enemy_projectile(enemy)
                        enemy["shoot_cooldown"] = 0.0
                
                # Bullet/projectile updates
                for bullet in player_bullets[:]:
                    bullet["rect"].x += int(bullet["vel"].x * dt)
                    bullet["rect"].y += int(bullet["vel"].y * dt)
                    
                    # Remove if off screen
                    if rect_offscreen(bullet["rect"]):
                        player_bullets.remove(bullet)
                        continue
                    
                    # Check collision with enemies
                    for enemy in enemies[:]:
                        if bullet["rect"].colliderect(enemy["rect"]):
                            damage = bullet.get("damage", player_bullet_damage)
                            enemy["hp"] -= damage
                            
                            # Damage number
                            damage_numbers.append({
                                "x": enemy["rect"].centerx,
                                "y": enemy["rect"].y - 20,
                                "damage": int(damage),
                                "timer": 1.0,
                                "color": (255, 255, 100)
                            })
                            
                            if enemy["hp"] <= 0:
                                kill_enemy(enemy)
                            
                            # Remove bullet (unless it has penetration)
                            if bullet.get("penetration", 0) <= 0:
                                player_bullets.remove(bullet)
                                break
                            else:
                                bullet["penetration"] -= 1
                    
                    # Check collision with blocks
                    if not bullet.get("removed", False):
                        for block in destructible_blocks + moveable_destructible_blocks:
                            if block.get("is_destructible") and bullet["rect"].colliderect(block["rect"]):
                                block["hp"] -= bullet.get("damage", player_bullet_damage)
                                if block["hp"] <= 0:
                                    destructible_blocks.remove(block) if block in destructible_blocks else moveable_destructible_blocks.remove(block)
                                if not bullet.get("bouncing", False):
                                    player_bullets.remove(bullet)
                                    bullet["removed"] = True
                                    break
                                else:
                                    # Bounce bullet
                                    bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
                
                for proj in enemy_projectiles[:]:
                    proj["rect"].x += int(proj["vel"].x * dt)
                    proj["rect"].y += int(proj["vel"].y * dt)
                    
                    if rect_offscreen(proj["rect"]):
                        enemy_projectiles.remove(proj)
                        continue
                    
                    # Check collision with player
                    if proj["rect"].colliderect(player):
                        if not shield_active:
                            damage = proj.get("damage", 10)
                            player_hp -= damage
                            damage_taken += damage
                            if player_hp <= 0:
                                if lives > 0:
                                    lives -= 1
                                    reset_after_death()
                                else:
                                    state = STATE_GAME_OVER
                        enemy_projectiles.remove(proj)
                
                # Pickup collection
                for pickup in pickups[:]:
                    if player.colliderect(pickup["rect"]):
                        apply_pickup_effect(pickup["type"])
                        pickups.remove(pickup)
                
                # Health zone interaction
                if player.colliderect(moving_health_zone["rect"]):
                    if player_hp < player_max_hp:
                        player_hp = min(player_max_hp, player_hp + 50 * dt)  # Heal over time
                
                # Friendly AI updates
                for friendly in friendly_ai[:]:
                    if friendly.get("hp", 1) <= 0:
                        friendly_ai.remove(friendly)
                        continue
                    
                    target = find_nearest_enemy(pygame.Vector2(friendly["rect"].center))
                    if target:
                        direction = vec_toward(friendly["rect"].centerx, friendly["rect"].centery, target["rect"].centerx, target["rect"].centery)
                        friendly_speed = friendly.get("speed", 100) * dt
                        move_x = int(direction.x * friendly_speed)
                        move_y = int(direction.y * friendly_speed)
                        move_enemy_with_push(friendly["rect"], move_x, move_y, blocks)
                        
                        # Friendly shooting
                        friendly["shoot_cooldown"] = friendly.get("shoot_cooldown", 0.0) + dt
                        if friendly["shoot_cooldown"] >= friendly.get("shoot_cooldown_time", 0.5):
                            spawn_friendly_projectile(friendly, target)
                            friendly["shoot_cooldown"] = 0.0
                
                # Friendly projectile updates
                for proj in friendly_projectiles[:]:
                    proj["rect"].x += int(proj["vel"].x * dt)
                    proj["rect"].y += int(proj["vel"].y * dt)
                    
                    if rect_offscreen(proj["rect"]):
                        friendly_projectiles.remove(proj)
                        continue
                    
                    for enemy in enemies[:]:
                        if proj["rect"].colliderect(enemy["rect"]):
                            damage = proj.get("damage", 20)
                            enemy["hp"] -= damage
                            if enemy["hp"] <= 0:
                                kill_enemy(enemy)
                            friendly_projectiles.remove(proj)
                            break
                
                # Grenade explosion updates
                for explosion in grenade_explosions[:]:
                    explosion["timer"] -= dt
                    explosion["radius"] = int(explosion["max_radius"] * (1.0 - explosion["timer"] / 0.3))
                    
                    if explosion["timer"] <= 0:
                        grenade_explosions.remove(explosion)
                        continue
                    
                    # Damage enemies and blocks in radius
                    explosion_pos = pygame.Vector2(explosion["x"], explosion["y"])
                    for enemy in enemies[:]:
                        enemy_pos = pygame.Vector2(enemy["rect"].center)
                        dist = (enemy_pos - explosion_pos).length()
                        if dist <= explosion["radius"]:
                            enemy["hp"] -= explosion["damage"]
                            if enemy["hp"] <= 0:
                                kill_enemy(enemy)
                    
                    # Damage destructible blocks
                    for block in destructible_blocks[:] + moveable_destructible_blocks[:]:
                        if block.get("is_destructible"):
                            block_pos = pygame.Vector2(block["rect"].center)
                            dist = (block_pos - explosion_pos).length()
                            if dist <= explosion["radius"]:
                                block["hp"] -= explosion["damage"]
                                if block["hp"] <= 0:
                                    if block in destructible_blocks:
                                        destructible_blocks.remove(block)
                                    else:
                                        moveable_destructible_blocks.remove(block)
                
                # Missile updates
                for missile in missiles[:]:
                    if missile["target_enemy"] not in enemies:
                        # Target died, find new target
                        target_enemy = None
                        min_dist = float("inf")
                        for enemy in enemies:
                            dist = (pygame.Vector2(enemy["rect"].center) - pygame.Vector2(missile["rect"].center)).length_squared()
                            if dist < min_dist:
                                min_dist = dist
                                target_enemy = enemy
                        missile["target_enemy"] = target_enemy
                    
                    if missile["target_enemy"]:
                        # Seek target
                        target_pos = pygame.Vector2(missile["target_enemy"]["rect"].center)
                        missile_pos = pygame.Vector2(missile["rect"].center)
                        direction = (target_pos - missile_pos).normalize()
                        missile["vel"] = direction * missile["speed"]
                    
                    missile["rect"].x += int(missile["vel"].x * dt)
                    missile["rect"].y += int(missile["vel"].y * dt)
                    
                    if rect_offscreen(missile["rect"]):
                        missiles.remove(missile)
                        continue
                    
                    # Check collision with target
                    if missile["target_enemy"] and missile["rect"].colliderect(missile["target_enemy"]["rect"]):
                        # Explode
                        explosion_pos = pygame.Vector2(missile["rect"].center)
                        for enemy in enemies[:]:
                            enemy_pos = pygame.Vector2(enemy["rect"].center)
                            dist = (enemy_pos - explosion_pos).length()
                            if dist <= missile["explosion_radius"]:
                                enemy["hp"] -= missile["damage"]
                                if enemy["hp"] <= 0:
                                    kill_enemy(enemy)
                        missiles.remove(missile)
                
                # Wave management
                if wave_active and len(enemies) == 0:
                    time_to_next_wave += dt
                    if time_to_next_wave >= 3.0:  # 3 second delay between waves
                        wave_number += 1
                        wave_in_level += 1
                        if wave_in_level > 3:
                            wave_in_level = 1
                            current_level += 1
                            if current_level > max_level:
                                state = STATE_VICTORY
                                wave_active = False
                        if state != STATE_VICTORY:
                            start_wave(wave_number)
                            time_to_next_wave = 0.0
            
            # Rendering
            # Clear screen with background color based on level theme
            theme = level_themes.get(current_level, level_themes[1])
            screen.fill(theme["bg_color"])
            
            # Draw game elements based on state
            if state == STATE_MENU:
                # Menu rendering
                draw_centered_text("MOUSE AIM SHOOTER", HEIGHT // 4, use_big=True)
                
                y_offset = HEIGHT // 2
                if menu_section == 0:
                    # Difficulty selection
                    draw_centered_text("Select Difficulty:", y_offset - 60)
                    for i, diff in enumerate(difficulty_options):
                        color = (255, 255, 0) if i == difficulty_selected else (200, 200, 200)
                        draw_centered_text(f"{'->' if i == difficulty_selected else '  '} {diff}", y_offset + i * 40, color)
                    draw_centered_text("Use UP/DOWN to select, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 1:
                    # Aiming mode selection
                    draw_centered_text("Select Aiming Mode:", y_offset - 60)
                    modes = ["Mouse", "Arrow Keys"]
                    for i, mode in enumerate(modes):
                        color = (255, 255, 0) if i == aiming_mode_selected else (200, 200, 200)
                        draw_centered_text(f"{'->' if i == aiming_mode_selected else '  '} {mode}", y_offset + i * 40, color)
                    draw_centered_text("Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 1.5:
                    # Character profile yes/no
                    draw_centered_text("Use Character Profile?", y_offset - 60)
                    options = ["No", "Yes"]
                    for i, opt in enumerate(options):
                        color = (255, 255, 0) if i == use_character_profile_selected else (200, 200, 200)
                        draw_centered_text(f"{'->' if i == use_character_profile_selected else '  '} {opt}", y_offset + i * 40, color)
                    draw_centered_text("Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 2:
                    # Character profile selection
                    draw_centered_text("Character Profile:", y_offset - 60)
                    for i, profile in enumerate(character_profile_options):
                        color = (255, 255, 0) if i == character_profile_selected else (200, 200, 200)
                        draw_centered_text(f"{'->' if i == character_profile_selected else '  '} {profile}", y_offset + i * 40, color)
                    draw_centered_text("Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 3:
                    # HUD options
                    draw_centered_text("HUD Options:", y_offset - 60)
                    options = ["Show Metrics", "Hide Metrics"]
                    for i, opt in enumerate(options):
                        color = (255, 255, 0) if i == ui_show_metrics_selected else (200, 200, 200)
                        draw_centered_text(f"{'->' if i == ui_show_metrics_selected else '  '} {opt}", y_offset + i * 40, color)
                    draw_centered_text("Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 4:
                    # Beam/weapon selection (if testing mode)
                    if testing_mode:
                        draw_centered_text("Select Weapon:", y_offset - 60)
                        for i, weapon in enumerate(weapon_selection_options):
                            color = (255, 255, 0) if i == beam_selection_selected else (200, 200, 200)
                            draw_centered_text(f"{'->' if i == beam_selection_selected else '  '} {weapon}", y_offset + i * 30, color)
                        draw_centered_text("Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to start", HEIGHT - 100, (150, 150, 150))
                    else:
                        menu_section = 5  # Skip to start
                
                elif menu_section == 5:
                    # Start game
                    draw_centered_text("Ready to Start!", y_offset)
                    draw_centered_text("Press ENTER or SPACE to begin", y_offset + 60, (150, 150, 150))
                    draw_centered_text("Press LEFT to go back", y_offset + 100, (150, 150, 150))
                
                elif menu_section == 6:
                    # Custom profile creator
                    draw_centered_text("Custom Profile Creator:", y_offset - 100)
                    for i, stat_name in enumerate(custom_profile_stats_list):
                        stat_key = custom_profile_stats_keys[i]
                        stat_value = custom_profile_stats[stat_key]
                        color = (255, 255, 0) if i == custom_profile_stat_selected else (200, 200, 200)
                        draw_centered_text(f"{'->' if i == custom_profile_stat_selected else '  '} {stat_name}: {stat_value:.1f}x", y_offset + i * 35, color)
                    draw_centered_text("Use UP/DOWN to select stat, LEFT/RIGHT to adjust, ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 7:
                    # Class selection
                    draw_centered_text("Select Class:", y_offset - 60)
                    for i, cls in enumerate(player_class_options):
                        color = (255, 255, 0) if i == player_class_selected else (200, 200, 200)
                        draw_centered_text(f"{'->' if i == player_class_selected else '  '} {cls}", y_offset + i * 40, color)
                    draw_centered_text("Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
            elif state == STATE_PLAYING or state == STATE_ENDURANCE:
                # Draw all game elements
                
                # Draw trapezoid blocks (cached surfaces)
                for tr in trapezoid_blocks:
                    block_id = f"trap_{id(tr)}"
                    if block_id not in _cached_trapezoid_surfaces:
                        # Create cached surface for this trapezoid
                        points = tr.get("points", [])
                        if points:
                            min_x = min(p[0] for p in points)
                            max_x = max(p[0] for p in points)
                            min_y = min(p[1] for p in points)
                            max_y = max(p[1] for p in points)
                            cached_surf = pygame.Surface((max_x - min_x + 10, max_y - min_y + 10), pygame.SRCALPHA)
                            offset_points = [(p[0] - min_x + 5, p[1] - min_y + 5) for p in points]
                            pygame.draw.polygon(cached_surf, tr["color"], offset_points)
                            pygame.draw.polygon(cached_surf, (255, 255, 255), offset_points, 2)
                            _cached_trapezoid_surfaces[block_id] = (cached_surf, (min_x - 5, min_y - 5))
                    
                    if block_id in _cached_trapezoid_surfaces:
                        cached_surf, offset = _cached_trapezoid_surfaces[block_id]
                        screen.blit(cached_surf, offset)
                
                # Draw triangle blocks (cached surfaces)
                for tr in triangle_blocks:
                    block_id = f"tri_{id(tr)}"
                    if block_id not in _cached_triangle_surfaces:
                        points = tr.get("points", [])
                        if points:
                            min_x = min(p[0] for p in points)
                            max_x = max(p[0] for p in points)
                            min_y = min(p[1] for p in points)
                            max_y = max(p[1] for p in points)
                            cached_surf = pygame.Surface((max_x - min_x + 10, max_y - min_y + 10), pygame.SRCALPHA)
                            offset_points = [(p[0] - min_x + 5, p[1] - min_y + 5) for p in points]
                            pygame.draw.polygon(cached_surf, tr["color"], offset_points)
                            pygame.draw.polygon(cached_surf, (255, 255, 255), offset_points, 2)
                            _cached_triangle_surfaces[block_id] = (cached_surf, (min_x - 5, min_y - 5))
                    
                    if block_id in _cached_triangle_surfaces:
                        cached_surf, offset = _cached_triangle_surfaces[block_id]
                        screen.blit(cached_surf, offset)
                
                # Draw destructible blocks
                for block in destructible_blocks:
                    if block.get("is_destructible") and block.get("hp", 0) > 0:
                        draw_cracked_brick_wall_texture(screen, block["rect"], block.get("crack_level", 0))
                    else:
                        draw_silver_wall_texture(screen, block["rect"])
                
                # Draw moveable destructible blocks
                for block in moveable_destructible_blocks:
                    if block.get("is_destructible") and block.get("hp", 0) > 0:
                        draw_cracked_brick_wall_texture(screen, block["rect"], block.get("crack_level", 0))
                    else:
                        draw_silver_wall_texture(screen, block["rect"])
                
                # Draw giant blocks
                for block in giant_blocks:
                    draw_silver_wall_texture(screen, block["rect"])
                
                # Draw super giant blocks
                for block in super_giant_blocks:
                    draw_silver_wall_texture(screen, block["rect"])
                
                # Draw hazard obstacles (paraboloids/trapezoids)
                for hazard in hazard_obstacles:
                    points = hazard.get("points", [])
                    if len(points) >= 3:
                        pygame.draw.polygon(screen, hazard["color"], points)
                        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
                
                # Draw moving health recovery zone
                zone = moving_health_zone
                zone_center = (zone["rect"].centerx, zone["rect"].centery)
                zone_width = zone["rect"].w
                zone_height = zone["rect"].h
                use_triangle = (wave_in_level % 2 == 0)
                
                zone_surf = pygame.Surface((zone["rect"].w + 20, zone["rect"].h + 20), pygame.SRCALPHA)
                
                if use_triangle:
                    triangle_points = [
                        (zone_width // 2, 10),
                        (10, zone_height + 10),
                        (zone_width + 10, zone_height + 10)
                    ]
                    pygame.draw.polygon(zone_surf, zone["color"], triangle_points)
                    screen.blit(zone_surf, (zone["rect"].x - 10, zone["rect"].y - 10))
                    pulse = 0.5 + 0.5 * math.sin(run_time * 3.0)
                    border_alpha = int(150 + 100 * pulse)
                    border_color = (50, 255, 50)
                    pygame.draw.polygon(screen, border_color, [
                        (zone_center[0], zone["rect"].y),
                        (zone["rect"].x, zone["rect"].bottom),
                        (zone["rect"].right, zone["rect"].bottom)
                    ], 3)
                else:
                    pygame.draw.rect(zone_surf, zone["color"], (10, 10, zone["rect"].w, zone["rect"].h))
                    screen.blit(zone_surf, (zone["rect"].x - 10, zone["rect"].y - 10))
                    pulse = 0.5 + 0.5 * math.sin(run_time * 3.0)
                    border_alpha = int(150 + 100 * pulse)
                    border_color = (50, 255, 50)
                    pygame.draw.rect(screen, border_color, zone["rect"], 3)
                
                # Draw pickups
                for pickup in pickups:
                    pygame.draw.circle(screen, pickup["color"], pickup["rect"].center, pickup["rect"].w // 2)
                    pygame.draw.circle(screen, (255, 255, 255), pickup["rect"].center, pickup["rect"].w // 2, 2)
                
                # Draw enemy projectiles
                for proj in enemy_projectiles:
                    draw_projectile(proj["rect"], proj["color"], proj.get("shape", "circle"))
                
                # Draw player bullets
                for bullet in player_bullets:
                    draw_projectile(bullet["rect"], bullet["color"], bullet.get("shape", "circle"))
                
                # Draw friendly projectiles
                for proj in friendly_projectiles:
                    draw_projectile(proj["rect"], proj["color"], proj.get("shape", "circle"))
                
                # Draw friendly AI
                for friendly in friendly_ai:
                    pygame.draw.rect(screen, friendly.get("color", (100, 200, 100)), friendly["rect"])
                    if friendly.get("hp", 0) > 0 and ui_show_health_bars:
                        draw_health_bar(friendly["rect"].x, friendly["rect"].y - 10, friendly["rect"].w, 5, friendly["hp"], friendly.get("max_hp", friendly["hp"]))
                
                # Draw enemies
                for enemy in enemies:
                    enemy_color = enemy.get("color", (200, 50, 50))
                    pygame.draw.rect(screen, enemy_color, enemy["rect"])
                    if enemy.get("hp", 0) > 0 and ui_show_health_bars:
                        draw_health_bar(enemy["rect"].x, enemy["rect"].y - 10, enemy["rect"].w, 5, enemy["hp"], enemy.get("max_hp", enemy["hp"]))
                
                # Draw grenade explosions
                for explosion in grenade_explosions:
                    alpha = int(255 * (explosion["timer"] / 0.3))
                    color = (255, 100, 0, alpha)
                    pygame.draw.circle(screen, (255, 100, 0), (explosion["x"], explosion["y"]), explosion["radius"], 3)
                    pygame.draw.circle(screen, (255, 200, 0), (explosion["x"], explosion["y"]), explosion["radius"] // 2)
                
                # Draw missiles
                for missile in missiles:
                    pygame.draw.rect(screen, (255, 200, 0), missile["rect"])
                    pygame.draw.rect(screen, (255, 100, 0), missile["rect"], 2)
                
                # Draw player
                player_color = (255, 255, 255)
                if shield_active:
                    player_color = (255, 100, 100)  # Red when shield is active
                pygame.draw.rect(screen, player_color, player)
                if ui_show_player_health_bar:
                    draw_health_bar(player.x, player.y - 15, player.w, 6, player_hp, player_max_hp)
                    # Draw overshield bar above health bar
                    if overshield > 0:
                        overshield_bar_height = 4
                        overshield_bar_width = player.w
                        overshield_fill = int((overshield / overshield_max) * overshield_bar_width)
                        pygame.draw.rect(screen, (60, 60, 60), (player.x, player.y - 20, overshield_bar_width, overshield_bar_height))
                        pygame.draw.rect(screen, (255, 150, 0), (player.x, player.y - 20, overshield_fill, overshield_bar_height))
                        pygame.draw.rect(screen, (20, 20, 20), (player.x, player.y - 20, overshield_bar_width, overshield_bar_height), 1)
                
                # Draw laser beams
                for beam in laser_beams:
                    if "start" in beam and "end" in beam:
                        pygame.draw.line(screen, beam.get("color", (255, 50, 50)), beam["start"], beam["end"], beam.get("width", 5))
                
                # Draw wave beams
                for beam in wave_beams:
                    points = beam.get("points", [])
                    if len(points) >= 2:
                        pygame.draw.lines(screen, beam.get("color", (50, 255, 50)), False, points, beam.get("width", 10))
                
                # Draw HUD
                if ui_show_hud:
                    y_pos = 10
                    if ui_show_metrics:
                        y_pos = render_hud_text(f"HP: {player_hp}/{player_max_hp}", y_pos)
                        if overshield > 0:
                            y_pos = render_hud_text(f"Overshield: {overshield}/{overshield_max}", y_pos)
                        y_pos = render_hud_text(f"Wave: {wave_number} | Level: {current_level}", y_pos)
                        y_pos = render_hud_text(f"Score: {score}", y_pos)
                        if state == STATE_PLAYING:
                            y_pos = render_hud_text(f"Lives: {lives}", y_pos)
                        y_pos = render_hud_text(f"Enemies: {len(enemies)}", y_pos)
                        y_pos = render_hud_text(f"Weapon: {current_weapon_mode.upper()}", y_pos)
                        if shield_active:
                            y_pos = render_hud_text("SHIELD ACTIVU", y_pos, (255, 100, 100))
                        
                        # Draw cooldown bars at bottom
                        bar_y = HEIGHT - 30
                        bar_height = 20
                        bar_width = 200
                        
                        # Grenade cooldown
                        grenade_progress = min(1.0, grenade_time_since_used / grenade_cooldown)
                        grenade_x = 10
                        pygame.draw.rect(screen, (60, 60, 60), (grenade_x, bar_y, bar_width, bar_height))
                        pygame.draw.rect(screen, (100, 255, 100) if grenade_progress >= 1.0 else (100, 100, 100), 
                                        (grenade_x, bar_y, int(bar_width * grenade_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (grenade_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("GRENADE (E)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (grenade_x + 5, bar_y + 2))
                        
                        # Missile cooldown
                        missile_progress = min(1.0, missile_time_since_used / missile_cooldown)
                        missile_x = grenade_x + bar_width + 10
                        pygame.draw.rect(screen, (60, 60, 60), (missile_x, bar_y, bar_width, bar_height))
                        pygame.draw.rect(screen, (255, 200, 0) if missile_progress >= 1.0 else (100, 100, 100), 
                                        (missile_x, bar_y, int(bar_width * missile_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (missile_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("MISSILE (R)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (missile_x + 5, bar_y + 2))
                        
                        # Ally drop cooldown
                        ally_progress = min(1.0, ally_drop_timer / ally_drop_cooldown)
                        ally_x = missile_x + bar_width + 10
                        pygame.draw.rect(screen, (60, 60, 60), (ally_x, bar_y, bar_width, bar_height))
                        pygame.draw.rect(screen, (200, 100, 255) if ally_progress >= 1.0 else (100, 100, 100), 
                                        (ally_x, bar_y, int(bar_width * ally_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (ally_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("ALLY DROP (Q)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (ally_x + 5, bar_y + 2))
                        
                        # Overshield cooldown
                        overshield_progress = min(1.0, overshield_recharge_timer / overshield_recharge_cooldown)
                        overshield_x = ally_x + bar_width + 10
                        pygame.draw.rect(screen, (60, 60, 60), (overshield_x, bar_y, bar_width, bar_height))
                        pygame.draw.rect(screen, (255, 150, 0) if overshield_progress >= 1.0 else (100, 100, 100), 
                                        (overshield_x, bar_y, int(bar_width * overshield_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (overshield_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("OVERSHIELD (TAB)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (overshield_x + 5, bar_y + 2))
                
                # Draw damage numbers
                for dmg_num in damage_numbers[:]:
                    if dmg_num["timer"] > 0:
                        alpha = int(255 * (dmg_num["timer"] / 1.0))
                        color = (*dmg_num["color"][:3], alpha) if len(dmg_num["color"]) > 3 else dmg_num["color"]
                        text_surf = small_font.render(str(dmg_num["damage"]), True, color[:3])
                        screen.blit(text_surf, (dmg_num["x"], dmg_num["y"]))
                    else:
                        damage_numbers.remove(dmg_num)
                
                # Draw weapon pickup messages
                for msg in weapon_pickup_messages[:]:
                    if msg["timer"] > 0:
                        alpha = int(255 * (msg["timer"] / 3.0))
                        color = (*msg["color"][:3], alpha) if len(msg["color"]) > 3 else msg["color"]
                        text_surf = font.render(f"PICKED UP: {msg['weapon_name']}", True, color[:3])
                        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(text_surf, text_rect)
                    else:
                        weapon_pickup_messages.remove(msg)
            elif state == STATE_PAUSED:
                # Draw paused game with overlay
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                
                draw_centered_text("PAUSED", HEIGHT // 2 - 100, use_big=True)
                
                y_offset = HEIGHT // 2
                for i, option in enumerate(pause_options):
                    color = (255, 255, 0) if i == pause_selected else (200, 200, 200)
                    draw_centered_text(f"{'->' if i == pause_selected else '  '} {option}", y_offset + i * 50, color)
                
                draw_centered_text("Press ENTER to select, ESC to unpause", HEIGHT - 100, (150, 150, 150))
            elif state == STATE_GAME_OVER:
                # Game over screen
                # (Game over rendering would go here)
                pass
            elif state == STATE_VICTORY:
                # Victory screen
                # (Victory rendering would go here)
                pass
            elif state == STATE_HIGH_SCORES:
                # High scores screen
                # (High scores rendering would go here)
                pass
            elif state == STATE_NAME_INPUT:
                # Name input screen
                # (Name input rendering would go here)
                pass
            elif state == STATE_CONTROLS:
                # Controls menu
                # (Controls menu rendering would go here)
                pass
            
            pygame.display.flip()
    
    except KeyboardInterrupt:
        print("Interrupted by user (Ctrl+C). Saving run...")
    
    except Exception as e:
        print("Unhandled exception:", repr(e))
        raise
    
    finally:
        run_ended_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if telemetry_enabled and telemetry:
            telemetry.end_run(
                ended_at_iso=run_ended_at,
                seconds_survived=run_time,
                player_hp_end=player_hp,
                shots_fired=shots_fired,
                hits=hits,
                damage_taken=damage_taken,
                damage_dealt=damage_dealt,
                enemies_spawned=enemies_spawned,
                enemies_killed=enemies_killed,
                deaths=deaths,
                max_wave=wave_number,
            )
            telemetry.close()
            print(f"Saved run_id={run_id} to game_telemetry.db")
        pygame.quit()


def _key_name_to_code(name: str) -> int:
    name = (name or "").lower().strip()
    try:
        return pygame.key.key_code(name)
    except Exception:
        return pygame.K_UNKNOWN


def load_controls() -> dict[str, int]:
    data = {}
    if os.path.exists(CONTROLS_PATH):
        try:
            with open(CONTROLS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
        except Exception:
            data = {}

    merged = {**DEFAULT_CONTROLS, **{k: v for k, v in data.items() if isinstance(v, str)}}
    return {action: _key_name_to_code(key_name) for action, key_name in merged.items()}


def save_controls(controls: dict[str, int]) -> None:
    # Persist as human-readable key names so players can edit the file too
    out: dict[str, str] = {}
    for action, key_code in controls.items():
        try:
            out[action] = pygame.key.name(key_code)
        except Exception:
            out[action] = "unknown"
    with open(CONTROLS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)


# Controls will be initialized in main() after pygame.init()
# Using a placeholder dict to avoid calling pygame.key.key_code() before pygame.init()
controls = {}

# ----------------------------
# Telemetry
# ----------------------------
# Telemetry can be disabled to improve performance
telemetry_enabled = False  # Default: Disabled (will be set by user in menu)
telemetry = None  # Will be initialized if enabled
run_started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

# ----------------------------
# Game state
# ----------------------------
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_CONTINUE = "CONTINUE"
STATE_ENDURANCE = "ENDURANCE"
STATE_GAME_OVER = "GAME_OVER"
STATE_NAME_INPUT = "NAME_INPUT"  # High score name input screen
STATE_HIGH_SCORES = "HIGH_SCORES"  # High score board display
STATE_VICTORY = "VICTORY"  # Game completed - all levels cleared
STATE_MODS = "MODS"  # Mod settings menu
STATE_WAVE_BUILDER = "WAVE_BUILDER"  # Custom wave builder

state = STATE_MENU
previous_game_state = None  # Track previous game state for pause/unpause (STATE_PLAYING or STATE_ENDURANCE)
menu_section = 0  # 0 = difficulty, 1 = aiming, 1.5 = character profile yes/no, 2 = class, 3 = HUD options, 3.5 = Telemetry options, 4 = beam_selection, 5 = start
ui_show_metrics_selected = 0  # 0 = Show, 1 = Hide - Default: Show (enabled)
ui_show_hud = True  # HUD visibility (follows metrics setting)
ui_options_selected = 0  # 0 = Metrics, 1 = Telemetry (which option is currently focused)
endurance_mode_selected = 0  # 0 = Normal, 1 = Endurance Mode

# Character profile system
use_character_profile = False  # Whether to use character profiles
use_character_profile_selected = 0  # 0 = No, 1 = Yes
character_profile_selected = 0  # 0 = Premade, 1 = Custom
character_profile_options = ["Premade Profiles", "Create Custom Profile"]
custom_profile_stat_selected = 0  # Which stat is being edited
custom_profile_stats = {
    "hp_mult": 1.0,
    "speed_mult": 1.0,
    "damage_mult": 1.0,
    "firerate_mult": 1.0,
}
custom_profile_stats_list = ["HP Multiplier", "Speed Multiplier", "Damage Multiplier", "Fire Rate Multiplier"]
custom_profile_stats_keys = ["hp_mult", "speed_mult", "damage_mult", "firerate_mult"]

# Side quests and goal tracking
side_quests = {
    "no_hit_wave": {
        "name": "Perfect Wave",
        "description": "Complete wave without getting hit",
        "bonus_points": 10000,
        "active": False,
        "completed": False,
    }
}
wave_damage_taken = 0  # Track damage taken in current wave
# Beam selection for testing (harder to access - requires testing mode)
testing_mode = False  # Set to True to enable weapon selection menu
beam_selection_selected = 6  # 0 = wave_beam, 1 = rocket, etc., 6 = basic (default)
beam_selection_pattern = "basic"  # Default weapon pattern

# Level system - 3 levels, each with 3 waves (boss on wave 3)
current_level = 1
max_level = 3
wave_in_level = 1  # Track which wave within current level (1, 2, or 3)
level_themes = {
    1: {"name": "Forest", "bg_color": (20, 60, 20), "block_color_shift": (0, 0, 0)},
    2: {"name": "Desert", "bg_color": (60, 50, 20), "block_color_shift": (20, 10, -10)},
    3: {"name": "Ice", "bg_color": (20, 40, 60), "block_color_shift": (-20, -10, 20)},
    4: {"name": "Volcano", "bg_color": (60, 20, 20), "block_color_shift": (30, -10, -20)},
    5: {"name": "Void", "bg_color": (10, 10, 20), "block_color_shift": (-30, -30, 10)},
}

# Difficulty settings
DIFFICULTY_EASY = "EASY"
DIFFICULTY_NORMAL = "NORMAL"
DIFFICULTY_HARD = "HARD"
difficulty = DIFFICULTY_NORMAL
difficulty_selected = 1  # 0 = Easy, 1 = Normal, 2 = Hard
difficulty_options = [DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD]

# Aiming mode selection
AIM_MOUSE = "MOUSE"
AIM_ARROWS = "ARROWS"
aiming_mode = AIM_MOUSE
aiming_mode_selected = 0  # 0 = Mouse, 1 = Arrows

# Player classes
PLAYER_CLASS_TANK = "TANK"
PLAYER_CLASS_SPEEDSTER = "SPEEDSTER"
PLAYER_CLASS_SNIPER = "SNIPER"
PLAYER_CLASS_BALANCED = "BALANCED"
player_class = PLAYER_CLASS_BALANCED
player_class_selected = 0  # 0 = Balanced, 1 = Tank, 2 = Speedster, 3 = Sniper
player_class_options = [PLAYER_CLASS_BALANCED, PLAYER_CLASS_TANK, PLAYER_CLASS_SPEEDSTER, PLAYER_CLASS_SNIPER]

# Mod settings
mod_enemy_spawn_multiplier = 1.0  # Custom enemy spawn multiplier
mod_custom_waves_enabled = False
custom_waves: list[dict] = []  # Custom wave definitions

# UI customization settings
ui_show_health_bars = True
ui_show_stats = True
ui_show_all_ui = True
ui_show_block_health_bars = False  # Health bars for destructible blocks
ui_show_player_health_bar = True  # Health bar above player character
ui_show_metrics = True  # Show metrics/stats in HUD - Default: Enabled
ui_telemetry_enabled_selected = 1  # 0 = Enabled, 1 = Disabled (for menu) - Default: Disabled

# Alternative aiming mechanics
aiming_mechanic = "mouse"  # "mouse", "lockon", "predictive", "directional", "hybrid"

# Difficulty multipliers
difficulty_multipliers = {
    DIFFICULTY_EASY: {"enemy_hp": 0.7, "enemy_speed": 0.8, "enemy_spawn": 0.8, "pickup_spawn": 1.3},
    DIFFICULTY_NORMAL: {"enemy_hp": 1.0, "enemy_speed": 1.0, "enemy_spawn": 1.0, "pickup_spawn": 1.0},
    DIFFICULTY_HARD: {"enemy_hp": 1.5, "enemy_speed": 1.3, "enemy_spawn": 1.5, "pickup_spawn": 0.7},
}

pause_options = ["Continue", "Quit"]
pause_selected = 0
continue_blink_t = 0.0

# Controls menu state
STATE_CONTROLS = "CONTROLS"
controls_actions = ["move_left", "move_right", "move_up", "move_down", "boost", "slow", "dash", "ally_drop"]
controls_selected = 0
controls_rebinding = False

# ----------------------------
# Player (initialized in main() after WIDTH/HEIGHT are set)
# ----------------------------
player = None  # Will be initialized in main() after WIDTH/HEIGHT are set
player_speed = 450  # px/s (base speed, modified by class) - 1.5x (300 * 1.5)
player_max_hp = 7500  # base HP (modified by class) - 10x (750 * 10)
player_hp = player_max_hp

# Player class stat modifiers
player_class_stats = {
    PLAYER_CLASS_BALANCED: {"hp_mult": 1.0, "speed_mult": 1.0, "damage_mult": 1.0, "firerate_mult": 1.0},
    PLAYER_CLASS_TANK: {"hp_mult": 2.0, "speed_mult": 0.7, "damage_mult": 1.2, "firerate_mult": 0.8},
    PLAYER_CLASS_SPEEDSTER: {"hp_mult": 0.7, "speed_mult": 1.5, "damage_mult": 0.9, "firerate_mult": 1.3},
    PLAYER_CLASS_SNIPER: {"hp_mult": 0.8, "speed_mult": 0.9, "damage_mult": 1.5, "firerate_mult": 0.7},
}
overshield_max = 50  # Maximum overshield capacity (base, can be increased by tab key)
overshield = 0  # Current overshield amount
overshield_recharge_cooldown = 45.0  # Cooldown for tab key overshield (seconds)
overshield_recharge_timer = 0.0  # Time since last overshield activation
shield_recharge_cooldown = 10.0  # Shield cooldown (for progress bar display)
shield_recharge_timer = 0.0  # Time since shield was used
# pygame.mouse.set_visible(True)  # Moved to main() after pygame.init()

LIVES_START = 10
lives = LIVES_START

# Track most recent movement keys so latest press wins on conflicts
last_horizontal_key = None  # keycode of current "latest" horizontal key
last_vertical_key = None  # keycode of current "latest" vertical key
last_move_velocity = pygame.Vector2(0, 0)

# Dash mechanic (space bar)
jump_cooldown = 0.5  # seconds between dashes
jump_cooldown_timer = 0.0
jump_velocity = pygame.Vector2(0, 0)  # Current jump velocity
jump_speed = 600  # pixels per second
jump_duration = 0.15  # seconds
jump_timer = 0.0
is_jumping = False

# Boost / slow
previous_boost_state = False  # Track for telemetry
previous_slow_state = False  # Track for telemetry

boost_meter_max = 100.0
boost_meter = boost_meter_max
boost_drain_per_s = 45.0
boost_regen_per_s = 25.0
boost_speed_mult = 1.7
slow_speed_mult = 0.45

# Fire-rate pickup buff
fire_rate_buff_t = 0.0
fire_rate_buff_duration = 10.0
fire_rate_mult = 0.55  # reduces cooldown while active

# Shield system (Left Alt key)
shield_active = False
shield_duration = 2.0  # Shield lasts 2 seconds
shield_duration_remaining = 0.0
shield_cooldown = random.uniform(10.0, 15.0)  # 10-15 seconds cooldown
shield_cooldown_remaining = 0.0

# Permanent player stat multipliers (from pickups)
player_stat_multipliers = {
    "speed": 1.0,
    "firerate": 1.0,  # permanent firerate boost (stacks with temporary buff)
    "bullet_size": 1.0,
    "bullet_speed": 1.0,
    "bullet_damage": 1.0,
    "bullet_knockback": 1.0,
    "bullet_penetration": 0,  # number of enemies bullet can pierce through
    "bullet_explosion_radius": 0.0,  # explosion radius in pixels (0 = no explosion)
}

# Random damage multiplier (from "random_damage" pickup)
# This multiplies the base damage, and changes randomly when pickup is collected
random_damage_multiplier = 1.0  # Starts at 1.0x

# Damage number display system (floating damage numbers over enemies)
damage_numbers: list[dict] = []  # List of {x, y, damage, timer, color}
weapon_pickup_messages: list[dict] = []  # List of {weapon_name, timer, color} for displaying weapon pickup notifications

# Weapon mode system (keys 1-6 to switch)
# "basic" = normal bullets, "rocket" = rocket launcher, "triple" = triple shot,
# "bouncing" = bouncing bullets, "giant" = giant bullets, "laser" = laser beam
current_weapon_mode = "basic"
previous_weapon_mode = "basic"  # Track for telemetry
unlocked_weapons: set[str] = {"basic"}  # Weapons player has unlocked (starts with basic only)

# Laser beam system
laser_beams: list[dict] = []  # List of active laser beams
laser_length = 800  # Maximum laser length in pixels
laser_damage = 50  # Damage per frame while on target
laser_cooldown = 0.3  # Cooldown between laser shots
laser_time_since_shot = 999.0

# Wave beam system (trigonometric wave patterns)
wave_beams: list[dict] = []  # List of active wave beams
wave_beam_length = 1000  # Beam length in pixels
wave_beam_width = 10  # Beam width in pixels
wave_beam_damage = 30  # Damage per frame while on target
wave_beam_cooldown = 0.5  # Cooldown between wave beam shots
wave_beam_time_since_shot = 999.0
wave_beam_pattern_index = 0  # Current wave pattern (cycles through patterns)
wave_beam_patterns = ["sine"]  # Only wave beam pattern for testing
# Weapon selection for testing (replaces beam selection)
weapon_selection_options = ["wave_beam", "rocket", "bouncing", "laser", "triple", "giant", "basic"]

# Rotating paraboloid/trapezoid hazard system
# On level 1: paraboloids, on level 2+: trapezoids
hazard_obstacles = [
    {
        "center": pygame.Vector2(250, 250),  # Top-left corner area
        "width": 250,  # Half size (250x250)
        "height": 250,
        "rotation_angle": 0.0,
        "rotation_speed": 0.9,  # 3x faster (0.3 * 3)
        "orbit_center": pygame.Vector2(250, 250),
        "orbit_radius": 100,
        "orbit_angle": 0.0,
        "orbit_speed": 0.6,  # 3x faster (0.2 * 3)
        "velocity": pygame.Vector2(150, 90),  # 3x faster (50*3, 30*3)
        "damage": 20,
        "color": (255, 100, 100),
        "points": [],
        "bounding_rect": pygame.Rect(0, 0, 250, 250),
        "shape": "paraboloid",  # Shape type
    },
    {
        "center": pygame.Vector2(WIDTH - 250, 250),  # Top-right corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 1.0,
        "rotation_speed": 0.75,  # 3x faster (0.25 * 3)
        "orbit_center": pygame.Vector2(WIDTH - 250, 250),
        "orbit_radius": 100,
        "orbit_angle": 1.5,
        "orbit_speed": 0.45,  # 3x faster (0.15 * 3)
        "velocity": pygame.Vector2(-120, 150),  # 3x faster (-40*3, 50*3)
        "damage": 10,
        "color": (255, 150, 100),
        "points": [],
        "bounding_rect": pygame.Rect(0, 0, 250, 250),
        "shape": "paraboloid",
    },
    {
        "center": pygame.Vector2(250, HEIGHT - 250),  # Bottom-left corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 2.0,
        "rotation_speed": 1.05,  # 3x faster (0.35 * 3)
        "orbit_center": pygame.Vector2(250, HEIGHT - 250),
        "orbit_radius": 100,
        "orbit_angle": 3.0,
        "orbit_speed": 0.54,  # 3x faster (0.18 * 3)
        "velocity": pygame.Vector2(90, -135),  # 3x faster (30*3, -45*3)
        "damage": 10,
        "color": (255, 120, 120),
        "points": [],
        "bounding_rect": pygame.Rect(0, 0, 250, 250),
        "shape": "paraboloid",
    },
    {
        "center": pygame.Vector2(WIDTH - 250, HEIGHT - 250),  # Bottom-right corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 1.5,
        "rotation_speed": 0.84,  # 3x faster (0.28 * 3)
        "orbit_center": pygame.Vector2(WIDTH - 250, HEIGHT - 250),
        "orbit_radius": 100,
        "orbit_angle": 2.5,
        "orbit_speed": 0.66,  # 3x faster (0.22 * 3)
        "velocity": pygame.Vector2(-105, -120),  # 3x faster (-35*3, -40*3)
        "damage": 10,
        "color": (255, 130, 110),
        "points": [],
        "bounding_rect": pygame.Rect(0, 0, 250, 250),
        "shape": "paraboloid",
    },
]

# ----------------------------
# World blocks
# ----------------------------
# Removed all moveable indestructible blocks - keeping only:
# - moveable_destructible_blocks (destructible, movable)
# - destructible_blocks (unmovable, destructible)
# - trapezoid_blocks (unmovable, indestructible) - new border layout
# - triangle_blocks (unmovable, indestructible) - decorative border elements

blocks = []  # Empty - no moveable indestructible blocks

# Destructible blocks: 50% destructible (with HP), 50% indestructible (no HP), all moveable
destructible_blocks = [
    # First 6 blocks: Destructible (with HP)
    {"rect": pygame.Rect(300, 200, 80, 80), "color": (150, 100, 200), "hp": 500, "max_hp": 500, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(450, 300, 60, 60), "color": (100, 200, 150), "hp": 400, "max_hp": 400, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(200, 500, 90, 50), "color": (200, 150, 100), "hp": 600, "max_hp": 600, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(750, 600, 70, 70), "color": (150, 150, 200), "hp": 450, "max_hp": 450, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(150, 700, 100, 40), "color": (200, 200, 100), "hp": 550, "max_hp": 550, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1100, 300, 90, 90), "color": (180, 120, 180), "hp": 550, "max_hp": 550, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    # Last 6 blocks: Indestructible (no HP)
    {"rect": pygame.Rect(1300, 500, 70, 70), "color": (120, 180, 120), "is_moveable": True},
    {"rect": pygame.Rect(1000, 800, 80, 60), "color": (200, 120, 100), "is_moveable": True},
    {"rect": pygame.Rect(400, 1000, 100, 50), "color": (150, 150, 220), "is_moveable": True},
    {"rect": pygame.Rect(800, 1200, 70, 70), "color": (220, 200, 120), "is_moveable": True},
    {"rect": pygame.Rect(1200, 1000, 90, 40), "color": (200, 150, 200), "is_moveable": True},
    {"rect": pygame.Rect(1400, 700, 60, 60), "color": (100, 200, 200), "is_moveable": True},
]

# Moveable destructible blocks: Reduced amount, bigger size
moveable_destructible_blocks = [
    # First 3 blocks: Destructible (with HP) - bigger and fewer
    {"rect": pygame.Rect(350, 400, 120, 120), "color": (200, 100, 100), "hp": 400, "max_hp": 400, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(850, 500, 120, 120), "color": (100, 200, 100), "hp": 350, "max_hp": 350, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(650, 700, 120, 120), "color": (200, 150, 100), "hp": 450, "max_hp": 450, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    # Last 3 blocks: Indestructible (no HP) - bigger and fewer
    {"rect": pygame.Rect(1050, 300, 120, 120), "color": (200, 120, 150), "is_moveable": True},
    {"rect": pygame.Rect(200, 600, 120, 120), "color": (150, 150, 200), "is_moveable": True},
    {"rect": pygame.Rect(500, 900, 120, 120), "color": (200, 100, 150), "is_moveable": True},
]

# Giant and super giant blocks (unmovable, indestructible)
giant_blocks: list[dict] = [
    # Giant blocks (200x200)
    {"rect": pygame.Rect(200, 200, 200, 200), "color": (80, 80, 120), "is_moveable": False, "size": "giant"},
    {"rect": pygame.Rect(1000, 400, 200, 200), "color": (80, 80, 120), "is_moveable": False, "size": "giant"},
    {"rect": pygame.Rect(600, 800, 200, 200), "color": (80, 80, 120), "is_moveable": False, "size": "giant"},
]

super_giant_blocks: list[dict] = [
    # Super giant blocks (300x300)
    {"rect": pygame.Rect(500, 300, 300, 300), "color": (60, 60, 100), "is_moveable": False, "size": "super_giant"},
    {"rect": pygame.Rect(1200, 700, 300, 300), "color": (60, 60, 100), "is_moveable": False, "size": "super_giant"},
]

# Border geometry: trapezoids and triangles (unmovable, indestructible)
# Layout: 3 trapezoids left (spaced), 2 trapezoids right (adjacent), 
#         5 trapezoids with 2 triangles each on top, line of triangles on bottom
trapezoid_blocks = []
triangle_blocks = []  # New: triangles for decorative border elements

# Calculate spacing for left side (3 trapezoids with gaps)
left_trap_height = HEIGHT // 4  # Each trapezoid takes 1/4 of screen height
left_gap = 50  # Gap between trapezoids
left_trap_width = 100  # Width of trapezoid hanging into screen

# Left side: 3 trapezoids with spaces
for i in range(3):
    y_start = i * (left_trap_height + left_gap)
    y_end = y_start + left_trap_height
    trap_rect = pygame.Rect(-60, y_start, left_trap_width + 60, y_end - y_start)
    trapezoid_blocks.append({
        "points": [(-60, y_start), (left_trap_width, y_start + 20), (left_trap_width, y_end - 20), (-60, y_end)],
        "bounding_rect": trap_rect,
        "rect": trap_rect,  # Add rect for pushing support
        "color": (140, 110, 170),
        "is_moveable": True,
        "side": "left"
    })

# Right side: 2 trapezoids next to each other
right_trap_height = HEIGHT // 2.5
right_trap_width = 100
right_y1 = 0
right_y2 = right_trap_height + 20  # Small gap

trap_rect1 = pygame.Rect(WIDTH - right_trap_width, right_y1, right_trap_width + 60, right_trap_height)
trapezoid_blocks.append({
    "points": [(WIDTH - right_trap_width, right_y1 + 20), (WIDTH + 60, right_y1), (WIDTH + 60, right_y1 + right_trap_height), (WIDTH - right_trap_width, right_y1 + right_trap_height - 20)],
    "bounding_rect": trap_rect1,
    "rect": trap_rect1,  # Add rect for pushing support
    "color": (110, 130, 190),
    "is_moveable": True,
    "side": "right"
})

trap_rect2 = pygame.Rect(WIDTH - right_trap_width, right_y2, right_trap_width + 60, right_trap_height)
trapezoid_blocks.append({
    "points": [(WIDTH - right_trap_width, right_y2 + 20), (WIDTH + 60, right_y2), (WIDTH + 60, right_y2 + right_trap_height), (WIDTH - right_trap_width, right_y2 + right_trap_height - 20)],
    "bounding_rect": trap_rect2,
    "rect": trap_rect2,  # Add rect for pushing support
    "color": (110, 130, 190),
    "is_moveable": True,
    "side": "right"
})

# Top: 5 trapezoids with 2 triangles each on top
top_trap_width = WIDTH // 5.5
top_trap_height = 80
top_trap_spacing = (WIDTH - 5 * top_trap_width) / 6  # Even spacing

for i in range(5):
    x_start = top_trap_spacing + i * (top_trap_width + top_trap_spacing)
    x_end = x_start + top_trap_width
    
    # Trapezoid hanging down
    trap_rect = pygame.Rect(x_start, -60, x_end - x_start, top_trap_height + 60)
    trapezoid_blocks.append({
        "points": [(x_start, -60), (x_end, -60), (x_end - 20, top_trap_height), (x_start + 20, top_trap_height)],
        "bounding_rect": trap_rect,
        "rect": trap_rect,  # Add rect for pushing support
        "color": (100, 120, 180),
        "is_moveable": True,
        "side": "top"
    })
    
    # 2 triangles on top of each trapezoid
    triangle_center_x = (x_start + x_end) // 2
    triangle_size = 30
    
    # Triangle 1 (left)
    tri_rect1 = pygame.Rect(triangle_center_x - triangle_size, -100, triangle_size, 40)
    triangle_blocks.append({
        "points": [(triangle_center_x - triangle_size, -60), (triangle_center_x, -100), (triangle_center_x - triangle_size // 2, -60)],
        "bounding_rect": tri_rect1,
        "rect": tri_rect1,  # Add rect for pushing support
        "color": (120, 140, 200),
        "is_moveable": True,
        "side": "top"
    })
    
    # Triangle 2 (right)
    tri_rect2 = pygame.Rect(triangle_center_x, -100, triangle_size, 40)
    triangle_blocks.append({
        "points": [(triangle_center_x + triangle_size // 2, -60), (triangle_center_x, -100), (triangle_center_x + triangle_size, -60)],
        "bounding_rect": tri_rect2,
        "rect": tri_rect2,  # Add rect for pushing support
        "color": (120, 140, 200),
        "is_moveable": True,
        "side": "top"
    })

# Bottom: Line of triangles across the bottom
bottom_triangle_count = 10
bottom_triangle_width = WIDTH // bottom_triangle_count
bottom_triangle_height = 40

for i in range(bottom_triangle_count):
    x_center = i * bottom_triangle_width + bottom_triangle_width // 2
    tri_rect = pygame.Rect(x_center - bottom_triangle_width // 2, HEIGHT, bottom_triangle_width, bottom_triangle_height)
    triangle_blocks.append({
        "points": [(x_center - bottom_triangle_width // 2, HEIGHT), (x_center, HEIGHT + bottom_triangle_height), (x_center + bottom_triangle_width // 2, HEIGHT)],
        "bounding_rect": tri_rect,
        "rect": tri_rect,  # Add rect for pushing support
        "color": (120, 100, 160),
        "is_moveable": True,
        "side": "bottom"
    })

# Add more blocks: 50% destructible, 50% indestructible, all moveable
destructible_blocks.extend([
    # First 6 blocks: Indestructible (no HP)
    {"rect": pygame.Rect(240, 360, 70, 70), "color": (160, 110, 210), "is_moveable": True},
    {"rect": pygame.Rect(400, 520, 60, 60), "color": (110, 210, 160), "is_moveable": True},
    {"rect": pygame.Rect(560, 680, 80, 50), "color": (210, 160, 110), "is_moveable": True},
    {"rect": pygame.Rect(720, 840, 70, 70), "color": (160, 160, 210), "is_moveable": True},
    {"rect": pygame.Rect(880, 1000, 60, 60), "color": (210, 210, 110), "is_moveable": True},
    {"rect": pygame.Rect(1040, 1160, 80, 50), "color": (190, 130, 190), "is_moveable": True},
    # Last 6 blocks: Destructible (with HP)
    {"rect": pygame.Rect(1200, 1320, 70, 70), "color": (130, 190, 130), "hp": 450, "max_hp": 450, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1360, 1160, 60, 60), "color": (210, 130, 110), "hp": 500, "max_hp": 500, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1520, 1000, 80, 50), "color": (160, 160, 230), "hp": 600, "max_hp": 600, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1680, 840, 70, 70), "color": (230, 210, 130), "hp": 450, "max_hp": 450, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1840, 680, 60, 60), "color": (200, 160, 210), "hp": 550, "max_hp": 550, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(200, 840, 80, 50), "color": (110, 210, 210), "hp": 400, "max_hp": 400, "is_destructible": True, "is_moveable": True, "crack_level": 0},
])

# Single moving health recovery zone
moving_health_zone = {
    "rect": pygame.Rect(WIDTH // 4 - 75, HEIGHT // 4 - 75, 150, 150),  # Offset from center (boss spawn)
    "heal_rate": 20.0,
    "color": (100, 255, 100, 80),
    "name": "Moving Healing Zone",
    "zone_id": 1,
    "velocity": 30.0,  # Movement speed in pixels per second (scalar)
    "target": None,  # Target position to move towards
}

# Track which zones player is currently in (for telemetry)
player_current_zones = set()  # Set of zone names player is in

# Player health regeneration rate (can be increased by pickups)
player_health_regen_rate = 0.0  # Base regeneration rate (0 = no regen)

# Bouncing destructor shapes (line 79)
destructor_shapes: list[dict] = []  # Large shapes that bounce around destroying things

# ----------------------------
# Player bullets
# ----------------------------
player_bullets: list[dict] = []
player_bullet_speed = 900
player_bullet_size = (8, 8)
player_bullet_damage = 20
player_shoot_cooldown = 0.12
player_time_since_shot = 999.0
player_bullets_color = (10, 200, 200)
player_bullet_shapes = ["circle", "square", "diamond"]
player_bullet_shape_index = 0

# Grenade system
grenade_explosions: list[dict] = []  # List of active explosions {x, y, radius, max_radius, timer, damage}
grenade_cooldown = 2.0  # Cooldown between grenades (seconds)
grenade_time_since_used = 999.0  # Time since last grenade
grenade_damage = 1500  # Damage to enemies and destructible blocks (increased from 500)

# Missile system (seeking missiles)
missiles: list[dict] = []  # List of active missiles {rect, vel, target_enemy, speed, damage, explosion_radius}
missile_cooldown = 3.0  # Cooldown between missiles (seconds)
missile_time_since_used = 999.0  # Time since last missile
missile_damage = 800  # Damage on explosion
missile_explosion_radius = 100  # Explosion radius
missile_speed = 400  # Missile movement speed

# Filter blocks to prevent them from spawning within 10x player size radius from player
# This must be done after all blocks are defined
# NOTE: This code runs at module level but player is None until main() is called
# The actual filtering will happen in main() after player is initialized
# player_center = pygame.Vector2(player.center)  # Moved to main()
# player_size = max(player.w, player.h)  # Use larger dimension (28)
# min_block_distance = player_size * 10  # 10x player size = 280 pixels

# Filter all block lists to remove blocks too close to player and prevent overlaps with each other
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

# Filter blocks to prevent overlaps (allies checked at runtime in random_spawn_position)
# Note: trapezoid_blocks and triangle_blocks are border elements and don't need overlap filtering
# NOTE: This filtering will be done in main() after player is initialized
# destructible_blocks = filter_blocks_no_overlap(...)  # Moved to main()
# moveable_destructible_blocks = filter_blocks_no_overlap(...)  # Moved to main()
# giant_blocks = filter_blocks_no_overlap(...)  # Moved to main()
# super_giant_blocks = filter_blocks_no_overlap(...)  # Moved to main()

# Ensure health zone doesn't overlap with blocks
health_zone_overlaps = True
max_health_zone_attempts = 100
for _ in range(max_health_zone_attempts):
    health_zone_overlaps = False
    # Check if health zone overlaps with any blocks
    for block_list in [destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks]:
        for block in block_list:
            if moving_health_zone["rect"].colliderect(block["rect"]):
                health_zone_overlaps = True
                break
        if health_zone_overlaps:
            break
    # Also check trapezoid and triangle blocks
    if not health_zone_overlaps:
        for tb in trapezoid_blocks:
            if moving_health_zone["rect"].colliderect(tb.get("bounding_rect", tb.get("rect"))):
                health_zone_overlaps = True
                break
    if not health_zone_overlaps:
        for tr in triangle_blocks:
            if moving_health_zone["rect"].colliderect(tr.get("bounding_rect", tr.get("rect"))):
                health_zone_overlaps = True
                break
    
    if not health_zone_overlaps:
        break  # Found a good position
    
    # Try a new random position for health zone
    new_x = random.randint(100, WIDTH - 250)
    new_y = random.randint(100, HEIGHT - 250)
    moving_health_zone["rect"].center = (new_x, new_y)

# ----------------------------
# Enemy templates + cloning
# ----------------------------
enemy_templates: list[dict] = [
    {
        "type": "pawn",
        "rect": pygame.Rect(120, 450, 28, 28),
        "color": (180, 180, 180),  # Gray
        "hp": 50,
        "max_hp": 50,
        "shoot_cooldown": 1.0,  # Basic fire rate
        "projectile_speed": 300,
        "projectile_color": (200, 200, 200),
        "projectile_shape": "circle",
        "speed": 80,  # Basic movement speed
        "enemy_class": "pawn",  # Enemy class identifier
    },
    {
        "type": "suicide",
        "rect": pygame.Rect(200, 200, 48, 48),  # Twice as big (24*2 = 48)
        "color": (255, 50, 50),  # Bright red
        "hp": 30,
        "max_hp": 30,
        "shoot_cooldown": 999.0,  # Doesn't shoot
        "projectile_speed": 0,
        "projectile_color": (255, 0, 0),
        "projectile_shape": "circle",
        "speed": 90,  # 0.75x current speed (120 * 0.75 = 90)
        "is_suicide": True,  # Marks this as suicide enemy
        "explosion_range": 150,  # Range for grenade explosion
        "detonation_distance": 50,  # Distance from player to detonate (closer before exploding)
    },
    {
        "type": "grunt",
        "rect": pygame.Rect(120, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "projectile_speed": 320,
        "projectile_color": (180, 220, 255),
        "projectile_shape": "square",
        "speed": 90,
    },
    {
        "type": "heavy",
        "rect": pygame.Rect(650, 120, 32, 32),
        "color": (220, 120, 80),
        "hp": 80,
        "max_hp": 80,
        "shoot_cooldown": 1.2,
        "projectile_speed": 280,
        "projectile_color": (255, 190, 120),
        "projectile_shape": "circle",
        "speed": 70,
    },
    {
        "type": "stinky",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "projectile_speed": 320,
        "projectile_color": (180, 220, 255),
        "projectile_shape": "diamond",
        "speed": 110,
    },
    {
        "type": "baka",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (100, 80, 80),
        "hp": 300,
        "max_hp": 300,
        "shoot_cooldown": 0.1,
        "projectile_speed": 500,
        "projectile_color": (255, 120, 180),
        "projectile_shape": "square",
        "speed": 150,
    },
    {
        "type": "neko neko desu",
        "rect": pygame.Rect(100, 450, 28, 28),
        "color": (100, 80, 0),
        "hp": 20,
        "max_hp": 20,
        "shoot_cooldown": 0.01,
        "projectile_speed": 500,
        "projectile_color": (200, 255, 140),
        "projectile_shape": "circle",
        "speed": 160,
    },
    {
        "type": "BIG NEKU",
        "rect": pygame.Rect(400, 450, 28, 28),
        "color": (100, 200, 0),
        "hp": 300,
        "max_hp": 300,
        "shoot_cooldown": 1,
        "projectile_speed": 700,
        "projectile_color": (160, 200, 255),
        "projectile_shape": "diamond",
        "speed": 60,
    },
    {
        "type": "bouncer",
        "rect": pygame.Rect(500, 500, 30, 30),
        "color": (255, 100, 100),
        "hp": 70,
        "max_hp": 70,
        "shoot_cooldown": 1.5,
        "projectile_speed": 350,
        "projectile_color": (255, 150, 150),
        "projectile_shape": "square",
        "speed": 85,
        "bouncing_projectiles": True,  # shoots bouncing projectiles
    },
    {
        "type": "shield enemy",
        "rect": pygame.Rect(300, 300, 32, 32),
        "color": (100, 150, 200),
        "hp": 100,
        "max_hp": 100,
        "shoot_cooldown": 1.0,
        "projectile_speed": 300,
        "projectile_color": (150, 200, 255),
        "projectile_shape": "circle",
        "speed": 60,
        "has_shield": True,  # Has directional shield
        "shield_angle": 0.0,  # Direction shield is facing (radians)
        "shield_length": 50,  # Length of shield line
    },
    {
        "type": "reflector",
        "rect": pygame.Rect(400, 400, 36, 36),
        "color": (200, 150, 100),
        "hp": 150,
        "max_hp": 150,
        "shoot_cooldown": 999.0,  # Doesn't shoot
        "projectile_speed": 0,
        "projectile_color": (255, 200, 100),
        "projectile_shape": "circle",
        "speed": 40,  # Slow turn speed
        "has_reflective_shield": True,  # Has reflective shield
        "shield_angle": 0.0,  # Direction shield is facing (radians)
        "shield_length": 60,  # Length of shield
        "shield_hp": 0,  # Damage absorbed by shield (fires back)
        "turn_speed": 0.5,  # Radians per second turn speed
    },
    {
        "type": "spawner",
        "rect": pygame.Rect(500, 500, 40, 40),
        "color": (150, 50, 150),  # Purple
        "hp": 120,
        "max_hp": 120,
        "shoot_cooldown": 999.0,  # Doesn't shoot projectiles
        "projectile_speed": 0,
        "projectile_color": (150, 50, 150),
        "projectile_shape": "circle",
        "speed": 30,  # Slow movement
        "is_spawner": True,  # Marks this as a spawner enemy
        "spawn_cooldown": 5.0,  # Spawns enemies every 5 seconds
        "time_since_spawn": 0.0,
        "spawn_count": 0,  # Track how many enemies spawned
        "max_spawns": 3,  # Maximum enemies to spawn per spawner
    },
    {
        "type": "queen",
        "name": "queen",  # Explicit name
        "rect": pygame.Rect(400, 400, 32, 32),
        "color": (100, 0, 0),  # Dark maroon (player clone)
        "hp": 5000,  # 5000 health (increased from 2000)
        "max_hp": 5000,
        "shoot_cooldown": 1.0,  # 1.0s cooldown
        "projectile_speed": 350,
        "projectile_color": (150, 0, 0),
        "projectile_shape": "circle",
        "speed": 240,  # 3x standard speed (80 * 3)
        "is_player_clone": True,  # Marks this as player clone
        "enemy_class": "queen",  # Enemy class identifier
        "has_shield": True,  # Queen has shield
        "shield_angle": 0.0,
        "shield_length": 60,
        "can_use_grenades": True,  # Queen can use grenades
        "grenade_cooldown": 5.0,  # Grenade cooldown for queen
        "time_since_grenade": 999.0,
        "damage_taken_since_rage": 0,  # Track damage for rage mode
        "rage_mode_active": False,  # Rage mode after 300-500 damage
        "rage_mode_timer": 0.0,  # Rage mode duration (5 seconds)
        "rage_damage_threshold": random.randint(300, 500),  # Random threshold between 300-500
        "predicts_player": True,  # Queen also predicts player position
    },
    {
        "type": "queen",
        "rect": pygame.Rect(400, 400, 32, 32),
        "color": (100, 0, 0),  # Dark maroon (player clone)
        "hp": 5000,  # 5000 health (increased from 2000)
        "max_hp": 5000,
        "shoot_cooldown": 1.0,  # 1.0s cooldown
        "projectile_speed": 350,
        "projectile_color": (150, 0, 0),
        "projectile_shape": "circle",
        "speed": 240,  # 3x standard speed (80 * 3)
        "is_player_clone": True,  # Marks this as player clone
    },
    {
        "type": "patrol",
        "rect": pygame.Rect(0, 0, 32, 32),
        "color": (150, 100, 200),  # Purple
        "hp": 150,
        "max_hp": 150,
        "shoot_cooldown": 0.5,
        "projectile_speed": 400,
        "projectile_color": (200, 150, 255),
        "projectile_shape": "circle",
        "speed": 100,
        "is_patrol": True,  # Marks this as patrol enemy
        "patrol_side": 0,  # 0=top, 1=right, 2=bottom, 3=left
        "patrol_progress": 0.0,  # Progress along current side (0.0 to 1.0)
        "uses_wave_beam": True,  # Uses wave beam weapon
    },

]

# Boss enemy template (spawned at specific waves)
boss_template = {
    "type": "FINAL_BOSS",
    "rect": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100),
    "color": (255, 0, 0),
    "hp": 300,
    "max_hp": 300,
    "shoot_cooldown": 0.5,
    "projectile_speed": 400,
    "projectile_color": (255, 50, 50),
    "projectile_shape": "circle",
    "speed": 50,
    "is_boss": True,
    "phase": 1,  # Boss has 3 phases
    "phase_hp_thresholds": [0.66, 0.33],  # Phase 2 at 66% HP, Phase 3 at 33% HP
    "time_since_shot": 0.0,
}


def clone_enemies_from_templates() -> list[dict]:
    # Kept for compatibility but waves use start_wave() instead.
    return [make_enemy_from_template(t, 1.0, 1.0) for t in enemy_templates]


enemies: list[dict] = []

# ----------------------------
# Friendly AI
# ----------------------------
friendly_ai_templates: list[dict] = [
    {
        "type": "scout",
        "rect": pygame.Rect(0, 0, 24, 24),
        "color": (100, 200, 255),  # Light blue
        "hp": 400,  # 10x health (was 40)
        "max_hp": 400,  # 10x health (was 40)
        "shoot_cooldown": 0.4,
        "projectile_speed": 600,
        "projectile_color": (150, 220, 255),
        "projectile_shape": "circle",
        "speed": 180,
        "behavior": "aggressive",  # Charges nearest enemy
        "damage": 15,
    },
    {
        "type": "guardian",
        "rect": pygame.Rect(0, 0, 28, 28),
        "color": (100, 255, 150),  # Light green
        "hp": 800,  # 10x health (was 80)
        "max_hp": 800,  # 10x health (was 80)
        "shoot_cooldown": 0.6,
        "projectile_speed": 500,
        "projectile_color": (150, 255, 200),
        "projectile_shape": "square",
        "speed": 120,
        "behavior": "defensive",  # Stays near player, attacks nearby enemies
        "damage": 20,
    },
    {
        "type": "sniper",
        "rect": pygame.Rect(0, 0, 22, 22),
        "color": (255, 200, 100),  # Orange
        "hp": 300,  # 10x health (was 30)
        "max_hp": 300,  # 10x health (was 30)
        "shoot_cooldown": 1.2,
        "projectile_speed": 800,
        "projectile_color": (255, 220, 150),
        "projectile_shape": "diamond",
        "speed": 100,
        "behavior": "ranged",  # Keeps distance, snipes enemies
        "damage": 35,
    },
    {
        "type": "tank",
        "rect": pygame.Rect(0, 0, 32, 32),
        "color": (200, 150, 255),  # Purple
        "hp": 1500,  # 10x health (was 150)
        "max_hp": 1500,  # 10x health (was 150)
        "shoot_cooldown": 0.8,
        "projectile_speed": 400,
        "projectile_color": (220, 180, 255),
        "projectile_shape": "square",
        "speed": 80,
        "behavior": "tank",  # Slow, high HP, draws enemy fire
        "damage": 25,
    },
]

friendly_ai: list[dict] = []

# Dropped ally system (distracts enemies)
dropped_ally: dict | None = None  # Single dropped ally that distracts enemies
ally_drop_cooldown = 30.0  # Cooldown between ally drops (seconds)
ally_drop_timer = 0.0  # Time since last ally drop
friendly_projectiles: list[dict] = []

# ----------------------------
# Enemy projectiles
# ----------------------------
enemy_projectiles: list[dict] = []
enemy_projectile_size = (10, 10)
enemy_projectile_damage = int(10 * 1.1)  # 110% damage (11 damage)
enemy_projectiles_color = (200, 200, 200)
enemy_projectile_shapes = ["circle", "square", "diamond"]

# ----------------------------
# Run counters (runs table) - initialized in main()
# ----------------------------
running = True  # Will be set in main()
run_time = 0.0

shots_fired = 0
hits = 0

damage_taken = 0
damage_dealt = 0

enemies_spawned = 0
enemies_killed = 0
deaths = 0
score = 0
survival_time = 0.0  # Total time survived in seconds

# High score system
HIGH_SCORES_DB = "high_scores.db"
player_name_input = ""  # Current name being typed
name_input_active = False  # Whether we're in name input mode
final_score_for_high_score = 0  # Score to save when name is entered

POS_SAMPLE_INTERVAL = 0.25  # Reduced frequency for better performance (was 0.10)
pos_timer = 0.0

# Waves / progression
wave_number = 1
wave_in_level = 1  # Wave within current level (1, 2, or 3)
wave_respawn_delay = 2.5  # seconds between waves
time_to_next_wave = 0.0
wave_active = True
base_enemies_per_wave = 9  # Increased for more enemies (was 6)
max_enemies_per_wave = 54  # Increased for more enemies (was 36)
boss_active = False

# Pickups
pickups: list[dict] = []
pickup_spawn_timer = 0.0
PICKUP_SPAWN_INTERVAL = 7.5

# Scoring constants
SCORE_BASE_POINTS = 100
SCORE_WAVE_MULTIPLIER = 50
SCORE_TIME_MULTIPLIER = 2

# Weapon key mapping
WEAPON_KEY_MAP = {
    pygame.K_1: "basic",
    pygame.K_2: "rocket",
    pygame.K_3: "triple",
    pygame.K_4: "bouncing",
    pygame.K_5: "giant",
    pygame.K_6: "laser",
    pygame.K_7: "wave_beam",  # Wave pattern beam weapon
}
enemy_spawn_boost_level = 0  # enemies can increase this by collecting "spawn_boost" pickups

# Visual effects for pickups
pickup_particles: list[dict] = []  # particles around pickups
collection_effects: list[dict] = []  # effects when pickups are collected


# ----------------------------
# Helpers
# ----------------------------
def clamp_rect_to_screen(r: pygame.Rect):
    r.x = max(0, min(r.x, WIDTH - r.w))
    r.y = max(0, min(r.y, HEIGHT - r.h))


def vec_toward(ax, ay, bx, by) -> pygame.Vector2:
    if USE_C_EXTENSION:
        x, y = game_physics.vec_toward(ax, ay, bx, by)
        return pygame.Vector2(x, y)
    else:
        v = pygame.Vector2(bx - ax, by - ay)
        if v.length_squared() == 0:
            return pygame.Vector2(1, 0)
        return v.normalize()


def line_rect_intersection(start: pygame.Vector2, end: pygame.Vector2, rect: pygame.Rect) -> pygame.Vector2 | None:
    """Find the closest intersection point between a line and a rectangle."""
    # Check if line intersects with rectangle
    clipped = rect.clipline(start, end)
    if not clipped:
        return None
    # Return the point closest to start
    p1, p2 = clipped
    dist1 = (pygame.Vector2(p1) - start).length_squared()
    dist2 = (pygame.Vector2(p2) - start).length_squared()
    return pygame.Vector2(p1) if dist1 < dist2 else pygame.Vector2(p2)


def can_move_rect(rect: pygame.Rect, dx: int, dy: int, other_rects: list[pygame.Rect]) -> bool:
    if USE_C_EXTENSION:
        return game_physics.can_move_rect(
            rect.x, rect.y, rect.w, rect.h, dx, dy, other_rects, WIDTH, HEIGHT
        )
    else:
        test = rect.move(dx, dy)
        if test.left < 0 or test.right > WIDTH or test.top < 0 or test.bottom > HEIGHT:
            return False
        for o in other_rects:
            if test.colliderect(o):
                return False
        return True


def move_player_with_push(player_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict]):
    """Solid collision + pushing blocks (single block push; no chain pushing)."""
    block_rects = [b["rect"] for b in block_list]
    # Include all moveable blocks: destructible, moveable_destructible, trapezoid, and triangle blocks
    destructible_rects = [b["rect"] for b in destructible_blocks]
    moveable_destructible_rects = [b["rect"] for b in moveable_destructible_blocks]
    trapezoid_rects = [tb["rect"] for tb in trapezoid_blocks]  # Now use rect instead of bounding_rect
    triangle_rects = [tr["rect"] for tr in triangle_blocks]  # Now use rect instead of bounding_rect
    # Include giant and super giant blocks (unmovable) - player cannot pass through
    giant_block_rects = [gb["rect"] for gb in giant_blocks]
    super_giant_block_rects = [sgb["rect"] for sgb in super_giant_blocks]
    # Include friendly AI rects - player cannot pass through allies
    friendly_ai_rects = [f["rect"] for f in friendly_ai if f.get("hp", 1) > 0]
    all_collision_rects = block_rects + destructible_rects + moveable_destructible_rects + trapezoid_rects + triangle_rects + giant_block_rects + super_giant_block_rects + friendly_ai_rects

    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        player_rect.x += axis_dx
        player_rect.y += axis_dy

        hit_block = None
        hit_is_unpushable = False
        # Check regular blocks first
        for b in block_list:
            if player_rect.colliderect(b["rect"]):
                hit_block = b
                break
        # Check destructible blocks (now moveable)
        if hit_block is None:
            for b in destructible_blocks:
                if player_rect.colliderect(b["rect"]):
                    hit_block = b
                    break
        # Check moveable destructible blocks
        if hit_block is None:
            for b in moveable_destructible_blocks:
                if player_rect.colliderect(b["rect"]):
                    hit_block = b
                    break
        # Check trapezoid blocks (now moveable)
        if hit_block is None:
            for tb in trapezoid_blocks:
                if player_rect.colliderect(tb["rect"]):
                    hit_block = tb
                    break
        # Check triangle blocks (now moveable)
        if hit_block is None:
            for tr in triangle_blocks:
                if player_rect.colliderect(tr["rect"]):
                    hit_block = tr
                    break
        # Check hazard obstacles (paraboloids/trapezoids) - player cannot pass through or push
        if hit_block is None:
            for hazard in hazard_obstacles:
                if hazard.get("points") and len(hazard["points"]) > 2:
                    # Use point-in-polygon check for accurate collision
                    player_center = pygame.Vector2(player_rect.center)
                    if check_point_in_hazard(player_center, hazard["points"], hazard["bounding_rect"]):
                        hit_block = hazard
                        hit_is_unpushable = True  # Hazards are unmovable
                        break
        # Check giant and super giant blocks (unmovable) - player cannot pass through or push
        if hit_block is None:
            for gb in giant_blocks:
                if player_rect.colliderect(gb["rect"]):
                    hit_block = gb
                    hit_is_unpushable = True  # Can't push giant blocks
                    break
        if hit_block is None:
            for sgb in super_giant_blocks:
                if player_rect.colliderect(sgb["rect"]):
                    hit_block = sgb
                    hit_is_unpushable = True  # Can't push super giant blocks
                    break
        # Check friendly AI (allies) - player cannot pass through or push
        if hit_block is None:
            for f in friendly_ai:
                if f.get("hp", 1) > 0 and player_rect.colliderect(f["rect"]):
                    hit_block = f
                    hit_is_unpushable = True  # Can't push allies
                    break

        if hit_block is None:
            continue

        # Hazards and allies are unmovable, so just block player movement
        if hit_is_unpushable:
            player_rect.x -= axis_dx
            player_rect.y -= axis_dy
            continue

        hit_rect = hit_block["rect"]
        other_rects = [r for r in all_collision_rects if r is not hit_rect]

        if can_move_rect(hit_rect, axis_dx, axis_dy, other_rects):
            hit_rect.x += axis_dx
            hit_rect.y += axis_dy
            # Update bounding_rect for trapezoid/triangle blocks to match rect position
            if "bounding_rect" in hit_block:
                hit_block["bounding_rect"].x = hit_rect.x
                hit_block["bounding_rect"].y = hit_rect.y
        else:
            player_rect.x -= axis_dx
            player_rect.y -= axis_dy

    clamp_rect_to_screen(player_rect)


def move_enemy_with_push(enemy_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict]):
    """Enemy movement - enemies cannot go through objects and must navigate around them."""
    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        enemy_rect.x += axis_dx
        enemy_rect.y += axis_dy

        # Check collisions with all objects - enemies cannot pass through anything
        collision = False
        
        # Check regular blocks
        for b in block_list:
            if enemy_rect.colliderect(b["rect"]):
                collision = True
                break
        
        # Check destructible blocks
        if not collision:
            for b in destructible_blocks:
                if enemy_rect.colliderect(b["rect"]):
                    collision = True
                    break
        
        # Check moveable destructible blocks
        if not collision:
            for b in moveable_destructible_blocks:
                if enemy_rect.colliderect(b["rect"]):
                    collision = True
                    break
        
        # Check giant blocks (unmovable)
        if not collision:
            for gb in giant_blocks:
                if enemy_rect.colliderect(gb["rect"]):
                    collision = True
                    break
        
        # Check super giant blocks (unmovable)
        if not collision:
            for sgb in super_giant_blocks:
                if enemy_rect.colliderect(sgb["rect"]):
                    collision = True
                    break
        
        # Check trapezoid blocks
        if not collision:
            for tb in trapezoid_blocks:
                if enemy_rect.colliderect(tb.get("bounding_rect", tb.get("rect"))):
                    collision = True
                    break
        
        # Check triangle blocks
        if not collision:
            for tr in triangle_blocks:
                if enemy_rect.colliderect(tr.get("bounding_rect", tr.get("rect"))):
                    collision = True
                    break
        
        # Check pickups
        if not collision:
            for pickup in pickups:
                if enemy_rect.colliderect(pickup["rect"]):
                    collision = True
                    break
        
        # Check health zone
        if not collision:
            if enemy_rect.colliderect(moving_health_zone["rect"]):
                collision = True
        
        # Check player
        if not collision:
            if enemy_rect.colliderect(player):
                collision = True
        
        # Check friendly AI
        if not collision:
            for f in friendly_ai:
                if f.get("hp", 1) > 0 and enemy_rect.colliderect(f["rect"]):
                    collision = True
                    break
        
        # Check other enemies (prevent enemy stacking)
        if not collision:
            for other_e in enemies:
                if other_e["rect"] is not enemy_rect and enemy_rect.colliderect(other_e["rect"]):
                    collision = True
                    break

        # If collision detected, revert movement
        if collision:
            enemy_rect.x -= axis_dx
            enemy_rect.y -= axis_dy

    clamp_rect_to_screen(enemy_rect)


def move_enemy_with_push_cached(enemy_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict],
                                 cached_moveable_destructible_rects: list,
                                 cached_trapezoid_rects: list,
                                 cached_triangle_rects: list):
    """Optimized enemy movement - enemies cannot go through objects and must navigate around them."""
    # Cache rects for performance
    block_rects = [b["rect"] for b in block_list]
    cached_destructible_rects = [b["rect"] for b in destructible_blocks]
    cached_giant_rects = [gb["rect"] for gb in giant_blocks]
    cached_super_giant_rects = [sgb["rect"] for sgb in super_giant_blocks]
    cached_pickup_rects = [p["rect"] for p in pickups]
    cached_friendly_rects = [f["rect"] for f in friendly_ai if f.get("hp", 1) > 0]
    cached_enemy_rects = [e["rect"] for e in enemies if e["rect"] is not enemy_rect]

    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        enemy_rect.x += axis_dx
        enemy_rect.y += axis_dy

        # Check collisions with all objects - enemies cannot pass through anything
        collision = False
        
        # Check regular blocks
        for rect in block_rects:
            if enemy_rect.colliderect(rect):
                collision = True
                break
        
        # Check destructible blocks
        if not collision:
            for rect in cached_destructible_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check moveable destructible blocks
        if not collision:
            for rect in cached_moveable_destructible_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check giant blocks (unmovable)
        if not collision:
            for rect in cached_giant_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check super giant blocks (unmovable)
        if not collision:
            for rect in cached_super_giant_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check trapezoid blocks
        if not collision:
            for rect in cached_trapezoid_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check triangle blocks
        if not collision:
            for rect in cached_triangle_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check pickups
        if not collision:
            for rect in cached_pickup_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check health zone
        if not collision:
            if enemy_rect.colliderect(moving_health_zone["rect"]):
                collision = True
        
        # Check player
        if not collision:
            if enemy_rect.colliderect(player):
                collision = True
        
        # Check friendly AI
        if not collision:
            for rect in cached_friendly_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check other enemies (prevent enemy stacking)
        if not collision:
            for rect in cached_enemy_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break

        # If collision detected, revert movement
        if collision:
            enemy_rect.x -= axis_dx
            enemy_rect.y -= axis_dy

    clamp_rect_to_screen(enemy_rect)


def rect_offscreen(r: pygame.Rect) -> bool:
    return r.right < 0 or r.left > WIDTH or r.bottom < 0 or r.top > HEIGHT


def filter_blocks_too_close_to_player(block_list: list[dict], player_center: pygame.Vector2, player_size: int) -> list[dict]:
    """Filter out blocks that are too close to the player (within 10x player size radius)."""
    min_distance = player_size * 10  # 10x player size radius
    filtered = []
    for block in block_list:
        block_center = pygame.Vector2(block["rect"].center)
        distance = block_center.distance_to(player_center)
        if distance >= min_distance:
            filtered.append(block)
    return filtered


def random_spawn_position(size: tuple[int, int], max_attempts: int = 25) -> pygame.Rect:
    """Find a spawn position not overlapping player or blocks. Player spawn takes priority."""
    w, h = size
    player_center = pygame.Vector2(player.center)
    player_size = max(player.w, player.h)  # Use larger dimension for player size
    min_distance = player_size * 10  # 10x player size radius
    
    for _ in range(max_attempts):
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        candidate = pygame.Rect(x, y, w, h)
        candidate_center = pygame.Vector2(candidate.center)
        
        # Check if too close to player (10x player size radius)
        if candidate_center.distance_to(player_center) < min_distance:
            continue
        
        # Player spawn takes priority - don't spawn blocks on player
        if candidate.colliderect(player):
            continue
        if any(candidate.colliderect(b["rect"]) for b in blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in moveable_destructible_blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in destructible_blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in giant_blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in super_giant_blocks):
            continue
        if any(candidate.colliderect(tb["bounding_rect"]) for tb in trapezoid_blocks):
            continue
        if any(candidate.colliderect(tr["bounding_rect"]) for tr in triangle_blocks):
            continue
        if any(candidate.colliderect(p["rect"]) for p in pickups):
            continue
        # Prevent spawning in health recovery zone
        if candidate.colliderect(moving_health_zone["rect"]):
            continue
        return candidate
    # fallback: top-left corner inside bounds
    return pygame.Rect(max(0, WIDTH // 2 - w), max(0, HEIGHT // 2 - h), w, h)


def make_enemy_from_template(t: dict, hp_scale: float, speed_scale: float) -> dict:
    # Apply 110% multipliers (1.1x) to all stats
    # Exception: Queen (player clone) has fixed 2000 HP and 3x speed, not affected by scaling
    if t.get("type") == "queen":
        hp = 5000  # Fixed 5000 health for queen
        base_speed = t.get("speed", 80)
        final_speed = base_speed * 1.1  # Still apply 110% multiplier
    else:
        hp = int(t["hp"] * hp_scale * 1.1)  # 110% health
        # Cap HP at 300 maximum (except queen)
        hp = min(hp, 300)
        final_speed = t.get("speed", 80) * speed_scale * 1.1  # 110% movement speed
    
    enemy = {
        "type": t["type"],
        "rect": pygame.Rect(t["rect"].x, t["rect"].y, t["rect"].w, t["rect"].h),
        "color": t["color"],
        "hp": hp,
        "max_hp": hp,
        "shoot_cooldown": t["shoot_cooldown"] / 1.5,  # 150% fire rate (faster = lower cooldown, increased from 1.1)
        "time_since_shot": random.uniform(0.0, t["shoot_cooldown"] / 1.5),
        "projectile_speed": t["projectile_speed"],
        "projectile_color": t.get("projectile_color", enemy_projectiles_color),
        "projectile_shape": t.get("projectile_shape", "circle"),
        "speed": final_speed,  # Speed (queen gets 3x, others get normal scaling)
    }
    # Add shield properties if present
    if t.get("has_shield"):
        enemy["has_shield"] = True
        enemy["shield_angle"] = random.uniform(0, 2 * math.pi)
        enemy["shield_length"] = t.get("shield_length", 50)
    if t.get("has_reflective_shield"):
        enemy["has_reflective_shield"] = True
        enemy["shield_angle"] = random.uniform(0, 2 * math.pi)
        enemy["shield_length"] = t.get("shield_length", 60)
        enemy["shield_hp"] = 0
        enemy["turn_speed"] = t.get("turn_speed", 0.5)
    # Add queen-specific properties
    if t.get("type") == "queen":
        enemy["name"] = t.get("name", "queen")
        enemy["can_use_grenades"] = t.get("can_use_grenades", False)
        enemy["grenade_cooldown"] = t.get("grenade_cooldown", 5.0)
        enemy["time_since_grenade"] = t.get("time_since_grenade", 999.0)
        enemy["damage_taken_since_rage"] = 0
        enemy["rage_mode_active"] = False
        enemy["rage_mode_timer"] = 0.0
        enemy["rage_damage_threshold"] = t.get("rage_damage_threshold", random.randint(300, 500))
        enemy["predicts_player"] = t.get("predicts_player", False)
    return enemy


def log_enemy_spawns(new_enemies: list[dict]):
    global enemies_spawned
    for e in new_enemies:
        enemies_spawned += 1
        telemetry.log_enemy_spawn(
            EnemySpawnEvent(
                t=run_time,
                enemy_type=e["type"],
                x=e["rect"].x,
                y=e["rect"].y,
                w=e["rect"].w,
                h=e["rect"].h,
                hp=e["hp"],
            )
        )


def make_friendly_from_template(t: dict, hp_scale: float, speed_scale: float) -> dict:
    """Create a friendly AI unit from a template."""
    # Set max HP to 1000 (10x health - was 100, now 1000 for all friendly AI)
    # Apply 110% multiplier (1.1x) to all stats
    max_hp = int(1000 * 1.1)  # 110% health
    hp = max_hp  # Always start with full health at wave start
    return {
        "type": t["type"],
        "rect": pygame.Rect(t["rect"].x, t["rect"].y, t["rect"].w, t["rect"].h),
        "color": t["color"],
        "hp": hp,
        "max_hp": max_hp,  # Full health, green bar at wave start
        "shoot_cooldown": t["shoot_cooldown"] / 1.5,  # 150% fire rate (faster = lower cooldown, increased from 1.1)
        "time_since_shot": random.uniform(0.0, t["shoot_cooldown"] / 1.5),
        "projectile_speed": t["projectile_speed"],
        "projectile_color": t["projectile_color"],
        "projectile_shape": t["projectile_shape"],
        "speed": t["speed"] * speed_scale * 1.1,  # 110% movement speed
        "behavior": t["behavior"],
        "damage": int(t["damage"] * 1.1),  # 110% damage
        "target": None,  # Current target enemy
    }


def find_nearest_enemy(friendly_pos: pygame.Vector2) -> dict | None:
    """Find the nearest enemy to a friendly AI unit."""
    if not enemies:
        return None
    nearest = None
    min_dist = float("inf")
    for e in enemies:
        dist = (pygame.Vector2(e["rect"].center) - friendly_pos).length_squared()
        if dist < min_dist:
            min_dist = dist
            nearest = e
    return nearest


def find_nearest_threat(enemy_pos: pygame.Vector2) -> tuple[pygame.Vector2, str] | None:
    """Find the nearest threat (player or friendly AI) to an enemy.
    Prioritizes dropped ally over player, then other friendly AI."""
    threats = []
    player_pos = pygame.Vector2(player.center)
    player_dist_sq = (player_pos - enemy_pos).length_squared()
    player_dist = math.sqrt(player_dist_sq)
    
    # Add friendly AI threats (prioritize dropped ally)
    dropped_ally_threats = []
    other_friendly_threats = []
    for f in friendly_ai:
        if f["hp"] <= 0:
            continue
        friendly_pos = pygame.Vector2(f["rect"].center)
        friendly_dist_sq = (friendly_pos - enemy_pos).length_squared()
        friendly_dist = math.sqrt(friendly_dist_sq)
        if f.get("is_dropped_ally", False):
            # Dropped ally has highest priority
            dropped_ally_threats.append((friendly_pos, friendly_dist_sq, "dropped_ally", friendly_dist))
        else:
            other_friendly_threats.append((friendly_pos, friendly_dist_sq, "friendly", friendly_dist))
    
    # Add player as threat (lowest priority)
    threats.append((player_pos, player_dist_sq, "player", player_dist))
    
    if not threats and not dropped_ally_threats and not other_friendly_threats:
        return None
    
    # Prioritize dropped ally first, then other friendly AI, then player
    if dropped_ally_threats:
        dropped_ally_threats.sort(key=lambda x: x[1])
        return (dropped_ally_threats[0][0], dropped_ally_threats[0][2])
    
    if other_friendly_threats:
        other_friendly_threats.sort(key=lambda x: x[1])
        return (other_friendly_threats[0][0], other_friendly_threats[0][2])
    
    # Return player if no friendly threats
    return (player_pos, "player")


def find_threats_in_dodge_range(enemy_pos: pygame.Vector2, dodge_range: float = 200.0) -> list[pygame.Vector2]:
    """Find bullets (player or friendly) that are close enough to dodge."""
    threats = []
    enemy_v2 = pygame.Vector2(enemy_pos)
    dodge_range_sq = dodge_range * dodge_range  # Use squared distance for faster comparison
    
    # Check player bullets
    for b in player_bullets:
        bullet_pos = pygame.Vector2(b["rect"].center)
        dist_sq = (bullet_pos - enemy_v2).length_squared()
        if dist_sq < dodge_range_sq:
            # Only compute actual distance if in range
            dist = math.sqrt(dist_sq)
            # Predict where bullet will be
            bullet_vel = b.get("vel", pygame.Vector2(0, 0))
            vel_length = bullet_vel.length()
            time_to_reach = dist / vel_length if vel_length > 0 else 999
            if time_to_reach < 0.5:  # Only dodge if bullet will reach soon
                threats.append(bullet_pos)
    
    # Check friendly projectiles
    for fp in friendly_projectiles:
        bullet_pos = pygame.Vector2(fp["rect"].center)
        dist_sq = (bullet_pos - enemy_v2).length_squared()
        if dist_sq < dodge_range_sq:
            # Only compute actual distance if in range
            dist = math.sqrt(dist_sq)
            bullet_vel = fp.get("vel", pygame.Vector2(0, 0))
            vel_length = bullet_vel.length()
            time_to_reach = dist / vel_length if vel_length > 0 else 999
            if time_to_reach < 0.5:
                threats.append(bullet_pos)
    
    return threats


def spawn_friendly_ai(count: int, hp_scale: float, speed_scale: float):
    """Spawn friendly AI units."""
    global friendly_ai
    spawned_list = []
    for _ in range(count):
        tmpl = random.choice(friendly_ai_templates)
        friendly = make_friendly_from_template(tmpl, hp_scale, speed_scale)
        # Use random_spawn_position to prevent spawning on blocks or health zone
        friendly["rect"] = random_spawn_position((friendly["rect"].w, friendly["rect"].h))
        friendly_ai.append(friendly)
        spawned_list.append(friendly)
    
    # Log friendly AI spawns
    for f in spawned_list:
        telemetry.log_friendly_spawn(
            FriendlyAISpawnEvent(
                t=run_time,
                friendly_type=f["type"],
                x=f["rect"].x,
                y=f["rect"].y,
                w=f["rect"].w,
                h=f["rect"].h,
                hp=f["hp"],
                behavior=f["behavior"],
            )
        )


def spawn_friendly_projectile(friendly: dict, target: dict):
    """Spawn a projectile from friendly AI targeting an enemy."""
    d = vec_toward(
        friendly["rect"].centerx, friendly["rect"].centery,
        target["rect"].centerx, target["rect"].centery
    )
    r = pygame.Rect(
        friendly["rect"].centerx - 6,
        friendly["rect"].centery - 6,
        12, 12
    )
    friendly_projectiles.append({
        "rect": r,
        "vel": d * friendly["projectile_speed"],
        "damage": friendly["damage"],
        "color": friendly["projectile_color"],
        "shape": friendly["projectile_shape"],
        "source_type": friendly["type"],
        "target_enemy_type": target.get("type", "unknown"),  # Store target type for telemetry
    })
    
    # Log friendly AI shot
    telemetry.log_friendly_shot(
        FriendlyAIShotEvent(
            t=run_time,
            friendly_type=friendly["type"],
            origin_x=friendly["rect"].centerx,
            origin_y=friendly["rect"].centery,
            target_x=target["rect"].centerx,
            target_y=target["rect"].centery,
            target_enemy_type=target.get("type", "unknown"),
        )
    )
    if telemetry_enabled and telemetry:
        telemetry.flush(force=True)


def start_wave(wave_num: int):
    """Spawn a new wave with scaling. Each level has 3 waves, boss on wave 3."""
    global enemies, wave_active, boss_active, wave_in_level, current_level, lives, overshield_recharge_timer, ally_drop_timer, shield_recharge_timer, shield_cooldown_remaining
    enemies = []
    boss_active = False
    # Reset lives to 3 at the beginning of each wave
    lives = 3  # Reset to 3 lives at the beginning of each wave
    
    # Calculate level and wave within level (1-based)
    current_level = min(max_level, (wave_num - 1) // 3 + 1)
    wave_in_level = ((wave_num - 1) % 3) + 1
    
    # Boss appears on wave 3 of each level
    if wave_in_level == 3:
        # Spawn boss
        boss = boss_template.copy()
        boss["rect"] = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
        diff_mult = difficulty_multipliers[difficulty]
        
        # Boss HP is capped at 300 (same as all enemies)
        # Scale boss HP for different levels, but cap at 300
        # Apply 110% multiplier (1.1x) to all boss stats
        boss_hp_scale = 1.0 + (current_level - 1) * 0.3
        boss["hp"] = min(int(boss["max_hp"] * boss_hp_scale * diff_mult["enemy_hp"] * 1.1), 300)  # 110% health
        boss["max_hp"] = boss["hp"]
        boss["shoot_cooldown"] = boss_template["shoot_cooldown"] / 1.5  # 150% fire rate (faster = lower cooldown, increased from 1.1)
        boss["speed"] = boss_template["speed"] * 1.1  # 110% movement speed
        
        boss["phase"] = 1
        boss["time_since_shot"] = 0.0
        enemies.append(boss)
        boss_active = True
        log_enemy_spawns([boss])
        # Log boss as enemy type for this wave
        telemetry.log_wave_enemy_types(
            WaveEnemyTypeEvent(
                t=run_time,
                wave_number=wave_num,
                enemy_type=boss["type"],
                count=1,
            )
        )
        wave_active = True
        
        # Charge overshield at wave start (boss wave)
        overshield_recharge_timer = overshield_recharge_cooldown  # Set to full charge
        
        return
    
    # Normal wave spawning (waves 1 and 2 of each level)
    # Apply difficulty multipliers
    diff_mult = difficulty_multipliers[difficulty]
    # Level-based scaling - increase difficulty with level and wave in level
    level_mult = 1.0 + (current_level - 1) * 0.3
    wave_in_level_mult = 1.0 + (wave_in_level - 1) * 0.15  # Wave 2 is harder than wave 1
    hp_scale = (1.0 + 0.15 * (wave_num - 1)) * diff_mult["enemy_hp"] * level_mult * wave_in_level_mult
    speed_scale = (1.0 + 0.05 * (wave_num - 1)) * diff_mult["enemy_speed"] * level_mult * wave_in_level_mult
    # Apply difficulty to enemy count
    base_count = base_enemies_per_wave + enemy_spawn_boost_level + 2 * (wave_num - 1)
    count = min(int(base_count * diff_mult["enemy_spawn"] * 3.0), max_enemies_per_wave)  # 3.0x multiplier (increased from 2.0x)

    spawned: list[dict] = []
    # Track enemy types for this wave
    enemy_type_counts: dict[str, int] = {}
    
    for _ in range(count):
        tmpl = random.choice(enemy_templates)
        enemy = make_enemy_from_template(tmpl, hp_scale, speed_scale)
        enemy["rect"] = random_spawn_position((enemy["rect"].w, enemy["rect"].h))
        spawned.append(enemy)
        # Count enemy types
        enemy_type = enemy["type"]
        enemy_type_counts[enemy_type] = enemy_type_counts.get(enemy_type, 0) + 1

    enemies.extend(spawned)
    log_enemy_spawns(spawned)
    
    # Log enemy types for this wave
    for enemy_type, type_count in enemy_type_counts.items():
        telemetry.log_wave_enemy_types(
            WaveEnemyTypeEvent(
                t=run_time,
                wave_number=wave_num,
                enemy_type=enemy_type,
                count=type_count,
            )
        )
    
    # Spawn friendly AI: 2-4 per wave (increased from 1-2)
    # Calculate friendly AI count based on enemy count - more friendly AI
    friendly_count = max(2, min(4, (count + 1) // 2))  # 2-4 friendly per wave
    spawn_friendly_ai(friendly_count, hp_scale, speed_scale)
    
    wave_active = True
    
    # Charge overshield at wave start
    overshield_recharge_timer = overshield_recharge_cooldown  # Set to full charge
    ally_drop_timer = ally_drop_cooldown  # Charge ally drop at wave start
    # Charge shield at wave start
    shield_recharge_timer = shield_recharge_cooldown  # Set to full charge
    shield_cooldown_remaining = 0.0  # Shield ready to use
    
    # Log wave start event
    telemetry.log_wave(
        WaveEvent(
            t=run_time,
            wave_number=wave_num,
            event_type="start",
            enemies_spawned=count,
            hp_scale=hp_scale,
            speed_scale=speed_scale,
        )
    )


def init_high_scores_db():
    """Initialize the high scores database."""
    conn = sqlite3.connect(HIGH_SCORES_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            waves_survived INTEGER NOT NULL,
            time_survived REAL NOT NULL,
            enemies_killed INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            date_achieved TEXT NOT NULL
        );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_score ON high_scores(score DESC);")
    conn.commit()
    conn.close()


def get_high_scores(limit: int = 10) -> list[dict]:
    """Get top high scores from database."""
    conn = sqlite3.connect(HIGH_SCORES_DB)
    cursor = conn.execute("""
        SELECT player_name, score, waves_survived, time_survived, enemies_killed, difficulty, date_achieved
        FROM high_scores
        ORDER BY score DESC
        LIMIT ?
    """, (limit,))
    scores = []
    for row in cursor.fetchall():
        scores.append({
            "name": row[0],
            "score": row[1],
            "waves": row[2],
            "time": row[3],
            "kills": row[4],
            "difficulty": row[5],
            "date": row[6]
        })
    conn.close()
    return scores


def save_high_score(name: str, score: int, waves: int, time_survived: float, enemies_killed: int, difficulty: str):
    """Save a high score to the database."""
    if not name or not name.strip():
        name = "Anonymous"
    conn = sqlite3.connect(HIGH_SCORES_DB)
    conn.execute("""
        INSERT INTO high_scores (player_name, score, waves_survived, time_survived, enemies_killed, difficulty, date_achieved)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name.strip()[:20], score, waves, time_survived, enemies_killed, difficulty, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()


def is_high_score(score: int) -> bool:
    """Check if a score qualifies for the high score board (top 10)."""
    scores = get_high_scores(10)
    if len(scores) < 10:
        return True
    return score > scores[-1]["score"]


def generate_wave_beam_points(start_pos: pygame.Vector2, direction: pygame.Vector2, pattern: str, length: int, amplitude: float = 50.0, frequency: float = 0.02, time_offset: float = 0.0) -> list[pygame.Vector2]:
    """Generate points along a wave pattern beam.
    
    Args:
        start_pos: Starting position of the beam
        direction: Normalized direction vector
        pattern: Wave pattern type ("sine", "cosine", "tangent", etc.)
        length: Length of the beam in pixels
        amplitude: Amplitude of the wave (pixels)
        frequency: Frequency of the wave (cycles per pixel)
        time_offset: Time-based phase offset for undulation (in seconds)
    
    Returns:
        List of points along the wave path
    """
    points = []
    perp = pygame.Vector2(-direction.y, direction.x)  # Perpendicular vector for wave offset
    
    num_points = max(200, length // 5)  # Generate more points for smoother solid line
    step = length / num_points
    
    # Undulation: 0.5 second period = 4 * pi radians per second
    undulation_phase = time_offset * 4 * math.pi  # Phase offset for 0.5 second period
    
    for i in range(num_points + 1):
        t = i * step
        x = start_pos.x + direction.x * t
        y = start_pos.y + direction.y * t
        
        # Calculate wave offset based on pattern with time-based undulation
        wave_value = 0.0
        angle = t * frequency * 2 * math.pi + undulation_phase
        
        if pattern == "sine":
            wave_value = math.sin(angle)
        elif pattern == "cosine":
            wave_value = math.cos(angle)
        elif pattern == "tangent":
            # Clamp to prevent infinite values
            wave_value = math.tan(angle)
            wave_value = max(-10.0, min(10.0, wave_value))
        elif pattern == "cotangent":
            # Clamp to prevent infinite values
            if abs(math.sin(angle)) > 0.01:
                wave_value = math.cos(angle) / math.sin(angle)
                wave_value = max(-10.0, min(10.0, wave_value))
            else:
                wave_value = 0.0
        elif pattern == "secant":
            # Clamp to prevent infinite values
            if abs(math.cos(angle)) > 0.01:
                wave_value = 1.0 / math.cos(angle)
                wave_value = max(-10.0, min(10.0, wave_value))
            else:
                wave_value = 0.0
        elif pattern == "cosecant":
            # Clamp to prevent infinite values
            if abs(math.sin(angle)) > 0.01:
                wave_value = 1.0 / math.sin(angle)
                wave_value = max(-10.0, min(10.0, wave_value))
            else:
                wave_value = 0.0
        
        # Apply wave offset perpendicular to direction
        offset = perp * (wave_value * amplitude)
        point = pygame.Vector2(x, y) + offset
        points.append(point)
    
    return points


def check_wave_beam_collision(points: list[pygame.Vector2], rect: pygame.Rect, width: int) -> tuple[pygame.Vector2 | None, float]:
    """Check if a wave beam (represented by points) collides with a rectangle.
    
    Returns:
        Tuple of (closest_hit_point, distance) or (None, infinity) if no collision
    """
    closest_hit = None
    closest_dist = float('inf')
    
    # Check each segment of the beam
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        
        # Check if this segment intersects the rect
        hit = line_rect_intersection(p1, p2, rect)
        if hit:
            dist = (hit - points[0]).length()
            if dist < closest_dist:
                closest_dist = dist
                closest_hit = hit
    
    # Also check if any point is inside the rect (for thick beams)
    for point in points:
        if rect.collidepoint(point.x, point.y):
            dist = (point - points[0]).length()
            if dist < closest_dist:
                closest_dist = dist
                closest_hit = point
    
    return (closest_hit, closest_dist)


def generate_paraboloid_points(center: pygame.Vector2, width: float, height: float, rotation: float) -> list[pygame.Vector2]:
    """Generate points for a paraboloid shape (parabolic curve in 2D).
    
    Args:
        center: Center position of the paraboloid
        width: Width of the paraboloid
        height: Height of the paraboloid
        rotation: Rotation angle in radians
    
    Returns:
        List of points forming the paraboloid shape
    """
    points = []
    num_points = 100  # Number of points for smooth curve
    
    # Generate points for a parabolic curve
    for i in range(num_points + 1):
        # Parameter t from -1 to 1
        t = (i / num_points) * 2.0 - 1.0
        
        # Parabolic curve: y = a * x^2
        # We'll create a U-shaped parabola
        x_local = t * (width / 2)
        y_local = (t ** 2) * (height / 2)  # Parabolic curve
        
        # Rotate the point around center
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)
        x_rotated = x_local * cos_r - y_local * sin_r
        y_rotated = x_local * sin_r + y_local * cos_r
        
        # Translate to center position
        point = pygame.Vector2(
            center.x + x_rotated,
            center.y + y_rotated
        )
        points.append(point)
    
    return points


def generate_trapezoid_points(center: pygame.Vector2, width: float, height: float, rotation: float) -> list[pygame.Vector2]:
    """Generate points for a trapezoid shape.
    
    Args:
        center: Center position of the trapezoid
        width: Width of the trapezoid (top and bottom)
        height: Height of the trapezoid
        rotation: Rotation angle in radians
    
    Returns:
        List of points forming the trapezoid shape
    """
    points = []
    # Create a trapezoid (wider at bottom)
    top_width = width * 0.6
    bottom_width = width
    
    # Local coordinates
    local_points = [
        (-top_width / 2, -height / 2),  # Top left
        (top_width / 2, -height / 2),   # Top right
        (bottom_width / 2, height / 2),  # Bottom right
        (-bottom_width / 2, height / 2),  # Bottom left
    ]
    
    # Rotate and translate
    cos_r = math.cos(rotation)
    sin_r = math.sin(rotation)
    for x_local, y_local in local_points:
        x_rotated = x_local * cos_r - y_local * sin_r
        y_rotated = x_local * sin_r + y_local * cos_r
        point = pygame.Vector2(center.x + x_rotated, center.y + y_rotated)
        points.append(point)
    
    return points


def check_point_in_hazard(point: pygame.Vector2, hazard_points: list[pygame.Vector2], bounding_rect: pygame.Rect) -> bool:
    """Check if a point is inside the hazard shape (paraboloid or trapezoid).
    
    Uses point-in-polygon algorithm.
    """
    if not bounding_rect.collidepoint(point.x, point.y):
        return False
    
    # Use ray casting algorithm for point-in-polygon
    x, y = point.x, point.y
    n = len(hazard_points)
    if n < 3:
        return False
    
    inside = False
    p1x, p1y = hazard_points[0].x, hazard_points[0].y
    for i in range(1, n + 1):
        p2x, p2y = hazard_points[i % n].x, hazard_points[i % n].y
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def check_hazard_collision(hazard1: dict, hazard2: dict) -> bool:
    """Check if two hazards are colliding based on their bounding rectangles."""
    return hazard1["bounding_rect"].colliderect(hazard2["bounding_rect"])


def resolve_hazard_collision(hazard1: dict, hazard2: dict):
    """Resolve collision between two hazards - make them bounce off each other."""
    # Calculate collision normal (direction from hazard1 to hazard2)
    center1 = hazard1["center"]
    center2 = hazard2["center"]
    normal = (center2 - center1)
    if normal.length_squared() > 0:
        normal = normal.normalize()
    else:
        # If centers overlap, use random direction
        normal = pygame.Vector2(1, 0)
    
    # Calculate relative velocity
    rel_vel = hazard2["velocity"] - hazard1["velocity"]
    
    # Calculate relative velocity along collision normal
    vel_along_normal = rel_vel.dot(normal)
    
    # Don't resolve if velocities are separating
    if vel_along_normal > 0:
        return
    
    # Calculate bounce (elastic collision)
    # For simplicity, we'll use a simple bounce with some energy loss
    restitution = 0.8  # Energy retention (0.8 = 80% energy retained)
    
    # Calculate impulse
    impulse = vel_along_normal * restitution
    
    # Apply impulse to velocities
    hazard1["velocity"] += normal * impulse
    hazard2["velocity"] -= normal * impulse
    
    # Separate the hazards slightly to prevent sticking
    separation = 10.0
    hazard1["center"] -= normal * separation
    hazard2["center"] += normal * separation


def update_hazard_obstacles(dt: float):
    """Update all rotating hazard obstacles (paraboloids/trapezoids) with collision physics."""
    global hazard_obstacles, current_level
    
    # Update each hazard
    for hazard in hazard_obstacles:
        # Determine shape based on level
        if current_level >= 2:
            hazard["shape"] = "trapezoid"
        else:
            hazard["shape"] = "paraboloid"
        # Update rotation
        hazard["rotation_angle"] += hazard["rotation_speed"] * dt
        if hazard["rotation_angle"] >= 2 * math.pi:
            hazard["rotation_angle"] -= 2 * math.pi
        
        # Update orbit position
        hazard["orbit_angle"] += hazard["orbit_speed"] * dt
        if hazard["orbit_angle"] >= 2 * math.pi:
            hazard["orbit_angle"] -= 2 * math.pi
        
        # Calculate orbit position
        orbit_pos = pygame.Vector2(
            hazard["orbit_center"].x + math.cos(hazard["orbit_angle"]) * hazard["orbit_radius"],
            hazard["orbit_center"].y + math.sin(hazard["orbit_angle"]) * hazard["orbit_radius"]
        )
        
        # Apply velocity for collision physics
        hazard["center"] += hazard["velocity"] * dt
        
        # Blend orbit position with velocity-based movement (50/50)
        hazard["center"] = hazard["center"] * 0.5 + orbit_pos * 0.5
        
        # Keep within screen bounds with bounce
        if hazard["center"].x < hazard["width"] // 2:
            hazard["center"].x = hazard["width"] // 2
            hazard["velocity"].x = abs(hazard["velocity"].x)  # Bounce right
        elif hazard["center"].x > WIDTH - hazard["width"] // 2:
            hazard["center"].x = WIDTH - hazard["width"] // 2
            hazard["velocity"].x = -abs(hazard["velocity"].x)  # Bounce left
        
        if hazard["center"].y < hazard["height"] // 2:
            hazard["center"].y = hazard["height"] // 2
            hazard["velocity"].y = abs(hazard["velocity"].y)  # Bounce up
        elif hazard["center"].y > HEIGHT - hazard["height"] // 2:
            hazard["center"].y = HEIGHT - hazard["height"] // 2
            hazard["velocity"].y = -abs(hazard["velocity"].y)  # Bounce down
        
        # Regenerate points with new rotation and position based on shape
        if hazard["shape"] == "trapezoid":
            hazard["points"] = generate_trapezoid_points(
                hazard["center"],
                hazard["width"],
                hazard["height"],
                hazard["rotation_angle"]
            )
        else:
            hazard["points"] = generate_paraboloid_points(
                hazard["center"],
                hazard["width"],
                hazard["height"],
                hazard["rotation_angle"]
            )
        
        # Update bounding rect
        if hazard["points"]:
            min_x = min(p.x for p in hazard["points"])
            max_x = max(p.x for p in hazard["points"])
            min_y = min(p.y for p in hazard["points"])
            max_y = max(p.y for p in hazard["points"])
            hazard["bounding_rect"] = pygame.Rect(
                min_x, min_y,
                max_x - min_x,
                max_y - min_y
            )
    
    # Check collisions between hazards
    for i in range(len(hazard_obstacles)):
        for j in range(i + 1, len(hazard_obstacles)):
            if check_hazard_collision(hazard_obstacles[i], hazard_obstacles[j]):
                resolve_hazard_collision(hazard_obstacles[i], hazard_obstacles[j])


def spawn_pickup(pickup_type: str):
    # Make pickups bigger
    size = (32, 32)
    max_attempts = 50  # Increased attempts to avoid overlaps
    for _ in range(max_attempts):
        r = random_spawn_position(size)
        # Check if pickup overlaps with existing pickups
        overlaps = False
        for existing_pickup in pickups:
            if r.colliderect(existing_pickup["rect"]):
                overlaps = True
                break
        # Check if pickup overlaps with health zone
        if r.colliderect(moving_health_zone["rect"]):
            overlaps = True
        
        if not overlaps:
            # All pickups look the same (mystery) - randomized color so player doesn't know what they're getting
            mystery_colors = [
                (180, 100, 255),  # purple
                (100, 255, 180),  # green
                (255, 180, 100),  # orange
                (180, 255, 255),  # cyan
                (255, 100, 180),  # pink
                (255, 255, 100),  # yellow
            ]
            color = random.choice(mystery_colors)
            pickups.append({
                "type": pickup_type,
                "rect": r,
                "color": color,
                "timer": 15.0,  # pickup despawns after 15 seconds
                "age": 0.0,  # current age for visual effects
            })
            return  # Successfully spawned, exit function
    # If we couldn't find a non-overlapping position, skip spawning this pickup


def spawn_weapon_in_center(weapon_type: str):
    """Spawn a weapon pickup in the center of the screen (level completion reward)."""
    # Do not spawn basic beam as a pickup
    if weapon_type == "basic":
        return
    weapon_colors_map = {
        "rocket": (255, 100, 0),
        "triple": (100, 200, 255),
        "bouncing": (100, 255, 100),
        "giant": (255, 200, 0),
        "laser": (255, 50, 50),
        "wave_beam": (50, 255, 50),
    }
    weapon_pickup_size = (40, 40)  # Bigger for level completion rewards
    weapon_pickup_rect = pygame.Rect(
        WIDTH // 2 - weapon_pickup_size[0] // 2,
        HEIGHT // 2 - weapon_pickup_size[1] // 2,
        weapon_pickup_size[0],
        weapon_pickup_size[1]
    )
    pickups.append({
        "type": weapon_type,
        "rect": weapon_pickup_rect,
        "color": weapon_colors_map.get(weapon_type, (180, 100, 255)),
        "timer": 30.0,  # Level completion weapons last longer
        "age": 0.0,
        "is_weapon_drop": True,
        "is_level_reward": True,  # Mark as level completion reward
    })


def spawn_weapon_drop(enemy: dict):
    """Spawn a weapon drop from a killed enemy."""
    enemy_type = enemy.get("type", "grunt")
    weapon_drop_map = {
        "grunt": "basic",
        "stinky": "basic",
        "heavy": "rocket",
        "baka": "triple",
        "neko neko desu": "bouncing",
        "BIG NEKU": "wave_beam",  # Wave beam second to last
        "bouncer": "bouncing",
    }
    # 30% chance to drop weapon (exclude basic beam)
    if random.random() < 0.3 and enemy_type in weapon_drop_map:
        weapon_type = weapon_drop_map[enemy_type]
        # Skip basic beam - do not drop it as a pickup
        if weapon_type == "basic":
            return
        # Spawn weapon pickup at enemy location
        weapon_pickup_size = (28, 28)
        weapon_pickup_rect = pygame.Rect(
            enemy["rect"].centerx - weapon_pickup_size[0] // 2,
            enemy["rect"].centery - weapon_pickup_size[1] // 2,
            weapon_pickup_size[0],
            weapon_pickup_size[1]
        )
        weapon_colors_map = {
            "basic": (200, 200, 200),
            "rocket": (255, 100, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "giant": (255, 200, 0),
            "laser": (255, 50, 50),
        }
        pickups.append({
            "type": weapon_type,
            "rect": weapon_pickup_rect,
            "color": weapon_colors_map.get(weapon_type, (180, 100, 255)),
            "timer": 10.0,  # Weapon pickups last 10 seconds
            "age": 0.0,
            "is_weapon_drop": True,  # Mark as weapon drop
        })


def _create_cached_silver_wall_texture(width: int, height: int) -> pygame.Surface:
    """Create a cached silver wall texture surface."""
    surf = pygame.Surface((width, height))
    silver_base = (192, 192, 192)
    silver_dark = (160, 160, 160)
    silver_light = (220, 220, 220)
    
    # Fill base
    surf.fill(silver_base)
    
    # Draw metallic grid pattern
    brick_width = max(8, width // 4)
    brick_height = max(6, height // 3)
    
    # Horizontal mortar lines
    for y in range(brick_height, height, brick_height):
        pygame.draw.line(surf, silver_dark, (0, y), (width, y), 1)
    
    # Vertical mortar lines (staggered)
    offset = 0
    for y in range(0, height, brick_height * 2):
        for x in range(offset, width, brick_width):
            pygame.draw.line(surf, silver_dark, (x, y), (x, min(y + brick_height, height)), 1)
        offset = brick_width // 2 if offset == 0 else 0
    
    # Add highlights for metallic shine
    for i in range(0, width, brick_width):
        for j in range(0, height, brick_height):
            highlight_x = i + brick_width // 4
            highlight_y = j + brick_height // 4
            if highlight_x < width and highlight_y < height:
                pygame.draw.circle(surf, silver_light, (highlight_x, highlight_y), 2)
    
    return surf


def draw_silver_wall_texture(screen, rect: pygame.Rect):
    """Draw a silver wall texture for indestructible blocks (uses cached surface when possible)."""
    global _wall_texture_cache
    # Use cache for common sizes (round to nearest 10 for better cache hit rate)
    cache_key = (rect.w // 10 * 10, rect.h // 10 * 10)
    
    if cache_key not in _wall_texture_cache:
        _wall_texture_cache[cache_key] = _create_cached_silver_wall_texture(cache_key[0], cache_key[1])
    
    cached_surf = _wall_texture_cache[cache_key]
    # Blit cached surface, scaling if needed
    if cache_key[0] == rect.w and cache_key[1] == rect.h:
        screen.blit(cached_surf, rect.topleft)
    else:
        # Scale if size doesn't match exactly
        scaled = pygame.transform.scale(cached_surf, (rect.w, rect.h))
        screen.blit(scaled, rect.topleft)


def _create_cached_cracked_brick_texture(width: int, height: int, crack_level: int) -> pygame.Surface:
    """Create a cached cracked brick wall texture surface."""
    surf = pygame.Surface((width, height))
    brick_red = (180, 80, 60)
    brick_dark = (140, 60, 40)
    brick_light = (200, 100, 80)
    mortar = (100, 100, 100)
    
    # Fill base brick color
    surf.fill(brick_red)
    
    # Draw brick pattern
    brick_width = max(10, width // 4)
    brick_height = max(8, height // 3)
    
    # Horizontal mortar lines
    for y in range(brick_height, height, brick_height):
        pygame.draw.line(surf, mortar, (0, y), (width, y), 2)
    
    # Vertical mortar lines (staggered brick pattern)
    offset = 0
    for y in range(0, height, brick_height * 2):
        for x in range(offset, width, brick_width):
            pygame.draw.line(surf, mortar, (x, y), (x, min(y + brick_height, height)), 2)
        offset = brick_width // 2 if offset == 0 else 0
    
    # Add individual brick highlights
    offset = 0
    for y in range(0, height, brick_height):
        for x in range(offset, width, brick_width):
            brick_rect = pygame.Rect(x + 1, y + 1, min(brick_width - 2, width - x - 1), min(brick_height - 2, height - y - 1))
            if brick_rect.w > 0 and brick_rect.h > 0:
                # Light highlight on top-left of each brick
                pygame.draw.line(surf, brick_light, (brick_rect.left, brick_rect.top), (brick_rect.right, brick_rect.top), 1)
                pygame.draw.line(surf, brick_light, (brick_rect.left, brick_rect.top), (brick_rect.left, brick_rect.bottom), 1)
                # Dark shadow on bottom-right
                pygame.draw.line(surf, brick_dark, (brick_rect.right, brick_rect.top), (brick_rect.right, brick_rect.bottom), 1)
                pygame.draw.line(surf, brick_dark, (brick_rect.left, brick_rect.bottom), (brick_rect.right, brick_rect.bottom), 1)
        offset = brick_width // 2 if offset == 0 else 0
    
    # Draw cracks based on damage level
    if crack_level >= 1:
        center = (width // 2, height // 2)
        crack_color = (40, 40, 40)
        # Main crack from center
        for i in range(crack_level):
            angle = (i * 2.4) * math.pi / 3
            end_x = center[0] + math.cos(angle) * (width // 2)
            end_y = center[1] + math.sin(angle) * (height // 2)
            pygame.draw.line(surf, crack_color, center, (end_x, end_y), 2)
        
        # Additional smaller cracks for higher damage
        if crack_level >= 2:
            for i in range(crack_level):
                angle = (i * 1.8 + 0.5) * math.pi / 3
                start_x = center[0] + math.cos(angle) * (width // 4)
                start_y = center[1] + math.sin(angle) * (height // 4)
                end_x = start_x + math.cos(angle) * (width // 3)
                end_y = start_y + math.sin(angle) * (height // 3)
                pygame.draw.line(surf, crack_color, (start_x, start_y), (end_x, end_y), 1)
    
    return surf


def draw_cracked_brick_wall_texture(screen, rect: pygame.Rect, crack_level: int = 1):
    """Draw a cracked brick wall texture for destructible blocks (uses cached surface when possible)."""
    global _wall_texture_cache
    # Use cache for common sizes (round to nearest 10 for better cache hit rate)
    cache_key = (rect.w // 10 * 10, rect.h // 10 * 10, crack_level)
    
    if cache_key not in _wall_texture_cache:
        _wall_texture_cache[cache_key] = _create_cached_cracked_brick_texture(cache_key[0], cache_key[1], crack_level)
    
    cached_surf = _wall_texture_cache[cache_key]
    # Blit cached surface, scaling if needed
    if cache_key[0] == rect.w and cache_key[1] == rect.h:
        screen.blit(cached_surf, rect.topleft)
    else:
        # Scale if size doesn't match exactly
        scaled = pygame.transform.scale(cached_surf, (rect.w, rect.h))
        screen.blit(scaled, rect.topleft)


def draw_health_bar(x, y, w, h, hp, max_hp):
    """Draw health bar (uses cached surface for common sizes/ratios when possible)."""
    global _health_bar_cache
    hp = max(0, min(hp, max_hp))
    hp_ratio = hp / max_hp if max_hp > 0 else 0.0
    
    # Cache for common health bar sizes (round to nearest 5 for better cache hits)
    # Only cache if bar is reasonably sized (not too many variations)
    # Only use cache if the rounded ratio matches the actual ratio (to avoid visual inaccuracies)
    if w <= 200 and h <= 20:
        rounded_ratio = int(hp_ratio * 10)  # Round to 10% increments
        actual_fill = int(w * hp_ratio)
        cached_fill = int(w * (rounded_ratio / 10.0))
        
        # Only use cache if rounded ratio produces the same visual result
        if actual_fill == cached_fill:
            cache_key = (w // 5 * 5, h, rounded_ratio)
            if cache_key not in _health_bar_cache:
                cached_w, cached_h, cached_ratio = cache_key
                cached_surf = pygame.Surface((cached_w, cached_h))
                cached_surf.fill((60, 60, 60))
                fill_w = int(cached_w * (cached_ratio / 10.0))
                if fill_w > 0:
                    pygame.draw.rect(cached_surf, (60, 200, 60), (0, 0, fill_w, cached_h))
                pygame.draw.rect(cached_surf, (20, 20, 20), (0, 0, cached_w, cached_h), 2)
                _health_bar_cache[cache_key] = cached_surf
            
            # Use cached surface if size matches exactly
            if cache_key[0] == w and cache_key[1] == h:
                screen.blit(_health_bar_cache[cache_key], (x, y))
                return
    
    # Fallback to direct drawing for non-cached sizes or when ratio doesn't match
    pygame.draw.rect(screen, (60, 60, 60), (x, y, w, h))
    fill_w = int(w * hp_ratio)
    if fill_w > 0:
        pygame.draw.rect(screen, (60, 200, 60), (x, y, fill_w, h))
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), 2)


def create_pickup_collection_effect(x: int, y: int, color: tuple[int, int, int]):
    """Create particle effect when pickup is collected."""
    global collection_effects
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 150)
        collection_effects.append({
            "x": float(x),
            "y": float(y),
            "vel_x": math.cos(angle) * speed,
            "vel_y": math.sin(angle) * speed,
            "color": color,
            "life": 0.4,  # particle lifetime
            "size": random.randint(3, 6),
        })


def update_pickup_effects(dt: float):
    """Update pickup particle effects."""
    global pickup_particles, collection_effects
    
    # Update collection effects
    for effect in collection_effects[:]:
        effect["x"] += effect["vel_x"] * dt
        effect["y"] += effect["vel_y"] * dt
        effect["life"] -= dt
        if effect["life"] <= 0:
            collection_effects.remove(effect)
    
    # Generate particles around pickups
    pickup_particles.clear()
    for p in pickups:
        center_x = p["rect"].centerx
        center_y = p["rect"].centery
        age = p.get("age", 0.0)
        # Create pulsing glow effect
        pulse = (math.sin(age * 4.0) + 1.0) / 2.0  # 0 to 1
        glow_radius = 20 + pulse * 10
        glow_alpha = int(100 + pulse * 80)
        
        # Add particles around pickup
        for i in range(8):
            angle = (i / 8.0) * 2 * math.pi + age * 2.0
            dist = glow_radius * 0.7
            px = center_x + math.cos(angle) * dist
            py = center_y + math.sin(angle) * dist
            pickup_particles.append({
                "x": px,
                "y": py,
                "color": p["color"],
                "alpha": int(glow_alpha * 0.6),
                "size": 3,
            })


def draw_centered_text(text: str, y: int, color=(235, 235, 235), use_big=False):
    f = big_font if use_big else font
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)


def draw_projectile(rect: pygame.Rect, color: tuple[int, int, int], shape: str):
    if shape == "circle":
        pygame.draw.circle(screen, color, rect.center, rect.w // 2)
    elif shape == "diamond":
        cx, cy = rect.center
        hw, hh = rect.w // 2, rect.h // 2
        points = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
        pygame.draw.polygon(screen, color, points)
    else:
        pygame.draw.rect(screen, color, rect)


def spawn_player_bullet_and_log():
    global shots_fired, player_bullet_shape_index

    # Determine aiming direction based on aiming mode
    if aiming_mode == AIM_ARROWS:
        # Arrow key aiming
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        
        if dx == 0 and dy == 0:
            # No arrow keys pressed, use last movement direction or default
            if last_move_velocity.length_squared() > 0:
                base_dir = last_move_velocity.normalize()
            else:
                base_dir = pygame.Vector2(1, 0)  # Default right
        else:
            base_dir = pygame.Vector2(dx, dy).normalize()
        
        # Calculate target position for telemetry (extend direction from player)
        target_dist = 100  # Distance to calculate target point
        mx = int(player.centerx + base_dir.x * target_dist)
        my = int(player.centery + base_dir.y * target_dist)
    else:
        # Mouse aiming (default)
        mx, my = pygame.mouse.get_pos()
        base_dir = vec_toward(player.centerx, player.centery, mx, my)

    shape = player_bullet_shapes[player_bullet_shape_index % len(player_bullet_shapes)]
    player_bullet_shape_index = (player_bullet_shape_index + 1) % len(player_bullet_shapes)

    # Determine shot pattern based on weapon mode
    if current_weapon_mode == "triple":
        # Triple shot: three basic beams offset by equal arc (120 degrees total, 60 degrees each side)
        spread_angle_deg = 30.0  # 30 degrees each side = 60 degree total arc
        directions = [
            base_dir,  # center
            base_dir.rotate(-spread_angle_deg),  # left
            base_dir.rotate(spread_angle_deg),  # right
        ]
    elif current_weapon_mode == "basic":
        # Basic beam: three beams offset by equal arc (same as triple shot pattern)
        spread_angle_deg = 30.0  # 30 degrees each side = 60 degree total arc
        directions = [
            base_dir,  # center
            base_dir.rotate(-spread_angle_deg),  # left
            base_dir.rotate(spread_angle_deg),  # right
        ]
    else:
        directions = [base_dir]

    # Spawn bullets for each direction
    for d in directions:
        # Apply stat multipliers
        size_mult = player_stat_multipliers["bullet_size"]
        if current_weapon_mode == "giant":
            size_mult *= 10.0  # 10x size multiplier
        elif current_weapon_mode == "rocket":
            size_mult *= 2.5  # Rockets are bigger (2.5x size)
        elif current_weapon_mode == "bouncing":
            size_mult *= 2.0  # Bouncing bullets are twice the size
        
        # Triple shot: 3x size multiplier
        if current_weapon_mode == "triple":
            size_mult *= 3.0
        
        effective_size = (
            int(player_bullet_size[0] * size_mult),
            int(player_bullet_size[1] * size_mult),
        )
        effective_speed = player_bullet_speed * player_stat_multipliers["bullet_speed"]
        base_damage = int(player_bullet_damage * player_stat_multipliers["bullet_damage"])
        
        # Rocket launcher: more damage and always has explosion
        if current_weapon_mode == "rocket":
            effective_damage = int(base_damage * 2.5)  # 2.5x damage
            rocket_explosion = max(120.0, player_stat_multipliers["bullet_explosion_radius"] + 100.0)  # Increased AOE
        else:
            effective_damage = base_damage
            rocket_explosion = 0.0

    r = pygame.Rect(
        player.centerx - effective_size[0] // 2,
        player.centery - effective_size[1] // 2,
        effective_size[0],
        effective_size[1],
    )
    player_bullets.append({
            "rect": r,
            "vel": d * effective_speed,
            "shape": shape,
            "color": (200, 100, 255) if current_weapon_mode == "triple" else (255, 100, 0) if current_weapon_mode == "rocket" else (255, 165, 0) if current_weapon_mode == "bouncing" else player_bullets_color,  # purple for triple, orange for rockets, orange for bouncing bullets
            "damage": effective_damage,
            "penetration": int(player_stat_multipliers["bullet_penetration"]),
            "explosion_radius": max(rocket_explosion, player_stat_multipliers["bullet_explosion_radius"]),
            "knockback": player_stat_multipliers["bullet_knockback"],
            "bounces": 10 if current_weapon_mode == "bouncing" else 0,  # max bounces
            "is_rocket": current_weapon_mode == "rocket",
        })
    shots_fired += 1

    telemetry.log_shot(
        ShotEvent(
            t=run_time,
            origin_x=player.centerx,
            origin_y=player.centery,
            target_x=mx,
            target_y=my,
            dir_x=float(d.x),
            dir_y=float(d.y),
        )
    )
    
    # Log bullet metadata
    telemetry.log_bullet_metadata(
        BulletMetadataEvent(
            t=run_time,
            bullet_type="player",
            shape=shape,
            color_r=player_bullets_color[0],
            color_g=player_bullets_color[1],
            color_b=player_bullets_color[2],
        )
    )


def spawn_enemy_projectile(enemy: dict):
    """Spawn projectile from enemy targeting nearest threat (player or friendly AI)."""
    e_pos = pygame.Vector2(enemy["rect"].center)
    threat_result = find_nearest_threat(e_pos)
    
    # Calculate direction
    if threat_result:
        threat_pos, threat_type = threat_result
        d = vec_toward(e_pos.x, e_pos.y, threat_pos.x, threat_pos.y)
    else:
        # Fallback to player if no threats
        d = vec_toward(enemy["rect"].centerx, enemy["rect"].centery, player.centerx, player.centery)
    
    # Create projectile rect and properties (used regardless of threat result)
    r = pygame.Rect(
        enemy["rect"].centerx - enemy_projectile_size[0] // 2,
        enemy["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    proj_color = enemy.get("projectile_color", enemy_projectiles_color)
    proj_shape = enemy.get("projectile_shape", "circle")
    bounces = enemy.get("bouncing_projectiles", False)
    
    enemy_projectiles.append({
        "rect": r,
        "vel": d * enemy["projectile_speed"],
        "enemy_type": enemy["type"],  # attribute damage source
        "color": proj_color,
        "shape": proj_shape,
        "bounces": 10 if bounces else 0,  # max bounces for bouncing enemy type
    })
    
    # Log enemy projectile metadata
    if telemetry_enabled and telemetry:
        telemetry.log_bullet_metadata(
            BulletMetadataEvent(
                t=run_time,
                bullet_type="enemy",
                shape=proj_shape,
                color_r=proj_color[0],
                color_g=proj_color[1],
                color_b=proj_color[2],
                source_enemy_type=enemy["type"],
            )
        )


def spawn_enemy_projectile_predictive(enemy: dict, direction: pygame.Vector2):
    """Spawn projectile from predictive enemy in a specific direction (predicted player position)."""
    r = pygame.Rect(
        enemy["rect"].centerx - enemy_projectile_size[0] // 2,
        enemy["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    proj_color = enemy.get("projectile_color", enemy_projectiles_color)
    proj_shape = enemy.get("projectile_shape", "diamond")  # Rhomboid shape
    enemy_projectiles.append({
        "rect": r,
        "vel": direction * enemy["projectile_speed"],
        "enemy_type": enemy["type"],
        "color": proj_color,
        "shape": proj_shape,
        "bounces": 0,
    })


def spawn_boss_projectile(boss: dict, direction: pygame.Vector2):
    """Spawn a projectile from the boss in a specific direction."""
    r = pygame.Rect(
        boss["rect"].centerx - enemy_projectile_size[0] // 2,
        boss["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    proj_color = boss.get("projectile_color", enemy_projectiles_color)
    proj_shape = boss.get("projectile_shape", "circle")
    enemy_projectiles.append(
        {
            "rect": r,
            "vel": direction * boss["projectile_speed"],
            "enemy_type": boss["type"],
            "color": proj_color,
            "shape": proj_shape,
            "bounces": 0,
        }
    )


def log_enemy_spawns_for_current_wave():
    log_enemy_spawns(enemies)


def calculate_kill_score(wave_num: int, run_time: float) -> int:
    """Calculate score for killing an enemy."""
    return SCORE_BASE_POINTS + (wave_num * SCORE_WAVE_MULTIPLIER) + int(run_time * SCORE_TIME_MULTIPLIER)


# Enemy defeat messages
enemy_defeat_messages: list[dict] = []  # List of {enemy_type, timer} for defeat messages

def kill_enemy(enemy: dict):
    """Handle enemy death: drop weapon, update score, remove from list."""
    global enemies_killed, score, current_level, enemy_defeat_messages
    is_boss = enemy.get("is_boss", False)
    
    # Add defeat message
    enemy_type = enemy.get("type", "enemy")
    enemy_defeat_messages.append({
        "enemy_type": enemy_type,
        "timer": 3.0,  # Display for 3 seconds
    })
    
    # If boss is killed, spawn level completion weapon in center
    if is_boss:
        # Weapons unlock in order: basic (start), rocket (level 1), triple (level 2), wave_beam (level 3), giant (level 4)
        weapon_unlock_order = {1: "rocket", 2: "triple", 3: "wave_beam", 4: "giant"}
        if current_level in weapon_unlock_order:
            weapon_to_unlock = weapon_unlock_order[current_level]
            if weapon_to_unlock not in unlocked_weapons:
                spawn_weapon_in_center(weapon_to_unlock)
    else:
        # Regular enemies drop weapons randomly
        spawn_weapon_drop(enemy)
    
    try:
        enemies.remove(enemy)
    except ValueError:
        pass  # Already removed
    enemies_killed += 1
    score += calculate_kill_score(wave_number, run_time)


def apply_pickup_effect(pickup_type: str):
    """Apply the effect of a collected pickup."""
    global boost_meter, fire_rate_buff_t, player_max_hp, player_hp
    global player_stat_multipliers, current_weapon_mode, overshield, weapon_pickup_messages
    
    if pickup_type == "boost":
        boost_meter = min(boost_meter_max, boost_meter + 45.0)
    elif pickup_type == "firerate":
        fire_rate_buff_t = fire_rate_buff_duration
    elif pickup_type == "health":
        # Restore 100 HP (capped at max HP)
        player_hp = min(player_max_hp, player_hp + 100)
    elif pickup_type == "max_health":
        player_max_hp += 15
        player_hp += 15  # also heal by the same amount
    elif pickup_type == "speed":
        player_stat_multipliers["speed"] += 0.15
    elif pickup_type == "firerate_permanent":
        # Cap fire rate multiplier at 2.0 (2x firing speed max) to prevent performance issues
        player_stat_multipliers["firerate"] = min(2.0, player_stat_multipliers["firerate"] + 0.12)
    elif pickup_type == "bullet_size":
        player_stat_multipliers["bullet_size"] += 0.20
    elif pickup_type == "bullet_speed":
        player_stat_multipliers["bullet_speed"] += 0.15
    elif pickup_type == "bullet_damage":
        player_stat_multipliers["bullet_damage"] += 0.20
    elif pickup_type == "bullet_knockback":
        player_stat_multipliers["bullet_knockback"] += 0.25
    elif pickup_type == "bullet_penetration":
        player_stat_multipliers["bullet_penetration"] += 1
    elif pickup_type == "bullet_explosion":
        player_stat_multipliers["bullet_explosion_radius"] += 25.0
    elif pickup_type == "health_regen":
        # Increase player health regeneration rate
        global player_health_regen_rate
        player_health_regen_rate += 5.0  # Add 5 HP per second regeneration
    # Weapon pickups - unlock and switch to weapon
    elif pickup_type in ["giant_bullets", "giant"]:
        unlocked_weapons.add("giant")
        previous_weapon_mode = current_weapon_mode
        # Clear beams when switching away from beam weapons
        if previous_weapon_mode == "wave_beam":
            wave_beams.clear()
        if previous_weapon_mode == "laser":
            laser_beams.clear()
        current_weapon_mode = "giant"
        # Log weapon switch from pickup
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type in ["triple_shot", "triple"]:
        unlocked_weapons.add("triple")
        previous_weapon_mode = current_weapon_mode
        # Clear beams when switching away from beam weapons
        if previous_weapon_mode == "wave_beam":
            wave_beams.clear()
        if previous_weapon_mode == "laser":
            laser_beams.clear()
        current_weapon_mode = "triple"
        weapon_names = {
            "giant": "GIANT BULLETS",
            "triple": "TRIPLE SHOT",
            "bouncing": "BOUNCING BULLETS",
            "rocket": "ROCKET LAUNCHER",
            "laser": "LASER BEAM",
            "basic": "BASIC FIRE",
            "wave_beam": "WAVE BEAM"
        }
        weapon_colors = {
            "giant": (255, 200, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "rocket": (255, 100, 0),
            "laser": (255, 50, 50),
            "basic": (200, 200, 200),
            "wave_beam": (50, 255, 50)
        }
        weapon_pickup_messages.append({
            "weapon_name": weapon_names.get("triple", "TRIPLE SHOT"),
            "timer": 3.0,
            "color": weapon_colors.get("triple", (255, 255, 255))
        })
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type in ["bouncing_bullets", "bouncing"]:
        unlocked_weapons.add("bouncing")
        previous_weapon_mode = current_weapon_mode
        # Clear beams when switching away from beam weapons
        if previous_weapon_mode == "wave_beam":
            wave_beams.clear()
        if previous_weapon_mode == "laser":
            laser_beams.clear()
        current_weapon_mode = "bouncing"
        weapon_names = {
            "giant": "GIANT BULLETS",
            "triple": "TRIPLE SHOT",
            "bouncing": "BOUNCING BULLETS",
            "rocket": "ROCKET LAUNCHER",
            "laser": "LASER BEAM",
            "basic": "BASIC FIRE",
            "wave_beam": "WAVE BEAM"
        }
        weapon_colors = {
            "giant": (255, 200, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "rocket": (255, 100, 0),
            "laser": (255, 50, 50),
            "basic": (200, 200, 200),
            "wave_beam": (50, 255, 50)
        }
        weapon_pickup_messages.append({
            "weapon_name": weapon_names.get("bouncing", "BOUNCING BULLETS"),
            "timer": 3.0,
            "color": weapon_colors.get("bouncing", (255, 255, 255))
        })
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type in ["rocket_launcher", "rocket"]:
        unlocked_weapons.add("rocket")
        previous_weapon_mode = current_weapon_mode
        # Clear beams when switching away from beam weapons
        if previous_weapon_mode == "wave_beam":
            wave_beams.clear()
        if previous_weapon_mode == "laser":
            laser_beams.clear()
        current_weapon_mode = "rocket"
        weapon_names = {
            "giant": "GIANT BULLETS",
            "triple": "TRIPLE SHOT",
            "bouncing": "BOUNCING BULLETS",
            "rocket": "ROCKET LAUNCHER",
            "laser": "LASER BEAM",
            "basic": "BASIC FIRE",
            "wave_beam": "WAVE BEAM"
        }
        weapon_colors = {
            "giant": (255, 200, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "rocket": (255, 100, 0),
            "laser": (255, 50, 50),
            "basic": (200, 200, 200),
            "wave_beam": (50, 255, 50)
        }
        weapon_pickup_messages.append({
            "weapon_name": weapon_names.get("rocket", "ROCKET LAUNCHER"),
            "timer": 3.0,
            "color": weapon_colors.get("rocket", (255, 255, 255))
        })
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type == "laser":
        unlocked_weapons.add("laser")
        previous_weapon_mode = current_weapon_mode
        # Clear beams when switching away from beam weapons
        if previous_weapon_mode == "wave_beam":
            wave_beams.clear()
        current_weapon_mode = "laser"
        weapon_names = {
            "giant": "GIANT BULLETS",
            "triple": "TRIPLE SHOT",
            "bouncing": "BOUNCING BULLETS",
            "rocket": "ROCKET LAUNCHER",
            "laser": "LASER BEAM",
            "basic": "BASIC FIRE",
            "wave_beam": "WAVE BEAM"
        }
        weapon_colors = {
            "giant": (255, 200, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "rocket": (255, 100, 0),
            "laser": (255, 50, 50),
            "basic": (200, 200, 200),
            "wave_beam": (50, 255, 50)
        }
        weapon_pickup_messages.append({
            "weapon_name": weapon_names.get("laser", "LASER BEAM"),
            "timer": 3.0,
            "color": weapon_colors.get("laser", (255, 255, 255))
        })
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type == "basic":
        unlocked_weapons.add("basic")  # Should already be unlocked, but ensure it
        previous_weapon_mode = current_weapon_mode
        # Clear beams when switching away from beam weapons
        if previous_weapon_mode == "wave_beam":
            wave_beams.clear()
        if previous_weapon_mode == "laser":
            laser_beams.clear()
        current_weapon_mode = "basic"
        weapon_names = {
            "giant": "GIANT BULLETS",
            "triple": "TRIPLE SHOT",
            "bouncing": "BOUNCING BULLETS",
            "rocket": "ROCKET LAUNCHER",
            "laser": "LASER BEAM",
            "basic": "BASIC FIRE",
            "wave_beam": "WAVE BEAM"
        }
        weapon_colors = {
            "giant": (255, 200, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "rocket": (255, 100, 0),
            "laser": (255, 50, 50),
            "basic": (200, 200, 200),
            "wave_beam": (50, 255, 50)
        }
        weapon_pickup_messages.append({
            "weapon_name": weapon_names.get("basic", "BASIC FIRE"),
            "timer": 3.0,
            "color": weapon_colors.get("basic", (255, 255, 255))
        })
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type == "wave_beam":
        unlocked_weapons.add("wave_beam")
        previous_weapon_mode = current_weapon_mode
        # Clear beams when switching away from beam weapons
        if previous_weapon_mode == "laser":
            laser_beams.clear()
        current_weapon_mode = "wave_beam"
        weapon_names = {
            "giant": "GIANT BULLETS",
            "triple": "TRIPLE SHOT",
            "bouncing": "BOUNCING BULLETS",
            "rocket": "ROCKET LAUNCHER",
            "laser": "LASER BEAM",
            "basic": "BASIC FIRE",
            "wave_beam": "WAVE BEAM"
        }
        weapon_colors = {
            "giant": (255, 200, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "rocket": (255, 100, 0),
            "laser": (255, 50, 50),
            "basic": (200, 200, 200),
            "wave_beam": (50, 255, 50)
        }
        weapon_pickup_messages.append({
            "weapon_name": weapon_names.get("wave_beam", "WAVE BEAM"),
            "timer": 3.0,
            "color": weapon_colors.get("wave_beam", (50, 255, 50))
        })
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type == "overshield":
        overshield = min(overshield_max, overshield + 25)


def render_hud_text(text: str, y: int, color=(230, 230, 230)) -> int:
    """Render HUD text at position and return next Y position (uses cached surface when possible)."""
    global _hud_text_cache
    cache_key = (text, color)
    if cache_key not in _hud_text_cache:
        _hud_text_cache[cache_key] = font.render(text, True, color)
    screen.blit(_hud_text_cache[cache_key], (10, y))
    return y + 24


def reset_after_death():
    global player_hp, player_time_since_shot, pos_timer, previous_weapon_mode, current_weapon_mode
    global previous_boost_state, previous_slow_state, player_current_zones
    global enemies, player_bullets, enemy_projectiles, wave_number, time_to_next_wave, wave_active
    global current_weapon_mode, overshield, unlocked_weapons, wave_in_level, current_level
    global jump_cooldown_timer, jump_timer, is_jumping, jump_velocity
    global laser_beams, laser_time_since_shot
    global shield_active, shield_duration_remaining, shield_cooldown_remaining
    global player_health_regen_rate, moving_health_zone, dropped_ally, ally_drop_timer

    player_hp = player_max_hp
    player_health_regen_rate = 0.0  # Reset health regeneration rate
    random_damage_multiplier = 1.0  # Reset random damage multiplier
    damage_numbers.clear()  # Clear damage numbers on death
    weapon_pickup_messages.clear()  # Clear weapon pickup messages on death
    grenade_explosions.clear()  # Clear grenade explosions on death
    grenade_time_since_used = 999.0  # Reset grenade cooldown
    missiles.clear()  # Clear missiles on death
    missile_time_since_used = 999.0  # Reset missile cooldown
    dropped_ally = None  # Clear dropped ally on death
    ally_drop_timer = 0.0  # Reset ally drop timer on death
    # Reset moving health zone to center
    moving_health_zone["rect"].center = (WIDTH // 4, HEIGHT // 4)  # Offset from center (boss spawn)
    moving_health_zone["target"] = None
    overshield = 0  # Reset overshield
    player_time_since_shot = 999.0
    laser_time_since_shot = 999.0
    pos_timer = 0.0
    wave_number = 1
    wave_in_level = 1
    current_level = 1
    unlocked_weapons = {"basic"}  # Reset to basic only
    current_weapon_mode = "basic"  # Reset to basic weapon
    previous_weapon_mode = "basic"
    previous_boost_state = False
    previous_slow_state = False
    player_current_zones = set()
    jump_cooldown_timer = 0.0
    jump_timer = 0.0
    is_jumping = False
    jump_velocity = pygame.Vector2(0, 0)
    laser_beams.clear()
    wave_beams.clear()
    # Reset hazard obstacles positions (corners)
    hazard_obstacles[0]["center"] = pygame.Vector2(250, 250)  # Top-left
    hazard_obstacles[0]["rotation_angle"] = 0.0
    hazard_obstacles[0]["orbit_angle"] = 0.0
    hazard_obstacles[0]["velocity"] = pygame.Vector2(150, 90)  # 3x faster
    hazard_obstacles[0]["points"] = []
    hazard_obstacles[1]["center"] = pygame.Vector2(WIDTH - 250, 250)  # Top-right
    hazard_obstacles[1]["rotation_angle"] = 1.0
    hazard_obstacles[1]["orbit_angle"] = 1.5
    hazard_obstacles[1]["velocity"] = pygame.Vector2(-120, 150)  # 3x faster
    hazard_obstacles[1]["points"] = []
    hazard_obstacles[2]["center"] = pygame.Vector2(250, HEIGHT - 250)  # Bottom-left
    hazard_obstacles[2]["rotation_angle"] = 2.0
    hazard_obstacles[2]["orbit_angle"] = 3.0
    hazard_obstacles[2]["velocity"] = pygame.Vector2(90, -135)  # 3x faster
    hazard_obstacles[2]["points"] = []
    hazard_obstacles[3]["center"] = pygame.Vector2(WIDTH - 250, HEIGHT - 250)  # Bottom-right
    hazard_obstacles[3]["rotation_angle"] = 1.5
    hazard_obstacles[3]["orbit_angle"] = 2.5
    hazard_obstacles[3]["velocity"] = pygame.Vector2(-105, -120)  # 3x faster
    hazard_obstacles[3]["points"] = []
    # Reset shield
    shield_active = False
    shield_duration_remaining = 0.0
    shield_cooldown_remaining = 0.0

    player.x = (WIDTH - player.w) // 2
    player.y = (HEIGHT - player.h) // 2
    clamp_rect_to_screen(player)

    player_bullets.clear()
    enemy_projectiles.clear()
    friendly_ai.clear()
    friendly_projectiles.clear()

    wave_number = 1
    time_to_next_wave = 0.0
    start_wave(wave_number)


if __name__ == "__main__":
    main()
