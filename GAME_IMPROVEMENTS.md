# Game Improvements

This document contains all improvement suggestions and TODO items for the game. These were extracted from comments in `game.py` for better organization.

## Visual Improvements

- Make player a circle with a border around it
- Make enemies move around the map more
- Fix health bar at bottom of screen, armor bar above it when active
- Make player stick out more on map by making player 10% larger, and have a highlight around the player - FIXED: Increased size to 28x28 and added glowing highlight
- Make player's model a circle - FIXED: Changed from rectangle to circle with circular highlight
- Make wave beam a solid line rather than dots, and turn the beam lime green
- Make wave beam an undulating wave, with a period of 1 second, and a amplitude of 10 pixels
- Make the wave beam have a period of 0.5 seconds, and a amplitude of 7 pixels
- Add texture into indestructible, moveable blocks that makes it looks like a silver wall
- Add texture into destructible, moveable blocks that makes it looks like a cracked brick wall
- Change player bullet color
- Change enemy bullet colors
- Make the rockets shot size bigger
- Make bouncing bullets projectiles twice the size, and projectiles orange - FIXED: Added 2x size multiplier and orange color
- Make damage done to enemies displayed over their health bar as an integer
- Make it so that after the player damages an enemy, the damage given number goes away after 2 seconds
- Make the weapon pickup messages display for 3 seconds, and then fade out
- Make health bar and HP amount above the control information at bottom of screen in-game
- Remove giant and super giant labels from obstacles

## Gameplay Features

### Player Mechanics
- Add boost mechanic using shift, and slow down mechanic using ctrl
- Add space bar to jump in direction of movement?
- Change "jump" name to "dash" in game and controls
- Add a shield for use with left alt key that lasts 2 seconds, and takes 10-15 seconds to recharge
- Make the player turn red while the shield is active, and a text displays in the hud SHIELD ACTIVU (spelled like that)
- Make "tab" key create an overshield the amount of the player's health that is an orange bar that stacks on top of the player's health, and recharges every 45 seconds, with a progress bar on the bottom
- When wave starts, start with overshield charged
- Start with shield, overshield, and drop ally charged at beginning of round, and add a "ALLY DROP" progress bar that is purple when charged
- Make it so that player is immune to player bomb damage
- Make a status bar at the bottom of the screen that shows player bomb readiness status with a progress bar that is red when not ready, and purple when ready and says "BOMB" in it
- Put shield recharge bar on the bottom
- Make a recharge bar for the missile, place on bottom
- Give player 3x health, 1.5x movement speed
- Increase player health by 10x
- Increase player base health to 250

### Weapons & Combat
- Add a map to key 1 for the basic fire, then key 2 for the rocket launcher, then key 3 for the triple shot, then key 4 for the bouncing bullets, then key 5 for the giant bullets
- Add a special pickup that adds a laser beam weapon that the player can use to destroy enemies from a distance, that's a long ray, but doesn't cut through solid blocks, but breaks temporary barriers
- Make weapons drop in the center of the screen, and the player has to pick them up to use them, adding one with each level completed
- Add in a beam selection option in the pre-game menu (useful for testing beams)
- Beam selection controls don't work
- Change beam selections to only be sine beam (instead of the other trig functions), and change beam selection to include rockets, bounce beam, etc., for ease of testing
- In menu, set default beam selection to basic - FIXED: Changed default selection to index 6 (basic)
- Take away wave beam as a starting weapon, leave it as only a pickup, leaving the player only with the basic beam and the other weapons as pickups
- Spawn with wave_beam in slot 2, in addition to basic
- When player collects a pickup, automatically switch to that weapon, and display the weapon name on the screen
- Do not drop the basic beam as a pickup weapon
- Make a weapon name document for reference, with enemy names
- Make wave beam second to last dropped, giant beam last
- Make beam selector harder to access (testing mode? if yes, display beam selection)
- Fix triple shot beam to include two more beams, offset by an equal arc on each side of center beam, and increase beam shot size to 3x current size, and turn purple
- Change triple shot to basic beam, with three beams in total, offset by an equal arc
- Make aoe bigger for rocket beam
- Make bomb do more damage
- Add in a grenade to use with e with an aoe of a radius that is 10x the player space that kills enemies and does damage to destructible obstacles
- Add a missile that seeks enemies and explodes on contact with "r" key
- Add a beam that fires in a sine wave pattern, and the beam is a line that is 10 pixels wide, and 1000 pixels long, and the beam is fired from the player's position, and the beam is fired in a sine wave pattern, and the beam is fired in a cosine wave pattern, and the beam is fired in a tangent wave pattern, and the beam is fired in a cotangent wave pattern, and the beam is fired in a secant wave pattern, and the beam is fired in a cosecant wave pattern, and the beam is fired in a arcsecant wave pattern, and the beam is fired in a arccosecant wave pattern, and the beam is fired in a arcsecant wave pattern, and the beam is fired in a arccosecant wave pattern

