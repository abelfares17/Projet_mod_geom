"""
Partie 3 — Règles comportementales d'Aoki (1982).

Trois zones concentriques autour de chaque poisson :
  - Répulsion  (d < R_repulsion)  : F = -k_rep * d̂
  - Alignement (R_rep ≤ d < R_align) : F = moyenne des vitesses des voisins
  - Attraction (R_align ≤ d < R_attr) : F = +k_attr * d̂

La nouvelle vitesse est la somme des forces, normalisée à la magnitude V.
"""

from ..config import SimConfig
from ..core.school import School


def step(school: School, config: SimConfig, step_count: int = 0) -> None:
    raise NotImplementedError("Partie 3 (Aoki) pas encore implémentée.")
