import numpy as np
from .fish import Fish

"Collection de poissons évoluant dans une zone cubique."
class School:
    
    "Initialisation de l'école avec :"
    "-> un nombre donné de poissons,"
    "-> une limite de zone,"
    "-> une vitesse initiale,"
    "-> une graine pour la reproductibilité."
    def __init__(self, n_fish: int, zone_limit: float, speed: float, seed: int = None):
        if seed is not None:
            np.random.seed(seed)
        self.zone_limit = zone_limit
        self.fish: list[Fish] = [
            Fish(
                position=np.random.uniform(-zone_limit, zone_limit, 3),
                velocity=self._random_unit_vector() * speed,
            )
            for _ in range(n_fish)
        ]

    "Accesseurs vectorisés (utiles pour les calculs NumPy en physique)."
    @property
    def positions(self) -> np.ndarray:
        return np.array([f.position for f in self.fish]) # (N, 3)

    @property
    def velocities(self) -> np.ndarray:
        return np.array([f.velocity for f in self.fish]) # (N, 3)

    @property
    def colors(self) -> list[str]:
        return [f.color for f in self.fish]

    def __len__(self) -> int:
        return len(self.fish)

    "Génère un vecteur aléatoire unitaire pour l'initialisation de la vitesse des poissons."
    @staticmethod
    def _random_unit_vector() -> np.ndarray:
        v = np.random.randn(3)
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else np.array([1.0, 0.0, 0.0])
