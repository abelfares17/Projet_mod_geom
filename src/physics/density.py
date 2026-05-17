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
    positions = np.array([fish.position for fish in school.fish])
    tree = cKDTree(positions)

    new_velocities = []

    for i, fish in enumerate(school.fish):
        # Remplissage du KDTree pour trouver les 6 voisins les plus proches
        distances, indices = tree.query(positions[i], k=min(7, len(school.fish)))

        neighbors = []

        for d, j in zip(distances[1:], indices[1:]):
            other = school.fish[j]
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

