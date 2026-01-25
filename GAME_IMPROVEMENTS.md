# Game Improvements

This document contains all improvement suggestions and TODO items for the game file "game.py". These were extracted from comments in `game.py` for better organization.

## Visual Improvements

- Make player a circle with a border around it
- Make enemies move around the map more
- Fix health bar at bottom of screen, armor bar above it when active
- Make wave beam a solid line rather than dots, and turn the beam lime green
- Make wave beam an undulating wave, with a period of 1 second, and a amplitude of 10 pixels
- Make the wave beam have a period of 0.5 seconds, and a amplitude of 7 pixels
- Add texture into indestructible, moveable blocks that makes it looks like a silver wall
- Add texture into destructible, moveable blocks that makes it looks like a cracked brick wall
- Make damage done to enemies displayed over their health bar as an integer
- Make it so that after the player damages an enemy, the damage given number goes away after 2 seconds
- Make the weapon pickup messages display for 3 seconds, and then fade out
- Make health bar and HP amount above the control information at bottom of screen in-game

/## Gameplay Features

### Player Mechanics
- Make the player turn red while the shield is active, and a text displays in the hud SHIELD ACTIVU (spelled like that)
- Start with shield, overshield, and drop ally charged at beginning of round, and add a "ALLY DROP" progress bar that is purple when charged
- Make a status bar at the bottom of the screen that shows player bomb readiness status with a progress bar that is red when not ready, and purple when ready and says "BOMB" in it
- Decrease ally drop cooldown to 5 seconds, increase ally's rate of fire, and remove all other spawned allies, and make enemies focus on ally, unless are some radius away from ally
#make missile shots a three shot burst
#put name of pickup over pickup, and increase pickup size 2x
#make WAVE STARTS IN 3, 2, 1 countdown in between waves, with wave number listed (ex: wave 2 starting in 3, 2, 1...)

### Weapons & Combat
#make large red enemy's shots disappear after they are shot, they are lingering
- Add in a testing section of the pre-game menu, and include beam selection option (for testing beams), and invulnerability selection (for testing)
- Fix wave beam draw to be constant, not flashing
- Verify: Do not drop the basic beam as a pickup weapon
- Make a weapon name document for reference
- Make beam selector harder to access (testing mode? if yes, display beam selection)
- Fix triple shot beam to include two more beams, offset by an equal arc on each side of center beam, and increase beam shot size to 3x current size, and turn purple
- Change triple shot to basic beam, with three beams in total, offset by an equal arc
/

### Pickups
- Add a pickup that creates the player's bullet penetration, otherwise player cannot shoot through walls
- Add a pickup effect when the player picks up a pickup
- Add a pickup that increases the player's health regeneration rate
- Add in a pickup that randomizes, with an on screen element on the HUD, how much base damage is multiplied by
#reduce player health by 0.75x
- Make a list of all pickups, and their effects, and their spawn order in a document labeled PICKUP_INFO.md
/

### Enemies & AI
#create space between trapezoids on right hand side, and triangles to allow player to get into outer part of map
- If enemies haven't moved for 5 seconds, have them change direction away from an object they are stuck on
- Remove allies from map
/- Add more enemies
#make allies drop from ally drop
- Create enemy classes; pawn = basic beam, basic movement speed
- Create enemy classes; queen = maroon, "player copy"
- Make player clone (maroon enemy) have 2000 health, and move 3x standard speed
- Increase "queen" rate of fire, and raise health to 5000, and give shield like "shield enemy" that activates and deactivates at rates of 10-20 seconds each phase, enabled for 5-10 seconds
/#spawn no more than three queens per wave, give them missiles that fire with a 10 second cool down
#make obstacles prevent shots from going through them
#make parabolas damage enemies, and kill them when their health drops to zero
- Make an enemy that predicts and shoots ahead of player's location; dark maroon rhomboid
- Make an enemy "patrol" that patrols the outside border of the map, with the wave beam
- Add an enemy that shoots shots that bounce around on the walls
- Add one shield enemy with reflective shield, which takes damage done to the shield and fires back at the player; enemy does not fire, enemy turns at speed player can flank
- Rename enemy with shield to "shield enemy"
- Add in suicide enemy that goes towards player and detonates themselves with grenade, and disappears after detonating, and damages player if in range of grenade; when enemy dies, the enemy despawns
- Make suicide enemies blow up when closer to player, not at beginning of wave
- Make suicide enemy twice as big, and 0.75x current movement speed
- Game; enemy type - spawner - spawns enemies during round, but when killed, all spawned enemies die
- Once there are 5 enemies remaining, have them move towards the player
-verify: After each enemy dies, put in bottom right corner a text feed that updates "(enemy type) defeated!"
/- Verify when health = zero, enemies and allies die and disappear from map

