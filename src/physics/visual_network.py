"""Partie 5 — Réseau d'influence visuel.

Chaque poisson ne perçoit que les poissons dans son cône de vision (angle
de demi-ouverture θ = vision_angle_deg / 2 autour de sa direction).

    visible = { p_j | angle(d⃗, v⃗_i) < θ }

Les forces d'Aoki sont ensuite appliquées uniquement aux voisins visibles.

TODO : implémenter cette partie.
"""

from ..config import SimConfig
from ..core.school import School


def step(school: School, config: SimConfig) -> None:
    raise NotImplementedError("Partie 5 (Réseau visuel) pas encore implémentée.")
