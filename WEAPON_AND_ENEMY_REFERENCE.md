# Weapon and Enemy Reference Guide

This document provides a comprehensive reference for all weapons and enemies in the game.

## Weapons

### Player Weapons (Spawn Order)

1. **basic** (Key: 1)
   - Standard peashooter weapon
   - Default starting weapon
   - Normal damage and fire rate
   - Always available

2. **wave_beam** (Key: 7)
   - Wave pattern beam weapon
   - Fires in trigonometric wave patterns
   - 1000px beam length
   - 10px beam width
   - 30 damage per frame while on target
   - Available at game start (slot 2)

3. **rocket** (Key: 2)
   - Rocket launcher
   - Unlocked: Level 1 (Boss drop)
   - Slower fire rate (3.5x multiplier)
   - 2.5x damage multiplier
   - Area of Effect (AOE) explosion: 120px base radius
   - Explosion damage falls off with distance
   - Orange colored projectiles

4. **triple** (Key: 3)
   - Triple shot weapon
   - Unlocked: Level 2 (Boss drop)
   - Fires 3 bullets in a spread pattern
   - Unlocked via pickup

5. **wave_beam** (Key: 7)
   - Wave pattern beam weapon
   - Unlocked: Level 3 (Boss drop) - Second to last
   - Fires in trigonometric wave patterns
   - 1000px beam length
   - 10px beam width
   - 30 damage per frame while on target

6. **giant** (Key: 5)
   - Giant bullets weapon
   - Unlocked: Level 4+ (Boss drop) - Last weapon
   - 10x bullet size multiplier
   - Unlocked via pickup

7. **bouncing** (Key: 4)
   - Bouncing bullets weapon
   - Bullets bounce off walls up to 10 times
   - Bullets are 2x size and orange colored
   - Unlocked via pickup

8. **laser** (Key: 6)
   - Laser beam weapon
   - Continuous beam while mouse is held
   - 800px maximum length
   - 50 damage per frame while on target
   - Unlocked via pickup

### Weapon Unlock Order
1. **basic** - Always available
2. **wave_beam** - Available at start
3. **rocket** - Level 1 boss
4. **triple** - Level 2 boss
5. **wave_beam** - Level 3 boss (second to last)
6. **giant** - Level 4+ boss (last)

## Enemies

### Regular Enemies

1. **grunt**
   - Basic enemy type
   - HP: 60 (scales with wave, 110% multiplier)
   - Speed: 90 (110% multiplier)
   - Shoot cooldown: 0.9s (110% fire rate)
   - Projectile: Square, blue color
   - Projectile speed: 320
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

2. **heavy**
   - Heavier, slower enemy
   - HP: 80 (scales with wave, 110% multiplier)
   - Speed: 70 (110% multiplier)
   - Shoot cooldown: 1.2s (110% fire rate)
   - Projectile: Circle, orange color
   - Projectile speed: 280
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

3. **stinky**
   - Fast enemy type
   - HP: 60 (scales with wave, 110% multiplier)
   - Speed: 110 (110% multiplier)
   - Shoot cooldown: 0.9s (110% fire rate)
   - Projectile: Diamond, blue color
   - Projectile speed: 320
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

4. **baka**
   - High HP, fast-firing enemy
   - HP: 300 (capped at 300, 110% multiplier)
   - Speed: 150 (110% multiplier)
   - Shoot cooldown: 0.1s (very fast, 110% fire rate)
   - Projectile: Square, pink color
   - Projectile speed: 500
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

5. **neko neko desu**
   - Low HP, very fast-firing enemy
   - HP: 20 (scales with wave, 110% multiplier)
   - Speed: 160 (110% multiplier)
   - Shoot cooldown: 0.01s (extremely fast, 110% fire rate)
   - Projectile: Circle, green color
   - Projectile speed: 500
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

6. **BIG NEKU**
   - High HP, slow-moving enemy
   - HP: 300 (capped at 300, 110% multiplier)
   - Speed: 60 (110% multiplier)
   - Shoot cooldown: 1.0s (110% fire rate)
   - Projectile: Diamond, blue color
   - Projectile speed: 700
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

7. **bouncer**
   - Enemy that fires bouncing projectiles
   - HP: 70 (scales with wave, 110% multiplier)
   - Speed: 85 (110% multiplier)
   - Shoot cooldown: 1.5s (110% fire rate)
   - Projectile: Square, red color
   - Projectile speed: 350
   - Special: Projectiles bounce off walls
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

8. **shielded**
   - Enemy with directional shield
   - HP: 100 (scales with wave, 110% multiplier)
   - Speed: 60 (110% multiplier)
   - Shoot cooldown: 1.0s (110% fire rate)
   - Projectile: Circle, blue color
   - Projectile speed: 300
   - Special: Has a front-facing shield that blocks bullets from the front
   - Shield length: 50px
   - Shield rotates to face threats
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