### Pickups
- Make pickups bigger, add in another pickup that increases the player's max health
- Add a pickup for boost
- Add a pickup for more firing speed
- Add a pickup that increases the player's speed
- Add a pickup that increases the player's firing rate
- Add a pickup that increases the player's bullet size
- Add a pickup that increases the player's bullet speed
- Add a pickup that increases the player's bullet damage
- Add a pickup that increases the player's bullet knockback
- Add a pickup that increases the player's bullet penetration
- Add a pickup that increases the player's bullet explosion radius
- Make pickup that increases the shot size to 10x regular size, and another pickup that increase the shot beams to 3 beams
- Add a pickup that bounces shots around on the walls
- Add a pickup timer, and effects around the pickup, and an effect when the player picks up the pickup
- Add a pickup that functions like a rocket launcher with a longer rate of fire, but the shots do more damage with an area of effect
- Add a pickup that increases the player's overshield
- Add a pickup that increases the player's health regeneration rate
- Add in a pickup that randomizes, with an on screen element on the HUD, how much base damage is multiplied by
- Randomize the pickups, so that the player never knows what they will get
- Stack pickups so that the player can get a combo of pickups
- Health pickups are worth 100 health
- Make a list of all pickups, and their effects, and their spawn order

### Enemies & AI
- Enemy movement
- Enemy respawn timer
- Make enemies move around the map more
- Make enemies prioritize player damage, unless player is over half the map away from them, then prioritize allies closeby
- Make it so that enemies cannot go through other objects, and must go around
- If enemies haven't moved for 5 seconds, have them change direction away from an object they are stuck on
- Add more enemies, and friendly ai, and give the ai more health (50-100), with their bar being full and green at the beginning of the waves
- Change all enemies to have no more than 300 health each. The enemies can have health lower than that.
- Increase enemy and ally movement speed by 110%
- Increase enemy and ally health by 110%
- Increase enemy and ally damage by 110%
- Increase enemy and ally fire rate by 110%
- Increase rate of fire for all enemies
- Create enemy classes; pawn = basic beam, basic movement speed
- Create enemy classes; queen = maroon, "player copy"
- Make player clone (maroon enemy) have 2000 health, and move 3x standard speed
- Increase "queen" rate of fire, and raise health to 5000, and give shield like "shield enemy" that activates and deactivates at rates of 10-20 seconds each phase, enabled for 5-10 seconds
- Change queen shoot cooldown to 0.2s, and update in WEAPON_AND_ENEMY_REFERENCE.md
- Change queen shot cooldown to 1 second, and update in WEAPON_AND_ENEMY_REFERENCE.md
- Make an enemy that predicts and shoots ahead of player's location; dark maroon rhomboid
- Make an enemy "patrol" that patrols the outside border of the map, with the wave beam
- Add an enemy that shoots shots that bounce around on the walls
- Add one shield enemy with reflective shield, which takes damage done to the shield and fires back at the player; enemy does not fire, enemy turns at speed player can flank
- Rename enemy with shield to "shield enemy"
- Add in suicide enemy that goes towards player and detonates themselves with grenade, and disappears after detonating, and damages player if in range of grenade; when enemy dies, the enemy despawns
- Make suicide enemies blow up when closer to player, not at beginning of wave
- Make suicide enemy twice as big, and 0.75x current movement speed
- Game; enemy type - spawner - spawns enemies during round
- Add a pickup for enemies spawn more often, that enemies can pick up, and that you have to shoot to destroy the pickup
- Once there are 5 enemies remaining, have them move towards the player, and the player has to move to avoid them, and the player has to shoot them to kill them
- Update WEAPON_AND_ENEMY_REFERNCE.md to reflect most recent weapons, their spawn order, enemies with their names, and their behavior patterns
- After each enemy dies, put in bottom right corner a text feed that updates "(enemy type) defeated!"
- Verify when health = zero, enemies and allies die and disappear from map

### Friendly AI
- Add friendly AI, about 1-2 per every 3-5 enemies that move independently, and attack the enemies, and help the player, with a health bar and various spawn classes and behavior patterns
- Make the friendly AI move, and make the enemy AI focus on the player, and the friendly, and move in response to the player and the friendly's bullets, and position
- Fix the health bars for the friendly ai, and make their health bars full and green at the beginning of the waves
- Make it so I cannot fly through allies
- Make it so that allies disappear after dying
- Make it so that allies disappear after dying - FIXED: Added cleanup checks and hazard collision handling
- Give allies 10x more health
- Game; fix ally collision to prevent player position and allies from being in the same spot
- New control: "ally_drop" key, "q": drop an ally behind you that regenerates every 30 seconds, that distracts all enemies chasing you

### Levels & Waves
- Survival timer, waves, multiple levels
- Make each level 3 waves, increasing in difficulty, with the last wave being the boss
- Make 3 different levels, with the final level being a boss with 10,000 health
- Multiple levels, with different themes and enemies, and pickups, and powerups
- Make lives 3 per wave, resetting at the beginning of each wave
- When player dies, keep enemy state on screen and allow player to continue next life from death point
- Allow the player to start in endurance mode
- Fix endurance mode crash when game starts
- Continue? after game is done, to add an endurance mode for postgame
- By end of game it's a bullet hell with the player having all their tools

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
- Make player's model a circle - FIXED: Changed from rectangle to circle with circular highlight
- Make bouncing bullets projectiles twice the size, and projectiles orange - FIXED: Added 2x size multiplier and orange color
- In menu, set default beam selection to basic - FIXED: Changed default selection to index 6 (basic)
- Fix issue where allies do not disappear after dying - FIXED: Added cleanup checks and hazard collision handling
- Fix issue where wave beams get stuck displayed after beam switched - FIXED: Added beam clearing when switching weapons
