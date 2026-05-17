"""
Partie 3 — Règles comportementales d'Aoki (1982).

Trois zones concentriques autour de chaque poisson :
  - Répulsion  (d < R_repulsion)  : F = -k_rep * d̂
  - Alignement (R_rep ≤ d < R_align) : F = moyenne des vitesses des voisins
  - Attraction (R_align ≤ d < R_attr) : F = +k_attr * d̂

La nouvelle vitesse est la somme des forces, normalisée à la magnitude V.
"""

import numpy as np
from ..config import SimConfig
from ..core.school import School
from . import movement


def compute_forces(fish, neighbors, config) -> None:
    force = np.zeros(3)
    repulsion = np.zeros(3)
    alignment = np.zeros(3)
    attraction = np.zeros(3)
    alignment_count = 0

    for other in neighbors:
        if other is fish:
            continue
        d_vec = other.position - fish.position
        d = np.linalg.norm(d_vec)
        direction = (d_vec / d) if d > 0 else 0
        if d < config.r_repulsion:
            repulsion -= direction
        elif d < config.r_alignment:
            alignment += other.velocity
            alignment_count += 1
        elif d < config.r_attraction:
            attraction += direction
    
    # Somme pondérée des forces
    force += config.k_repulsion * repulsion
    if alignment_count > 0:
        avg_velocity = alignment / alignment_count
        force += config.k_alignement * (avg_velocity - fish.velocity)
    force += config.k_attraction * attraction

    return force


def step(school: School, config: SimConfig, step_count: int = 0) -> None:
    for fish in school.fish:
        neighbors = school.get_neighbors(fish, config.r_attraction)
        if not neighbors:
            continue

        force = compute_forces(fish, neighbors, config)

        # Mise à jour de la vitesse avec la force totale, normalisée à la magnitude V
        new_velocity = fish.velocity + force
        norm = np.linalg.norm(new_velocity)
        fish.velocity = (new_velocity / norm) * config.speed if norm > 0 else fish.velocity

    # Mise à jour de la position de chaque poisson selon sa vitesse, avec rebond aux frontières
    for fish in school.fish:
        fish.position += fish.velocity * config.dt
        movement.bounce_boundary(fish, school.zone_limit)