9. **reflector**
   - Enemy with reflective shield
   - HP: 150 (scales with wave, 110% multiplier)
   - Speed: 40 (slow, 110% multiplier)
   - Shoot cooldown: 999.0s (doesn't shoot)
   - Special: Has a reflective shield that reflects player bullets back
   - Shield length: 60px
   - Shield turns slowly toward threats (0.5 rad/s)
   - Shield absorbs damage and fires reflected projectiles
   - Behavior: Standard enemy, prioritizes player unless player is over half map away

10. **pawn**
    - Basic enemy class
    - HP: 60 (scales with wave, 110% multiplier)
    - Speed: 90 (basic movement speed, 110% multiplier)
    - Shoot cooldown: 0.9s (basic beam weapon, 110% fire rate)
    - Projectile: Circle, gray color
    - Projectile speed: 320
    - Behavior: Standard enemy, prioritizes player unless player is over half map away

11. **spawner**
    - Enemy that spawns other enemies
    - HP: 200 (scales with wave, 110% multiplier)
    - Speed: 30 (slow movement, 110% multiplier)
    - Shoot cooldown: 5.0s (spawns enemies every 5 seconds)
    - Color: Purple
    - Special: Spawns random enemy types during the round
    - Does not shoot projectiles
    - Behavior: Standard enemy, prioritizes player unless player is over half map away

12. **queen**
    - Maroon "player copy" enemy
    - HP: 5000 (increased from 2000, 110% multiplier)
    - Speed: 240 (3x standard speed, 110% multiplier)
    - Shoot cooldown: 0.2s (increased rate of fire, 110% fire rate)
    - Projectile: Diamond (rhomboid shape), dark red color
    - Projectile speed: 400
    - Special abilities:
      - Predictive aiming (shoots ahead of player)
      - Shield: Directional shield like shield enemy that activates and deactivates in cycles
        - Shield phase duration: 10-20 seconds (random, inactive period)
        - Shield active duration: 5-10 seconds (random, active period)
        - Shield blocks damage from front when active
        - Shield rotates to face threats when active
      - Grenades: When enraged and player is within 200px, throws grenades at player
      - Enraged state: After taking 300-500 damage (random threshold), enters 5-second enraged state
      - Destroys destructible cover with grenades to reduce player hiding spots
    - Behavior: Aggressive pursuit, prioritizes player

13. **suicide**
    - Suicide bomber enemy
    - HP: 30 (scales with wave, 110% multiplier)
    - Speed: 150 (fast movement towards player, 110% multiplier)
    - Shoot cooldown: 999.0s (doesn't shoot)
    - Color: Bright red
    - Special: Moves directly towards player and detonates when within 200px
    - Detonation radius: 200px
    - Detonation damage: 150 to player
    - Behavior: Direct movement towards player, detonates on contact
    - Disappears after detonation

14. **patrol**
    - Border patrol enemy
    - HP: 100 (scales with wave, 110% multiplier)
    - Speed: 80 (moderate speed for patrolling, 110% multiplier)
    - Shoot cooldown: 0.5s (wave beam weapon)
    - Projectile: Wave beam (lime green, undulating pattern)
    - Projectile speed: 400
    - Color: Light blue
    - Special: Patrols the outside border of the map in a rectangular path
    - Weapon: Wave beam (trigonometric wave pattern)
    - Behavior: Moves along map border, shoots wave beams at player

### Boss Enemy

1. **FINAL_BOSS**
   - Boss enemy (spawns on wave 3 of each level)
   - HP: 300 (capped at 300, scales with level, 110% multiplier)
   - Speed: 50 (110% multiplier)
   - Shoot cooldown: 0.5s (110% fire rate)
   - Projectile: Circle, red color
   - Projectile speed: 400
   - Special: Has 3 phases with different attack patterns
   - Phase thresholds: 66% HP (Phase 2), 33% HP (Phase 3)
   - Phase 1: Single shots
   - Phase 2: Triple shot spread (faster shooting)
   - Phase 3: 8-way spread (very fast shooting)
   - Behavior: Aggressive pursuit, prioritizes player

## Enemy Behavior Patterns

### Threat Prioritization
- **Default**: Enemies prioritize the player for damage
- **Exception**: If the player is over half the map distance away, enemies prioritize nearby allies instead
- **Fallback**: If no nearby allies are found, enemies still target the player

### Movement Patterns
- **Standard**: Enemies move towards nearest threat (player or nearby ally)
- **Aggressive**: When 5 or fewer enemies remain, they move directly towards player
- **Dodging**: Enemies attempt to dodge player bullets when nearby
- **Suicide**: Moves directly towards player and detonates on contact

## Friendly AI Types

Friendly AI units help the player fight enemies. They have different behavior patterns:

1. **scout** - Fast, aggressive behavior
2. **guard** - Defensive, stays near player
3. **sniper** - Ranged, keeps distance from enemies
4. **tank** - Slow advance, high durability

All friendly AI have:
- Max HP: 1100 (110% multiplier)
- Health bars that are green when full
- Independent targeting and movement
- Projectile attacks against enemies
- 110% movement speed, damage, and fire rate multipliers

## Notes

- All enemy HP values scale with wave number and difficulty (110% multiplier applied)
- Enemy HP is capped at 300 maximum (including bosses, except queen)
- Boss enemies spawn on wave 3 of each level
- Weapons can be unlocked via pickups or boss drops
- Rocket launcher has increased AOE explosion radius (120px base)
- Bouncing bullets are 2x size and orange colored
- Queen enemy is a challenging "player copy" with shield, grenades, and enraged behavior
- Suicide enemies detonate on contact with player, dealing 150 damage
- Enemies prioritize player damage unless player is over half map away, then prioritize nearby allies