### Friendly AI
- Make it so I can fly through allies - VERIFIED: Implemented - Friendly AI collision removed from player movement (lines 2905-2907, 2982)

/### Levels & Waves

### Geometry & Blocks

- Make the map bigger, and add in more geometry, with areas of health recovery, and overshields (extra health bar that can be used to block damage)
- Add in more squares and rectangles that can be moved around, but have health bars that enemies can shoot at to destroy them
- Add in more moveable blocks
- Add in moveable blocks that can be destroyed by the player's, and enemy's bullets
- Add in more geometry (moveable blocks, unmovable blocks, destructible blocks, indestructible blocks) to fill up the map more
- Add in trapezoids that hang off the top, bottom, and sides of the screen, that are unmovable, and indestructible
- Make all blocks moveable, and indestructible, and the player can push them around
- Add destructible, moveable blocks back in. Make blocks 50% of all blocks, and the other 50% be indestructible, moveable blocks
- Add another block size - giant, super giant, which cannot be moved
- Lower blocks amount, and make them bigger
- Make it so that player spawn and block spawn cannot overlap, player spawn takes priority
- Prevent blocks from spawning within a radius of 10x the player size, from the player
- Prevent enemies and allies from spawning where blocks are
- Prevent allies or enemies from spawning in health block
- Prevent boxes from overlapping with allies, on other boxes, or player, on spawn
- Make it so that the health box and other objects do not overlap with each other
- Make it so that the health box does not overlap with other objects
- Prevent any blocks from overlapping with each other
- Let the enemies move the blocks out of the way as well, to chase the player
- Take the moveable, indestructible geometry, and leave only the destructible, movable geometry, and the unmovable, destructible, and unmovable, destructible geometry.
- Outside/border: create spaces between trapezoids, creating 3 total on left side, 2 on right, next to each other, with 5 trapezoids with 2 triangles each on top of them on top, and then a line of triangles across the bottom

### Hazards
- Add a rotating paraboloid that slowly rotates around the stage, that is 500 pixels wide, and 500 pixels tall, and is a hazard that does damage to the player, and the player has to avoid it
- Add in two more paraboloids with collision physics, so that they'll bounce off each other, and that do damage to the player at 10 damage/second
- Make the paraboloids half size, add another one, and have them start at the corners of the map
- On the second level, turn the paraboloids into trapezoids that do the same function as the paraboloid
- Make it so that the player can "bully" the obstacles by shooting them and they move in response to being shot, and make the obstacles kill the enemies when they collide with the hazard
- Make it so that the player cannot fly through the hazards (paraboloid, trapezoids, and all future hazards)
- Make shots from players move the hazards
- Make hazards move 3x faster

### Health & Healing
- Add a health bar for the player
- Make only one health area, and have it move around the map, and the player has to move to it to heal
- Make health block be in a different spot from the boss spawn point
- Make it so that the health box and other objects do not overlap with each other
- Make it so that the health box does not overlap with other objects

## UI & Menu Improvements

- Make the metrics optional in the menu
- Make the default telemetry selection to be disabled, but still able to be enabled
- Select telemetry, and select metrics, as two different options in the menu that can be selected independently, with disabled as the default for both
- Metrics menu: show and hide, independent from telemetry
- Telemetry menu: enable and disable, independent from metrics
- Change hud and telemetry to two different pages, rather than sharing the same page
- Delete second HUD menu on options menu
- When metrics are disabled, disable all hud information; when selecting options (HUD: enable, disable)
- Set to show HUD by default
- Fix text overlap in "ready to start" menu with weapon basic, and other text
- Fix text overlap in "select player class" menu
- Add restart game to menu in-game
- Game; Make a placeholder text for each drop saying whether it's health, or which weapon it is
- Game; Change shape of healing pattern with each stage between triangles and rectangles
- Game; add controls at bottom of screen (wasd to move, mouse + click to aim and shoot) or (wasd to move, arrow keys to aim and shoot), grenade, and which weapon is mapped to which weapon slot with first letter of weapon name
- Fix overshield bar and health bar overlay, and amount shown in health and overshield, show bars full, with health and overshield amounts full

## Controls & Settings

