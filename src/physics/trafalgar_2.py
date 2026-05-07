"""
Partie 2 bis — Effet Trafalgar plus visible (propagation des directions).

Logique :
    1) Sélection aléatoire d'un leader à l'initialisation.
    2) Tous les 'propagation_interval' pas :
    -> On récupère tous les poissons contaminés.
    -> Chaque poisson non contaminé proche d'un contaminé devient contaminé.
    -> Le poisson contaminé adopte le comportement du contaminant.
    3) Les mouvements des poissons sont prévsibles et linéaires, sans perturbation aléatoire, pour mieux visualiser la propagation du comportement.
    4) Le leader change de direction de manière aléatoire tous les 'random_movement_step' pas pour initier de nouvelles propagations.
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

"Initialisation de la vitesse des poissons de façon uniforme"
def initialize_school(school: School, config: SimConfig) -> None:
    init_vel = np.random.randn(3) * config.velocity_noise
    normalized_init_vel = (init_vel / np.linalg.norm(init_vel)) * config.speed if np.linalg.norm(init_vel) > 0 else init_vel
    for fish in school.fish:
        fish.velocity = normalized_init_vel.copy()
        


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
                        diff = (1 - config.trafalgar_velocity_variation) * fish.velocity - other.velocity * config.trafalgar_velocity_variation
                        diff = diff / np.linalg.norm(diff)
                        fish.velocity = (diff.copy() / np.linalg.norm(diff)) * config.speed  # Adopte la direction du contaminant
                        break
                    
    # Phase de mouvement
    for fish in school.fish:
        if fish.is_leader and step_count % config.random_movement_step == 0:
          movement.perturb_velocity(fish, config.speed, config.velocity_noise)
        fish.position += fish.velocity * config.dt
        movement.bounce_boundary(fish, config.zone_limit)