"""Partie 2 — Effet Trafalgar (propagation des mouvements).

Algorithme :
  1. Sélection aléatoire d'un leader (une seule fois au démarrage).
  2. Calcul des distances euclidiennes entre poissons.
  3. Tous les `propagation_interval` pas : si un poisson est à moins de
     `contamination_radius` d'un poisson contaminé, il adopte une variation
     de vitesse similaire et devient contaminé (couleur verte).
  4. Mise à jour des positions avec rebond aux frontières.

TODO : implémenter cette partie.
"""

import numpy as np

from ..config import SimConfig
from ..core.school import School
from . import movement


def _select_leader(school: School) -> None:
    leader = np.random.choice(school.fish)
    leader.is_leader = True
    leader.is_contaminated = True
    leader.color = "red"


def step(school: School, config: SimConfig) -> None:
    raise NotImplementedError("Partie 2 (Trafalgar) pas encore implémentée.")