- Add a control mapping system, so the player can map the keys to the actions
- Game; controls; add in arrows for shooting, and an option to choose between mouse and arrow keys
- Arrow keys: Add it as an option in the menu to use either mouse or arrow aiming
- Game.py; change aiming mechanic
- Update controls.json with new controls
- Jump = spacebar, add to json file controls listing

## Character Profiles

- Create custom character profile creator
- Character profile premade and custom character profile do not allow for right to continue to next menu
- Make character profile option yes or no, and if yes, allow player to select premade, or make a profile, prior to start of game
- Make custom stats able to be updated
- Make custom stats able to select to next menu by enter, and right arrow

## Classes & Mods

- Game; classes to play as, custom mod setting to change enemy spawn amount, custom wave builder
- Game; Make a placeholder text for each drop saying whether it's health, or which weapon it is

## Difficulty & Scoring

- Add a difficulty selector, so the player can choose the difficulty of the game, which impacts enemy spawns (more, harder enemies, fewer pickups?)
- Add a score counter and survival wave amount/time survived
- Add a high score board after each death, and the ability to type in a name
- Add side quests, and goal tracking; complete wave without getting hit, get a bonus 10,000 points

## Boss & Final Content

- Final boss, with a unique weapon that the player has to defeat (combo of all weapons), multiple phases, and a unique weapon for each phase
- Give maroon enemy name "queen", and allow it to use grenades and shield as well as it gets damage done to it after 300-500 damage, for 5 seconds, and player gets close (grenade), and destroys destructible cover to lower ability for player to hide

## Performance & Optimization

- Fix game slowdown when many shots are on screen
- Read the supporting files of game_physics, and optimize them with game.py, telemetry.py, and visualize.py, and then optimize game.py, telemetry.py, and visualize.py amongst each other, given the new updates in game.py
- Is there a way to utilize the GPU for processing as well?
- I have an NVIDIA GPU, a 4080 super, so CUDA cores should be available;
- GPU acceleration status:
  - game.py: ✅ IMPLEMENTED - Uses GPU for bullet updates (50+ bullets) via gpu_physics module
  - telemetry.py: ✅ IMPLEMENTED - GPU support added for batch event processing (when CUDA available)
  - visualize.py: ✅ IMPLEMENTED - GPU support added for data processing operations (when CUDA available)
  - ✅ CUDA 12.9 CONFIGURED - GPU acceleration is active (RTX 4080 SUPER detected)
  - Falls back to CPU JIT (2-5x speedup) if CUDA becomes unavailable.
- I'm still encountering frame rate issues. Let's add a feature where at the beginning of the game, you ask if the user wants to run telemetry and write to game_telemetry.db.
- Verify all code in repo is working correctly, and all features are implemented correctly, and all code is optimized for performance

## Telemetry & Analytics

- In telemetry.py, track the player's position and velocity, and the enemy's position and velocity, and which enemy types spawned that wave; do the wave's tracking for the enemies as its own table
- Visualize.py: update the charts to be the most recent run

## Bug Fixes & Technical Issues

- Fix issue where allies do not disappear after dying - FIXED: Added cleanup checks and hazard collision handling
- Fix issue where wave beams get stuck displayed after beam switched - FIXED: Added beam clearing when switching weapons
- Fix endurance mode crash when game starts
- Game; fix overshield bar and health bar overlay, and amount shown in health and overshield, show bars full, with health and overshield amounts full
- Fix shots staying displayed in map after shot has moved past position

## Miscellaneous

- Movement direction overwrites to most recent move direction
- Player path prediction
- Different shapes for shots (circle, squares, etc., like 2hu)
- Start game fullscreen
- Put the health bar on the bottom of the screen
- When game launches in command line, print "welcome to my game! :D"
- Test mode menu: puts enemy name over the enemy health bar
- Increase base enemy spawn amount by 3x
- Give destructible obstacles 10x more health

## Completed Items

- Make player stick out more on map by making player 10% larger, and have a highlight around the player - FIXED: Increased size to 28x28 and added glowing highlight
- Note: Player is currently drawn as a rectangle; "Make player a circle with a border" is still pending
- Make bouncing bullets projectiles twice the size, and projectiles orange - FIXED: Added 2x size multiplier and orange color
- In menu, set default beam selection to basic - FIXED: Changed default selection to index 6 (basic)
- Fix issue where allies do not disappear after dying - FIXED: Added cleanup checks and hazard collision handling
- Fix issue where wave beams get stuck displayed after beam switched - FIXED: Added beam clearing when switching weapons
