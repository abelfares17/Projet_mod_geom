"""
Partie 5 — Réseau d'influence visuelle sur les règles comportementales d'Aoki.

Lancer :
    python simulations/partie5_visual_network.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import SimConfig
from src.core.simulation import Simulation
from src.visualization.renderer import Renderer3D

"Simulation pour la partie 5, configurant les paramètres et lançant le moteur de simulation avec un rendu 3D."
def main() -> None:
    config = SimConfig(
        n_fish=90,
        dt=0.05,
        n_steps=3500,
        zone_limit=15.0,
        speed=2.0,
        r_repulsion=0.9,
        r_alignment=2.5,
        r_attraction=5.0,
        k_repulsion=0.95,
        k_attraction=0.16,
        k_alignement=0.40,
        vision_angle_deg=60.0,
        render_every=2,
        seed=5,
    )

    sim = Simulation(config, mode="partie5")
    renderer = Renderer3D(config.zone_limit, config.show_velocities, title="Partie 5 — Réseau dinfluence visuelle")

    "Callback pour le rendu à chaque pas de simulation, avec une condition d'arrêt si la fenêtre est fermée."
    def on_step(simulation: Simulation) -> bool:
        if not renderer.is_open():
            return False
        if simulation.step_count % config.render_every == 0:
            renderer.update(simulation.school, simulation.step_count)
        return True

    sim.run(mode="partie5", callback=on_step)
    renderer.close()

"Point d'entrée du script, lançant la fonction principale."
if __name__ == "__main__":
    main()
