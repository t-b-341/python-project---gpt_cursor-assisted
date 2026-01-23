# Weapon and Enemy Reference Guide

This document provides a comprehensive reference for all weapons and enemies in the game.

## Weapons

### Player Weapons

1. **basic** (Key: 1)
   - Standard peashooter weapon
   - Default starting weapon
   - Normal damage and fire rate

2. **rocket** (Key: 2)
   - Rocket launcher
   - Slower fire rate (3.5x multiplier)
   - 2.5x damage multiplier
   - Area of Effect (AOE) explosion: 120px base radius (increased from 80px)
   - Explosion damage falls off with distance
   - Orange colored projectiles

3. **triple** (Key: 3)
   - Triple shot weapon
   - Fires 3 bullets in a spread pattern
   - Unlocked via pickup

4. **bouncing** (Key: 4)
   - Bouncing bullets weapon
   - Bullets bounce off walls up to 10 times
   - Unlocked via pickup

5. **giant** (Key: 5)
   - Giant bullets weapon
   - 10x bullet size multiplier
   - Unlocked via pickup

6. **laser** (Key: 6)
   - Laser beam weapon
   - Continuous beam while mouse is held
   - 800px maximum length
   - 50 damage per frame while on target
   - Unlocked via pickup

7. **wave_beam** (Key: 7)
   - Wave pattern beam weapon
   - Fires in trigonometric wave patterns
   - 1000px beam length
   - 10px beam width
   - 30 damage per frame while on target
   - Currently only uses "sine" pattern
   - Unlocked at game start (slot 2)

### Wave Beam Patterns (Currently Only Sine Active)

The wave beam system supports these trigonometric patterns (currently only "sine" is enabled):
- **sine** - Standard sine wave pattern
- **cosine** - Cosine wave pattern
- **tangent** - Tangent wave pattern (clamped to prevent infinite values)
- **cotangent** - Cotangent wave pattern (clamped to prevent infinite values)
- **secant** - Secant wave pattern (clamped to prevent infinite values)
- **cosecant** - Cosecant wave pattern (clamped to prevent infinite values)

## Enemies

### Regular Enemies

1. **grunt**
   - Basic enemy type
   - HP: 60 (scales with wave)
   - Speed: 90
   - Shoot cooldown: 0.9s
   - Projectile: Square, blue color
   - Projectile speed: 320

3. **heavy**
   - Heavier, slower enemy
   - HP: 80 (scales with wave)
   - Speed: 70
   - Shoot cooldown: 1.2s
   - Projectile: Circle, orange color
   - Projectile speed: 280

4. **stinky**
   - Fast enemy type
   - HP: 60 (scales with wave)
   - Speed: 110
   - Shoot cooldown: 0.9s
   - Projectile: Diamond, blue color
   - Projectile speed: 320

5. **baka**
   - High HP, fast-firing enemy
   - HP: 300 (capped at 300)
   - Speed: 150
   - Shoot cooldown: 0.1s (very fast)
   - Projectile: Square, pink color
   - Projectile speed: 500

6. **neko neko desu**
   - Low HP, very fast-firing enemy
   - HP: 20 (scales with wave)
   - Speed: 160
   - Shoot cooldown: 0.01s (extremely fast)
   - Projectile: Circle, green color
   - Projectile speed: 500

7. **BIG NEKU**
   - High HP, slow-moving enemy
   - HP: 300 (capped at 300)
   - Speed: 60
   - Shoot cooldown: 1.0s
   - Projectile: Diamond, blue color
   - Projectile speed: 700

8. **bouncer**
   - Enemy that fires bouncing projectiles
   - HP: 70 (scales with wave)
   - Speed: 85
   - Shoot cooldown: 1.5s
   - Projectile: Square, red color
   - Projectile speed: 350
   - Special: Projectiles bounce off walls

9. **shielded**
   - Enemy with directional shield
   - HP: 100 (scales with wave)
   - Speed: 60
   - Shoot cooldown: 1.0s
   - Projectile: Circle, blue color
   - Projectile speed: 300
   - Special: Has a front-facing shield that blocks bullets from the front
   - Shield length: 50px
   - Shield rotates to face threats

