# Pickup Information

This document provides a comprehensive list of all pickups in the game, their effects, and spawn order.

## Pickup Types and Effects

### Health Pickups

1. **health**
   - Effect: Restores 100 HP (capped at max HP)
   - Type: Temporary restoration
   - Spawn Order: Common
   - Visual: Particle effect on collection

2. **max_health**
   - Effect: Permanently increases max HP by 15, also heals by 15
   - Type: Permanent upgrade
   - Spawn Order: Uncommon
   - Visual: Particle effect on collection

### Temporary Buffs

3. **boost**
   - Effect: Restores 45 boost meter (capped at max)
   - Type: Temporary resource
   - Spawn Order: Common
   - Visual: Particle effect on collection

4. **firerate**
   - Effect: Temporary fire rate buff (duration-based)
   - Type: Temporary buff
   - Spawn Order: Common
   - Visual: Particle effect on collection

### Permanent Stat Upgrades

5. **speed**
   - Effect: Permanently increases movement speed by 15%
   - Type: Permanent upgrade
   - Spawn Order: Uncommon
   - Visual: Particle effect on collection

6. **firerate_permanent**
   - Effect: Permanently increases fire rate by 12% (capped at 2.0x max)
   - Type: Permanent upgrade
   - Spawn Order: Uncommon
   - Visual: Particle effect on collection

7. **bullet_size**
   - Effect: Permanently increases bullet size by 20%
   - Type: Permanent upgrade
   - Spawn Order: Uncommon
   - Visual: Particle effect on collection

8. **bullet_speed**
   - Effect: Permanently increases bullet speed by 15%
   - Type: Permanent upgrade
   - Spawn Order: Uncommon
   - Visual: Particle effect on collection

9. **bullet_damage**
   - Effect: Permanently increases bullet damage by 20%
   - Type: Permanent upgrade
   - Spawn Order: Uncommon
   - Visual: Particle effect on collection

10. **bullet_knockback**
    - Effect: Permanently increases bullet knockback by 25%
    - Type: Permanent upgrade
    - Spawn Order: Rare
    - Visual: Particle effect on collection

11. **bullet_penetration**
    - Effect: Permanently adds 1 penetration (bullets can pierce through enemies AND walls/blocks)
    - Type: Permanent upgrade
    - Spawn Order: Rare
    - Visual: Particle effect on collection
    - Note: Without this pickup, bullets cannot pass through walls/blocks

12. **bullet_explosion**
    - Effect: Permanently adds 25px explosion radius to bullets
    - Type: Permanent upgrade
    - Spawn Order: Rare
    - Visual: Particle effect on collection

13. **health_regen**
    - Effect: Permanently increases health regeneration rate by 5 HP per second
    - Type: Permanent upgrade
    - Spawn Order: Rare
    - Visual: Particle effect on collection

14. **random_damage**
    - Effect: Randomizes base damage multiplier (between 0.5x and 2.0x)
    - Type: Temporary multiplier (changes each time collected)
    - Spawn Order: Rare
    - Visual: Particle effect on collection
    - HUD Display: Shows "DMG MULT: X.XXx" in HUD when active (yellow if >1.0x, red if <1.0x)

### Weapon Pickups

15. **rocket** (weapon)
    - Effect: Unlocks rocket launcher weapon, switches to it
    - Type: Weapon unlock
    - Spawn Order: Level 1 completion (also random drops from "heavy" enemies)
    - Visual: Particle effect on collection, weapon name message

16. **triple** (weapon)
    - Effect: Unlocks triple shot weapon, switches to it
    - Type: Weapon unlock
    - Spawn Order: Level 2 completion (also random drops from "baka" enemies)
    - Visual: Particle effect on collection, weapon name message

17. **wave_beam** (weapon)
    - Effect: Unlocks wave beam weapon, switches to it
    - Type: Weapon unlock
    - Spawn Order: Level 3 completion (also random drops from "BIG NEKU" enemies, second to last)
    - Visual: Particle effect on collection, weapon name message

18. **giant** / **giant_bullets** (weapon)
    - Effect: Unlocks giant bullets weapon, switches to it
    - Type: Weapon unlock
    - Spawn Order: Level 4 completion (last)
    - Visual: Particle effect on collection, weapon name message

19. **bouncing** (weapon)
    - Effect: Unlocks bouncing bullets weapon, switches to it
    - Type: Weapon unlock
    - Spawn Order: Random drops from "neko neko desu" and "bouncer" enemies
    - Visual: Particle effect on collection, weapon name message

20. **laser** (weapon)
    - Effect: Unlocks laser beam weapon, switches to it
    - Type: Weapon unlock
    - Spawn Order: Random drops only
    - Visual: Particle effect on collection, weapon name message

### Special Pickups

21. **spawn_boost**
    - Effect: Reduces ally drop cooldown by 20% (boosts player's ability to spawn allies)
    - Type: Permanent upgrade (stacks, minimum cooldown 1 second)
    - Spawn Order: Rare
    - Visual: Particle effect on collection
    - Note: Enemies cannot collect pickups - only the player can collect them

## Spawn Order Summary

### By Rarity:
- **Common**: health, boost, firerate
- **Uncommon**: max_health, speed, firerate_permanent, bullet_size, bullet_speed, bullet_damage
- **Rare**: bullet_knockback, bullet_penetration, bullet_explosion, health_regen, random_damage, spawn_boost
- **Weapon Unlocks**: rocket (Level 1), triple (Level 2), wave_beam (Level 3), giant (Level 4)
- **Random Weapons**: bouncing, laser (via enemy drops)

### By Level Completion:
- Level 1: rocket
- Level 2: triple
- Level 3: wave_beam
- Level 4: giant

### By Enemy Drops (30% chance):
- **grunt** / **stinky**: basic (but basic is not dropped - pickup skipped)
- **heavy**: rocket
- **baka**: triple
- **neko neko desu**: bouncing
- **BIG NEKU**: wave_beam
- **bouncer**: bouncing

## Notes

- All pickups despawn after 15 seconds if not collected (weapon pickups last 10 seconds)
- Weapon pickups automatically switch the player to that weapon when collected
- Permanent upgrades stack (can be collected multiple times)
- Fire rate permanent upgrade is capped at 2.0x maximum to prevent performance issues
- Basic weapon is not dropped as a pickup (starting weapon only)
- **Bullet penetration is required to shoot through walls/blocks** - without the penetration pickup, bullets stop at destructible blocks
- All pickups create a particle effect when collected
- Random damage multiplier is displayed in HUD when active (not 1.0x)
- Player base health is reduced by 0.75x (750 HP instead of 1000 HP for default class)
- **Enemies cannot collect pickups** - only the player can collect them (enemies only detect pickups for collision avoidance)
