"""
Partie 4 — Influence de la densité (6 voisins topologiques).

Même règles qu'Aoki, mais les forces ne s'appliquent qu'aux 6 voisins les
plus proches (distance topologique, indépendante de la densité globale).
Recherche efficace via scipy.spatial.KDTree.
"""

from ..config import SimConfig
from ..core.school import School
from scipy.spatial import cKDTree
import numpy as np
from . import movement
from .aoki import compute_forces


def step(school: School, config: SimConfig, step_count: int = 0) -> None:
    # Créer le KDTree pour trouver les voisins les plus proches
    positions = school.positions
    velocities = school.velocities
    n_fish = len(positions)
    k = min(7, n_fish)
    if k <= 1:
        return

    tree = cKDTree(positions)
    _, indices = tree.query(positions, k=k)
    nbr_idx = indices[:, 1:]  # (N, k-1), exclut le poisson lui-même

    nbr_pos = positions[nbr_idx]
    nbr_vel = velocities[nbr_idx]
    d_vec = nbr_pos - positions[:, None, :]
    d = np.linalg.norm(d_vec, axis=-1)
    directions = np.divide(d_vec, d[..., None], out=np.zeros_like(d_vec), where=d[..., None] > 0)

    mask_rep = d < config.r_repulsion
    mask_align = (d >= config.r_repulsion) & (d < config.r_alignment)
    mask_attr = (d >= config.r_alignment) & (d < config.r_attraction)

    repulsion = -np.sum(np.where(mask_rep[..., None], directions, 0.0), axis=1)
    attraction = np.sum(np.where(mask_attr[..., None], directions, 0.0), axis=1)

    align_count = np.sum(mask_align, axis=1, keepdims=True)
    align_sum = np.sum(np.where(mask_align[..., None], nbr_vel, 0.0), axis=1)
    avg_vel = np.divide(align_sum, align_count, out=np.zeros_like(velocities), where=align_count > 0)
    align_force = np.where(align_count > 0, config.k_alignement * (avg_vel - velocities), 0.0)

    forces = config.k_repulsion * repulsion + align_force + config.k_attraction * attraction

    # Nouvelle vélocité normalisée à une magnitude fixée
    new_velocities = velocities + forces
    norms = np.linalg.norm(new_velocities, axis=-1, keepdims=True)
    new_velocities = np.where(norms > 1e-12, config.speed * new_velocities / np.maximum(norms, 1e-12), velocities)

    # Mise à jour de la vélocité et de la position de chaque poisson
    for fish, v in zip(school.fish, new_velocities):
        fish.velocity = v
        fish.position += fish.velocity * config.dt
        movement.bounce_boundary(fish, school.zone_limit)