10. **reflector**
    - Enemy with reflective shield
    - HP: 150 (scales with wave)
    - Speed: 40 (slow)
    - Shoot cooldown: 999.0s (doesn't shoot)
    - Special: Has a reflective shield that reflects player bullets back
    - Shield length: 60px
    - Shield turns slowly toward threats (0.5 rad/s)
    - Shield absorbs damage and fires reflected projectiles

11. **spawner**
    - Enemy that spawns other enemies during the round
    - HP: 120 (scales with wave)
    - Speed: 50 (slow)
    - Shoot cooldown: 999.0s (doesn't shoot)
    - Special: Spawns enemies every 5 seconds
    - Max spawns: 3 enemies per spawner
    - Spawns random enemy types (excluding spawner and queen)

12. **queen**
    - Maroon enemy (player clone)
    - HP: 5000 (fixed, does not scale, increased from 2000)
    - Speed: 240 (3x standard speed)
    - Shoot cooldown: 0.2s (increased fire rate, changed from 1.0s)
    - Projectile: Circle, dark red color
    - Projectile speed: 350
    - Special abilities:
      - Has a shield that activates and deactivates (10-20s phases, active for 5-10s)
      - Shield rotates to face the player when active
      - Can use grenades (5 second cooldown)
      - Rage mode: Activates after taking 300-500 damage, lasts 5 seconds
      - In rage mode: Uses grenades aggressively and destroys nearby destructible blocks
      - Predicts player position when shooting
    - Behavior: Advanced AI that mimics player abilities

13. **suicide**
    - Suicide bomber enemy
    - HP: 30 (scales with wave)
    - Speed: 120 (fast movement toward player)
    - Shoot cooldown: 999.0s (doesn't shoot)
    - Special: Moves directly toward player and detonates when within 80 pixels
    - Explosion range: 150 pixels
    - Explosion damage: Same as player grenade (500 damage)
    - Behavior: Despawns immediately after detonation (no weapon drops)

10. **spawner**
    - Enemy that spawns other enemies during the round
    - HP: 120 (scales with wave)
    - Speed: 50 (slow)
    - Shoot cooldown: 999.0s (doesn't shoot)
    - Special: Spawns enemies every 5 seconds
    - Max spawns: 3 enemies per spawner
    - Spawns random enemy types (excluding spawner and queen)

11. **queen**
    - Maroon enemy (player clone)
    - HP: 5000 (fixed, does not scale, increased from 2000)
    - Speed: 240 (3x standard speed)
    - Shoot cooldown: 0.2s (increased fire rate, changed from 1.0s)
    - Projectile: Circle, dark red color
    - Projectile speed: 350
    - Special abilities:
      - Has a shield that activates and deactivates (10-20s phases, active for 5-10s)
      - Shield rotates to face the player when active
      - Can use grenades (5 second cooldown)
      - Rage mode: Activates after taking 300-500 damage, lasts 5 seconds
      - In rage mode: Uses grenades aggressively and destroys nearby destructible blocks
      - Predicts player position when shooting
    - Behavior: Advanced AI that mimics player abilities

12. **suicide**
    - Suicide bomber enemy
    - HP: 30 (scales with wave)
    - Speed: 120 (fast movement toward player)
    - Shoot cooldown: 999.0s (doesn't shoot)
    - Special: Moves directly toward player and detonates when within 80 pixels
    - Explosion range: 150 pixels
    - Explosion damage: Same as player grenade (500 damage)
    - Behavior: Despawns immediately after detonation (no weapon drops)

### Boss Enemy

1. **FINAL_BOSS**
   - Boss enemy (spawns on wave 3 of each level)
   - HP: 300 (capped at 300, scales with level)
   - Speed: 50
   - Shoot cooldown: 0.5s
   - Projectile: Circle, red color
   - Projectile speed: 400
   - Special: Has 3 phases with different attack patterns
   - Phase thresholds: 66% HP (Phase 2), 33% HP (Phase 3)

## Friendly AI Types

Friendly AI units help the player fight enemies. They have different behavior patterns:

1. **scout** - Fast, aggressive behavior
2. **guard** - Defensive, stays near player
3. **sniper** - Ranged, keeps distance from enemies
4. **tank** - Slow advance, high durability

All friendly AI have:
- Max HP: 100
- Health bars that are green when full
- Independent targeting and movement
- Projectile attacks against enemies

## Notes

- All enemy HP values scale with wave number and difficulty
- Enemy HP is capped at 300 maximum (including bosses)
- Boss enemies spawn on wave 3 of each level
- Weapons can be unlocked via pickups or at game start
- Rocket launcher has increased AOE explosion radius (120px base, up from 80px)
