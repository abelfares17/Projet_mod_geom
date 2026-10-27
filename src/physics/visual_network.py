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
    pos = school.positions
    vel = school.velocities

    # Vecteurs et distances inter-poissons vectorisés (N, N, 3) et (N, N)
    d_vec = pos[None, :, :] - pos[:, None, :]
    d = np.linalg.norm(d_vec, axis=-1)
    directions = np.divide(d_vec, d[..., None], out=np.zeros_like(d_vec), where=d[..., None] > 1e-12)

    # Cône de vision
    speeds = np.linalg.norm(vel, axis=-1)
    vel_dir = np.divide(vel, speeds[:, None], out=np.zeros_like(vel), where=speeds[:, None] > 1e-12)
    cos_angle = np.einsum("ijk,ik->ij", directions, vel_dir)
    cos_half_angle = np.cos(np.radians(config.vision_angle_deg / 2))

    visible = (d >= 1e-12) & ((speeds[:, None] < 1e-12) | (cos_angle >= cos_half_angle))
    np.fill_diagonal(visible, False)

    # Zones d'Aoki restreintes aux voisins visibles
    mask_rep = visible & (d < config.r_repulsion)
    mask_align = visible & (d >= config.r_repulsion) & (d < config.r_alignment)
    mask_attr = visible & (d >= config.r_alignment) & (d < config.r_attraction)

    repulsion = -np.sum(np.where(mask_rep[..., None], directions, 0.0), axis=1)
    attraction = np.sum(np.where(mask_attr[..., None], directions, 0.0), axis=1)

    align_count = np.sum(mask_align, axis=1, keepdims=True)
    align_sum = mask_align.astype(float) @ vel
    avg_vel = np.divide(align_sum, align_count, out=np.zeros_like(vel), where=align_count > 0)
    align_force = np.where(align_count > 0, config.k_alignement * (avg_vel - vel), 0.0)

    forces = config.k_repulsion * repulsion + align_force + config.k_attraction * attraction

    # Nouvelle vélocité normalisée à une magnitude fixée
    new_velocities = vel + forces
    norms = np.linalg.norm(new_velocities, axis=-1, keepdims=True)
    new_velocities = np.where(norms > 1e-12, config.speed * new_velocities / np.maximum(norms, 1e-12), vel)

    # Mise à jour de la vélocité et de la position de chaque poisson
    for fish, v in zip(school.fish, new_velocities):
        fish.velocity = v
        fish.position += fish.velocity * config.dt
        movement.bounce_boundary(fish, school.zone_limit)