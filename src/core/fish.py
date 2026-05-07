import numpy as np

"Particule représentant un poisson dans le banc."
class Fish:
    
    "Initialisation d'un poisson avec :"
    "-> une position,"
    "-> une vitesse,"
    "-> des attributs visuels,"
    "-> des attributs supplémentaires (suivant les parties du projet)."
    def __init__(self, position: np.ndarray, velocity: np.ndarray):

        # Propriétés physiques de base
        self.position = position.astype(float)
        self.velocity = velocity.astype(float)

        # Attributs visuels
        self.color: str = "blue"
        
        # Attributs Partie 2 – Trafalgar
        self.is_leader: bool = False
        self.is_contaminated: bool = False
        self.velocity_variation: np.ndarray = np.zeros(3)
