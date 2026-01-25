# Pickup Reference Guide

This document provides a comprehensive list of all pickups in the game, their effects, and spawn order.

## Pickup Types and Effects

### Health Pickups

1. **health**
   - Effect: Restores 100 HP (capped at max HP)
   - Type: Temporary restoration
   - Spawn Order: Common

2. **max_health**
   - Effect: Permanently increases max HP by 15, also heals by 15
   - Type: Permanent upgrade
   - Spawn Order: Uncommon

### Temporary Buffs

3. **boost**
   - Effect: Restores 45 boost meter (capped at max)
   - Type: Temporary resource
   - Spawn Order: Common

4. **firerate**
   - Effect: Temporary fire rate buff (duration-based)
   - Type: Temporary buff
   - Spawn Order: Common

### Permanent Stat Upgrades

5. **speed**
   - Effect: Permanently increases movement speed by 15%
   - Type: Permanent upgrade
   - Spawn Order: Uncommon

6. **firerate_permanent**
   - Effect: Permanently increases fire rate by 12% (capped at 2.0x max)
   - Type: Permanent upgrade
   - Spawn Order: Uncommon

7. **bullet_size**
   - Effect: Permanently increases bullet size by 20%
   - Type: Permanent upgrade
   - Spawn Order: Uncommon

8. **bullet_speed**
   - Effect: Permanently increases bullet speed by 15%
   - Type: Permanent upgrade
   - Spawn Order: Uncommon

9. **bullet_damage**
   - Effect: Permanently increases bullet damage by 20%
   - Type: Permanent upgrade
   - Spawn Order: Uncommon

10. **bullet_knockback**
    - Effect: Permanently increases bullet knockback by 25%
    - Type: Permanent upgrade
    - Spawn Order: Rare

11. **bullet_penetration**
    - Effect: Permanently adds 1 penetration (bullets can pierce through enemies)
    - Type: Permanent upgrade
    - Spawn Order: Rare

12. **bullet_explosion**
    - Effect: Permanently adds 25px explosion radius to bullets
    - Type: Permanent upgrade
    - Spawn Order: Rare

13. **health_regen**
    - Effect: Permanently increases health regeneration rate by 5 HP per second
    - Type: Permanent upgrade
    - Spawn Order: Rare

### Weapon Pickups

14. **rocket** (weapon)
    - Effect: Unlocks rocket launcher weapon
    - Type: Weapon unlock
    - Spawn Order: Level 1 completion (also random drops)

15. **triple** (weapon)
    - Effect: Unlocks triple shot weapon
    - Type: Weapon unlock
    - Spawn Order: Level 2 completion (also random drops)

16. **wave_beam** (weapon)
    - Effect: Unlocks wave beam weapon
    - Type: Weapon unlock
    - Spawn Order: Level 3 completion (second to last)

17. **giant** / **giant_bullets** (weapon)
    - Effect: Unlocks giant bullets weapon
    - Type: Weapon unlock
    - Spawn Order: Level 4 completion (last)

18. **bouncing** (weapon)
    - Effect: Unlocks bouncing bullets weapon
    - Type: Weapon unlock
    - Spawn Order: Random drops only

19. **laser** (weapon)
    - Effect: Unlocks laser beam weapon
    - Type: Weapon unlock
    - Spawn Order: Random drops only

### Special Pickups

20. **spawn_boost**
    - Effect: Enemies can collect this to increase spawn rate; player can shoot to destroy
    - Type: Enemy buff (negative for player)
    - Spawn Order: Random

## Spawn Order Summary

### By Rarity:
- **Common**: health, boost, firerate
- **Uncommon**: max_health, speed, firerate_permanent, bullet_size, bullet_speed, bullet_damage
- **Rare**: bullet_knockback, bullet_penetration, bullet_explosion, health_regen
- **Weapon Unlocks**: rocket (Level 1), triple (Level 2), wave_beam (Level 3), giant (Level 4)
- **Random Weapons**: bouncing, laser (via enemy drops)

### By Level Completion:
- Level 1: rocket
- Level 2: triple
- Level 3: wave_beam
- Level 4: giant

## Notes

- All pickups despawn after 15 seconds if not collected
- Weapon pickups automatically switch the player to that weapon when collected
- Permanent upgrades stack (can be collected multiple times)
- Fire rate permanent upgrade is capped at 2.0x maximum to prevent performance issues
- Basic weapon is not dropped as a pickup (starting weapon only)
