"""
Partie 2 — Effet Trafalgar (propagation des comportements).

Logique :
    1) Sélection aléatoire d'un leader à l'initialisation.
    2) Tous les 'propagation_interval' pas :
    -> On récupère tous les poissons contaminés.
    -> Chaque poisson non contaminé proche d'un contaminé devient contaminé.
    -> Le poisson contaminé adopte une partie du comportement du contaminant (variation de vitesse).
    3) Le reste des mouvements de base est similaire à la partie précédente, donc on les réutilise ici.
"""

import numpy as np

from ..config import SimConfig
from src.core.fish import Fish
from ..core.school import School
from . import movement

"Sélection aléatoire d'un leader qui initie la contamination."
def select_leader(school: School) -> None:
    leader = np.random.choice(school.fish)
    leader.is_leader = True
    leader.is_contaminated = True
    leader.color = "red"


"Mise à jour de la position de chaque poisson selon sa vitesse, avec propagation du comportement contaminé."
def step(school: School, config: SimConfig, step_count: int = 0) -> None:
    
    # Phase de contamination (à chaque intervalle définie)
    if step_count % config.propagation_interval == 0:
        for fish in school.fish:
            if not fish.is_contaminated:
                for other in school.fish:

                    # Un poisson non contaminé devient contaminé s'il est proche d'un contaminé : il adopte son comportement
                    if other.is_contaminated and np.linalg.norm(fish.position - other.position) < config.contamination_radius:
                        fish.is_contaminated = True
                        fish.color = "green"
                        fish.velocity += (other.velocity - fish.velocity) * config.trafalgar_velocity_variation
                        break

    # Phase de mouvement
    for fish in school.fish:
        if step_count%config.random_movement_step == 0:
          movement.perturb_velocity(fish, config.speed, config.velocity_noise)
        fish.position += fish.velocity * config.dt
        movement.bounce_boundary(fish, config.zone_limit)