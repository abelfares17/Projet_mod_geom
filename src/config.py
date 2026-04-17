from dataclasses import dataclass, field


@dataclass
class SimConfig:
    # --- Simulation générale ---
    n_fish: int = 50
    dt: float = 0.05
    n_steps: int = 1000
    zone_limit: float = 10.0
    seed: int = None

    # --- Partie 1 : Mouvement aléatoire ---
    speed: float = 1.0
    velocity_noise: float = 0.4

    # --- Partie 2 : Effet Trafalgar ---
    contamination_radius: float = 2.5
    propagation_interval: int = 5   # tous les N pas de temps
    trafalgar_velocity_variation: float = 0.5

    # --- Partie 3 : Règles d'Aoki ---
    r_repulsion: float = 1.0
    r_alignment: float = 3.0
    r_attraction: float = 6.0
    k_repulsion: float = 0.5
    k_attraction: float = 0.3

    # --- Partie 4 : Densité (6 voisins topologiques) ---
    n_neighbors: int = 6

    # --- Partie 5 : Réseau d'influence visuel ---
    vision_angle_deg: float = 60.0   # demi-angle du cône = 30°

    # --- Visualisation ---
    render_every: int = 2            # dessiner 1 image sur N pas
    show_velocities: bool = True
