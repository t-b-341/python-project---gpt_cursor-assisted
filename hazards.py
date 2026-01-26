"""Rotating paraboloid/trapezoid hazard system. Used by game.py for collision and rendering."""
from __future__ import annotations

import math

import pygame

# Design-time dimensions for initial hazard layout (same as game default)
_WIDTH = 1920
_HEIGHT = 1080

# Rotating paraboloid/trapezoid hazard system
# On level 1: paraboloids, on level 2+: trapezoids
hazard_obstacles: list[dict] = [
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
        "center": pygame.Vector2(_WIDTH - 250, 250),  # Top-right corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 1.0,
        "rotation_speed": 0.75,  # 3x faster (0.25 * 3)
        "orbit_center": pygame.Vector2(_WIDTH - 250, 250),
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
        "center": pygame.Vector2(250, _HEIGHT - 250),  # Bottom-left corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 2.0,
        "rotation_speed": 1.05,  # 3x faster (0.35 * 3)
        "orbit_center": pygame.Vector2(250, _HEIGHT - 250),
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
        "center": pygame.Vector2(_WIDTH - 250, _HEIGHT - 250),  # Bottom-right corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 1.5,
        "rotation_speed": 0.84,  # 3x faster (0.28 * 3)
        "orbit_center": pygame.Vector2(_WIDTH - 250, _HEIGHT - 250),
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


def generate_paraboloid_points(center: pygame.Vector2, width: float, height: float, rotation: float) -> list[pygame.Vector2]:
    """Generate points for a paraboloid shape (parabolic curve in 2D)."""
    points = []
    num_points = 100  # Number of points for smooth curve

    for i in range(num_points + 1):
        t = (i / num_points) * 2.0 - 1.0
        x_local = t * (width / 2)
        y_local = (t ** 2) * (height / 2)  # Parabolic curve
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)
        x_rotated = x_local * cos_r - y_local * sin_r
        y_rotated = x_local * sin_r + y_local * cos_r
        point = pygame.Vector2(
            center.x + x_rotated,
            center.y + y_rotated
        )
        points.append(point)

    return points


def generate_trapezoid_points(center: pygame.Vector2, width: float, height: float, rotation: float) -> list[pygame.Vector2]:
    """Generate points for a trapezoid shape."""
    points = []
    top_width = width * 0.6
    bottom_width = width
    local_points = [
        (-top_width / 2, -height / 2),  # Top left
        (top_width / 2, -height / 2),   # Top right
        (bottom_width / 2, height / 2),  # Bottom right
        (-bottom_width / 2, height / 2),  # Bottom left
    ]
    cos_r = math.cos(rotation)
    sin_r = math.sin(rotation)
    for x_local, y_local in local_points:
        x_rotated = x_local * cos_r - y_local * sin_r
        y_rotated = x_local * sin_r + y_local * cos_r
        point = pygame.Vector2(center.x + x_rotated, center.y + y_rotated)
        points.append(point)

    return points


def check_point_in_hazard(point: pygame.Vector2, hazard_points: list[pygame.Vector2], bounding_rect: pygame.Rect) -> bool:
    """Check if a point is inside the hazard shape (paraboloid or trapezoid). Uses point-in-polygon algorithm."""
    if not bounding_rect.collidepoint(point.x, point.y):
        return False

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


def resolve_hazard_collision(hazard1: dict, hazard2: dict) -> None:
    """Resolve collision between two hazards - make them bounce off each other."""
    center1 = hazard1["center"]
    center2 = hazard2["center"]
    normal = (center2 - center1)
    if normal.length_squared() > 0:
        normal = normal.normalize()
    else:
        normal = pygame.Vector2(1, 0)

    rel_vel = hazard2["velocity"] - hazard1["velocity"]
    vel_along_normal = rel_vel.dot(normal)

    if vel_along_normal > 0:
        return

    restitution = 0.8
    impulse = vel_along_normal * restitution

    hazard1["velocity"] += normal * impulse
    hazard2["velocity"] -= normal * impulse

    separation = 10.0
    hazard1["center"] -= normal * separation
    hazard2["center"] += normal * separation


def update_hazard_obstacles(dt: float, hazard_list: list, current_lvl: int, width: int, height: int) -> None:
    """Update all rotating hazard obstacles (paraboloids/trapezoids) with collision physics."""
    for hazard in hazard_list:
        if current_lvl >= 2:
            hazard["shape"] = "trapezoid"
        else:
            hazard["shape"] = "paraboloid"
        hazard["rotation_angle"] += hazard["rotation_speed"] * dt
        if hazard["rotation_angle"] >= 2 * math.pi:
            hazard["rotation_angle"] -= 2 * math.pi

        hazard["orbit_angle"] += hazard["orbit_speed"] * dt
        if hazard["orbit_angle"] >= 2 * math.pi:
            hazard["orbit_angle"] -= 2 * math.pi

        orbit_pos = pygame.Vector2(
            hazard["orbit_center"].x + math.cos(hazard["orbit_angle"]) * hazard["orbit_radius"],
            hazard["orbit_center"].y + math.sin(hazard["orbit_angle"]) * hazard["orbit_radius"]
        )

        hazard["center"] += hazard["velocity"] * dt
        hazard["center"] = hazard["center"] * 0.5 + orbit_pos * 0.5

        # Keep within screen bounds with bounce (use width, height params)
        if hazard["center"].x < hazard["width"] // 2:
            hazard["center"].x = hazard["width"] // 2
            hazard["velocity"].x = abs(hazard["velocity"].x)
        elif hazard["center"].x > width - hazard["width"] // 2:
            hazard["center"].x = width - hazard["width"] // 2
            hazard["velocity"].x = -abs(hazard["velocity"].x)

        if hazard["center"].y < hazard["height"] // 2:
            hazard["center"].y = hazard["height"] // 2
            hazard["velocity"].y = abs(hazard["velocity"].y)
        elif hazard["center"].y > height - hazard["height"] // 2:
            hazard["center"].y = height - hazard["height"] // 2
            hazard["velocity"].y = -abs(hazard["velocity"].y)

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

    for i in range(len(hazard_list)):
        for j in range(i + 1, len(hazard_list)):
            if check_hazard_collision(hazard_list[i], hazard_list[j]):
                resolve_hazard_collision(hazard_list[i], hazard_list[j])
