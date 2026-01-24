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

pygame.init()

# Welcome message when game launches
print("welcome to my game! :D")

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

# ----------------------------
# Controls (remappable)
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


controls = load_controls()

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
# Player
# ----------------------------
player = pygame.Rect((WIDTH - 28) // 2, (HEIGHT - 28) // 2, 28, 28)  # 10% larger (25 * 1.1 = 27.5, rounded to 28)
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
pygame.mouse.set_visible(True)

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
player_center = pygame.Vector2(player.center)
player_size = max(player.w, player.h)  # Use larger dimension (28)
min_block_distance = player_size * 10  # 10x player size = 280 pixels

# Filter all block lists to remove blocks too close to player and prevent overlaps with each other
def filter_blocks_no_overlap(block_list: list[dict], all_other_blocks: list[list[dict]], player_rect: pygame.Rect) -> list[dict]:
    """Filter blocks to remove those too close to player and overlapping with other blocks."""
    filtered = []
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
destructible_blocks = filter_blocks_no_overlap(destructible_blocks, [moveable_destructible_blocks, giant_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], player)
moveable_destructible_blocks = filter_blocks_no_overlap(moveable_destructible_blocks, [destructible_blocks, giant_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], player)
giant_blocks = filter_blocks_no_overlap(giant_blocks, [destructible_blocks, moveable_destructible_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], player)
super_giant_blocks = filter_blocks_no_overlap(super_giant_blocks, [destructible_blocks, moveable_destructible_blocks, giant_blocks, trapezoid_blocks, triangle_blocks], player)

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
# Run counters (runs table)
# ----------------------------
running = True
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

try:
    while running:
        # Cap FPS at 120 for better performance and stability (prevents excessive CPU usage)
        dt_real = clock.tick(120) / 1000.0  # Cap at 120 FPS
        # Cap dt to prevent large jumps
        dt = min(dt_real if (state == STATE_PLAYING or state == STATE_ENDURANCE) else 0.0, 0.033)  # Max 30ms = ~30 FPS minimum

        if state == STATE_PLAYING or state == STATE_ENDURANCE:
            run_time += dt
            survival_time += dt  # Track total survival time
            player_time_since_shot += dt
            grenade_time_since_used += dt
            missile_time_since_used += dt
            overshield_recharge_timer += dt
            shield_recharge_timer += dt
            ally_drop_timer += dt
            
            # Update enemy defeat messages timer
            for msg in enemy_defeat_messages[:]:
                msg["timer"] -= dt
                if msg["timer"] <= 0:
                    enemy_defeat_messages.remove(msg)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Controls rebinding mode
                if state == STATE_CONTROLS and controls_rebinding:
                    action = controls_actions[controls_selected]
                    controls[action] = event.key
                    save_controls(controls)
                    controls_rebinding = False
                    continue

                # Update last-pressed direction for conflict resolution
                if event.key in (controls["move_left"], controls["move_right"]):
                    last_horizontal_key = event.key
                if event.key in (controls["move_up"], controls["move_down"]):
                    last_vertical_key = event.key

                # Weapon switching (keys 1-6) - only works if weapon is unlocked
                if state == STATE_PLAYING or state == STATE_ENDURANCE:
                    if event.key in WEAPON_KEY_MAP:
                        requested_weapon = WEAPON_KEY_MAP[event.key]
                        # Only switch if weapon is unlocked
                        if requested_weapon in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            # Clear beams when switching away from beam weapons
                            if previous_weapon_mode == "wave_beam" and requested_weapon != "wave_beam":
                                wave_beams.clear()
                            if previous_weapon_mode == "laser" and requested_weapon != "laser":
                                laser_beams.clear()
                            current_weapon_mode = requested_weapon
                            # Log weapon switch
                            if previous_weapon_mode != current_weapon_mode:
                                telemetry.log_player_action(PlayerActionEvent(
                                    t=run_time,
                                    action_type="weapon_switch",
                                    x=player.centerx,
                                    y=player.centery,
                                    duration=None,
                                    success=True
                                ))
                    # Dash in direction of movement
                    elif event.key == controls.get("dash", pygame.K_SPACE) and jump_cooldown_timer <= 0.0 and not is_jumping:
                        jump_success = False
                        if last_move_velocity.length_squared() > 0:
                            # Dash in direction of movement
                            jump_dir = last_move_velocity.normalize()
                            jump_velocity = jump_dir * jump_speed
                            jump_timer = jump_duration
                            is_jumping = True
                            jump_cooldown_timer = jump_cooldown
                            jump_success = True
                        elif move_dir.length_squared() > 0:
                            # Fallback: use current move direction
                            jump_dir = move_dir.normalize()
                            jump_velocity = jump_dir * jump_speed
                            jump_timer = jump_duration
                            is_jumping = True
                            jump_cooldown_timer = jump_cooldown
                            jump_success = True
                        
                        # Log dash action
                        if jump_success:
                            telemetry.log_player_action(PlayerActionEvent(
                                t=run_time,
                                action_type="dash",
                                x=player.centerx,
                                y=player.centery,
                                duration=jump_duration,
                                success=True
                            ))

                # Menu navigation
                if state == STATE_MENU:
                    if menu_section == 0:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            difficulty_selected = (difficulty_selected - 1) % len(difficulty_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            difficulty_selected = (difficulty_selected + 1) % len(difficulty_options)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            menu_section = 1
                    elif menu_section == 1:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            aiming_mode_selected = (aiming_mode_selected - 1) % 2
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            aiming_mode_selected = (aiming_mode_selected + 1) % 2
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            menu_section = 1.5  # Go to character profile yes/no
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 0
                    elif menu_section == 1.5:
                        # Character profile yes/no selection
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            use_character_profile_selected = (use_character_profile_selected - 1) % 2
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            use_character_profile_selected = (use_character_profile_selected + 1) % 2
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            use_character_profile = use_character_profile_selected == 1
                            if use_character_profile:
                                menu_section = 2  # Go to profile selection
                            else:
                                menu_section = 3  # Skip to options
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 1
                    elif menu_section == 2:
                        # Character profile creator
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            character_profile_selected = (character_profile_selected - 1) % len(character_profile_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            character_profile_selected = (character_profile_selected + 1) % len(character_profile_options)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if character_profile_selected == 0:
                                # Use premade profiles (existing class system)
                                menu_section = 7  # Go to class selection
                            elif character_profile_selected == 1:
                                # Create custom profile
                                menu_section = 6  # Go to custom profile creator
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            # Continue to next menu based on selection
                            if character_profile_selected == 0:
                                menu_section = 7  # Go to class selection
                            elif character_profile_selected == 1:
                                menu_section = 6  # Go to custom profile creator
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 1
                    elif menu_section == 6:
                        # Custom character profile creator
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            custom_profile_stat_selected = (custom_profile_stat_selected - 1) % len(custom_profile_stats_list)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            custom_profile_stat_selected = (custom_profile_stat_selected + 1) % len(custom_profile_stats_list)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                            custom_profile_stats[stat_key] = max(0.5, custom_profile_stats[stat_key] - 0.1)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            # Continue to next menu (options)
                            menu_section = 3
                        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or (event.key == pygame.K_EQUALS and pygame.key.get_mods() & pygame.KMOD_SHIFT):
                            # Increase stat using + key
                            stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                            custom_profile_stats[stat_key] = min(3.0, custom_profile_stats[stat_key] + 0.1)
                        elif event.key == pygame.K_MINUS:
                            # Decrease stat using - key (alternative to LEFT)
                            stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                            custom_profile_stats[stat_key] = max(0.5, custom_profile_stats[stat_key] - 0.1)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            # Apply custom profile and continue
                            menu_section = 3  # Go to options
                        elif event.key == pygame.K_BACKSPACE:
                            menu_section = 2  # Go back to profile selection
                    elif menu_section == 7:
                        # Player class selection (premade profiles)
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            player_class_selected = (player_class_selected - 1) % len(player_class_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            player_class_selected = (player_class_selected + 1) % len(player_class_options)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            menu_section = 3  # Go to options
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 2  # Go back to profile selection
                    elif menu_section == 3:
                        # HUD options page
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            ui_show_metrics_selected = (ui_show_metrics_selected - 1) % 2
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            ui_show_metrics_selected = (ui_show_metrics_selected + 1) % 2
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            # Toggle HUD
                            ui_show_metrics_selected = (ui_show_metrics_selected + 1) % 2
                            ui_show_hud = ui_show_metrics_selected == 0  # HUD follows metrics
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            menu_section = 3.5  # Go to Telemetry options
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            # Go back - check if character profile was used
                            if use_character_profile:
                                menu_section = 2
                            else:
                                menu_section = 1.5
                    elif menu_section == 3.5:
                        # Telemetry options page
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            ui_telemetry_enabled_selected = (ui_telemetry_enabled_selected - 1) % 2
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            ui_telemetry_enabled_selected = (ui_telemetry_enabled_selected + 1) % 2
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            # Toggle telemetry
                            ui_telemetry_enabled_selected = (ui_telemetry_enabled_selected + 1) % 2
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            menu_section = 4  # Go to weapon selection
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 3  # Go back to HUD options
                    elif menu_section == 4:
                        # Weapon selection menu (for testing)
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            beam_selection_selected = (beam_selection_selected - 1) % len(weapon_selection_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            beam_selection_selected = (beam_selection_selected + 1) % len(weapon_selection_options)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            menu_section = 5
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 3
                    elif menu_section == 5:
                        # Endurance mode selection (UP/DOWN)
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            endurance_mode_selected = (endurance_mode_selected - 1) % 2
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            endurance_mode_selected = (endurance_mode_selected + 1) % 2
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            # Start game with selected settings
                            difficulty = difficulty_options[difficulty_selected]
                            aiming_mode = AIM_MOUSE if aiming_mode_selected == 0 else AIM_ARROWS
                            # Apply character profile
                            if use_character_profile:
                                if character_profile_selected == 0:
                                    # Use premade class
                                    player_class = player_class_options[player_class_selected]
                                else:
                                    # Use custom profile - add to player_class_stats
                                    player_class = "CUSTOM"
                                    player_class_stats["CUSTOM"] = custom_profile_stats.copy()
                            else:
                                # No character profile - use default class selection
                                player_class = player_class_options[player_class_selected]
                            
                            # Apply class stats to player
                            class_stats = player_class_stats[player_class]
                            player_max_hp = int(2500 * class_stats["hp_mult"])  # 10x (250 * 10)
                            player_hp = player_max_hp
                            player_speed = int(300 * class_stats["speed_mult"])
                            
                            ui_show_metrics = ui_show_metrics_selected == 0
                            ui_show_hud = ui_show_metrics  # HUD follows metrics setting
                            # Set telemetry enabled based on user choice
                            telemetry_enabled = ui_telemetry_enabled_selected == 0
                            # Set weapon from selection
                            selected_weapon = weapon_selection_options[beam_selection_selected]
                            # Unlock and switch to selected weapon
                            unlocked_weapons.add(selected_weapon)
                            # Clear beams when switching away from beam weapons
                            if current_weapon_mode == "wave_beam" and selected_weapon != "wave_beam":
                                wave_beams.clear()
                            if current_weapon_mode == "laser" and selected_weapon != "laser":
                                laser_beams.clear()
                            current_weapon_mode = selected_weapon
                            if selected_weapon == "wave_beam":
                                wave_beam_pattern_index = 0  # Use sine pattern
                                beam_selection_pattern = "sine"
                            else:
                                beam_selection_pattern = selected_weapon
                            # Initialize telemetry if enabled
                            if telemetry_enabled:
                                telemetry = Telemetry(db_path="game_telemetry.db", flush_interval_s=0.5, max_buffer=700)
                            else:
                                # Create a no-op telemetry object
                                class NoOpTelemetry:
                                    def __getattr__(self, name):
                                        return lambda *args, **kwargs: None
                                telemetry = NoOpTelemetry()
                            # Apply class stats
                            stats = player_class_stats[player_class]
                            player_max_hp = int(1000 * stats["hp_mult"])  # 10x (100 * 10)
                            player_hp = player_max_hp
                            player_speed = int(300 * stats["speed_mult"])
                            player_bullet_damage = int(20 * stats["damage_mult"])
                            player_shoot_cooldown = 0.12 / stats["firerate_mult"]
                            # Set state based on endurance mode selection
                            if endurance_mode_selected == 1:
                                state = STATE_ENDURANCE
                                lives = 999  # Infinite lives in endurance mode
                                previous_game_state = STATE_ENDURANCE  # Track for pause/unpause
                            else:
                                state = STATE_PLAYING
                                previous_game_state = STATE_PLAYING  # Track for pause/unpause
                            run_id = telemetry.start_run(run_started_at, player_max_hp) if telemetry_enabled else None
                            start_wave(wave_number)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 4
                
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_PLAYING or state == STATE_ENDURANCE:
                        previous_game_state = state  # Save current state before pausing
                        state = STATE_PAUSED
                        pause_selected = 0
                    elif state == STATE_PAUSED:
                        # Restore previous game state (STATE_PLAYING or STATE_ENDURANCE)
                        state = previous_game_state if previous_game_state else STATE_PLAYING
                    elif state == STATE_CONTINUE:
                        running = False
                    elif state == STATE_CONTROLS:
                        state = STATE_PAUSED
                    elif state == STATE_MENU:
                        running = False
                    elif state == STATE_VICTORY or state == STATE_GAME_OVER or state == STATE_HIGH_SCORES:
                        running = False  # Quit from victory/game over/high scores screens
                    elif state == STATE_NAME_INPUT:
                        # Allow ESC to skip name input and go to high scores
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

                if event.key == pygame.K_p:
                    if state == STATE_PLAYING or state == STATE_ENDURANCE:
                        previous_game_state = state  # Save current state before pausing
                        state = STATE_PAUSED
                        pause_selected = 0
                    elif state == STATE_PAUSED:
                        # Restore previous game state (STATE_PLAYING or STATE_ENDURANCE)
                        state = previous_game_state if previous_game_state else STATE_PLAYING

                # Pause menu
                if state == STATE_PAUSED:
                    if event.key == pygame.K_UP:
                        pause_selected = (pause_selected - 1) % len(pause_options)
                    elif event.key == pygame.K_DOWN:
                        pause_selected = (pause_selected + 1) % len(pause_options)
                    elif event.key == pygame.K_RETURN:
                        choice = pause_options[pause_selected]
                        if choice == "Continue":
                            # Restore previous game state (STATE_PLAYING or STATE_ENDURANCE)
                            state = previous_game_state if previous_game_state else STATE_PLAYING
                        elif choice == "Quit":
                            running = False
                    elif event.key == pygame.K_c:
                        state = STATE_CONTROLS
                        controls_selected = 0
                        controls_rebinding = False

                # Controls menu
                if state == STATE_CONTROLS and not controls_rebinding:
                    if event.key == pygame.K_UP:
                        controls_selected = (controls_selected - 1) % len(controls_actions)
                    elif event.key == pygame.K_DOWN:
                        controls_selected = (controls_selected + 1) % len(controls_actions)
                    elif event.key == pygame.K_RETURN:
                        controls_rebinding = True

                # Shield activation (Left Alt key)
                if state == STATE_PLAYING or state == STATE_ENDURANCE:
                    if event.key == pygame.K_LALT:
                        # Activate shield if cooldown is ready
                        if shield_cooldown_remaining <= 0.0 and not shield_active:
                            shield_active = True
                            shield_duration_remaining = shield_duration
                            # Random cooldown between 10-15 seconds
                            shield_cooldown = random.uniform(10.0, 15.0)
                            shield_recharge_cooldown = shield_cooldown
                            shield_recharge_timer = 0.0
                            shield_cooldown_remaining = 0.0  # Reset cooldown when activating
                    
                    # Overshield activation (Tab key)
                    if event.key == pygame.K_TAB:
                        if overshield_recharge_timer >= overshield_recharge_cooldown:
                            # Create overshield equal to player's max health
                            overshield = player_max_hp
                            overshield_max = max(overshield_max, player_max_hp)  # Update max if needed
                            overshield_recharge_timer = 0.0
                    
                    # Ally drop activation (Q key)
                    if event.key == controls.get("ally_drop", pygame.K_q):
                        if ally_drop_timer >= ally_drop_cooldown:
                            # Remove existing dropped ally if any
                            if dropped_ally and dropped_ally in friendly_ai:
                                friendly_ai.remove(dropped_ally)
                            
                            # Spawn ally behind player (opposite direction of last movement)
                            player_center = pygame.Vector2(player.center)
                            if last_move_velocity.length_squared() > 0:
                                # Spawn behind player in opposite direction of movement
                                spawn_dir = -last_move_velocity.normalize()
                            else:
                                # Default: spawn below player
                                spawn_dir = pygame.Vector2(0, 1)
                            
                            # Use tank template for dropped ally (high HP, draws fire)
                            tank_template = next((t for t in friendly_ai_templates if t["type"] == "tank"), friendly_ai_templates[0])
                            dropped_ally = make_friendly_from_template(tank_template, 1.0, 1.0)
                            spawn_offset = spawn_dir * 50  # 50 pixels behind player
                            dropped_ally["rect"].center = (int(player_center.x + spawn_offset.x), int(player_center.y + spawn_offset.y))
                            dropped_ally["is_dropped_ally"] = True  # Mark as dropped ally for priority targeting
                            clamp_rect_to_screen(dropped_ally["rect"])
                            friendly_ai.append(dropped_ally)
                            ally_drop_timer = 0.0
                    
                    # Grenade activation (E key)
                    if event.key == pygame.K_e:
                        # Only trigger grenade if not in menu/victory screens (E is used there too)
                        if grenade_time_since_used >= grenade_cooldown:
                            # Create explosion at player position
                            player_center = pygame.Vector2(player.center)
                            grenade_radius = max(player.w, player.h) * 10  # 10x player size
                            grenade_explosions.append({
                                "x": player_center.x,
                                "y": player_center.y,
                                "radius": 0,  # Start at 0, expand to max_radius
                                "max_radius": grenade_radius,
                                "timer": 0.3,  # Explosion lasts 0.3 seconds
                                "damage": grenade_damage,
                                "damaged_enemies": set(),  # Track which enemies already took damage
                                "damaged_blocks": set(),  # Track which blocks already took damage
                                "source": "player"  # Mark as player grenade (player is immune)
                            })
                            grenade_time_since_used = 0.0
                    
                    # Missile activation (R key)
                    if event.key == pygame.K_r:
                        if missile_time_since_used >= missile_cooldown and enemies:
                            # Find nearest enemy to target
                            player_center = pygame.Vector2(player.center)
                            nearest_enemy = None
                            nearest_dist = float("inf")
                            for e in enemies:
                                enemy_center = pygame.Vector2(e["rect"].center)
                                dist = player_center.distance_to(enemy_center)
                                if dist < nearest_dist:
                                    nearest_dist = dist
                                    nearest_enemy = e
                            
                            if nearest_enemy:
                                # Create missile at player position
                                missile_rect = pygame.Rect(player.centerx - 8, player.centery - 8, 16, 16)
                                target_center = pygame.Vector2(nearest_enemy["rect"].center)
                                direction = (target_center - player_center)
                                if direction.length() > 0:
                                    direction = direction.normalize()
                                    missiles.append({
                                        "rect": missile_rect,
                                        "vel": direction * missile_speed,
                                        "target_enemy": nearest_enemy,
                                        "speed": missile_speed,
                                        "damage": missile_damage,
                                        "explosion_radius": missile_explosion_radius
                                    })
                                    missile_time_since_used = 0.0
                
                # Victory screen
                if state == STATE_VICTORY:
                    if event.key == pygame.K_e:
                        # Enter endurance mode after victory
                        state = STATE_ENDURANCE
                        lives = 999  # Infinite lives in endurance mode
                        wave_number += 1  # Continue from next wave
                        start_wave(wave_number)
                
                # Name input screen (for high scores)
                if state == STATE_NAME_INPUT:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Save high score and show high score board
                        save_high_score(
                            player_name_input if player_name_input.strip() else "Anonymous",
                            final_score_for_high_score,
                            wave_number - 1,
                            survival_time,
                            enemies_killed,
                            difficulty
                        )
                        state = STATE_HIGH_SCORES
                        name_input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        if player_name_input:
                            player_name_input = player_name_input[:-1]
                    elif event.unicode and len(player_name_input) < 20:
                        # Add character if it's printable
                        if event.unicode.isprintable():
                            player_name_input += event.unicode
                
                # High score board screen
                if state == STATE_HIGH_SCORES:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_e:
                        # Go to game over screen
                        state = STATE_GAME_OVER
                
                # Game Over screen
                if state == STATE_GAME_OVER:
                    if event.key == pygame.K_e:
                        # Enter endurance mode
                        state = STATE_ENDURANCE
                        lives = 999  # Infinite lives in endurance mode
                        wave_number += 1  # Continue from next wave
                        start_wave(wave_number)

                # Continue screen
                if state == STATE_CONTINUE:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        reset_after_death()
                        state = STATE_PLAYING

            if event.type == pygame.KEYUP:
                keys_now = pygame.key.get_pressed()
                if event.key in (controls["move_left"], controls["move_right"]):
                    if last_horizontal_key == event.key:
                        left_k = controls["move_left"]
                        right_k = controls["move_right"]
                        if keys_now[left_k] and not keys_now[right_k]:
                            last_horizontal_key = left_k
                        elif keys_now[right_k] and not keys_now[left_k]:
                            last_horizontal_key = right_k
                        else:
                            last_horizontal_key = None
                if event.key in (controls["move_up"], controls["move_down"]):
                    if last_vertical_key == event.key:
                        up_k = controls["move_up"]
                        down_k = controls["move_down"]
                        if keys_now[up_k] and not keys_now[down_k]:
                            last_vertical_key = up_k
                        elif keys_now[down_k] and not keys_now[up_k]:
                            last_vertical_key = down_k
                        else:
                            last_vertical_key = None

        # --- Simulation ---
        if state == STATE_PLAYING or state == STATE_ENDURANCE:
            # Movement
            if not enemies and wave_active:
                wave_active = False
                time_to_next_wave = max(0.5, wave_respawn_delay - 0.25 * enemy_spawn_boost_level)
                
                # Check side quest completion
                if side_quests["no_hit_wave"]["active"] and wave_damage_taken == 0:
                    side_quests["no_hit_wave"]["completed"] = True
                    bonus_points = side_quests["no_hit_wave"]["bonus_points"]
                    score += bonus_points
                    # Show bonus message
                    weapon_pickup_messages.append({
                        "weapon_name": f"PERFECT WAVE! +{bonus_points:,} BONUS",
                        "timer": 5.0,
                        "color": (255, 255, 0)
                    })
                side_quests["no_hit_wave"]["active"] = False
                
                # Log wave end event
                telemetry.log_wave(
                    WaveEvent(
                        t=run_time,
                        wave_number=wave_number,
                        event_type="end",
                        enemies_spawned=0,
                        hp_scale=1.0 + 0.15 * (wave_number - 1),
                        speed_scale=1.0 + 0.05 * (wave_number - 1),
                    )
                )

            if not wave_active:
                time_to_next_wave = max(0.0, time_to_next_wave - dt)
                if time_to_next_wave <= 0.0:
                    # Check if all levels are complete (wave 9 = level 3, wave 3)
                    if wave_number >= max_level * 3:
                        # All levels completed - victory!
                        state = STATE_VICTORY
                    else:
                        wave_number += 1
                        # Level progression is now handled in start_wave() (3 waves per level)
                        start_wave(wave_number)

            keys = pygame.key.get_pressed()
            dx = dy = 0
            left_k = controls["move_left"]
            right_k = controls["move_right"]
            up_k = controls["move_up"]
            down_k = controls["move_down"]
            boost_k = controls["boost"]
            slow_k = controls["slow"]

            left = keys[left_k]
            right = keys[right_k]
            up = keys[up_k]
            down = keys[down_k]
            wants_boost = keys[boost_k]
            wants_slow = keys[slow_k]

            if left and right:
                dx = -1 if last_horizontal_key == left_k else 1
            elif left:
                dx = -1
            elif right:
                dx = 1

            if up and down:
                dy = -1 if last_vertical_key == up_k else 1
            elif up:
                dy = -1
            elif down:
                dy = 1

            move_dir = pygame.Vector2(dx, dy)
            speed_mult = player_stat_multipliers["speed"]  # Apply permanent speed multiplier
            if wants_slow:
                speed_mult *= slow_speed_mult
            boosting = wants_boost and boost_meter > 0.0 and not wants_slow
            
            # Log boost/slow state changes
            if boosting != previous_boost_state:
                if boosting:
                    telemetry.log_player_action(PlayerActionEvent(
                        t=run_time,
                        action_type="boost",
                        x=player.centerx,
                        y=player.centery,
                        duration=None,
                        success=True
                    ))
                previous_boost_state = boosting
            
            if wants_slow != previous_slow_state:
                if wants_slow:
                    telemetry.log_player_action(PlayerActionEvent(
                        t=run_time,
                        action_type="slow",
                        x=player.centerx,
                        y=player.centery,
                        duration=None,
                        success=True
                    ))
                previous_slow_state = wants_slow
            
            if boosting:
                speed_mult *= boost_speed_mult
                boost_meter = max(0.0, boost_meter - boost_drain_per_s * dt)
            else:
                boost_meter = min(boost_meter_max, boost_meter + boost_regen_per_s * dt)
            
            # Shield update logic
            if shield_active:
                shield_duration_remaining -= dt
                if shield_duration_remaining <= 0.0:
                    shield_active = False
                    shield_cooldown_remaining = shield_cooldown
            else:
                # Shield is on cooldown
                if shield_cooldown_remaining > 0.0:
                    shield_cooldown_remaining = max(0.0, shield_cooldown_remaining - dt)
                    # Update shield recharge timer for progress bar
                    if shield_cooldown_remaining <= 0.0:
                        shield_recharge_timer = shield_recharge_cooldown  # Reset when ready
                    else:
                        shield_recharge_timer = shield_recharge_cooldown - shield_cooldown_remaining

            if move_dir.length_squared() > 0:
                move_dir = move_dir.normalize()
                last_move_velocity = move_dir * player_speed * speed_mult
            else:
                last_move_velocity = pygame.Vector2(0, 0)

            # Update jump timers
            if jump_cooldown_timer > 0.0:
                jump_cooldown_timer -= dt
            if is_jumping:
                jump_timer -= dt
                if jump_timer <= 0.0:
                    is_jumping = False
                    jump_velocity = pygame.Vector2(0, 0)

            # Apply jump velocity if jumping
            total_velocity = last_move_velocity.copy()
            if is_jumping:
                # Apply jump velocity (decay over time)
                jump_factor = jump_timer / jump_duration
                total_velocity += jump_velocity * jump_factor

            move_x = int(total_velocity.x * dt)
            move_y = int(total_velocity.y * dt)

            # Shooting
            # Note: These are module-level variables, no global declaration needed
            laser_time_since_shot += dt
            if current_weapon_mode == "laser":
                # Laser beam weapon - continuous beam while mouse is held
                if pygame.mouse.get_pressed(3)[0] and laser_time_since_shot >= laser_cooldown:
                    # Create or update laser beam
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    player_center = pygame.Vector2(player.center)
                    mouse_pos = pygame.Vector2(mouse_x, mouse_y)
                    direction = (mouse_pos - player_center)
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                        # Calculate laser end point (stops at blocks or enemies)
                        laser_end = player_center + direction * laser_length
                        closest_hit = None
                        closest_dist = laser_length
                        
                        # Check collision with blocks first (solid blocks stop laser)
                        for blk in blocks:
                            hit = line_rect_intersection(player_center, laser_end, blk["rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                        
                        # Check collision with trapezoid blocks
                        for tb in trapezoid_blocks:
                            hit = line_rect_intersection(player_center, laser_end, tb["bounding_rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                        
                        # Check collision with triangle blocks
                        for tr in triangle_blocks:
                            hit = line_rect_intersection(player_center, laser_end, tr["bounding_rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                        
                        # Check collision with destructible blocks (can damage if destructible)
                        for db in destructible_blocks[:]:
                            hit = line_rect_intersection(player_center, laser_end, db["rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                                # Damage destructible block if it has HP
                                if db.get("is_destructible") and "hp" in db:
                                    db["hp"] -= laser_damage * dt * 60  # Damage per second
                                    if db["hp"] <= 0:
                                        destructible_blocks.remove(db)
                        
                        # Check collision with moveable destructible blocks (can damage if destructible)
                        for mdb in moveable_destructible_blocks[:]:
                            hit = line_rect_intersection(player_center, laser_end, mdb["rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                                # Damage moveable destructible block if it has HP
                                if mdb.get("is_destructible") and "hp" in mdb:
                                    mdb["hp"] -= laser_damage * dt * 60  # Damage per second
                                    if mdb["hp"] <= 0:
                                        moveable_destructible_blocks.remove(mdb)
                        
                        # Check collision with enemies (can damage them)
                        for e in enemies[:]:
                            hit = line_rect_intersection(player_center, laser_end, e["rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                                # Damage enemy continuously
                                e["hp"] -= laser_damage * dt * 60
                                damage_dealt += int(laser_damage * dt * 60)
                                if e["hp"] <= 0:
                                    # Suicide enemies despawn immediately when killed (no drops)
                                    if e.get("is_suicide", False):
                                        if e in enemies:
                                            enemies.remove(e)
                                    else:
                                        kill_enemy(e)
                        # Store laser beam for drawing
                        if len(laser_beams) == 0:
                            laser_beams.append({
                                "start": player_center,
                                "end": laser_end,
                                "color": (255, 50, 50),  # Bright red
                                "width": 8,
                            })
                        else:
                            laser_beams[0]["start"] = player_center
                            laser_beams[0]["end"] = laser_end
                else:
                    # Clear laser when not shooting
                    laser_beams.clear()
            elif current_weapon_mode == "wave_beam":
                # Wave beam weapon - continuous curved beam while mouse is held
                wave_beam_time_since_shot += dt
                
                if pygame.mouse.get_pressed(3)[0] and wave_beam_time_since_shot >= wave_beam_cooldown:
                    # Create or update wave beam
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    player_center = pygame.Vector2(player.center)
                    mouse_pos = pygame.Vector2(mouse_x, mouse_y)
                    direction = (mouse_pos - player_center)
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                        
                        # Get current wave pattern (cycles through patterns)
                        pattern = wave_beam_patterns[wave_beam_pattern_index % len(wave_beam_patterns)]
                        
                        # Generate wave beam points with undulation (0.5 second period, 7 pixel amplitude)
                        beam_points = generate_wave_beam_points(
                            player_center, 
                            direction, 
                            pattern, 
                            wave_beam_length,
                            amplitude=7.0,  # 7 pixel amplitude
                            frequency=0.02,
                            time_offset=run_time  # Time-based undulation with 0.5 second period
                        )
                        
                        # Find closest collision along the beam path
                        closest_hit = None
                        closest_dist = wave_beam_length
                        final_points = beam_points.copy()
                        
                        # Check collision with blocks first (solid blocks stop beam)
                        for blk in blocks:
                            hit, dist = check_wave_beam_collision(beam_points, blk["rect"], wave_beam_width)
                            if hit and dist < closest_dist:
                                closest_dist = dist
                                closest_hit = hit
                                # Truncate beam points at hit
                                final_points = [p for p in beam_points if (p - player_center).length() <= dist]
                        
                        # Check collision with trapezoid blocks
                        for tb in trapezoid_blocks:
                            hit, dist = check_wave_beam_collision(beam_points, tb["bounding_rect"], wave_beam_width)
                            if hit and dist < closest_dist:
                                closest_dist = dist
                                closest_hit = hit
                                final_points = [p for p in beam_points if (p - player_center).length() <= dist]
                        
                        # Check collision with triangle blocks
                        for tr in triangle_blocks:
                            hit, dist = check_wave_beam_collision(beam_points, tr["bounding_rect"], wave_beam_width)
                            if hit and dist < closest_dist:
                                closest_dist = dist
                                closest_hit = hit
                                final_points = [p for p in beam_points if (p - player_center).length() <= dist]
                        
                        # Check collision with destructible blocks (can damage if destructible)
                        for db in destructible_blocks[:]:
                            hit, dist = check_wave_beam_collision(beam_points, db["rect"], wave_beam_width)
                            if hit:
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    final_points = [p for p in beam_points if (p - player_center).length() <= dist]
                                # Damage destructible block if it has HP
                                if db.get("is_destructible") and "hp" in db:
                                    db["hp"] -= wave_beam_damage * dt * 60
                                    if db["hp"] <= 0:
                                        destructible_blocks.remove(db)
                        
                        # Check collision with moveable destructible blocks (can damage if destructible)
                        for mdb in moveable_destructible_blocks[:]:
                            hit, dist = check_wave_beam_collision(beam_points, mdb["rect"], wave_beam_width)
                            if hit:
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    final_points = [p for p in beam_points if (p - player_center).length() <= dist]
                                # Damage moveable destructible block if it has HP
                                if mdb.get("is_destructible") and "hp" in mdb:
                                    mdb["hp"] -= wave_beam_damage * dt * 60
                                    if mdb["hp"] <= 0:
                                        moveable_destructible_blocks.remove(mdb)
                        
                        # Check collision with enemies (can damage them)
                        for e in enemies[:]:
                            hit, dist = check_wave_beam_collision(beam_points, e["rect"], wave_beam_width)
                            if hit:
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    final_points = [p for p in beam_points if (p - player_center).length() <= dist]
                                # Damage enemy continuously
                                e["hp"] -= wave_beam_damage * dt * 60
                                damage_dealt += int(wave_beam_damage * dt * 60)
                                if e["hp"] <= 0:
                                    # Suicide enemies despawn immediately when killed (no drops)
                                    if e.get("is_suicide", False):
                                        if e in enemies:
                                            enemies.remove(e)
                                    else:
                                        kill_enemy(e)
                        
                        # Store wave beam for drawing
                        if len(wave_beams) == 0:
                            wave_beams.append({
                                "points": final_points,
                                "pattern": pattern,
                                "color": (50, 255, 50),  # Lime green
                                "width": wave_beam_width,
                            })
                        else:
                            wave_beams[0]["points"] = final_points
                            wave_beams[0]["pattern"] = pattern
                            wave_beams[0]["color"] = (50, 255, 50)  # Lime green (update color)
                        
                        # Cycle to next pattern on each shot
                        wave_beam_pattern_index = (wave_beam_pattern_index + 1) % len(wave_beam_patterns)
                else:
                    # Clear wave beam when not shooting
                    wave_beams.clear()
            else:
                # Normal shooting for other weapons
                # Apply both temporary and permanent fire rate multipliers
                temp_mult = fire_rate_mult if fire_rate_buff_t > 0 else 1.0
                # Cap permanent multiplier to prevent excessive firing rates
                capped_firerate = min(2.0, player_stat_multipliers["firerate"])
                perm_mult = 1.0 / capped_firerate if capped_firerate > 1.0 else 1.0
                # Rocket launcher has slower fire rate
                rocket_mult = 3.5 if current_weapon_mode == "rocket" else 1.0
                # Cap minimum cooldown to prevent performance issues (max 10 shots per second)
                effective_cooldown = max(0.1, player_shoot_cooldown * temp_mult * perm_mult * rocket_mult)
                
                # Check for shooting input based on aiming mode
                should_shoot = False
                if aiming_mode == AIM_ARROWS:
                    # Arrow key aiming: shoot with spacebar or any arrow key held
                    keys = pygame.key.get_pressed()
                    should_shoot = (keys[pygame.K_SPACE] or 
                                   keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or 
                                   keys[pygame.K_UP] or keys[pygame.K_DOWN])
                else:
                    # Mouse aiming: shoot with mouse button
                    should_shoot = pygame.mouse.get_pressed(3)[0]
                
                if should_shoot and player_time_since_shot >= effective_cooldown:
                    spawn_player_bullet_and_log()
                    player_time_since_shot = 0.0
                player_time_since_shot += dt

            # Update bouncing destructor shapes
            for ds in destructor_shapes[:]:
                ds["vel"].x += int(ds["vel"].x * dt)
                ds["vel"].y += int(ds["vel"].y * dt)
                ds["rect"].x += int(ds["vel"].x * dt)
                ds["rect"].y += int(ds["vel"].y * dt)
                
                # Bounce off walls
                if ds["rect"].left < 0 or ds["rect"].right > WIDTH:
                    ds["vel"].x = -ds["vel"].x
                if ds["rect"].top < 0 or ds["rect"].bottom > HEIGHT:
                    ds["vel"].y = -ds["vel"].y
                
                # Clamp to screen
                ds["rect"].x = max(0, min(ds["rect"].x, WIDTH - ds["rect"].w))
                ds["rect"].y = max(0, min(ds["rect"].y, HEIGHT - ds["rect"].h))
                
                # Check collision with destructible blocks (can damage if destructible)
                for db in destructible_blocks[:]:
                    if ds["rect"].colliderect(db["rect"]):
                        if db.get("is_destructible") and "hp" in db:
                            db["hp"] -= ds.get("damage", 50) * dt * 60
                            if db["hp"] <= 0:
                                destructible_blocks.remove(db)
                
                # Check collision with moveable destructible blocks (can damage if destructible)
                for mdb in moveable_destructible_blocks[:]:
                    if ds["rect"].colliderect(mdb["rect"]):
                        if mdb.get("is_destructible") and "hp" in mdb:
                            mdb["hp"] -= ds.get("damage", 50) * dt * 60
                            if mdb["hp"] <= 0:
                                moveable_destructible_blocks.remove(mdb)
                
                # Check collision with enemies
                for e in enemies[:]:
                    if ds["rect"].colliderect(e["rect"]):
                        e["hp"] -= ds.get("damage", 50) * dt * 60
                        if e["hp"] <= 0:
                            kill_enemy(e)
                
                # Check collision with player
                if ds["rect"].colliderect(player):
                    damage_amount = ds.get("damage", 50) * dt * 60
                    player_hp -= damage_amount
                    wave_damage_taken += int(damage_amount)  # Track for side quests
                    if player_hp <= 0:
                        deaths += 1
                        lives -= 1
                        if lives > 0:
                            state = STATE_CONTINUE
                        else:
                            # Game over - check if it's a high score
                            final_score_for_high_score = score
                            if is_high_score(score):
                                state = STATE_NAME_INPUT
                                player_name_input = ""
                                name_input_active = True
                            else:
                                state = STATE_GAME_OVER

            move_player_with_push(player, move_x, move_y, blocks)

            # Update hazard obstacles
            update_hazard_obstacles(dt)
            
            # Check collision with all hazard obstacles
            player_center = pygame.Vector2(player.center)
            for hazard in hazard_obstacles:
                if check_point_in_hazard(player_center, hazard["points"], hazard["bounding_rect"]):
                    # Check if shield is active - shield blocks all damage
                    if not shield_active:
                        # Apply damage - overshield absorbs damage first
                        remaining_damage = hazard["damage"] * dt * 60
                        if overshield > 0:
                            if overshield >= remaining_damage:
                                overshield -= remaining_damage
                                remaining_damage = 0
                            else:
                                remaining_damage -= overshield
                                overshield = 0
                        
                        # Apply remaining damage to player HP
                        if remaining_damage > 0:
                            player_hp -= remaining_damage
                        damage_taken += int(hazard["damage"] * dt * 60)
                        wave_damage_taken += int(hazard["damage"] * dt * 60)  # Track for side quests
                        
                        if player_hp < 0:
                            player_hp = 0
                        
                        if telemetry_enabled and telemetry:
                            telemetry.log_player_damage(
                                PlayerDamageEvent(
                                    t=run_time,
                                    amount=int(hazard["damage"] * dt * 60),
                                    source_type="paraboloid_hazard",
                                    source_enemy_type=None,
                                    player_x=player.x,
                                    player_y=player.y,
                                    player_hp_after=player_hp,
                                )
                            )
            
            # Update moving health zone position
            zone = moving_health_zone
            
            # Helper function to check if health zone overlaps with any objects
            def health_zone_overlaps_with_objects(zone_rect: pygame.Rect) -> bool:
                """Check if health zone overlaps with blocks, pickups, enemies, or player."""
                # Check blocks
                for block_list in [destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks]:
                    for block in block_list:
                        if zone_rect.colliderect(block["rect"]):
                            return True
                # Check trapezoid and triangle blocks
                for tb in trapezoid_blocks:
                    if zone_rect.colliderect(tb.get("bounding_rect", tb.get("rect"))):
                        return True
                for tr in triangle_blocks:
                    if zone_rect.colliderect(tr.get("bounding_rect", tr.get("rect"))):
                        return True
                # Check pickups
                for pickup in pickups:
                    if zone_rect.colliderect(pickup["rect"]):
                        return True
                # Check enemies (with small margin to avoid constant collisions)
                for enemy in enemies:
                    if zone_rect.colliderect(enemy["rect"]):
                        return True
                # Check player (with small margin)
                if zone_rect.colliderect(player):
                    return True
                return False
            
            if zone["target"] is None or (pygame.Vector2(zone["rect"].center) - zone["target"]).length() < 10:
                # Pick a new random target position that doesn't overlap
                max_target_attempts = 50
                new_target = None
                for _ in range(max_target_attempts):
                    candidate_target = pygame.Vector2(
                        random.randint(100, WIDTH - 250),
                        random.randint(100, HEIGHT - 250)
                    )
                    # Create a test rect at the candidate position
                    test_rect = pygame.Rect(
                        int(candidate_target.x - zone["rect"].w // 2),
                        int(candidate_target.y - zone["rect"].h // 2),
                        zone["rect"].w,
                        zone["rect"].h
                    )
                    if not health_zone_overlaps_with_objects(test_rect):
                        new_target = candidate_target
                        break
                if new_target:
                    zone["target"] = new_target
                else:
                    # If we can't find a good target, keep current position
                    zone["target"] = None
            
            # Move zone towards target
            zone_center = pygame.Vector2(zone["rect"].center)
            if zone["target"]:
                direction = (zone["target"] - zone_center)
                if direction.length() > 0:
                    direction = direction.normalize()
                    move_amount = zone["velocity"] * dt  # velocity is a scalar (float)
                    move_vector = direction * move_amount  # direction is Vector2, move_amount is float, result is Vector2
                    new_center = zone_center + move_vector
                    
                    # Test new position for overlaps before applying
                    test_rect = pygame.Rect(
                        int(new_center.x - zone["rect"].w // 2),
                        int(new_center.y - zone["rect"].h // 2),
                        zone["rect"].w,
                        zone["rect"].h
                    )
                    # Keep zone on screen
                    test_rect.left = max(0, min(test_rect.left, WIDTH - test_rect.w))
                    test_rect.top = max(0, min(test_rect.top, HEIGHT - test_rect.h))
                    
                    # Only move if new position doesn't overlap
                    if not health_zone_overlaps_with_objects(test_rect):
                        zone["rect"].centerx = int(new_center.x)
                        zone["rect"].centery = int(new_center.y)
                        # Keep zone on screen
                        zone["rect"].left = max(0, min(zone["rect"].left, WIDTH - zone["rect"].w))
                        zone["rect"].top = max(0, min(zone["rect"].top, HEIGHT - zone["rect"].h))
                    else:
                        # If new position would overlap, pick a new target
                        zone["target"] = None
            
            # Health recovery zone - heal player when inside
            current_frame_zones = set()
            if player.colliderect(zone["rect"]):
                zone_name = zone["name"]
                current_frame_zones.add(zone_name)
                
                # Log zone entry if just entered
                if zone_name not in player_current_zones:
                    telemetry.log_zone_visit(ZoneVisitEvent(
                        t=run_time,
                        zone_id=zone.get("zone_id"),
                        zone_name=zone_name,
                        zone_type="health_recovery",
                        event_type="enter",
                        x=player.centerx,
                        y=player.centery
                    ))
                
                heal_amount = zone["heal_rate"] * dt
                player_hp = min(player_max_hp, player_hp + heal_amount)
            
            # Log zone exits
            for zone_name in player_current_zones - current_frame_zones:
                telemetry.log_zone_visit(ZoneVisitEvent(
                    t=run_time,
                    zone_id=zone.get("zone_id"),
                    zone_name=zone_name,
                    zone_type="health_recovery",
                    event_type="exit",
                    x=player.centerx,
                    y=player.centery
                ))
            player_current_zones = current_frame_zones
            
            # Apply passive health regeneration (from pickups)
            if player_health_regen_rate > 0:
                regen_amount = player_health_regen_rate * dt
                player_hp = min(player_max_hp, player_hp + regen_amount)

            # Update timed buffs
            if fire_rate_buff_t > 0:
                fire_rate_buff_t = max(0.0, fire_rate_buff_t - dt)
            
            # Update pickup visual effects
            update_pickup_effects(dt)
            
            # Update damage numbers (fade out and move up)
            for dn in damage_numbers[:]:
                dn["timer"] -= dt
                dn["y"] -= 30 * dt  # Move up
                if dn["timer"] <= 0:
                    damage_numbers.remove(dn)
            
            # Update weapon pickup messages
            for msg in weapon_pickup_messages[:]:
                msg["timer"] -= dt
                if msg["timer"] <= 0:
                    weapon_pickup_messages.remove(msg)

            block_rects = [b["rect"] for b in blocks] + [b["rect"] for b in moveable_destructible_blocks] + [tb["bounding_rect"] for tb in trapezoid_blocks] + [tr["bounding_rect"] for tr in triangle_blocks]
            # Cache player position to avoid recalculating
            player_pos_cached = pygame.Vector2(player.center)
            
            # Cache block lists for enemy movement (reused in move_enemy_with_push)
            cached_block_rects = block_rects
            cached_destructible_rects = [b["rect"] for b in destructible_blocks]
            cached_moveable_destructible_rects = [b["rect"] for b in moveable_destructible_blocks]
            cached_trapezoid_rects = [tb["rect"] for tb in trapezoid_blocks]  # Now use rect instead of bounding_rect
            cached_triangle_rects = [tr["rect"] for tr in triangle_blocks]  # Now use rect instead of bounding_rect
            
            for enemy_idx, e in enumerate(enemies):
                e_pos = pygame.Vector2(e["rect"].center)
                
                # Suicide enemy behavior: move toward player and detonate when close
                if e.get("is_suicide", False):
                    player_pos = pygame.Vector2(player.center)
                    dist_to_player = (player_pos - e_pos).length()
                    
                    # Move directly toward player
                    if dist_to_player > 0:
                        move_dir = (player_pos - e_pos).normalize()
                        move_speed = e.get("speed", 120) * dt
                        e["rect"].x += int(move_dir.x * move_speed)
                        e["rect"].y += int(move_dir.y * move_speed)
                        clamp_rect_to_screen(e["rect"])
                    
                    # Detonate if close enough to player
                    detonation_dist = e.get("detonation_distance", 80)
                    if dist_to_player <= detonation_dist:
                        # Create grenade explosion
                        explosion_range = e.get("explosion_range", 150)
                        grenade_explosions.append({
                            "center": pygame.Vector2(e["rect"].center),
                            "radius": explosion_range,
                            "damage": grenade_damage,
                            "timer": 0.3,
                            "color": (255, 50, 50),  # Red for suicide explosion
                            "damaged_enemies": set(),
                            "damaged_blocks": set(),
                            "damaged_player": False,
                        })
                        # Remove enemy (despawn)
                        if e in enemies:
                            enemies.remove(e)
                        continue
                
                # When 5 or fewer enemies remain, they move directly towards player
                if len(enemies) <= 5:
                    # Direct movement towards player (aggressive pursuit)
                    toward_threat = (pygame.Vector2(player.center) - e_pos)
                    if toward_threat.length_squared() > 0:
                        toward_threat = toward_threat.normalize()
                    else:
                        toward_threat = pygame.Vector2(0, 0)
                else:
                    # Find nearest threat (player or friendly AI)
                    threat_result = find_nearest_threat(e_pos)
                    if not threat_result:
                        continue
                    threat_pos, threat_type = threat_result
                    
                    # Base movement toward threat
                    toward_threat = (threat_pos - e_pos)
                    if toward_threat.length_squared() > 0:
                        toward_threat = toward_threat.normalize()
                    else:
                        toward_threat = pygame.Vector2(0, 0)
                
                # Check for nearby bullets to dodge (only check every 3rd frame for performance)
                dodge_vector = pygame.Vector2(0, 0)
                # Only check dodge every 3rd frame to improve performance (reduced from every other frame)
                # Use frame counter + enemy index to stagger checks
                frame_mod = (int(run_time * 60) % 3)  # Cycle every 3 frames
                if enemy_idx % 3 == frame_mod:
                    nearby_bullets = find_threats_in_dodge_range(e_pos, dodge_range=250.0)
                else:
                    nearby_bullets = []
                
                if nearby_bullets:
                    # Calculate dodge direction (away from nearest bullet)
                    closest_bullet = None
                    closest_dist = float("inf")
                    for bullet_pos in nearby_bullets:
                        dist = (bullet_pos - e_pos).length_squared()
                        if dist < closest_dist:
                            closest_dist = dist
                            closest_bullet = bullet_pos
                    
                    if closest_bullet:
                        # Move perpendicular to bullet direction
                        away_from_bullet = (e_pos - pygame.Vector2(closest_bullet))
                        if away_from_bullet.length_squared() > 0:
                            away_from_bullet = away_from_bullet.normalize()
                            # Add perpendicular component for better dodging
                            perp = pygame.Vector2(-away_from_bullet.y, away_from_bullet.x)
                            # Combine away + perpendicular for better dodge
                            dodge_vector = (away_from_bullet * 0.6 + perp * 0.4).normalize()
                
                # Combine threat pursuit with dodging (prioritize dodging if bullets are very close)
                if nearby_bullets and closest_dist < 15000:  # ~122 pixels squared
                    # Heavy dodge when bullet is very close
                    final_dir = dodge_vector * 1.5 + toward_threat * 0.3
                else:
                    # Normal pursuit with light dodging
                    final_dir = toward_threat * 0.9 + dodge_vector * 0.1
                
                if final_dir.length_squared() > 0:
                    final_dir = final_dir.normalize()
                
                # Update shield angle for shield enemies
                if e.get("has_shield"):
                    # Shield faces toward threat
                    if toward_threat.length_squared() > 0:
                        e["shield_angle"] = math.atan2(toward_threat.y, toward_threat.x)
                elif e.get("has_reflective_shield"):
                    # Reflective shield turns slowly toward threat
                    if toward_threat.length_squared() > 0:
                        target_angle = math.atan2(toward_threat.y, toward_threat.x)
                        current_angle = e.get("shield_angle", 0.0)
                        # Normalize angles
                        angle_diff = target_angle - current_angle
                        while angle_diff > math.pi:
                            angle_diff -= 2 * math.pi
                        while angle_diff < -math.pi:
                            angle_diff += 2 * math.pi
                        # Turn at limited speed
                        turn_speed = e.get("turn_speed", 0.5)
                        max_turn = turn_speed * dt
                        if abs(angle_diff) > max_turn:
                            e["shield_angle"] = current_angle + (max_turn if angle_diff > 0 else -max_turn)
                        else:
                            e["shield_angle"] = target_angle
                
                # Track enemy position for stuck detection
                if "last_position" not in e:
                    e["last_position"] = pygame.Vector2(e["rect"].center)
                    e["stuck_timer"] = 0.0
                
                current_pos = pygame.Vector2(e["rect"].center)
                distance_moved = current_pos.distance_to(e["last_position"])
                
                # Update stuck timer if enemy hasn't moved much
                if distance_moved < 5.0:  # Less than 5 pixels moved
                    e["stuck_timer"] += dt
                else:
                    e["stuck_timer"] = 0.0
                    e["last_position"] = current_pos
                
                # If stuck for 5 seconds, change direction away from obstacle
                if e["stuck_timer"] >= 5.0:
                    # Try to move away from current position (random direction)
                    escape_dir = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
                    if escape_dir.length_squared() > 0:
                        escape_dir = escape_dir.normalize()
                        final_dir = escape_dir  # Override movement direction
                        e["stuck_timer"] = 0.0  # Reset timer
                        e["last_position"] = current_pos  # Update position
                
                move_vec = final_dir * e["speed"] * dt
                dx_e = int(move_vec.x)
                dy_e = int(move_vec.y)
                
                if dx_e or dy_e:
                    # Enemies cannot go through objects and must navigate around them
                    # Pass cached block rects to avoid recreating lists
                    old_center = pygame.Vector2(e["rect"].center)
                    move_enemy_with_push_cached(e["rect"], dx_e, dy_e, blocks, 
                                                 cached_moveable_destructible_rects,
                                                 cached_trapezoid_rects,
                                                 cached_triangle_rects)
                    # Update last position after movement
                    new_center = pygame.Vector2(e["rect"].center)
                    if new_center.distance_to(old_center) > 5.0:
                        e["last_position"] = new_center
                        e["stuck_timer"] = 0.0

            # Check enemy collision with hazard obstacles (kill enemies)
            for e in enemies[:]:
                enemy_center = pygame.Vector2(e["rect"].center)
                for hazard in hazard_obstacles:
                    if check_point_in_hazard(enemy_center, hazard["points"], hazard["bounding_rect"]):
                        # Hazard kills enemy instantly
                        kill_enemy(e)
                        break

            # Check friendly AI collision with hazard obstacles (kill friendly AI)
            for f in friendly_ai[:]:
                friendly_center = pygame.Vector2(f["rect"].center)
                for hazard in hazard_obstacles:
                    if check_point_in_hazard(friendly_center, hazard["points"], hazard["bounding_rect"]):
                        # Hazard kills friendly AI instantly
                        if telemetry_enabled and telemetry:
                            telemetry.log_friendly_death(
                                FriendlyAIDeathEvent(
                                    t=run_time,
                                    friendly_type=f.get("type", "unknown"),
                                    x=f["rect"].x,
                                    y=f["rect"].y,
                                    killed_by="hazard",
                                )
                            )
                        friendly_ai.remove(f)
                        break

            # Cleanup: Remove any enemies that somehow got stuck with HP <= 0
            # This is a safety check to prevent enemies from getting stuck alive
            for e in enemies[:]:
                if e.get("hp", 1) <= 0:
                    kill_enemy(e)

            # Cleanup: Remove any friendly AI that somehow got stuck with HP <= 0
            # This is a safety check to prevent allies from getting stuck alive
            for f in friendly_ai[:]:
                if f.get("hp", 1) <= 0:
                    # Log friendly AI death if telemetry is enabled
                    if telemetry_enabled and telemetry:
                        telemetry.log_friendly_death(
                            FriendlyAIDeathEvent(
                                t=run_time,
                                friendly_type=f.get("type", "unknown"),
                                x=f["rect"].x,
                                y=f["rect"].y,
                                killed_by="damage",
                            )
                        )
                    friendly_ai.remove(f)

            # Friendly AI movement and behavior
            # Reuse block_rects from enemy movement (already computed above)
            for f in friendly_ai[:]:
                if f.get("hp", 1) <= 0:
                    friendly_ai.remove(f)
                    continue
                
                # Find target based on behavior
                f_pos = pygame.Vector2(f["rect"].center)
                target_enemy = find_nearest_enemy(f_pos)
                
                if target_enemy:
                    f["target"] = target_enemy
                    target_pos = pygame.Vector2(target_enemy["rect"].center)
                    dist_to_target = (target_pos - f_pos).length()
                    
                    # Behavior patterns
                    if f["behavior"] == "aggressive":
                        # Charge nearest enemy
                        move_dir = (target_pos - f_pos)
                        if move_dir.length_squared() > 0:
                            move_dir = move_dir.normalize()
                    elif f["behavior"] == "defensive":
                        # Stay near player, attack nearby enemies
                        player_pos = pygame.Vector2(player.center)
                        dist_to_player = (player_pos - f_pos).length()
                        if dist_to_target < 300 and dist_to_player < 200:
                            # Close to player and enemy nearby - attack
                            move_dir = (target_pos - f_pos)
                            if move_dir.length_squared() > 0:
                                move_dir = move_dir.normalize()
                        else:
                            # Return to player
                            move_dir = (player_pos - f_pos)
                            if move_dir.length_squared() > 0:
                                move_dir = move_dir.normalize() * 0.5  # Slower return
                    elif f["behavior"] == "ranged":
                        # Keep distance, snipe
                        if dist_to_target < 400:
                            # Too close, back away
                            move_dir = (f_pos - target_pos)
                            if move_dir.length_squared() > 0:
                                move_dir = move_dir.normalize()
                        else:
                            # Good distance, approach slowly
                            move_dir = (target_pos - f_pos)
                            if move_dir.length_squared() > 0:
                                move_dir = move_dir.normalize() * 0.3
                    elif f["behavior"] == "tank":
                        # Slow advance toward nearest enemy
                        move_dir = (target_pos - f_pos)
                        if move_dir.length_squared() > 0:
                            move_dir = move_dir.normalize() * 0.6
                    else:
                        # Default: follow player
                        player_pos = pygame.Vector2(player.center)
                        move_dir = (player_pos - f_pos)
                        if move_dir.length_squared() > 0:
                            move_dir = move_dir.normalize()
                else:
                    # No enemies, follow player
                    f["target"] = None
                    player_pos = pygame.Vector2(player.center)
                    move_dir = (player_pos - f_pos)
                    if move_dir.length_squared() > 0:
                        move_dir = move_dir.normalize() * 0.5
                
                # Apply movement
                if move_dir.length_squared() > 0:
                    move_vec = move_dir * f["speed"] * dt
                    dx_f = int(move_vec.x)
                    dy_f = int(move_vec.y)
                    if dx_f or dy_f:
                        if can_move_rect(f["rect"], dx_f, dy_f, block_rects):
                            f["rect"].x += dx_f
                            f["rect"].y += dy_f
                        else:
                            if dx_f and can_move_rect(f["rect"], dx_f, 0, block_rects):
                                f["rect"].x += dx_f
                            if dy_f and can_move_rect(f["rect"], 0, dy_f, block_rects):
                                f["rect"].y += dy_f
                        clamp_rect_to_screen(f["rect"])
                
                # Fix ally collision: push away from player if overlapping
                if f["rect"].colliderect(player):
                    player_center = pygame.Vector2(player.center)
                    friendly_center = pygame.Vector2(f["rect"].center)
                    separation_dir = friendly_center - player_center
                    if separation_dir.length_squared() > 0:
                        separation_dir = separation_dir.normalize()
                        # Push ally away from player
                        push_distance = 5.0  # Push 5 pixels per frame
                        push_vec = separation_dir * push_distance
                        f["rect"].x += int(push_vec.x)
                        f["rect"].y += int(push_vec.y)
                        clamp_rect_to_screen(f["rect"])

            # Position sampling
            pos_timer += dt
            if pos_timer >= POS_SAMPLE_INTERVAL:
                pos_timer -= POS_SAMPLE_INTERVAL
                telemetry.log_player_position(PlayerPosEvent(t=run_time, x=player.x, y=player.y))
                
                # Log player velocity
                telemetry.log_player_velocity(
                    PlayerVelocityEvent(
                        t=run_time,
                        x=player.x,
                        y=player.y,
                        vel_x=float(last_move_velocity.x),
                        vel_y=float(last_move_velocity.y),
                        speed=float(last_move_velocity.length()),
                    )
                )
                
                # Log enemy positions (reduced frequency for performance)
                # Only log every 3rd enemy to reduce telemetry overhead
                for i, e in enumerate(enemies):
                    if i % 3 == 0:  # Sample every 3rd enemy
                        e_pos = pygame.Vector2(e["rect"].center)
                        # Use cached player position
                        dir_vec = vec_toward(e["rect"].centerx, e["rect"].centery, player_pos_cached.x, player_pos_cached.y)
                        vel_vec = dir_vec * e["speed"]
                        telemetry.log_enemy_position(
                            EnemyPositionEvent(
                                t=run_time,
                                enemy_type=e["type"],
                                x=e["rect"].x,
                                y=e["rect"].y,
                                speed=float(e["speed"]),
                                vel_x=float(vel_vec.x),
                                vel_y=float(vel_vec.y),
                            )
                        )
                
                # Log friendly AI positions (reduced frequency for performance)
                # Only log every 2nd friendly to reduce telemetry overhead
                for i, f in enumerate(friendly_ai):
                    if i % 2 == 0:  # Sample every 2nd friendly
                        if f["target"]:
                            target_type = f["target"].get("type")
                            vel_vec = vec_toward(f["rect"].centerx, f["rect"].centery, f["target"]["rect"].centerx, f["target"]["rect"].centery) * f["speed"]
                        else:
                            target_type = None
                            vel_vec = pygame.Vector2(0, 0)
                        telemetry.log_friendly_position(
                            FriendlyAIPositionEvent(
                                t=run_time,
                                friendly_type=f["type"],
                                x=f["rect"].x,
                                y=f["rect"].y,
                                speed=float(f["speed"]),
                                vel_x=float(vel_vec.x),
                                vel_y=float(vel_vec.y),
                                target_enemy_type=target_type,
                            )
                        )

            # Friendly AI shooting
            for f in friendly_ai:
                f["time_since_shot"] += dt
                if f["target"] and f["time_since_shot"] >= f["shoot_cooldown"]:
                    # Check if target is still alive and in range
                    if f["target"] in enemies:
                        target_pos = pygame.Vector2(f["target"]["rect"].center)
                        f_pos = pygame.Vector2(f["rect"].center)
                        dist = (target_pos - f_pos).length()
                        # Shoot if in range (varies by behavior)
                        max_range = 600 if f["behavior"] == "ranged" else 400
                        if dist <= max_range:
                            spawn_friendly_projectile(f, f["target"])
                            f["time_since_shot"] = 0.0
                    else:
                        f["target"] = None

            # Enemy shooting and special behaviors
            for e in enemies:
                e["time_since_shot"] += dt
                
                # Queen-specific behaviors (grenades, shield, rage mode)
                if e.get("type") == "queen":
                    # Update rage mode timer
                    if e.get("rage_mode_active", False):
                        e["rage_mode_timer"] -= dt
                        if e["rage_mode_timer"] <= 0:
                            e["rage_mode_active"] = False
                    
                    # Update grenade cooldown
                    e["time_since_grenade"] = e.get("time_since_grenade", 999.0) + dt
                    
                    # Shield toggle logic (like shield enemy: 10-20s phases, active for 5-10s)
                    if e.get("has_shield", False):
                        # Initialize shield timing if not present
                        if "shield_toggle_timer" not in e:
                            e["shield_toggle_timer"] = random.uniform(10.0, 20.0)  # Random phase duration
                            e["shield_active"] = False
                            e["shield_active_duration"] = random.uniform(5.0, 10.0)  # Active duration
                            e["shield_active_timer"] = 0.0
                        
                        if e.get("shield_active", False):
                            # Shield is active - count down active timer
                            e["shield_active_timer"] += dt
                            if e["shield_active_timer"] >= e["shield_active_duration"]:
                                # Deactivate shield and start cooldown
                                e["shield_active"] = False
                                e["shield_toggle_timer"] = random.uniform(10.0, 20.0)  # Random cooldown
                                e["shield_active_timer"] = 0.0
                        else:
                            # Shield is inactive - count down toggle timer
                            e["shield_toggle_timer"] -= dt
                            if e["shield_toggle_timer"] <= 0:
                                # Activate shield
                                e["shield_active"] = True
                                e["shield_active_duration"] = random.uniform(5.0, 10.0)  # Random active duration
                                e["shield_active_timer"] = 0.0
                        
                        # Rotate shield to face player (only when active)
                        if e.get("shield_active", False):
                            player_pos = pygame.Vector2(player.center)
                            queen_pos = pygame.Vector2(e["rect"].center)
                            angle_to_player = math.atan2(player_pos.y - queen_pos.y, player_pos.x - queen_pos.x)
                            e["shield_angle"] = angle_to_player
                    
                    # Grenade logic: use grenade if player is close and cooldown ready, or in rage mode
                    if e.get("can_use_grenades", False):
                        player_pos = pygame.Vector2(player.center)
                        queen_pos = pygame.Vector2(e["rect"].center)
                        dist_to_player = (player_pos - queen_pos).length()
                        grenade_range = player.w * 10  # 10x player size (same as player grenade)
                        
                        # Use grenade if: (player close AND cooldown ready) OR (rage mode active AND cooldown ready)
                        if e["time_since_grenade"] >= e.get("grenade_cooldown", 5.0):
                            if dist_to_player <= grenade_range * 1.5 or e.get("rage_mode_active", False):
                                # Spawn grenade explosion
                                grenade_explosions.append({
                                    "center": pygame.Vector2(e["rect"].center),
                                    "radius": player.w * 10,
                                    "damage": grenade_damage,
                                    "timer": 0.3,
                                    "color": (255, 165, 0),  # Orange
                                    "damaged_enemies": set(),
                                    "damaged_blocks": set(),
                                    "damaged_player": False,  # Track if player was damaged
                                })
                                e["time_since_grenade"] = 0.0
                                
                                # In rage mode, destroy nearby destructible blocks
                                if e.get("rage_mode_active", False):
                                    for db in destructible_blocks[:]:
                                        block_center = pygame.Vector2(db["rect"].center)
                                        dist_to_block = (block_center - queen_pos).length()
                                        if dist_to_block <= grenade_range * 1.5 and db.get("is_destructible"):
                                            # Destroy block
                                            destructible_blocks.remove(db)
                                    for mdb in moveable_destructible_blocks[:]:
                                        block_center = pygame.Vector2(mdb["rect"].center)
                                        dist_to_block = (block_center - queen_pos).length()
                                        if dist_to_block <= grenade_range * 1.5 and mdb.get("is_destructible"):
                                            # Destroy block
                                            moveable_destructible_blocks.remove(mdb)
                
                # Patrol enemy: patrols the outside border of the map
                if e.get("is_patrol", False):
                    # Initialize patrol state if not present
                    if "patrol_side" not in e:
                        e["patrol_side"] = random.randint(0, 3)  # 0=top, 1=right, 2=bottom, 3=left
                        e["patrol_progress"] = random.uniform(0.0, 1.0)  # Random starting position
                    
                    # Calculate patrol position based on side and progress
                    border_margin = 20  # Distance from edge
                    patrol_speed = e.get("speed", 100) * dt * 0.001  # Convert to progress per frame
                    
                    if e["patrol_side"] == 0:  # Top
                        e["rect"].x = border_margin + (WIDTH - 2 * border_margin) * e["patrol_progress"]
                        e["rect"].y = border_margin
                        e["patrol_progress"] += patrol_speed
                        if e["patrol_progress"] >= 1.0:
                            e["patrol_side"] = 1  # Move to right side
                            e["patrol_progress"] = 0.0
                    elif e["patrol_side"] == 1:  # Right
                        e["rect"].x = WIDTH - border_margin - e["rect"].w
                        e["rect"].y = border_margin + (HEIGHT - 2 * border_margin) * e["patrol_progress"]
                        e["patrol_progress"] += patrol_speed
                        if e["patrol_progress"] >= 1.0:
                            e["patrol_side"] = 2  # Move to bottom side
                            e["patrol_progress"] = 0.0
                    elif e["patrol_side"] == 2:  # Bottom
                        e["rect"].x = WIDTH - border_margin - e["rect"].w - (WIDTH - 2 * border_margin) * e["patrol_progress"]
                        e["rect"].y = HEIGHT - border_margin - e["rect"].h
                        e["patrol_progress"] += patrol_speed
                        if e["patrol_progress"] >= 1.0:
                            e["patrol_side"] = 3  # Move to left side
                            e["patrol_progress"] = 0.0
                    else:  # Left
                        e["rect"].x = border_margin
                        e["rect"].y = HEIGHT - border_margin - e["rect"].h - (HEIGHT - 2 * border_margin) * e["patrol_progress"]
                        e["patrol_progress"] += patrol_speed
                        if e["patrol_progress"] >= 1.0:
                            e["patrol_side"] = 0  # Move to top side
                            e["patrol_progress"] = 0.0
                    
                    # Patrol enemy uses wave beam
                    if e.get("uses_wave_beam", False):
                        e["time_since_shot"] = e.get("time_since_shot", 999.0) + dt
                        if e["time_since_shot"] >= e.get("shoot_cooldown", 0.5):
                            # Fire wave beam toward player
                            player_pos = pygame.Vector2(player.center)
                            patrol_pos = pygame.Vector2(e["rect"].center)
                            direction = (player_pos - patrol_pos)
                            if direction.length_squared() > 0:
                                direction = direction.normalize()
                                # Spawn wave beam (similar to player wave beam)
                                wave_beam_points = generate_wave_beam_points(
                                    patrol_pos, direction, "sine", wave_beam_length, 
                                    amplitude=50.0, frequency=0.02, time_offset=run_time
                                )
                                wave_beams.append({
                                    "points": wave_beam_points,
                                    "color": e.get("projectile_color", (100, 255, 100)),
                                    "width": wave_beam_width,
                                    "damage": wave_beam_damage,
                                    "source_type": "patrol",
                                })
                                e["time_since_shot"] = 0.0
                
                # Spawner enemy: spawns enemies during round
                if e.get("is_spawner", False):
                    e["time_since_spawn"] = e.get("time_since_spawn", 0.0) + dt
                    spawn_count = e.get("spawn_count", 0)
                    max_spawns = e.get("max_spawns", 3)
                    
                    if e["time_since_spawn"] >= e.get("spawn_cooldown", 5.0) and spawn_count < max_spawns:
                        # Spawn a random enemy near the spawner
                        spawn_templates = [t for t in enemy_templates if t["type"] not in ["spawner", "queen"]]
                        if spawn_templates:
                            tmpl = random.choice(spawn_templates)
                            hp_scale = 1.0
                            speed_scale = 1.0
                            spawned_enemy = make_enemy_from_template(tmpl, hp_scale, speed_scale)
                            # Spawn near the spawner (within 100 pixels)
                            offset_x = random.randint(-100, 100)
                            offset_y = random.randint(-100, 100)
                            spawned_enemy["rect"].x = e["rect"].x + offset_x
                            spawned_enemy["rect"].y = e["rect"].y + offset_y
                            clamp_rect_to_screen(spawned_enemy["rect"])
                            enemies.append(spawned_enemy)
                            e["spawn_count"] = spawn_count + 1
                            e["time_since_spawn"] = 0.0
                            log_enemy_spawns([spawned_enemy])
                
                # Boss phase detection and special shooting
                if e.get("is_boss", False):
                    hp_ratio = e["hp"] / e["max_hp"]
                    # Check phase transitions
                    if e["phase"] == 1 and hp_ratio <= e["phase_hp_thresholds"][0]:
                        e["phase"] = 2
                        e["shoot_cooldown"] = 0.3  # Faster shooting in phase 2
                        e["color"] = (255, 100, 0)  # Orange
                    elif e["phase"] == 2 and hp_ratio <= e["phase_hp_thresholds"][1]:
                        e["phase"] = 3
                        e["shoot_cooldown"] = 0.15  # Very fast shooting in phase 3
                        e["color"] = (255, 0, 255)  # Magenta
                    
                    # Boss shooting patterns based on phase
                    if e["time_since_shot"] >= e["shoot_cooldown"]:
                        if e["phase"] == 1:
                            # Phase 1: Single shots
                            spawn_enemy_projectile(e)
                        elif e["phase"] == 2:
                            # Phase 2: Triple shot spread at nearest threat
                            e_pos = pygame.Vector2(e["rect"].center)
                            threat_result = find_nearest_threat(e_pos)
                            if threat_result:
                                threat_pos, _ = threat_result
                                base_dir = vec_toward(e_pos.x, e_pos.y, threat_pos.x, threat_pos.y)
                            else:
                                base_dir = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                            for angle in [-15, 0, 15]:
                                dir_vec = base_dir.rotate(angle)
                                spawn_boss_projectile(e, dir_vec)
                        elif e["phase"] == 3:
                            # Phase 3: 8-way spread (still targets nearest threat for base direction)
                            e_pos = pygame.Vector2(e["rect"].center)
                            threat_result = find_nearest_threat(e_pos)
                            if threat_result:
                                threat_pos, _ = threat_result
                                base_dir = vec_toward(e_pos.x, e_pos.y, threat_pos.x, threat_pos.y)
                            else:
                                base_dir = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                            for angle in range(0, 360, 45):
                                dir_vec = base_dir.rotate(angle)
                                spawn_boss_projectile(e, dir_vec)
                        e["time_since_shot"] = 0.0
                elif e["time_since_shot"] >= e["shoot_cooldown"]:
                    # Regular enemy shooting (non-boss)
                    # Reflective shield enemies don't shoot
                    if not e.get("has_reflective_shield", False):
                        # Predictive enemy: predicts player position
                        if e.get("predicts_player", False):
                            # Calculate predicted position based on player velocity
                            player_vel = last_move_velocity
                            player_pos = pygame.Vector2(player.center)
                            enemy_pos = pygame.Vector2(e["rect"].center)
                            
                            # Predict where player will be in ~0.5 seconds
                            prediction_time = 0.5
                            predicted_pos = player_pos + player_vel * prediction_time
                            
                            # Shoot at predicted position
                            dir_to_predicted = vec_toward(enemy_pos.x, enemy_pos.y, predicted_pos.x, predicted_pos.y)
                            spawn_enemy_projectile_predictive(e, dir_to_predicted)
                        else:
                            spawn_enemy_projectile(e)
                        e["time_since_shot"] = 0.0

            # Pickup spawning (affected by difficulty)
            if state == STATE_PLAYING or state == STATE_ENDURANCE:
                # Use cached multiplier if available, otherwise calculate
                if 'diff_mult' in locals():
                    effective_spawn_interval = PICKUP_SPAWN_INTERVAL / diff_mult["pickup_spawn"]
                else:
                    diff_mult = difficulty_multipliers[difficulty]
                    effective_spawn_interval = PICKUP_SPAWN_INTERVAL / diff_mult["pickup_spawn"]
            else:
                effective_spawn_interval = PICKUP_SPAWN_INTERVAL
            pickup_spawn_timer += dt
            if pickup_spawn_timer >= effective_spawn_interval:
                pickup_spawn_timer = 0.0
                # Randomize pickup type - player never knows what they'll get
                pickup_types = [
                    "boost",  # temporary boost meter refill
                    "firerate",  # temporary fire rate buff
                    "spawn_boost",  # enemy can grab, player can shoot
                    "health",  # restores 100 HP
                    "max_health",  # permanent max HP increase
                    "health_regen",  # increases health regeneration rate
                    "speed",  # permanent speed increase
                    "firerate_permanent",  # permanent fire rate increase
                    "bullet_size",  # permanent bullet size increase
                    "bullet_speed",  # permanent bullet speed increase
                    "bullet_damage",  # permanent bullet damage increase
                    "bullet_knockback",  # permanent knockback increase
                    "bullet_penetration",  # permanent penetration increase
                    "bullet_explosion",  # permanent explosion radius increase
                    "giant_bullets",  # 10x bullet size
                    "triple_shot",  # shoot 3 beams
                    "bouncing_bullets",  # bullets bounce off walls
                    "rocket_launcher",  # slower fire rate, more damage, AOE
                    "laser",  # laser beam weapon
                    "wave_beam",  # wave beam weapon (undulating lime green beam)
                    "overshield",  # adds overshield (extra health bar)
                    "random_damage",  # randomizes base damage multiplier (0.5x to 3.0x)
                ]
                spawn_pickup(random.choice(pickup_types))

            # Update pickup timers and remove expired pickups
            for p in pickups[:]:
                p["timer"] = p.get("timer", 15.0) - dt
                p["age"] = p.get("age", 0.0) + dt
                if p.get("timer", 15.0) <= 0.0:
                    pickups.remove(p)
                    continue

            # Pickup interactions
            for p in pickups[:]:
                pr = p["rect"]
                ptype = p["type"]

                # Player collects beneficial pickups
                if ptype != "spawn_boost" and pr.colliderect(player):
                    apply_pickup_effect(ptype)
                    # Create pickup collection effect (particles)
                    create_pickup_collection_effect(pr.centerx, pr.centery, p["color"])
                    pickups.remove(p)
                    continue

                # Enemies can collect spawn boost pickup
                if ptype == "spawn_boost":
                    grabbed = False
                    for e in enemies:
                        if pr.colliderect(e["rect"]):
                            enemy_spawn_boost_level = min(10, enemy_spawn_boost_level + 1)
                            # also make current wave a bit scarier by slightly reducing remaining respawn delay
                            wave_respawn_delay = max(0.8, wave_respawn_delay - 0.15)
                            grabbed = True
                            break
                    if grabbed:
                        pickups.remove(p)
                        continue

            # Friendly projectiles update
            for fp in friendly_projectiles[:]:
                fp["rect"].x += int(fp["vel"].x * dt)
                fp["rect"].y += int(fp["vel"].y * dt)
                
                if rect_offscreen(fp["rect"]):
                    friendly_projectiles.remove(fp)
                    continue
                
                # Check collision with enemies
                hit_enemy = None
                for e in enemies:
                    if fp["rect"].colliderect(e["rect"]):
                        hit_enemy = e
                        break
                
                if hit_enemy:
                    hit_enemy["hp"] -= fp["damage"]
                    damage_dealt += fp["damage"]
                    # Log friendly AI hit
                    telemetry.log_enemy_hit(
                        EnemyHitEvent(
                            t=run_time,
                            enemy_type=hit_enemy["type"],
                            enemy_x=hit_enemy["rect"].x,
                            enemy_y=hit_enemy["rect"].y,
                            damage=fp["damage"],
                            enemy_hp_after=hit_enemy["hp"],
                            killed=hit_enemy["hp"] <= 0,
                        )
                    )
                    if hit_enemy["hp"] <= 0:
                        kill_enemy(hit_enemy)
                    friendly_projectiles.remove(fp)
                    continue
                
                # Check collision with blocks
                for blk in blocks:
                    if fp["rect"].colliderect(blk["rect"]):
                        friendly_projectiles.remove(fp)
                        break
                
                # Check collision with trapezoid blocks
                for tb in trapezoid_blocks:
                    if fp["rect"].colliderect(tb["bounding_rect"]):
                        friendly_projectiles.remove(fp)
                        break
                
                # Check collision with triangle blocks
                for tr in triangle_blocks:
                    if fp["rect"].colliderect(tr["bounding_rect"]):
                        friendly_projectiles.remove(fp)
                        break
                
                # Check collision with moveable destructible blocks
                for mdb in moveable_destructible_blocks:
                    if fp["rect"].colliderect(mdb["rect"]):
                        friendly_projectiles.remove(fp)
                        break

            # Player bullets update
            # Use GPU acceleration for large batches (50+ bullets), CPU for smaller batches or complex logic
            use_gpu_bullets = USE_GPU and len(player_bullets) > 50
            
            if use_gpu_bullets:
                # GPU-accelerated position updates for simple bullets (no bouncing)
                simple_bullets = []
                complex_bullets = []
                
                # Separate bullets into simple (no bouncing) and complex (bouncing)
                for b in player_bullets:
                    if b.get("bounces", 0) == 0:
                        simple_bullets.append(b)
                    else:
                        complex_bullets.append(b)
                
                # Update simple bullets on GPU
                if simple_bullets:
                    bullets_data = []
                    bullet_indices = []
                    for i, b in enumerate(simple_bullets):
                        bullets_data.append({
                            'x': float(b["rect"].x),
                            'y': float(b["rect"].y),
                            'vx': float(b["vel"].x),
                            'vy': float(b["vel"].y),
                            'w': b["rect"].w,
                            'h': b["rect"].h
                        })
                        bullet_indices.append(i)
                    
                    # Update on GPU
                    keep_indices = update_bullets_batch(bullets_data, dt, WIDTH, HEIGHT)
                    
                    # Update bullet rects
                    new_simple_bullets = []
                    for idx in keep_indices:
                        if idx < len(simple_bullets):
                            b = simple_bullets[idx]
                            b["rect"].x = int(bullets_data[idx]['x'])
                            b["rect"].y = int(bullets_data[idx]['y'])
                            new_simple_bullets.append(b)
                    simple_bullets = new_simple_bullets
                
                # Update complex bullets (with bouncing) on CPU
                for b in complex_bullets[:]:
                    r = b["rect"]
                    v = b["vel"]
                    r.x += int(v.x * dt)
                    r.y += int(v.y * dt)

                    # Handle bouncing bullets
                    bounces_left = b.get("bounces", 0)
                    if bounces_left > 0:
                        bounced = False
                        if r.left < 0:
                            v.x = abs(v.x)
                            bounced = True
                        elif r.right > WIDTH:
                            v.x = -abs(v.x)
                            bounced = True
                        if r.top < 0:
                            v.y = abs(v.y)
                            bounced = True
                        elif r.bottom > HEIGHT:
                            v.y = -abs(v.y)
                            bounced = True
                        if bounced:
                            b["bounces"] = bounces_left - 1
                            b["vel"] = v
                            # Keep bullet on screen
                            r.x = max(0, min(r.x, WIDTH - r.w))
                            r.y = max(0, min(r.y, HEIGHT - r.h))

                    if rect_offscreen(r) and bounces_left == 0:
                        complex_bullets.remove(b)
                
                # Combine simple and complex bullets
                player_bullets[:] = simple_bullets + complex_bullets
                
                # Check for hazard collisions with all bullets (GPU path)
                for b in player_bullets[:]:
                    bullet_center = pygame.Vector2(b["rect"].center)
                    for hazard in hazard_obstacles:
                        if check_point_in_hazard(bullet_center, hazard["points"], hazard["bounding_rect"]):
                            # Push hazard in direction of bullet velocity
                            push_force = 150.0
                            push_dir = b["vel"]
                            if push_dir.length_squared() > 0:
                                push_dir = push_dir.normalize()
                                hazard["velocity"] += push_dir * push_force * dt
                            # Remove bullet after hitting hazard
                            if b in player_bullets:
                                player_bullets.remove(b)
                            break
            else:
                # CPU fallback for small batches or when GPU unavailable
                for b in player_bullets[:]:
                    r = b["rect"]
                    v = b["vel"]
                    r.x += int(v.x * dt)
                    r.y += int(v.y * dt)

                    # Handle bouncing bullets
                    bounces_left = b.get("bounces", 0)
                    if bounces_left > 0:
                        bounced = False
                        if r.left < 0:
                            v.x = abs(v.x)
                            bounced = True
                        elif r.right > WIDTH:
                            v.x = -abs(v.x)
                            bounced = True
                        if r.top < 0:
                            v.y = abs(v.y)
                            bounced = True
                        elif r.bottom > HEIGHT:
                            v.y = -abs(v.y)
                            bounced = True
                        if bounced:
                            b["bounces"] = bounces_left - 1
                            b["vel"] = v
                            # Keep bullet on screen
                            r.x = max(0, min(r.x, WIDTH - r.w))
                            r.y = max(0, min(r.y, HEIGHT - r.h))

                    if rect_offscreen(r) and bounces_left == 0:
                        if b in player_bullets:
                            player_bullets.remove(b)
                        continue

                    # Bullets can push hazard obstacles ("bully" them)
                    bullet_center = pygame.Vector2(r.center)
                    for hazard in hazard_obstacles:
                        if check_point_in_hazard(bullet_center, hazard["points"], hazard["bounding_rect"]):
                            # Push hazard in direction of bullet velocity
                            push_force = 150.0  # Force applied to hazard (increased for better effect)
                            push_dir = b["vel"]
                            if push_dir.length_squared() > 0:
                                push_dir = push_dir.normalize()
                                hazard["velocity"] += push_dir * push_force * dt
                            # Remove bullet after hitting hazard
                            if b in player_bullets:
                                player_bullets.remove(b)
                            break

                    # bullets can destroy spawn_boost pickups
                    hit_pickup = None
                    for p in pickups:
                        if p["type"] == "spawn_boost" and r.colliderect(p["rect"]):
                            hit_pickup = p
                            break
                    if hit_pickup is not None:
                        try:
                            pickups.remove(hit_pickup)
                        except ValueError:
                            pass
                        if b in player_bullets:
                            player_bullets.remove(b)
                            continue

                    # bullet hits enemy
                    hit_enemy_index = None
                    for i, e in enumerate(enemies):
                        if r.colliderect(e["rect"]):
                            hit_enemy_index = i
                            break

                    if hit_enemy_index is not None:
                        hits += 1
                        e = enemies[hit_enemy_index]
                        # Apply random damage multiplier to base damage
                        base_damage = b.get("damage", player_bullet_damage)
                        bullet_damage = int(base_damage * random_damage_multiplier)
                        
                        # Check for shield enemies
                        if e.get("has_shield"):
                            # Queen shield only blocks when active
                            if e.get("type") == "queen" and not e.get("shield_active", False):
                                # Queen shield inactive, allow damage through (fall through to damage code)
                                pass
                            else:
                                # Check if bullet hit the shield (front-facing line)
                                shield_angle = e.get("shield_angle", 0.0)
                                shield_length = e.get("shield_length", 50)
                                enemy_center = pygame.Vector2(e["rect"].center)
                                bullet_pos = pygame.Vector2(r.center)
                                
                                # Calculate shield line endpoints
                                shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                                shield_start = enemy_center + shield_dir * (e["rect"].w // 2)
                                shield_end = enemy_center + shield_dir * (e["rect"].w // 2 + shield_length)
                                
                                # Check if bullet is in front of enemy (shield side)
                                to_bullet = bullet_pos - enemy_center
                                dot_product = to_bullet.dot(shield_dir)
                                
                                if dot_product > 0:  # Bullet is in front
                                    # Check distance to shield line
                                    line_vec = shield_end - shield_start
                                    if line_vec.length_squared() > 0:
                                        t = max(0, min(1, (bullet_pos - shield_start).dot(line_vec) / line_vec.length_squared()))
                                        closest_point = shield_start + line_vec * t
                                        dist_to_shield = (bullet_pos - closest_point).length()
                                        
                                        if dist_to_shield < 15:  # Bullet hit shield
                                            # Shield blocks damage, remove bullet
                                            if b in player_bullets:
                                                player_bullets.remove(b)
                                            continue
                            
                            # Bullet hit from behind/side, apply damage normally
                            e["hp"] -= bullet_damage
                            damage_dealt += bullet_damage
                        elif e.get("has_reflective_shield"):
                            # Reflective shield - check if hit shield
                            shield_angle = e.get("shield_angle", 0.0)
                            shield_length = e.get("shield_length", 60)
                            enemy_center = pygame.Vector2(e["rect"].center)
                            bullet_pos = pygame.Vector2(r.center)
                            
                            shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                            shield_start = enemy_center + shield_dir * (e["rect"].w // 2)
                            shield_end = enemy_center + shield_dir * (e["rect"].w // 2 + shield_length)
                            
                            to_bullet = bullet_pos - enemy_center
                            dot_product = to_bullet.dot(shield_dir)
                            
                            if dot_product > 0:  # Bullet is in front
                                line_vec = shield_end - shield_start
                                if line_vec.length_squared() > 0:
                                    t = max(0, min(1, (bullet_pos - shield_start).dot(line_vec) / line_vec.length_squared()))
                                    closest_point = shield_start + line_vec * t
                                    dist_to_shield = (bullet_pos - closest_point).length()
                                    
                                    if dist_to_shield < 20:  # Bullet hit reflective shield
                                        # Reflect bullet back at player
                                        e["shield_hp"] += bullet_damage
                                        # Calculate reflection direction
                                        normal = -shield_dir  # Normal to shield
                                        incoming = b["vel"].normalize()
                                        reflected = incoming - 2 * incoming.dot(normal) * normal
                                        
                                        # Spawn reflected projectile
                                        reflected_proj = {
                                            "rect": pygame.Rect(r.x, r.y, r.w, r.h),
                                            "vel": reflected * b["vel"].length(),
                                            "enemy_type": "reflector",
                                            "color": (255, 200, 100),
                                            "shape": "circle",
                                            "bounces": 0,
                                        }
                                        enemy_projectiles.append(reflected_proj)
                                        if b in player_bullets:
                                            player_bullets.remove(b)
                                        continue
                            
                            # Bullet hit from behind/side, apply damage normally
                            e["hp"] -= bullet_damage
                            damage_dealt += bullet_damage
                            # Track damage for queen rage mode
                            if e.get("type") == "queen":
                                e["damage_taken_since_rage"] = e.get("damage_taken_since_rage", 0) + bullet_damage
                                # Activate rage mode if threshold reached
                                if not e.get("rage_mode_active", False) and e["damage_taken_since_rage"] >= e.get("rage_damage_threshold", 400):
                                    e["rage_mode_active"] = True
                                    e["rage_mode_timer"] = 5.0  # 5 seconds of rage mode
                                    e["damage_taken_since_rage"] = 0  # Reset counter
                            # Add damage number display
                            damage_numbers.append({
                                "x": e["rect"].centerx,
                                "y": e["rect"].y - 15,
                                "damage": bullet_damage,
                                "timer": 2.0,  # Display for 2 seconds
                                "color": (255, 100, 100),
                            })
                        else:
                            # Normal enemy, apply damage
                            e["hp"] -= bullet_damage
                            damage_dealt += bullet_damage
                            # Track damage for queen rage mode
                            if e.get("type") == "queen":
                                e["damage_taken_since_rage"] = e.get("damage_taken_since_rage", 0) + bullet_damage
                                # Activate rage mode if threshold reached
                                if not e.get("rage_mode_active", False) and e["damage_taken_since_rage"] >= e.get("rage_damage_threshold", 400):
                                    e["rage_mode_active"] = True
                                    e["rage_mode_timer"] = 5.0  # 5 seconds of rage mode
                                    e["damage_taken_since_rage"] = 0  # Reset counter
                            # Add damage number display
                            damage_numbers.append({
                                "x": e["rect"].centerx,
                                "y": e["rect"].y - 15,
                                "damage": bullet_damage,
                                "timer": 2.0,  # Display for 2 seconds
                                "color": (255, 100, 100),
                            })

                        # Apply knockback if available
                        knockback = b.get("knockback", 0.0)
                        if knockback > 0.0:
                            knockback_vec = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                            e["rect"].x += int(knockback_vec.x * knockback * 5)
                            e["rect"].y += int(knockback_vec.y * knockback * 5)
                            clamp_rect_to_screen(e["rect"])

                        # Handle explosion if available
                        explosion_radius = b.get("explosion_radius", 0.0)
                        if explosion_radius > 0.0:
                            exp_center = pygame.Vector2(b["rect"].center)
                            for other_e in enemies:
                                if other_e is e:
                                    continue
                                dist = pygame.Vector2(other_e["rect"].center).distance_to(exp_center)
                                if dist <= explosion_radius:
                                    # Damage falls off with distance
                                    exp_damage = int(bullet_damage * (1.0 - dist / explosion_radius) * 0.6)
                                    if exp_damage > 0:
                                        other_e["hp"] -= exp_damage
                                        damage_dealt += exp_damage
                                        # Log explosion hit
                                        if telemetry_enabled and telemetry:
                                            telemetry.log_enemy_hit(
                                                EnemyHitEvent(
                                                    t=run_time,
                                                    enemy_type=other_e["type"],
                                                    enemy_x=other_e["rect"].x,
                                                    enemy_y=other_e["rect"].y,
                                                    damage=exp_damage,
                                                    enemy_hp_after=max(0, other_e["hp"]),
                                                    killed=other_e["hp"] <= 0,
                                                )
                                            )
                                        if other_e["hp"] <= 0:
                                            kill_enemy(other_e)

                        killed = e["hp"] <= 0
                        hp_after = max(0, e["hp"])

                        if telemetry_enabled and telemetry:
                            telemetry.log_enemy_hit(
                                EnemyHitEvent(
                                    t=run_time,
                                    enemy_type=e["type"],
                                    enemy_x=e["rect"].x,
                                    enemy_y=e["rect"].y,
                                    damage=bullet_damage,
                                    enemy_hp_after=hp_after,
                                    killed=killed,
                                )
                            )

                        # Handle penetration
                        penetration = b.get("penetration", 0)
                        if penetration > 0:
                            # Bullet can pierce through
                            b["penetration"] = penetration - 1
                            # Continue to next enemy if penetration remains
                            if b["penetration"] > 0:
                                continue
                        else:
                            # No penetration left, remove bullet
                            if b in player_bullets:
                                player_bullets.remove(b)

                        if killed:
                            # Suicide enemies despawn immediately when killed (no drops)
                            if e.get("is_suicide", False):
                                if e in enemies:
                                    enemies.remove(e)
                            else:
                                kill_enemy(e)

                        # If bullet was removed, continue to next bullet
                        if b not in player_bullets:
                            continue

                    # bullets interact with indestructible blocks
                    for blk in blocks:
                        if r.colliderect(blk["rect"]):
                            # Bouncing bullets can bounce off blocks too
                            if b.get("bounces", 0) > 0:
                                # Simple bounce: reverse velocity
                                b["vel"] = -b["vel"]
                                b["bounces"] = b.get("bounces", 0) - 1
                            else:
                                if b in player_bullets:
                                    player_bullets.remove(b)
                            break
                    
                    # Bullets interact with trapezoid blocks
                    for tb in trapezoid_blocks:
                        if r.colliderect(tb["bounding_rect"]):
                            # Bouncing bullets can bounce off trapezoids too
                            if b.get("bounces", 0) > 0:
                                # Simple bounce: reverse velocity
                                b["vel"] = -b["vel"]
                                b["bounces"] = b.get("bounces", 0) - 1
                            else:
                                if b in player_bullets:
                                    player_bullets.remove(b)
                                break
                    
                    # Bullets interact with triangle blocks
                    for tr in triangle_blocks:
                        if r.colliderect(tr["bounding_rect"]):
                            # Bouncing bullets can bounce off triangles too
                            if b.get("bounces", 0) > 0:
                                # Simple bounce: reverse velocity
                                b["vel"] = -b["vel"]
                                b["bounces"] = b.get("bounces", 0) - 1
                            else:
                                if b in player_bullets:
                                    player_bullets.remove(b)
                                break
                    
                    # Player bullets can destroy destructible blocks
                    for db in destructible_blocks[:]:
                        if r.colliderect(db["rect"]):
                            if db.get("is_destructible") and "hp" in db:
                                # Apply random damage multiplier to base damage
                                base_damage = b.get("damage", player_bullet_damage)
                                bullet_damage = int(base_damage * random_damage_multiplier)
                                db["hp"] -= bullet_damage
                                if db["hp"] <= 0:
                                    destructible_blocks.remove(db)
                            # Remove bullet unless it has penetration
                            if b.get("penetration", 0) == 0 and b in player_bullets:
                                player_bullets.remove(b)
                            break
                    
                    # Player bullets can destroy moveable destructible blocks
                    for mdb in moveable_destructible_blocks[:]:
                        if r.colliderect(mdb["rect"]):
                            if mdb.get("is_destructible") and "hp" in mdb:
                                bullet_damage = b.get("damage", player_bullet_damage)
                                mdb["hp"] -= bullet_damage
                                if mdb["hp"] <= 0:
                                    moveable_destructible_blocks.remove(mdb)
                            # Remove bullet unless it has penetration
                            if b.get("penetration", 0) == 0 and b in player_bullets:
                                player_bullets.remove(b)
                            break
                    if b not in player_bullets:
                        continue

            # Enemy projectiles update
            for p in enemy_projectiles[:]:
                r = p["rect"]
                v = p["vel"]
                r.x += int(v.x * dt)
                r.y += int(v.y * dt)

                # Handle bouncing enemy projectiles
                bounces_left = p.get("bounces", 0)
                if bounces_left > 0:
                    bounced = False
                    if r.left < 0:
                        v.x = abs(v.x)
                        bounced = True
                    elif r.right > WIDTH:
                        v.x = -abs(v.x)
                        bounced = True
                    if r.top < 0:
                        v.y = abs(v.y)
                        bounced = True
                    elif r.bottom > HEIGHT:
                        v.y = -abs(v.y)
                        bounced = True
                    if bounced:
                        p["bounces"] = bounces_left - 1
                        p["vel"] = v
                        # Keep projectile on screen
                        r.x = max(0, min(r.x, WIDTH - r.w))
                        r.y = max(0, min(r.y, HEIGHT - r.h))

                if rect_offscreen(r) and bounces_left == 0:
                    if p in enemy_projectiles:
                        enemy_projectiles.remove(p)
                    continue

                # Enemy projectiles can damage destructible blocks
                for db in destructible_blocks[:]:
                    if r.colliderect(db["rect"]):
                        if db.get("is_destructible") and "hp" in db:
                            db["hp"] -= enemy_projectile_damage
                            if db["hp"] <= 0:
                                destructible_blocks.remove(db)
                        if p in enemy_projectiles:
                            enemy_projectiles.remove(p)
                        break
                if p not in enemy_projectiles:
                    continue
                
                # Enemy projectiles can damage moveable destructible blocks
                for mdb in moveable_destructible_blocks[:]:
                    if r.colliderect(mdb["rect"]):
                        if mdb.get("is_destructible") and "hp" in mdb:
                            mdb["hp"] -= enemy_projectile_damage
                            if mdb["hp"] <= 0:
                                moveable_destructible_blocks.remove(mdb)
                        if p in enemy_projectiles:
                            enemy_projectiles.remove(p)
                        break
                if p not in enemy_projectiles:
                    continue

                # Check collision with friendly AI first
                hit_friendly = None
                for f in friendly_ai:
                    if r.colliderect(f["rect"]):
                        hit_friendly = f
                        break
                
                if hit_friendly:
                    hit_friendly["hp"] -= enemy_projectile_damage
                    if hit_friendly["hp"] <= 0:
                        # Log friendly AI death
                        telemetry.log_friendly_death(
                            FriendlyAIDeathEvent(
                                t=run_time,
                                friendly_type=hit_friendly["type"],
                                x=hit_friendly["rect"].x,
                                y=hit_friendly["rect"].y,
                                killed_by="enemy_projectile",
                            )
                        )
                        friendly_ai.remove(hit_friendly)
                    if p in enemy_projectiles:
                        enemy_projectiles.remove(p)
                    continue

                if r.colliderect(player):
                    # Check if shield is active - shield blocks all damage
                    if shield_active:
                        # Shield blocks the projectile
                        if p in enemy_projectiles:
                            enemy_projectiles.remove(p)
                        continue
                    
                    # apply damage - overshield absorbs damage first
                    remaining_damage = enemy_projectile_damage
                    if overshield > 0:
                        if overshield >= remaining_damage:
                            overshield -= remaining_damage
                            remaining_damage = 0
                        else:
                            remaining_damage -= overshield
                            overshield = 0
                    
                    # Apply remaining damage to player HP
                    if remaining_damage > 0:
                        player_hp -= remaining_damage
                    damage_taken += enemy_projectile_damage
                    wave_damage_taken += enemy_projectile_damage  # Track for side quests

                    if player_hp < 0:
                        player_hp = 0

                    telemetry.log_player_damage(
                        PlayerDamageEvent(
                            t=run_time,
                            amount=enemy_projectile_damage,
                            source_type="enemy_projectile",
                            source_enemy_type=p.get("enemy_type"),
                            player_x=player.x,
                            player_y=player.y,
                            player_hp_after=player_hp,
                        )
                    )

                    if p in enemy_projectiles:
                        enemy_projectiles.remove(p)

                    # death handling
                    if player_hp <= 0:
                        deaths += 1
                        lives -= 1

                        telemetry.log_player_death(
                            PlayerDeathEvent(
                                t=run_time,
                                player_x=player.x,
                                player_y=player.y,
                                lives_left=lives,
                            )
                        )

                        if lives > 0:
                            state = STATE_CONTINUE
                            continue_blink_t = 0.0
                            continue
                        else:
                            # Game over - check if it's a high score
                            final_score_for_high_score = score
                            if is_high_score(score):
                                state = STATE_NAME_INPUT
                                player_name_input = ""
                                name_input_active = True
                            else:
                                state = STATE_GAME_OVER

                    continue

                # projectiles collide with blocks
                for blk in blocks:
                    if r.colliderect(blk["rect"]):
                        if p in enemy_projectiles:
                            enemy_projectiles.remove(p)
                        break
                
                # Enemy projectiles collide with trapezoid blocks
                for tb in trapezoid_blocks:
                    if r.colliderect(tb["bounding_rect"]):
                        if p in enemy_projectiles:
                            enemy_projectiles.remove(p)
                        break
                
                # Enemy projectiles collide with triangle blocks
                for tr in triangle_blocks:
                    if r.colliderect(tr["bounding_rect"]):
                        if p in enemy_projectiles:
                            enemy_projectiles.remove(p)
                        break
                
                # Enemy projectiles also collide with moveable destructible blocks (non-bouncing only)
                if bounces_left == 0:
                    for mdb in moveable_destructible_blocks:
                        if r.colliderect(mdb["rect"]):
                            if p in enemy_projectiles:
                                enemy_projectiles.remove(p)
                            break

            # Update grenade explosions
            # Update missiles (seeking enemies)
            for missile in missiles[:]:
                # Update target if enemy is still alive, otherwise find new target
                if missile["target_enemy"] not in enemies:
                    # Find new nearest enemy
                    missile_center = pygame.Vector2(missile["rect"].center)
                    nearest_enemy = None
                    nearest_dist = float("inf")
                    for e in enemies:
                        enemy_center = pygame.Vector2(e["rect"].center)
                        dist = missile_center.distance_to(enemy_center)
                        if dist < nearest_dist:
                            nearest_dist = dist
                            nearest_enemy = e
                    
                    if nearest_enemy:
                        missile["target_enemy"] = nearest_enemy
                    else:
                        # No enemies left, remove missile
                        missiles.remove(missile)
                        continue
                
                # Update missile velocity to seek target
                missile_center = pygame.Vector2(missile["rect"].center)
                target_center = pygame.Vector2(missile["target_enemy"]["rect"].center)
                direction = (target_center - missile_center)
                if direction.length() > 0:
                    direction = direction.normalize()
                    missile["vel"] = direction * missile["speed"]
                
                # Move missile
                missile["rect"].x += int(missile["vel"].x * dt)
                missile["rect"].y += int(missile["vel"].y * dt)
                
                # Check collision with target enemy
                if missile["rect"].colliderect(missile["target_enemy"]["rect"]):
                    # Explode on contact
                    exp_center = pygame.Vector2(missile["rect"].center)
                    grenade_explosions.append({
                        "x": exp_center.x,
                        "y": exp_center.y,
                        "radius": missile["explosion_radius"],
                        "timer": 0.3,
                        "damage": missile["damage"],
                        "damaged_enemies": set(),
                        "damaged_blocks": set(),
                        "source": "player"  # Player missiles don't damage player
                    })
                    missiles.remove(missile)
                    continue
                
                # Remove if off screen
                if rect_offscreen(missile["rect"]):
                    missiles.remove(missile)
                    continue
            
            for exp in grenade_explosions[:]:
                exp["timer"] -= dt
                
                # Handle different grenade explosion formats
                if "max_radius" in exp:
                    # Player grenades: expand from 0 to max_radius over 0.3 seconds
                    exp["radius"] = int(exp["max_radius"] * (1.0 - exp["timer"] / 0.3))
                elif "radius" not in exp:
                    # If radius doesn't exist, set a default
                    exp["radius"] = 150
                # Otherwise, radius is already set (queen/suicide enemy grenades)
                
                if exp["timer"] <= 0:
                    grenade_explosions.remove(exp)
                    continue
                
                # Get explosion center (handle both old and new format)
                if "center" in exp:
                    exp_center = exp["center"]
                else:
                    exp_center = pygame.Vector2(exp["x"], exp["y"])
                
                # Apply damage to player (if not already damaged by this explosion and not from player)
                if not exp.get("damaged_player", False) and exp.get("source") != "player":
                    player_center = pygame.Vector2(player.center)
                    dist_to_player = exp_center.distance_to(player_center)
                    if dist_to_player <= exp["radius"]:
                        player_hp -= exp["damage"]
                        wave_damage_taken += exp["damage"]  # Track for side quests
                        exp["damaged_player"] = True
                        damage_numbers.append({
                            "x": player.centerx,
                            "y": player.y - 15,
                            "damage": exp["damage"],
                            "timer": 2.0,
                            "color": (255, 165, 0),
                        })
                        # Log player damage
                        if telemetry_enabled and telemetry:
                            telemetry.log_player_damage(PlayerDamageEvent(
                                t=run_time,
                                damage=exp["damage"],
                                source="queen_grenade",
                                player_hp_after=player_hp,
                            ))
                
                # Apply damage to enemies in radius (only once per explosion)
                for e in enemies[:]:
                    if id(e) in exp["damaged_enemies"]:
                        continue  # Already damaged
                    
                    enemy_center = pygame.Vector2(e["rect"].center)
                    dist = exp_center.distance_to(enemy_center)
                    
                    if dist <= exp["radius"]:
                        # Enemy is in explosion radius
                        e["hp"] -= exp["damage"]
                        damage_dealt += exp["damage"]
                        exp["damaged_enemies"].add(id(e))
                        
                        # Add damage number display
                        damage_numbers.append({
                            "x": e["rect"].centerx,
                            "y": e["rect"].y - 15,
                            "damage": exp["damage"],
                            "timer": 2.0,
                            "color": (255, 200, 0),  # Orange/yellow for grenade damage
                        })
                        
                        if e["hp"] <= 0:
                            kill_enemy(e)
                
                # Apply damage to destructible blocks
                for db in destructible_blocks[:]:
                    if id(db) in exp["damaged_blocks"]:
                        continue
                    
                    block_center = pygame.Vector2(db["rect"].center)
                    dist = exp_center.distance_to(block_center)
                    
                    if dist <= exp["radius"]:
                        if db.get("is_destructible") and "hp" in db:
                            db["hp"] -= exp["damage"]
                            exp["damaged_blocks"].add(id(db))
                            if db["hp"] <= 0:
                                destructible_blocks.remove(db)
                
                # Apply damage to moveable destructible blocks
                for mdb in moveable_destructible_blocks[:]:
                    if id(mdb) in exp["damaged_blocks"]:
                        continue
                    
                    block_center = pygame.Vector2(mdb["rect"].center)
                    dist = exp_center.distance_to(block_center)
                    
                    if dist <= exp["radius"]:
                        if mdb.get("is_destructible") and "hp" in mdb:
                            mdb["hp"] -= exp["damage"]
                            exp["damaged_blocks"].add(id(mdb))
                            if mdb["hp"] <= 0:
                                moveable_destructible_blocks.remove(mdb)

            telemetry.tick(dt)

        else:
            # allow background flush timing while paused/continue screen
            if telemetry_enabled and telemetry:
                telemetry.tick(dt_real)

        # --- Draw ---
        # Apply level theme
        theme = level_themes.get(current_level, level_themes[1])
        screen.fill(theme["bg_color"])
        
        # Victory screen - all levels completed!
        if state == STATE_VICTORY:
            theme = level_themes.get(current_level, level_themes[1])
            screen.fill(theme["bg_color"])
            draw_centered_text("VICTORY!", 200, (100, 255, 100), use_big=True)
            draw_centered_text("All Levels Completed!", 280, (150, 255, 150))
            draw_centered_text(f"Final Score: {score:,}", 350, (255, 255, 100))
            draw_centered_text(f"Levels Completed: {max_level}", 400, (200, 200, 255))
            draw_centered_text(f"Time Survived: {int(survival_time//60)}m {int(survival_time%60)}s", 450, (200, 200, 255))
            draw_centered_text("Press E for Endurance Mode", 550, (100, 255, 100))
            draw_centered_text("Press ESC to Quit", 600, (200, 200, 200))
            pygame.display.flip()
            continue
        
        # Name input screen (for high scores)
        if state == STATE_NAME_INPUT:
            theme = level_themes.get(current_level, level_themes[1])
            screen.fill(theme["bg_color"])
            draw_centered_text("NEW HIGH SCORE!", 150, (255, 255, 100), use_big=True)
            draw_centered_text(f"Score: {final_score_for_high_score:,}", 220, (255, 255, 255))
            draw_centered_text("Enter your name:", 280, (200, 200, 255))
            # Draw name input with blinking cursor
            name_display = player_name_input + ("_" if int(pygame.time.get_ticks() / 500) % 2 == 0 else " ")
            draw_centered_text(name_display, 330, (255, 255, 255), use_big=True)
            draw_centered_text("Press ENTER to submit", 400, (150, 255, 150))
            draw_centered_text("Press ESC to skip", 450, (200, 200, 200))
            pygame.display.flip()
            continue
        
        # High score board screen
        if state == STATE_HIGH_SCORES:
            theme = level_themes.get(current_level, level_themes[1])
            screen.fill(theme["bg_color"])
            draw_centered_text("HIGH SCORES", 80, (255, 255, 100), use_big=True)
            scores = get_high_scores(10)
            y_offset = 150
            for i, hs in enumerate(scores, 1):
                name_text = f"{i}. {hs['name'][:15]:<15}"
                score_text = f"{hs['score']:,}"
                waves_text = f"Waves: {hs['waves']}"
                time_text = f"Time: {int(hs['time']//60)}m {int(hs['time']%60)}s"
                # Highlight if this is the current score
                color = (255, 255, 200) if (hs['score'] == final_score_for_high_score and i <= len(scores)) else (200, 200, 255)
                draw_centered_text(f"{name_text} {score_text:>10}  {waves_text}  {time_text}", y_offset, color)
                y_offset += 35
            if len(scores) == 0:
                draw_centered_text("No high scores yet!", 300, (200, 200, 200))
            draw_centered_text("Press ENTER, SPACE, or E to continue", 550, (150, 255, 150))
            draw_centered_text("Press ESC to Quit", 600, (200, 200, 200))
            pygame.display.flip()
            continue
        
        # Game Over screen
        if state == STATE_GAME_OVER:
            theme = level_themes.get(current_level, level_themes[1])
            screen.fill(theme["bg_color"])
            draw_centered_text("GAME OVER", 200, (255, 100, 100), use_big=True)
            draw_centered_text(f"Final Score: {score:,}", 300, (255, 255, 100))
            draw_centered_text(f"Waves Survived: {wave_number - 1}", 350, (200, 200, 255))
            draw_centered_text(f"Time Survived: {int(survival_time//60)}m {int(survival_time%60)}s", 400, (200, 200, 255))
            draw_centered_text("Press E for Endurance Mode", 550, (100, 255, 100))
            draw_centered_text("Press ESC to Quit", 600, (200, 200, 200))
            pygame.display.flip()
            continue
        
        # Menu screen
        if state == STATE_MENU:
            draw_centered_text("MOUSE AIM SHOOTER", 150, (255, 255, 255), use_big=True)
            
            # Menu sections: 0 = difficulty, 1 = aiming, 2 = class, 3 = options, 4 = start
            if menu_section == 0:
                draw_centered_text("Select Difficulty", 250, (200, 200, 200))
                y_start = 350
                for i, diff_option in enumerate(difficulty_options):
                    color = (255, 255, 100) if i == difficulty_selected else (150, 150, 150)
                    prefix = "> " if i == difficulty_selected else "  "
                    draw_centered_text(f"{prefix}{diff_option}", y_start + i * 50, color)
                draw_centered_text("Press UP/DOWN to select, RIGHT to continue", 600, (150, 150, 150))
            elif menu_section == 1:
                draw_centered_text("Select Aiming Mode", 250, (200, 200, 200))
                aiming_options = ["Mouse", "Arrow Keys"]
                y_start = 350
                for i, aim_option in enumerate(aiming_options):
                    color = (255, 255, 100) if i == aiming_mode_selected else (150, 150, 150)
                    prefix = "> " if i == aiming_mode_selected else "  "
                    draw_centered_text(f"{prefix}{aim_option}", y_start + i * 50, color)
                draw_centered_text("Press UP/DOWN to select, RIGHT to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 1.5:
                draw_centered_text("Use Character Profile?", 250, (200, 200, 200))
                profile_options = ["No", "Yes"]
                y_start = 350
                for i, option in enumerate(profile_options):
                    color = (255, 255, 100) if i == use_character_profile_selected else (150, 150, 150)
                    prefix = "> " if i == use_character_profile_selected else "  "
                    draw_centered_text(f"{prefix}{option}", y_start + i * 50, color)
                draw_centered_text("Press UP/DOWN to select, RIGHT/ENTER/SPACE to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 2:
                draw_centered_text("Character Profile", 250, (200, 200, 200))
                y_start = 350
                for i, profile_option in enumerate(character_profile_options):
                    color = (255, 255, 100) if i == character_profile_selected else (150, 150, 150)
                    prefix = "> " if i == character_profile_selected else "  "
                    draw_centered_text(f"{prefix}{profile_option}", y_start + i * 50, color)
                draw_centered_text("Press UP/DOWN to select, RIGHT/ENTER/SPACE to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 6:
                # Custom character profile creator
                draw_centered_text("Custom Character Profile", 200, (255, 200, 100))
                y_start = 300
                for i, stat_name in enumerate(custom_profile_stats_list):
                    stat_key = custom_profile_stats_keys[i]
                    stat_value = custom_profile_stats[stat_key]
                    color = (255, 255, 100) if i == custom_profile_stat_selected else (150, 150, 150)
                    prefix = "> " if i == custom_profile_stat_selected else "  "
                    draw_centered_text(f"{prefix}{stat_name}: {stat_value:.1f}x", y_start + i * 40, color)
                draw_centered_text("Press UP/DOWN to select, LEFT/- to decrease, +/- to increase, RIGHT/ENTER to continue, BACKSPACE to go back", 550, (150, 150, 150))
            elif menu_section == 7:
                draw_centered_text("Select Player Class", 250, (200, 200, 200))
                class_names = ["Balanced", "Tank", "Speedster", "Sniper"]
                y_start = 350
                for i, class_name in enumerate(class_names):
                    color = (255, 255, 100) if i == player_class_selected else (150, 150, 150)
                    prefix = "> " if i == player_class_selected else "  "
                    draw_centered_text(f"{prefix}{class_name}", y_start + i * 50, color)
                # Show class stats
                selected_class = player_class_options[player_class_selected]
                stats = player_class_stats[selected_class]
                draw_centered_text(f"HP: {stats['hp_mult']:.1f}x | Speed: {stats['speed_mult']:.1f}x | Damage: {stats['damage_mult']:.1f}x | Fire Rate: {stats['firerate_mult']:.1f}x", 550, (150, 150, 255))
                draw_centered_text("Press UP/DOWN to select, RIGHT to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 3:
                # HUD options page
                draw_centered_text("HUD Options", 250, (200, 200, 200))
                hud_options = ["Show HUD", "Hide HUD"]
                y_start = 350
                for i, opt in enumerate(hud_options):
                    option_color = (255, 255, 100) if i == ui_show_metrics_selected else (150, 150, 150)
                    option_prefix = "> " if i == ui_show_metrics_selected else "  "
                    draw_centered_text(f"{option_prefix}{opt}", y_start + i * 50, option_color)
                draw_centered_text("Press UP/DOWN to select, ENTER/SPACE to toggle, RIGHT to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 3.5:
                # Telemetry options page
                draw_centered_text("Telemetry Options", 250, (200, 200, 200))
                telemetry_options = ["Enable Telemetry", "Disable Telemetry"]
                y_start = 350
                for i, opt in enumerate(telemetry_options):
                    option_color = (255, 255, 100) if i == ui_telemetry_enabled_selected else (150, 150, 150)
                    option_prefix = "> " if i == ui_telemetry_enabled_selected else "  "
                    draw_centered_text(f"{option_prefix}{opt}", y_start + i * 50, option_color)
                draw_centered_text("Press UP/DOWN to select, ENTER/SPACE to toggle, RIGHT to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 4:
                draw_centered_text("Weapon Selection (Testing)", 250, (200, 200, 200))
                y_start = 320
                for i, weapon in enumerate(weapon_selection_options):
                    color = (255, 255, 100) if i == beam_selection_selected else (150, 150, 150)
                    prefix = "> " if i == beam_selection_selected else "  "
                    weapon_display = weapon.replace("_", " ").upper()
                    draw_centered_text(f"{prefix}{weapon_display}", y_start + i * 40, color)
                draw_centered_text("Press UP/DOWN to select, RIGHT to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 5:
                draw_centered_text("Ready to Start", 250, (100, 255, 100))
                draw_centered_text(f"Difficulty: {difficulty_options[difficulty_selected]}", 300, (200, 200, 200))
                draw_centered_text(f"Aiming: {['Mouse', 'Arrow Keys'][aiming_mode_selected]}", 340, (200, 200, 200))
                if use_character_profile:
                    if character_profile_selected == 0:
                        draw_centered_text(f"Class: {['Balanced', 'Tank', 'Speedster', 'Sniper'][player_class_selected]}", 380, (200, 200, 200))
                    else:
                        draw_centered_text("Class: Custom Profile", 380, (200, 200, 200))
                else:
                    draw_centered_text(f"Class: {['Balanced', 'Tank', 'Speedster', 'Sniper'][player_class_selected]}", 380, (200, 200, 200))
                draw_centered_text(f"HUD: {['Show', 'Hide'][ui_show_metrics_selected]}", 420, (200, 200, 200))
                draw_centered_text(f"Telemetry: {['Enabled', 'Disabled'][ui_telemetry_enabled_selected]}", 460, (200, 200, 200))
                selected_weapon_display = weapon_selection_options[beam_selection_selected].replace("_", " ").upper()
                draw_centered_text(f"Weapon: {selected_weapon_display}", 500, (200, 200, 200))
                # Endurance mode selection
                endurance_color = (255, 255, 100) if endurance_mode_selected == 1 else (200, 200, 200)
                endurance_prefix = "> " if endurance_mode_selected == 1 else "  "
                draw_centered_text(f"{endurance_prefix}Mode: {['Normal', 'Endurance Mode'][endurance_mode_selected]}", 560, endurance_color)
                draw_centered_text("Press UP/DOWN to select mode, ENTER/SPACEBAR to Start! :D", 620, (100, 255, 100))
                draw_centered_text("Press LEFT to go back, ESC to Quit", 680, (150, 150, 150))
            
            pygame.display.flip()
            continue

        # Draw trapezoid blocks hanging off screen edges (draw first so they appear behind other blocks)
        # Use cached surfaces for static geometry
        for tb in trapezoid_blocks:
            # Create cache key based on block ID (use id() or a unique identifier)
            block_id = id(tb)
            if block_id not in _cached_trapezoid_surfaces:
                # Create cached surface for this trapezoid
                # Calculate bounding box (handle both tuples and Vector2 objects)
                if tb["points"]:
                    min_x = min(int(p.x) if hasattr(p, 'x') else p[0] for p in tb["points"])
                    max_x = max(int(p.x) if hasattr(p, 'x') else p[0] for p in tb["points"])
                    min_y = min(int(p.y) if hasattr(p, 'y') else p[1] for p in tb["points"])
                    max_y = max(int(p.y) if hasattr(p, 'y') else p[1] for p in tb["points"])
                    surf_w = max_x - min_x + 10
                    surf_h = max_y - min_y + 10
                    cached_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
                    # Draw to cached surface (offset points to surface coordinates)
                    offset_points = []
                    for p in tb["points"]:
                        if hasattr(p, 'x'):
                            offset_points.append((int(p.x) - min_x + 5, int(p.y) - min_y + 5))
                        else:
                            offset_points.append((p[0] - min_x + 5, p[1] - min_y + 5))
                    pygame.draw.polygon(cached_surf, tb["color"], offset_points)
                    pygame.draw.polygon(cached_surf, (255, 255, 255), offset_points, 3)
                    # Draw pattern lines
                    if len(offset_points) >= 2:
                        for i in range(0, len(offset_points) - 1):
                            pattern_color = (tb["color"][0] + 20, tb["color"][1] + 20, tb["color"][2] + 20)
                            pygame.draw.line(cached_surf, pattern_color, offset_points[i], offset_points[i + 1], 2)
                    _cached_trapezoid_surfaces[block_id] = (cached_surf, (min_x - 5, min_y - 5))
            
            # Blit cached surface
            if block_id in _cached_trapezoid_surfaces:
                cached_surf, offset = _cached_trapezoid_surfaces[block_id]
                screen.blit(cached_surf, offset)
        
        # Draw triangle blocks (decorative border elements)
        for tr in triangle_blocks:
            # Create cache key based on block ID
            block_id = id(tr)
            if block_id not in _cached_triangle_surfaces:
                # Create cached surface for this triangle
                if tr["points"]:
                    min_x = min(int(p.x) if hasattr(p, 'x') else p[0] for p in tr["points"])
                    max_x = max(int(p.x) if hasattr(p, 'x') else p[0] for p in tr["points"])
                    min_y = min(int(p.y) if hasattr(p, 'y') else p[1] for p in tr["points"])
                    max_y = max(int(p.y) if hasattr(p, 'y') else p[1] for p in tr["points"])
                    surf_w = max_x - min_x + 10
                    surf_h = max_y - min_y + 10
                    cached_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
                    # Draw to cached surface
                    offset_points = []
                    for p in tr["points"]:
                        if hasattr(p, 'x'):
                            offset_points.append((int(p.x) - min_x + 5, int(p.y) - min_y + 5))
                        else:
                            offset_points.append((p[0] - min_x + 5, p[1] - min_y + 5))
                    pygame.draw.polygon(cached_surf, tr["color"], offset_points)
                    pygame.draw.polygon(cached_surf, (255, 255, 255), offset_points, 2)
                    _cached_triangle_surfaces[block_id] = (cached_surf, (min_x - 5, min_y - 5))
            
            # Blit cached surface
            if block_id in _cached_triangle_surfaces:
                cached_surf, offset = _cached_triangle_surfaces[block_id]
                screen.blit(cached_surf, offset)
        
        # Indestructible blocks drawn with destructible blocks (see below)
        
        # Draw moving health recovery zone (semi-transparent green)
        # Shape alternates between triangle and rectangle based on wave_in_level
        zone = moving_health_zone
        zone_center = (zone["rect"].centerx, zone["rect"].centery)
        zone_width = zone["rect"].w
        zone_height = zone["rect"].h
        
        # Alternate shape: wave_in_level 1 = rectangle, 2 = triangle, 3 = rectangle, etc.
        use_triangle = (wave_in_level % 2 == 0)
        
        zone_surf = pygame.Surface((zone["rect"].w + 20, zone["rect"].h + 20), pygame.SRCALPHA)
        
        if use_triangle:
            # Draw triangle shape
            triangle_points = [
                (zone_width // 2, 10),  # Top point
                (10, zone_height + 10),  # Bottom left
                (zone_width + 10, zone_height + 10)  # Bottom right
            ]
            pygame.draw.polygon(zone_surf, zone["color"], triangle_points)
            screen.blit(zone_surf, (zone["rect"].x - 10, zone["rect"].y - 10))
            # Draw border with pulsing effect
            pulse = 0.5 + 0.5 * math.sin(run_time * 3.0)
            border_alpha = int(150 + 100 * pulse)
            border_color = (50, 255, 50)
            pygame.draw.polygon(screen, border_color, [
                (zone_center[0], zone["rect"].y),
                (zone["rect"].x, zone["rect"].bottom),
                (zone["rect"].right, zone["rect"].bottom)
            ], 3)
        else:
            # Draw rectangle shape
            pygame.draw.rect(zone_surf, zone["color"], (10, 10, zone["rect"].w, zone["rect"].h))
            screen.blit(zone_surf, (zone["rect"].x - 10, zone["rect"].y - 10))
            # Draw border with pulsing effect
            pulse = 0.5 + 0.5 * math.sin(run_time * 3.0)
            border_alpha = int(150 + 100 * pulse)
            border_color = (50, 255, 50)
            pygame.draw.rect(screen, border_color, zone["rect"], 3)
        
        # Draw destructible blocks (50% destructible with HP, 50% indestructible, all moveable)
        for db in destructible_blocks:
            # Check if block is destructible (has HP)
            if db.get("is_destructible") and "hp" in db:
                # Calculate crack level based on HP
                hp_ratio = db["hp"] / db["max_hp"]
                if hp_ratio < 0.33:
                    crack_level = 3  # Heavily cracked
                elif hp_ratio < 0.66:
                    crack_level = 2  # Moderately cracked
                else:
                    crack_level = 1  # Slightly cracked
                
                # Draw cracked brick wall texture
                draw_cracked_brick_wall_texture(screen, db["rect"], crack_level)
                
                # Health bar only if enabled
                if ui_show_block_health_bars:
                    draw_health_bar(db["rect"].x, db["rect"].y - 10, db["rect"].w, 6, db["hp"], db["max_hp"])
            else:
                # Indestructible block - draw silver wall texture
                draw_silver_wall_texture(screen, db["rect"])
        
        # Draw giant blocks (unmovable, indestructible)
        for gb in giant_blocks:
            pygame.draw.rect(screen, gb["color"], gb["rect"])
            # Draw border to indicate it's giant and unmovable
            pygame.draw.rect(screen, (100, 100, 150), gb["rect"], 4)
        
        # Draw super giant blocks (unmovable, indestructible)
        for sgb in super_giant_blocks:
            pygame.draw.rect(screen, sgb["color"], sgb["rect"])
            # Draw border to indicate it's super giant and unmovable
            pygame.draw.rect(screen, (80, 80, 120), sgb["rect"], 6)
        
        # Draw moveable destructible blocks (50% destructible with HP, 50% indestructible, all moveable)
        for mdb in moveable_destructible_blocks:
            # Check if block is destructible (has HP)
            if mdb.get("is_destructible") and "hp" in mdb:
                # Calculate crack level based on HP
                hp_ratio = mdb["hp"] / mdb["max_hp"]
                if hp_ratio < 0.33:
                    crack_level = 3  # Heavily cracked
                elif hp_ratio < 0.66:
                    crack_level = 2  # Moderately cracked
                else:
                    crack_level = 1  # Slightly cracked
                
                # Draw cracked brick wall texture
                draw_cracked_brick_wall_texture(screen, mdb["rect"], crack_level)
                
                # Draw border to indicate it's moveable (different from regular destructible)
                pygame.draw.rect(screen, (255, 200, 100), mdb["rect"], 2)  # Orange border for moveable
                
                # Health bar only if enabled
                if ui_show_block_health_bars:
                    draw_health_bar(mdb["rect"].x, mdb["rect"].y - 10, mdb["rect"].w, 6, mdb["hp"], mdb["max_hp"])
            else:
                # Indestructible block - draw silver wall texture
                draw_silver_wall_texture(screen, mdb["rect"])
                # Draw border to indicate it's moveable
                pygame.draw.rect(screen, (255, 200, 100), mdb["rect"], 2)  # Orange border for moveable
        
        # Draw indestructible blocks with texture (solid appearance)
        for blk in blocks:
            # Draw with pattern/texture to show it's indestructible
            pygame.draw.rect(screen, blk["color"], blk["rect"])
            # Draw border to indicate indestructible
            pygame.draw.rect(screen, (255, 255, 255), blk["rect"], 3)
            # Draw pattern lines
            for i in range(0, blk["rect"].w, 10):
                pygame.draw.line(screen, (blk["color"][0] + 20, blk["color"][1] + 20, blk["color"][2] + 20),
                                (blk["rect"].x + i, blk["rect"].y),
                                (blk["rect"].x + i, blk["rect"].y + blk["rect"].h), 1)

        # Draw pickup particles (glow effect)
        for particle in pickup_particles:
            particle_surf = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
            color_with_alpha = (*particle["color"], particle["alpha"])
            pygame.draw.circle(particle_surf, color_with_alpha, (particle["size"], particle["size"]), particle["size"])
            screen.blit(particle_surf, (particle["x"] - particle["size"], particle["y"] - particle["size"]))
        
        # Draw pickups with pulsing effect
        for pu in pickups:
            age = pu.get("age", 0.0)
            pulse = (math.sin(age * 4.0) + 1.0) / 2.0
            # Draw glow ring
            glow_surf = pygame.Surface((pu["rect"].w + 20, pu["rect"].h + 20), pygame.SRCALPHA)
            glow_alpha = int(80 + pulse * 60)
            glow_color = (*pu["color"], glow_alpha)
            pygame.draw.ellipse(glow_surf, glow_color, (0, 0, pu["rect"].w + 20, pu["rect"].h + 20))
            screen.blit(glow_surf, (pu["rect"].x - 10, pu["rect"].y - 10))
            # Draw pickup
            pygame.draw.rect(screen, pu["color"], pu["rect"])
            
            # Draw text label above pickup showing what it is
            pickup_type = pu.get("type", "unknown")
            if pickup_type == "health":
                label_text = "HEALTH"
                label_color = (100, 255, 100)
            elif pickup_type == "max_health":
                label_text = "MAX HEALTH"
                label_color = (100, 255, 100)
            elif pickup_type in ["rocket", "triple", "bouncing", "giant", "laser", "wave_beam", "bouncing_bullets"]:
                # Weapon pickup - show weapon name
                weapon_names = {
                    "rocket": "ROCKET",
                    "triple": "TRIPLE",
                    "bouncing": "BOUNCING",
                    "bouncing_bullets": "BOUNCING",
                    "giant": "GIANT",
                    "laser": "LASER",
                    "wave_beam": "WAVE BEAM"
                }
                label_text = weapon_names.get(pickup_type, pickup_type.upper())
                label_color = (255, 255, 100)
            else:
                # Other pickup types
                label_text = pickup_type.upper().replace("_", " ")
                label_color = (200, 200, 200)
            
            # Draw label text above pickup
            label_surf = font.render(label_text, True, label_color)
            label_x = pu["rect"].centerx - label_surf.get_width() // 2
            label_y = pu["rect"].y - 20
            # Draw background for text readability
            bg_rect = pygame.Rect(label_x - 2, label_y - 1, label_surf.get_width() + 4, label_surf.get_height() + 2)
            pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
            screen.blit(label_surf, (label_x, label_y))
            
            # Draw timer bar
            timer_ratio = pu.get("timer", 15.0) / 15.0
            timer_bar_y = pu["rect"].bottom + 2
            timer_bar_w = pu["rect"].w
            timer_bar_h = 3
            pygame.draw.rect(screen, (60, 60, 60), (pu["rect"].x, timer_bar_y, timer_bar_w, timer_bar_h))
            pygame.draw.rect(screen, (255, 200, 0), (pu["rect"].x, timer_bar_y, int(timer_bar_w * timer_ratio), timer_bar_h))
        
        # Draw collection effects
        for effect in collection_effects:
            alpha = int(255 * (effect["life"] / 0.4))
            effect_surf = pygame.Surface((effect["size"] * 2, effect["size"] * 2), pygame.SRCALPHA)
            color_with_alpha = (*effect["color"], alpha)
            pygame.draw.circle(effect_surf, color_with_alpha, (effect["size"], effect["size"]), effect["size"])
            screen.blit(effect_surf, (effect["x"] - effect["size"], effect["y"] - effect["size"]))

        # Draw friendly AI
        for f in friendly_ai:
            pygame.draw.rect(screen, f["color"], f["rect"])
            # Draw health bar above friendly AI (bright green when full)
            if ui_show_health_bars:
                bar_x = f["rect"].x
                bar_y = f["rect"].y - 8
                bar_w = f["rect"].w
                bar_h = 4
                hp_ratio = f["hp"] / f["max_hp"] if f["max_hp"] > 0 else 0
                # Background (dark gray)
                pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
                # Health fill - bright green when full, transitions to yellow/red when damaged
                fill_w = int(bar_w * hp_ratio)
                if hp_ratio > 0.66:
                    # Full to 66%: Bright green (0, 255, 0) to slightly dimmed green
                    green_val = int(255 * (hp_ratio - 0.66) / 0.34) if hp_ratio < 1.0 else 255
                    health_color = (0, max(200, green_val), 0)
                elif hp_ratio > 0.33:
                    # 66% to 33%: Green to yellow transition
                    yellow_ratio = (hp_ratio - 0.33) / 0.33
                    health_color = (int(255 * (1 - yellow_ratio)), 200, 0)
                else:
                    # Below 33%: Yellow to red
                    red_ratio = hp_ratio / 0.33
                    health_color = (255, int(200 * red_ratio), 0)
                pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_w, bar_h))
                # Border
                pygame.draw.rect(screen, (20, 20, 20), (bar_x, bar_y, bar_w, bar_h), 1)
            pygame.draw.rect(screen, (20, 20, 20), (bar_x, bar_y, bar_w, bar_h), 2)  # Border
        
        # Draw friendly projectiles
        for fp in friendly_projectiles:
            draw_projectile(fp["rect"], fp["color"], fp["shape"])

        for e in enemies:
            pygame.draw.rect(screen, e["color"], e["rect"])
            if ui_show_health_bars:
                # Draw health bar
                health_bar_y = e["rect"].y - 10
                draw_health_bar(e["rect"].x, health_bar_y, e["rect"].w, 6, e["hp"], e["max_hp"])
                # Test mode: Draw enemy name over health bar
                if testing_mode:
                    enemy_type = e.get("type", "enemy")
                    enemy_name = enemy_type.replace("_", " ").title()
                    name_text = small_font.render(enemy_name, True, (255, 255, 255))
                    name_x = e["rect"].centerx - name_text.get_width() // 2
                    name_y = health_bar_y - 15
                    # Draw background for readability
                    bg_rect = pygame.Rect(name_x - 2, name_y - 1, name_text.get_width() + 4, name_text.get_height() + 2)
                    pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
                    screen.blit(name_text, (name_x, name_y))
        
        # Draw damage numbers (floating above enemies)
        for dn in damage_numbers:
            # Calculate alpha based on timer (fade out)
            alpha = int(255 * (dn["timer"] / 2.0))  # Fade from 255 to 0 over 2 seconds
            alpha = max(0, min(255, alpha))
            # Adjust color with alpha
            color_with_alpha = tuple(min(255, c) for c in dn["color"])
            # Draw damage number
            damage_text = font.render(f"-{int(dn['damage'])}", True, color_with_alpha)
            text_rect = damage_text.get_rect(center=(int(dn["x"]), int(dn["y"])))
            screen.blit(damage_text, text_rect)
        
        # Draw weapon pickup messages (centered, large text)
        for msg in weapon_pickup_messages:
            # Calculate alpha based on timer (fade out over 3 seconds)
            alpha = int(255 * (msg["timer"] / 3.0))  # Fade from 255 to 0 over 3 seconds
            alpha = max(0, min(255, alpha))
            # Adjust color with alpha
            color_with_alpha = tuple(min(255, int(c * alpha / 255)) for c in msg["color"])
            # Draw weapon name in large text, centered on screen
            weapon_text = big_font.render(msg["weapon_name"], True, color_with_alpha)
            text_rect = weapon_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(weapon_text, text_rect)

            # Draw shield for shielded enemies (only when active for queen)
            if e.get("has_shield"):
                # Queen shield only shows when active
                if e.get("type") == "queen":
                    if not e.get("shield_active", False):
                        continue  # Don't draw shield if inactive
                shield_angle = e.get("shield_angle", 0.0)
                shield_length = e.get("shield_length", 50)
                enemy_center = pygame.Vector2(e["rect"].center)
                shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                shield_start = enemy_center + shield_dir * (e["rect"].w // 2)
                shield_end = enemy_center + shield_dir * (e["rect"].w // 2 + shield_length)
                # Draw shield line
                pygame.draw.line(screen, (100, 200, 255), shield_start, shield_end, 4)
                # Draw shield indicator
                pygame.draw.circle(screen, (150, 220, 255), (int(shield_start.x), int(shield_start.y)), 5)
            
            # Draw reflective shield for reflector enemies
            if e.get("has_reflective_shield"):
                shield_angle = e.get("shield_angle", 0.0)
                shield_length = e.get("shield_length", 60)
                enemy_center = pygame.Vector2(e["rect"].center)
                shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                shield_start = enemy_center + shield_dir * (e["rect"].w // 2)
                shield_end = enemy_center + shield_dir * (e["rect"].w // 2 + shield_length)
                # Draw reflective shield (glowing)
                shield_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.line(shield_surf, (255, 200, 100, 200), shield_start, shield_end, 6)
                pygame.draw.line(shield_surf, (255, 255, 150, 150), shield_start, shield_end, 3)
                screen.blit(shield_surf, (0, 0))
                # Draw shield indicator
                pygame.draw.circle(screen, (255, 220, 100), (int(shield_start.x), int(shield_start.y)), 6)
                # Show absorbed damage
                if e.get("shield_hp", 0) > 0:
                    shield_hp_text = font.render(f"{int(e['shield_hp'])}", True, (255, 255, 100))
                    screen.blit(shield_hp_text, (e["rect"].x, e["rect"].y - 25))

        # Draw bouncing destructor shapes
        for ds in destructor_shapes:
            # Draw with pulsing effect
            pulse = 0.5 + 0.5 * math.sin(run_time * 3.0)
            color = tuple(min(255, int(c * (0.8 + pulse * 0.2))) for c in ds.get("color", (200, 100, 100)))
            pygame.draw.rect(screen, color, ds["rect"])
            # Draw warning border
            pygame.draw.rect(screen, (255, 0, 0), ds["rect"], 3)
        
        # Draw grenade explosions
        for exp in grenade_explosions:
            # Get explosion center (handle both old and new format)
            if "center" in exp:
                exp_center = exp["center"]
                exp_x = int(exp_center.x)
                exp_y = int(exp_center.y)
            else:
                exp_x = int(exp.get("x", 0))
                exp_y = int(exp.get("y", 0))
            
            # Get explosion color (enemy grenades may have custom colors)
            exp_color = exp.get("color", (255, 100, 0))  # Default orange
            
            # Draw expanding explosion circle with pulsing effect
            exp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # Outer ring (orange/red or custom color)
            alpha = int(255 * (1.0 - exp["timer"] / 0.3))  # Fade out
            outer_color = (*exp_color[:3], alpha) if len(exp_color) == 3 else exp_color
            pygame.draw.circle(exp_surf, outer_color, (exp_x, exp_y), exp["radius"], 3)
            # Inner ring (yellow/white)
            inner_alpha = int(200 * (1.0 - exp["timer"] / 0.3))
            inner_color = (255, 255, 150, inner_alpha)
            pygame.draw.circle(exp_surf, inner_color, (exp_x, exp_y), max(1, exp["radius"] // 2), 2)
            # Center flash
            center_alpha = int(255 * (1.0 - exp["timer"] / 0.3))
            center_color = (255, 255, 255, center_alpha)
            pygame.draw.circle(exp_surf, center_color, (exp_x, exp_y), max(5, exp["radius"] // 4))
            screen.blit(exp_surf, (0, 0))
        
        # Draw player highlight/glow (always visible)
        player_radius = player.w // 2  # Radius for circle (player is square)
        highlight_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Outer glow circle
        pygame.draw.circle(highlight_surf, (255, 255, 200, 100), player.center, player_radius + 3, 2)
        # Inner glow circle
        pygame.draw.circle(highlight_surf, (255, 255, 150, 150), player.center, player_radius + 1, 1)
        screen.blit(highlight_surf, (0, 0))
        
        # Draw player as circle - red when shield is active, normal color otherwise
        player_color = (255, 50, 50) if shield_active else (200, 60, 60)
        pygame.draw.circle(screen, player_color, player.center, player_radius)
        
        # Draw health bar above player character
        if ui_show_player_health_bar:
            health_bar_width = max(player.w, 40)
            health_bar_height = 6
            health_bar_x = player.centerx - health_bar_width // 2
            health_bar_y = player.y - 12
            draw_health_bar(health_bar_x, health_bar_y, health_bar_width, health_bar_height, player_hp, player_max_hp)
        
        # Draw shield visual effect when active
        if shield_active:
            shield_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # Pulsing effect based on remaining duration
            pulse = 0.5 + 0.5 * math.sin(run_time * 10.0)
            alpha = int(150 + 100 * pulse)
            # Draw shield circle around player
            radius = max(player.w, player.h) + 10
            pygame.draw.circle(shield_surf, (150, 220, 255, alpha), player.center, radius, 3)
            # Inner glow
            pygame.draw.circle(shield_surf, (200, 240, 255, alpha // 2), player.center, radius - 2, 1)
            screen.blit(shield_surf, (0, 0))

        if last_move_velocity.length_squared() > 0:
            path_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            future_times = [0.2, 0.4, 0.6, 0.8, 1.0]
            for idx, t_pred in enumerate(future_times):
                future_pos = pygame.Vector2(player.center) + last_move_velocity * t_pred
                alpha = max(40, 170 - idx * 25)
                pygame.draw.circle(
                    path_overlay,
                    (120, 255, 120, alpha),
                    (int(future_pos.x), int(future_pos.y)),
                    6,
                )
            screen.blit(path_overlay, (0, 0))

        # Draw laser beams
        for laser in laser_beams:
            pygame.draw.line(screen, laser["color"], laser["start"], laser["end"], laser["width"])
            # Draw glow effect
            glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(glow_surf, (*laser["color"], 100), laser["start"], laser["end"], laser["width"] + 4)
            screen.blit(glow_surf, (0, 0))
        
        # Draw hazard obstacles (paraboloids on level 1, trapezoids on level 2+)
        for hazard in hazard_obstacles:
            if hazard["points"] and len(hazard["points"]) > 2:
                # Draw filled shape
                pygame.draw.polygon(screen, hazard["color"], hazard["points"])
                # Draw outline for visibility
                outline_color = tuple(max(0, c - 50) for c in hazard["color"])
                pygame.draw.polygon(screen, outline_color, hazard["points"], 3)
                # Draw center indicator
                pygame.draw.circle(screen, (255, 200, 200), (int(hazard["center"].x), int(hazard["center"].y)), 5)
        
        # Draw wave beams
        for wave_beam in wave_beams:
            points = wave_beam["points"]
            if len(points) > 1:
                # Convert Vector2 points to tuples for pygame.draw.lines
                point_tuples = [(int(p.x), int(p.y)) for p in points]
                # Draw glow effect first (behind the main beam)
                glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                glow_color = (*wave_beam["color"], 100)  # Semi-transparent lime green glow
                pygame.draw.lines(glow_surf, glow_color, False, point_tuples, wave_beam["width"] + 4)
                screen.blit(glow_surf, (0, 0))
                # Draw the wave beam as a solid continuous lime green line (on top of glow)
                pygame.draw.lines(screen, wave_beam["color"], False, point_tuples, wave_beam["width"])

        # Optimize bullet rendering: only draw bullets on screen
        for b in player_bullets:
            # Skip off-screen bullets to improve performance
            if not (b["rect"].right < 0 or b["rect"].left > WIDTH or b["rect"].bottom < 0 or b["rect"].top > HEIGHT):
                draw_projectile(b["rect"], b.get("color", player_bullets_color), b.get("shape", "square"))
                # Draw explosion radius indicator if bullet has explosion
                if b.get("explosion_radius", 0.0) > 0.0:
                    exp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    radius = int(b["explosion_radius"])
                    pygame.draw.circle(exp_surf, (255, 200, 0, 30), b["rect"].center, radius, 2)
                    screen.blit(exp_surf, (0, 0))
        for p in enemy_projectiles:
            # Skip off-screen projectiles to improve performance
            if not (p["rect"].right < 0 or p["rect"].left > WIDTH or p["rect"].bottom < 0 or p["rect"].top > HEIGHT):
                draw_projectile(p["rect"], p.get("color", enemy_projectiles_color), p.get("shape", "circle"))
        
        # Draw missiles (orange/red with trail effect)
        for missile in missiles:
            if not rect_offscreen(missile["rect"]):
                # Draw missile body (orange/red)
                pygame.draw.rect(screen, (255, 150, 50), missile["rect"])
                # Draw trail effect
                trail_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                missile_center = missile["rect"].center
                # Draw small trail behind missile
                vel_dir = missile["vel"].normalize() if missile["vel"].length() > 0 else pygame.Vector2(0, 0)
                trail_start = pygame.Vector2(missile_center) - vel_dir * 10
                pygame.draw.line(trail_surf, (255, 200, 100, 150), trail_start, missile_center, 3)
                screen.blit(trail_surf, (0, 0))

        # HUD (only if UI and HUD are enabled)
        if ui_show_all_ui and ui_show_hud and ui_show_metrics:
            # Draw health bar above controls (controls are at HEIGHT - 60, so health bar goes above that)
            hp_bar_width = 400
            hp_bar_height = 30
            hp_bar_x = (WIDTH - hp_bar_width) // 2  # Center horizontally
            hp_bar_y = HEIGHT - 120  # Above controls (controls_y = HEIGHT - 60, so 60 pixels above that)
            
            # Draw overshield bar (above HP bar at bottom) - always show, even when empty
            overshield_bar_w = hp_bar_width
            overshield_bar_h = 12
            overshield_bar_x = hp_bar_x
            overshield_bar_y = hp_bar_y - 18  # Above HP bar
            overshield_ratio = overshield / overshield_max if overshield_max > 0 else 0.0
            # Background
            pygame.draw.rect(screen, (40, 40, 40), (overshield_bar_x, overshield_bar_y, overshield_bar_w, overshield_bar_h))
            # Overshield (orange color when full, darker orange when partial)
            if overshield > 0:
                overshield_color = (255, 150, 50) if overshield >= overshield_max else (255, 100, 0)
                pygame.draw.rect(screen, overshield_color, (overshield_bar_x, overshield_bar_y, int(overshield_bar_w * overshield_ratio), overshield_bar_h))
            # Border
            pygame.draw.rect(screen, (150, 150, 150), (overshield_bar_x, overshield_bar_y, overshield_bar_w, overshield_bar_h), 2)
            # Text - show full amounts
            shield_text = font.render(f"Overshield: {int(overshield)}/{int(overshield_max)}", True, (255, 200, 100))
            shield_text_x = overshield_bar_x + (overshield_bar_w - shield_text.get_width()) // 2
            screen.blit(shield_text, (shield_text_x, overshield_bar_y - 1))
            
            # Draw HP bar at bottom - always show full bar
            draw_health_bar(hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height, player_hp, player_max_hp)
            # HP text centered above the bar - show full amounts
            hp_text = font.render(f"HP: {int(player_hp)}/{int(player_max_hp)}", True, (230, 230, 230))
            hp_text_x = hp_bar_x + (hp_bar_width - hp_text.get_width()) // 2
            screen.blit(hp_text, (hp_text_x, hp_bar_y - 24))
            
            # Other HUD elements remain at top-left
            lives_y = 10
            # Render HUD using helper function
            y = render_hud_text(f"Lives: {lives}", lives_y)
            y = render_hud_text(f"Level: {current_level} - {level_themes[current_level]['name']}", y, (255, 200, 100))
            y = render_hud_text(f"Wave: {wave_number} (Wave {wave_in_level}/3)", y)
            if wave_active:
                wave_text = f"Enemies: {len(enemies)}"
            else:
                wave_text = f"Next wave in: {time_to_next_wave:.1f}s"
            y = render_hud_text(wave_text, y)
            y = render_hud_text(f"Damage dealt: {damage_dealt}", y)
            y = render_hud_text(f"Damage taken: {damage_taken}", y)
            y = render_hud_text(f"Score: {score:,}", y, (255, 255, 100))
            y = render_hud_text(f"Time: {int(survival_time//60)}m {int(survival_time%60)}s", y, (200, 200, 255))
            if state == STATE_ENDURANCE:
                y = render_hud_text("ENDURANCE MODE", y, (255, 100, 100))
            y = render_hud_text(f"Boost: {int(boost_meter)}/{int(boost_meter_max)}", y)
            # Shield status
            if shield_active:
                y = render_hud_text("SHIELD ACTIVU", y, (150, 220, 255))
            elif shield_cooldown_remaining > 0.0:
                y = render_hud_text(f"Shield CD: {shield_cooldown_remaining:.1f}s", y, (200, 150, 150))
            else:
                y = render_hud_text("Shield: Ready (Left Alt)", y, (100, 255, 100))
            if fire_rate_buff_t > 0:
                y = render_hud_text(f"Firerate buff: {fire_rate_buff_t:.1f}s", y, (255, 220, 120))
            if enemy_spawn_boost_level > 0:
                y = render_hud_text(f"Enemy spawn boost: +{enemy_spawn_boost_level}", y, (255, 140, 220))
            
            # Display permanent stat upgrades
            y_offset = y
            if player_stat_multipliers["speed"] > 1.0:
                y_offset = render_hud_text(f"Speed: +{int((player_stat_multipliers['speed']-1.0)*100)}%", y_offset, (150, 255, 150))
            if player_stat_multipliers["firerate"] > 1.0:
                y_offset = render_hud_text(f"Fire Rate: +{int((player_stat_multipliers['firerate']-1.0)*100)}%", y_offset, (150, 255, 150))
            if player_stat_multipliers["bullet_damage"] > 1.0:
                y_offset = render_hud_text(f"Damage: +{int((player_stat_multipliers['bullet_damage']-1.0)*100)}%", y_offset, (150, 255, 150))
            if player_stat_multipliers["bullet_penetration"] > 0:
                y_offset = render_hud_text(f"Penetration: {int(player_stat_multipliers['bullet_penetration'])}", y_offset, (150, 255, 150))
            if player_stat_multipliers["bullet_explosion_radius"] > 0:
                y_offset = render_hud_text(f"Explosion: {int(player_stat_multipliers['bullet_explosion_radius'])}px", y_offset, (150, 255, 150))
            # Display current weapon mode
            weapon_names = {
                "basic": "BASIC FIRE",
                "rocket": "ROCKET LAUNCHER",
                "triple": "TRIPLE SHOT",
                "bouncing": "BOUNCING BULLETS",
                "giant": "GIANT BULLETS (10x)",
                "laser": "LASER BEAM"
            }
            weapon_colors = {
                "basic": (200, 200, 200),
                "rocket": (255, 100, 0),
                "triple": (100, 200, 255),
                "bouncing": (100, 255, 100),
                "giant": (255, 200, 0),
                "laser": (255, 50, 50)
            }
            screen.blit(font.render(f"Weapon: {weapon_names.get(current_weapon_mode, 'UNKNOWN')}", True, weapon_colors.get(current_weapon_mode, (255, 255, 255))), (10, y_offset))
            y_offset += 22
            # Show unlocked weapons
            unlocked_list = sorted(unlocked_weapons)
            unlocked_str = "Unlocked: " + ", ".join([weapon_names.get(w, w) for w in unlocked_list])
            screen.blit(font.render(unlocked_str, True, (150, 255, 150)), (10, y_offset))
            y_offset += 22
            screen.blit(font.render("Press 1-6 to switch weapons (if unlocked)", True, (150, 150, 150)), (10, y_offset))
            y_offset += 22
            
            # Draw enemy defeat messages in bottom right corner
            defeat_y = HEIGHT - 30
            for msg in enemy_defeat_messages:
                enemy_type = msg["enemy_type"]
                enemy_name = enemy_type.replace("_", " ").title()
                defeat_text = font.render(f"{enemy_name} defeated!", True, (255, 200, 100))
                defeat_x = WIDTH - defeat_text.get_width() - 20
                defeat_y -= 25
                # Draw background for readability
                bg_rect = pygame.Rect(defeat_x - 5, defeat_y - 2, defeat_text.get_width() + 10, defeat_text.get_height() + 4)
                pygame.draw.rect(screen, (0, 0, 0, 200), bg_rect)
                screen.blit(defeat_text, (defeat_x, defeat_y))
            
            # Status bars at bottom of screen (arranged horizontally)
            bar_width = 150
            bar_height = 25
            bar_spacing = 10
            total_bars_width = (bar_width + bar_spacing) * 5 - bar_spacing  # 5 bars: bomb, missile, shield, overshield, ally drop
            bars_start_x = (WIDTH - total_bars_width) // 2
            bars_y = HEIGHT - 100  # Above controls
            
            # Bomb status bar
            bomb_bar_x = bars_start_x
            bomb_readiness = min(1.0, grenade_time_since_used / grenade_cooldown)
            is_ready = grenade_time_since_used >= grenade_cooldown
            pygame.draw.rect(screen, (40, 40, 40), (bomb_bar_x, bars_y, bar_width, bar_height))
            bar_color = (200, 100, 255) if is_ready else (255, 50, 50)
            pygame.draw.rect(screen, bar_color, (bomb_bar_x, bars_y, int(bar_width * bomb_readiness), bar_height))
            pygame.draw.rect(screen, (150, 150, 150), (bomb_bar_x, bars_y, bar_width, bar_height), 2)
            bomb_text = small_font.render("BOMB", True, (255, 255, 255))
            screen.blit(bomb_text, (bomb_bar_x + (bar_width - bomb_text.get_width()) // 2, bars_y + (bar_height - bomb_text.get_height()) // 2))
            
            # Missile status bar
            missile_bar_x = bars_start_x + bar_width + bar_spacing
            missile_readiness = min(1.0, missile_time_since_used / missile_cooldown)
            missile_ready = missile_time_since_used >= missile_cooldown
            pygame.draw.rect(screen, (40, 40, 40), (missile_bar_x, bars_y, bar_width, bar_height))
            missile_color = (100, 200, 255) if missile_ready else (255, 100, 50)
            pygame.draw.rect(screen, missile_color, (missile_bar_x, bars_y, int(bar_width * missile_readiness), bar_height))
            pygame.draw.rect(screen, (150, 150, 150), (missile_bar_x, bars_y, bar_width, bar_height), 2)
            missile_text = small_font.render("MISSILE", True, (255, 255, 255))
            screen.blit(missile_text, (missile_bar_x + (bar_width - missile_text.get_width()) // 2, bars_y + (bar_height - missile_text.get_height()) // 2))
            
            # Shield recharge bar
            shield_bar_x = bars_start_x + (bar_width + bar_spacing) * 2
            shield_readiness = min(1.0, shield_recharge_timer / shield_recharge_cooldown) if shield_recharge_cooldown > 0 else 1.0
            shield_ready = shield_cooldown_remaining <= 0.0
            pygame.draw.rect(screen, (40, 40, 40), (shield_bar_x, bars_y, bar_width, bar_height))
            shield_bar_color = (100, 220, 255) if shield_ready else (150, 150, 255)
            pygame.draw.rect(screen, shield_bar_color, (shield_bar_x, bars_y, int(bar_width * shield_readiness), bar_height))
            pygame.draw.rect(screen, (150, 150, 150), (shield_bar_x, bars_y, bar_width, bar_height), 2)
            shield_text = small_font.render("SHIELD", True, (255, 255, 255))
            screen.blit(shield_text, (shield_bar_x + (bar_width - shield_text.get_width()) // 2, bars_y + (bar_height - shield_text.get_height()) // 2))
            
            # Overshield recharge bar
            overshield_bar_x = bars_start_x + (bar_width + bar_spacing) * 3
            overshield_readiness = min(1.0, overshield_recharge_timer / overshield_recharge_cooldown)
            overshield_ready = overshield_recharge_timer >= overshield_recharge_cooldown
            pygame.draw.rect(screen, (40, 40, 40), (overshield_bar_x, bars_y, bar_width, bar_height))
            overshield_bar_color = (255, 150, 50) if overshield_ready else (255, 100, 0)
            pygame.draw.rect(screen, overshield_bar_color, (overshield_bar_x, bars_y, int(bar_width * overshield_readiness), bar_height))
            pygame.draw.rect(screen, (150, 150, 150), (overshield_bar_x, bars_y, bar_width, bar_height), 2)
            overshield_text = small_font.render("OVERSHLD", True, (255, 255, 255))
            screen.blit(overshield_text, (overshield_bar_x + (bar_width - overshield_text.get_width()) // 2, bars_y + (bar_height - overshield_text.get_height()) // 2))
            
            # Ally drop recharge bar
            ally_drop_bar_x = bars_start_x + (bar_width + bar_spacing) * 4
            ally_drop_readiness = min(1.0, ally_drop_timer / ally_drop_cooldown)
            ally_drop_ready = ally_drop_timer >= ally_drop_cooldown
            pygame.draw.rect(screen, (40, 40, 40), (ally_drop_bar_x, bars_y, bar_width, bar_height))
            ally_drop_bar_color = (200, 100, 255) if ally_drop_ready else (150, 50, 200)  # Purple when ready, darker purple when charging
            pygame.draw.rect(screen, ally_drop_bar_color, (ally_drop_bar_x, bars_y, int(bar_width * ally_drop_readiness), bar_height))
            pygame.draw.rect(screen, (150, 150, 150), (ally_drop_bar_x, bars_y, bar_width, bar_height), 2)
            ally_drop_text = small_font.render("ALLY DROP", True, (255, 255, 255))
            screen.blit(ally_drop_text, (ally_drop_bar_x + (bar_width - ally_drop_text.get_width()) // 2, bars_y + (bar_height - ally_drop_text.get_height()) // 2))
            
            # Controls display at bottom of screen
            controls_y = HEIGHT - 60
            controls_bg = pygame.Surface((WIDTH, 50), pygame.SRCALPHA)
            controls_bg.fill((0, 0, 0, 180))  # Semi-transparent black background
            screen.blit(controls_bg, (0, controls_y))
            
            # Build controls text based on aiming mode
            if aiming_mode == AIM_MOUSE:
                move_text = "WASD: Move"
                aim_text = "Mouse: Aim"
                shoot_text = "Click: Shoot"
            else:
                move_text = "WASD: Move"
                aim_text = "Arrow Keys: Aim"
                shoot_text = "Space: Shoot"
            
            grenade_text = "E: Grenade"
            
            # Weapon slot indicators: 1: basic, 2: (next weapon), etc.
            weapon_slots = []
            key_to_number = {pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7"}
            for key, weapon in sorted(WEAPON_KEY_MAP.items()):  # Sort by key to maintain order
                if weapon in unlocked_weapons or weapon == "basic":
                    weapon_name = weapon.replace("_", " ").title()
                    key_num = key_to_number.get(key, "?")
                    weapon_slots.append(f"{key_num}: {weapon_name}")
            
            weapon_text = " | ".join(weapon_slots) if weapon_slots else "No weapons unlocked"
            
            # Draw controls text
            controls_text = f"{move_text} | {aim_text} | {shoot_text} | {grenade_text} | Weapons: {weapon_text}"
            controls_surf = font.render(controls_text, True, (200, 200, 200))
            controls_x = (WIDTH - controls_surf.get_width()) // 2
            screen.blit(controls_surf, (controls_x, controls_y + 15))
            
            # Only show metrics if enabled
            if ui_show_metrics:
                screen.blit(
                    font.render(
                        f"Run: {run_time:.1f}s  Shots: {shots_fired}  Hits: {hits}  Kills: {enemies_killed}  Deaths: {deaths}",
                        True,
                        (230, 230, 230),
                    ),
                    (10, 168),
                )

        # Pause overlay
        if state == STATE_PAUSED:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            draw_centered_text("Paused", HEIGHT // 2 - 140, use_big=True)
            draw_centered_text("Press C for Controls", HEIGHT // 2 - 90, color=(190, 190, 190))

            for i, opt in enumerate(pause_options):
                prefix = "> " if i == pause_selected else "  "
                draw_centered_text(prefix + opt, HEIGHT // 2 - 40 + i * 40)

            draw_centered_text("Up/Down + Enter.  P or Esc to resume.", HEIGHT // 2 + 120, color=(190, 190, 190))

        # Controls overlay
        elif state == STATE_CONTROLS:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            draw_centered_text("Controls", HEIGHT // 2 - 200, use_big=True)
            draw_centered_text("Up/Down select  Enter rebind  Esc back", HEIGHT // 2 - 150, color=(190, 190, 190))

            for i, action in enumerate(controls_actions):
                key_name = pygame.key.name(controls.get(action, pygame.K_UNKNOWN))
                prefix = "> " if i == controls_selected else "  "
                label = f"{action}: {key_name}"
                draw_centered_text(prefix + label, HEIGHT // 2 - 60 + i * 32)

            if controls_rebinding:
                draw_centered_text("Press a key...", HEIGHT // 2 + 160, color=(255, 230, 120))

        # Continue overlay
        elif state == STATE_CONTINUE:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            draw_centered_text("You Died", HEIGHT // 2 - 150, use_big=True)
            draw_centered_text(f"Lives left: {lives}", HEIGHT // 2 - 90)

            continue_blink_t += dt_real
            show = (int(continue_blink_t * 2) % 2) == 0
            if show:
                draw_centered_text("Press Enter or Space to continue", HEIGHT // 2 + 10)
            draw_centered_text("Press Esc to quit", HEIGHT // 2 + 60, color=(190, 190, 190))

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
