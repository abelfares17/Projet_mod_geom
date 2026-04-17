"""Partie 4 — Influence de la densité (6 voisins topologiques).

Même règles qu'Aoki, mais les forces ne s'appliquent qu'aux 6 voisins les
plus proches (distance topologique, indépendante de la densité globale).
Recherche efficace via scipy.spatial.KDTree.

    v_nouvelle = v_i + F_repulsion + F_alignement + F_attraction
    v_nouvelle = V * v_nouvelle / ||v_nouvelle||

TODO : implémenter cette partie.
"""

from ..config import SimConfig
from ..core.school import School


def step(school: School, config: SimConfig) -> None:
    raise NotImplementedError("Partie 4 (Densité / KDTree) pas encore implémentée.")
