"""Partie 1 — Mouvement aléatoire en 3D.

Lancer :
    python simulations/partie1_mouvement_aleatoire.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import SimConfig
from src.core.simulation import Simulation
from src.visualization.renderer import Renderer3D


def main() -> None:
    config = SimConfig(
        n_fish=60,
        dt=0.05,
        n_steps=2000,
        zone_limit=10.0,
        speed=1.0,
        velocity_noise=0.4,
        render_every=2,
        show_velocities=True,
        seed=42,
    )

    sim = Simulation(config, mode="partie1")
    renderer = Renderer3D(config.zone_limit, config.show_velocities, title="Partie 1 — Mouvement aléatoire")

    def on_step(simulation: Simulation) -> None:
        if simulation.step_count % config.render_every == 0:
            renderer.update(simulation.school, simulation.step_count)

    sim.run(callback=on_step)
    renderer.close()


if __name__ == "__main__":
    main()
