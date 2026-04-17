import numpy as np


class Fish:
    """Particule représentant un poisson dans le banc."""

    def __init__(self, position: np.ndarray, velocity: np.ndarray):
        self.position = position.astype(float)
        self.velocity = velocity.astype(float)
        # Attributs visuels
        self.color: str = "blue"
        # Attributs Partie 2 – Trafalgar
        self.is_leader: bool = False
        self.is_contaminated: bool = False
        self.velocity_variation: np.ndarray = np.zeros(3)
