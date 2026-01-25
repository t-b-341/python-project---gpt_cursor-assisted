"""Page dataclass and registry of all plot pages."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Callable, List

import matplotlib.pyplot as plt

from telemetry_viz.plots_player import (
    draw_movement_path,
    draw_movement_heatmap,
    draw_movement_path_with_velocity,
    draw_player_velocity_over_time,
    draw_shots_scatter,
)
from telemetry_viz.plots_damage import (
    draw_damage_taken_timeline,
    draw_damage_taken_by_enemy,
    draw_damage_dealt_by_enemy,
    draw_damage_heatmap_by_wave,
    draw_death_locations,
)
from telemetry_viz.plots_waves import (
    draw_wave_progression,
    draw_wave_difficulty_scaling,
    draw_survival_time_per_wave,
)
from telemetry_viz.plots_meta import (
    draw_accuracy_over_runs,
    draw_damage_totals_over_runs,
    draw_performance_summary_view,
)
from telemetry_viz.plots_misc import (
    draw_bullet_shape_distribution,
    draw_bullet_color_usage,
    draw_enemy_movement_paths,
    draw_enemy_density_heatmap,
    draw_score_progression,
    draw_score_by_source,
    draw_level_progression,
    draw_boss_encounters,
    draw_weapon_usage,
    draw_pickup_collection,
    draw_overshield_usage,
    draw_player_action_frequency,
    draw_weapon_effectiveness_comparison,
    draw_action_patterns_with_cte,
    draw_running_statistics,
    draw_zone_effectiveness,
)


@dataclass
class Page:
    title: str
    filename: str
    draw: Callable[[plt.Axes, sqlite3.Connection, int], bool]


def get_pages() -> List[Page]:
    """Return the default list of plot pages in display order."""
    return [
        Page("Movement path", "movement_path.png", draw_movement_path),
        Page("Movement heatmap", "movement_heatmap.png", draw_movement_heatmap),
        Page("Movement path with velocity", "movement_path_velocity.png", draw_movement_path_with_velocity),
        Page("Player velocity over time", "player_velocity.png", draw_player_velocity_over_time),
        Page("Shots scatter", "shots_scatter.png", draw_shots_scatter),
        Page("Damage taken timeline", "damage_taken_timeline.png", draw_damage_taken_timeline),
        Page("Damage taken by enemy type", "damage_taken_by_enemy.png", draw_damage_taken_by_enemy),
        Page("Damage dealt by enemy type", "damage_dealt_by_enemy.png", draw_damage_dealt_by_enemy),
        Page("Damage heatmap by wave", "damage_heatmap_wave.png", draw_damage_heatmap_by_wave),
        Page("Death locations", "death_locations.png", draw_death_locations),
        Page("Wave progression", "wave_progression.png", draw_wave_progression),
        Page("Wave difficulty scaling", "wave_difficulty.png", draw_wave_difficulty_scaling),
        Page("Survival time per wave", "survival_per_wave.png", draw_survival_time_per_wave),
        Page("Enemy movement paths", "enemy_movement.png", draw_enemy_movement_paths),
        Page("Enemy density heatmap", "enemy_density.png", draw_enemy_density_heatmap),
        Page("Bullet shape distribution", "bullet_shapes.png", draw_bullet_shape_distribution),
        Page("Bullet color usage", "bullet_colors.png", draw_bullet_color_usage),
        Page("Score progression", "score_progression.png", draw_score_progression),
        Page("Score by source", "score_by_source.png", draw_score_by_source),
        Page("Level progression", "level_progression.png", draw_level_progression),
        Page("Boss encounters", "boss_encounters.png", draw_boss_encounters),
        Page("Weapon usage", "weapon_usage.png", draw_weapon_usage),
        Page("Pickup collection", "pickup_collection.png", draw_pickup_collection),
        Page("Overshield usage", "overshield_usage.png", draw_overshield_usage),
        Page("Player action frequency", "player_actions.png", draw_player_action_frequency),
        Page("Weapon effectiveness comparison", "weapon_effectiveness.png", draw_weapon_effectiveness_comparison),
        Page("Action patterns (CTE)", "action_patterns.png", draw_action_patterns_with_cte),
        Page("Running statistics", "running_stats.png", draw_running_statistics),
        Page("Zone effectiveness", "zone_effectiveness.png", draw_zone_effectiveness),
        Page("Performance summary (View)", "performance_summary.png", draw_performance_summary_view),
        Page("Accuracy over runs", "accuracy_over_runs.png", draw_accuracy_over_runs),
        Page("Damage totals over runs", "damage_totals_over_runs.png", draw_damage_totals_over_runs),
    ]


def get_pages_all_runs() -> List[Page]:
    """Return only the pages that show data aggregated over all runs."""
    all_pages = get_pages()
    # Indices (0-based) of cross-run / all-runs pages in get_pages() order
    all_runs_indices = {30, 31}  # Accuracy over runs, Damage totals over runs
    return [p for i, p in enumerate(all_pages) if i in all_runs_indices]
