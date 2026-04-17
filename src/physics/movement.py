"""Partie 1 — Mouvement aléatoire.

Équation de mise à jour :
    position(t + dt) = position(t) + vitesse(t) * dt

La vitesse est perturbée aléatoirement à chaque pas, puis normalisée pour
conserver une magnitude constante. Les frontières de la zone rebondissent.
"""

import numpy as np

from ..config import SimConfig
from ..core.fish import Fish
from ..core.school import School


def _perturb_velocity(fish: Fish, speed: float, noise: float) -> None:
    new_vel = fish.velocity + np.random.randn(3) * noise
    norm = np.linalg.norm(new_vel)
    fish.velocity = (new_vel / norm) * speed if norm > 0 else fish.velocity


def _bounce_boundary(fish: Fish, zone_limit: float) -> None:
    for i in range(3):
        if fish.position[i] < -zone_limit or fish.position[i] > zone_limit:
            fish.velocity[i] *= -1
            fish.position[i] = np.clip(fish.position[i], -zone_limit, zone_limit)


def step(school: School, config: SimConfig) -> None:
    for fish in school.fish:
        _perturb_velocity(fish, config.speed, config.velocity_noise)
        fish.position += fish.velocity * config.dt
        _bounce_boundary(fish, school.zone_limit)
