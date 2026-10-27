"""
Partie 2 bis — Effet Trafalgar (propagation des directions).

Lancer :
    python simulations/partie2_bis.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import SimConfig
from src.core.simulation import Simulation
from src.visualization.renderer import Renderer3D

"Simulation pour la partie 2 bis, configurant les paramètres et lançant le moteur de simulation avec un rendu 3D."
def main() -> None:
    config = SimConfig(
        n_fish=60,
        dt=0.05,
        n_steps=2000,
        zone_limit=10.0,
        speed=1.0,
        velocity_noise=0.08,
        contamination_radius=2.5,
        propagation_interval=5,
        trafalgar_velocity_variation=0.9,
        render_every=2,
        seed=3,
    )

    sim = Simulation(config, mode="partie2_bis")
    renderer = Renderer3D(config.zone_limit, config.show_velocities, title="Partie 2 bis — Effet Trafalgar")

    "Callback pour le rendu à chaque pas de simulation, avec une condition d'arrêt si la fenêtre est fermée."
    def on_step(simulation: Simulation) -> bool:
        if not renderer.is_open():
            return False
        if simulation.step_count % config.render_every == 0:
            renderer.update(simulation.school, simulation.step_count)
        return True

    sim.run(mode="partie2_bis", callback=on_step)
    renderer.close()

"Point d'entrée du script, lançant la fonction principale."
if __name__ == "__main__":
    main()
