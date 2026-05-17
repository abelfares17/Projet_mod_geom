"""
Partie 5 — Réseau d'influence visuel.

Chaque poisson ne perçoit que les poissons dans son cône de vision (angle
de demi-ouverture θ = vision_angle_deg / 2 autour de sa direction).

    visible = { p_j | angle(d⃗, v⃗_i) < θ }

Les forces d'Aoki sont ensuite appliquées uniquement aux voisins visibles.
"""

from ..config import SimConfig
from ..core.school import School
from .aoki import compute_forces
from . import movement
import numpy as np

def is_visible(fish_i, fish_j, config) -> bool:
    d_vec = fish_j.position - fish_i.position
    d = np.linalg.norm(d_vec)
    if d < 1e-12:
        return False

    speed = np.linalg.norm(fish_i.velocity)

    if speed < 1e-12:
        return True
    
    direction = d_vec / d
    velocity_dir = fish_i.velocity / speed
    cos_angle = np.dot(direction, velocity_dir)
    cos_half_angle = np.cos(np.radians(config.vision_angle_deg / 2))
    return cos_angle >= cos_half_angle

def step(school: School, config: SimConfig, step_count: int = 0) -> None:
    new_velocities = []
    for fish in school.fish:
        neighbors = []
        for other in school.fish:
            if is_visible(fish, other, config):
                neighbors.append(other)
            
        force = compute_forces(fish, neighbors, config)
        # Nouvelle vélocité
        new_velocity = fish.velocity + force
        norm_v = np.linalg.norm(new_velocity)

        # Normalisation de la nouvelle vitesse à une magnitude fixée
        if norm_v > 1e-12:
            new_velocity = config.speed * new_velocity / norm_v

        else:
            new_velocity = fish.velocity.copy()
        new_velocities.append(new_velocity)

    # Mise à jour de la vélocité de chaque poisson
    for fish, v in zip(school.fish, new_velocities):
        fish.velocity = v
    # Mise à jour de la position de chaque poisson
    for fish in school.fish:
        fish.position += fish.velocity * config.dt
        movement.bounce_boundary(fish, school.zone_limit)