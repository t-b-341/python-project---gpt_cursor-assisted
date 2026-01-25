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
- Add in more geometry (moveable blocks, unmovable blocks, destructible blocks, indestructible blocks) to fill up the map more
- VERIFIED: Make it so that player spawn and block spawn cannot overlap, player spawn takes priority - Implemented in `filter_blocks_no_overlap()` (line 2677-2678) and `random_spawn_position()` (line 3148-3150)
- VERIFIED: Prevent blocks from spawning within a radius of 10x the player size, from the player - Implemented in `filter_blocks_no_overlap()` (line 2666, 2673) and `random_spawn_position()` (line 3136, 3145)
- VERIFIED: Prevent enemies and allies from spawning where blocks are - Implemented in `random_spawn_position()` (lines 3151-3164) which checks all block types before spawning
- VERIFIED: Prevent allies or enemies from spawning in health block - Implemented in `random_spawn_position()` (line 3167-3169) which checks collision with `moving_health_zone`
- VERIFIED: Prevent boxes from overlapping with allies, on other boxes, or player, on spawn - Implemented in `random_spawn_position()` (lines 3148-3165) which checks player, blocks, and pickups
- VERIFIED: Make it so that the health box and other objects do not overlap with each other - Implemented in health zone overlap prevention code (lines 2710-2727)
- VERIFIED: Make it so that the health box does not overlap with other objects - Same as above (lines 2710-2727)
- VERIFIED: Prevent any blocks from overlapping with each other - Implemented in `filter_blocks_no_overlap()` (lines 2680-2695) which checks collisions with other blocks
- VERIFIED: Let the enemies move the blocks out of the way as well, to chase the player - Implemented in `move_enemy_with_push()` (line 3016+) which allows enemies to push moveable blocks
/

### Hazards
- VERIFIED: Make it so that the player can shoot and move the obstacles by shooting them and they move in response to being shot - Implemented in player bullet update loop (lines 1302-1317). When bullets hit hazards, they push the hazard in the direction of bullet velocity with a force of 200.0 * dt
/

## Difficulty & Scoring

- **VERIFIED (PARTIAL)**: Add a score counter and survival wave amount/time survived
  - ✅ Score counter displayed in HUD: `f"Score: {score}"` (line 1973)
  - ✅ Wave number displayed in HUD: `f"Wave: {wave_number} | Level: {current_level}"` (line 1972)
  
- **VERIFIED (PARTIAL)**: Add a high score board after each death, and the ability to type in a name
  - ✅ High score database functions exist: `init_high_scores_db()`, `save_high_score()`, `get_high_scores()` (lines 3411-3468)
  - ✅ `STATE_NAME_INPUT` and `STATE_HIGH_SCORES` states exist (constants.py)
  - ✅ Name input handling exists (lines 252-263)
- **VERIFIED (NOT IMPLEMENTED)**: Add side quests, and goal tracking; complete wave without getting hit, get a bonus 10,000 points
  - ✅ `side_quests` dictionary exists with "no_hit_wave" quest (lines 2282-2290)
  - ✅ `wave_damage_taken` variable exists (line 2291)
  /


IMPLEMENT
- ❌ Time survived NOT displayed in HUD (variable `survival_time` exists but not shown)
  - ❌ High scores screen rendering NOT implemented (line 2171: `# (High scores rendering would go here)`)
  - ❌ Name input screen rendering NOT implemented (line 2175: `# (Name input rendering would go here)`)
  - ❌ Side quest tracking logic NOT implemented (no code to check if wave completed without getting hit, no code to award bonus points, no code to activate/complete quests)
/