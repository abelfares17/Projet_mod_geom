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

def _bounce_boundary(fish: Fish, zone_limit: float) -> None:
    for i in range(3):
        if fish.position[i] < -zone_limit or fish.position[i] > zone_limit:
            fish.velocity[i] *= -1
            fish.position[i] = np.clip(fish.position[i], -zone_limit, zone_limit)


def step(school: School, config: SimConfig, step_count: int) -> None:
    #Propagation du comportement Trafalgar
    if(step_count % config.propagation_interval == 0):
      for fish in school.fish:
        if fish.is_contaminated:
          non_contaminated = [f for f in school.fish if not f.is_contaminated]
          distances = np.array([np.linalg.norm(fish.position - f.position) for f in non_contaminated])