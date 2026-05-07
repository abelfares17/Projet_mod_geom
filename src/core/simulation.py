from typing import Callable, Optional

from ..config import SimConfig
from .school import School
from ..physics import movement, trafalgar, trafalgar_2, aoki, density, visual_network

"Dictionnaire des différents modes de simulation, associant chaque mode à sa fonction de mise à jour physique correspondante."
_PHYSICS = {
    "partie1": movement.step,
    "partie2": trafalgar.step,
    "partie2_bis": trafalgar_2.step,
    "partie3": aoki.step,
    "partie4": density.step,
    "partie5": visual_network.step,
}

"Moteur de simulation — orchestre physique et rendu."
class Simulation:
    
    "Initialisation de la simulation avec une configuration donnée et un mode de physique choisi."
    def __init__(self, config: SimConfig, mode: str = "partie1"):
        # Validation du mode de simulation
        if mode not in _PHYSICS:
            raise ValueError(f"Mode inconnu : {mode!r}. Choisir parmi {list(_PHYSICS)}")
        
        self.config = config
        self.mode = mode
        self.school = School(config.n_fish, config.zone_limit, config.speed, config.seed)
        self.step_count = 0
        self._physics_step = _PHYSICS[mode]

    "Exécute un pas de simulation en appliquant la fonction de mise à jour physique du mode actuel."
    def step(self) -> None:
        self._physics_step(self.school, self.config, self.step_count)
        self.step_count += 1

    "Lance la simulation dans le mode spécifié, avec une option de callback pour le rendu ou l'arrêt conditionnel."
    def run(self, mode, callback: Optional[Callable[["Simulation"], Optional[bool]]] = None) -> None:
        # Changement de mode de simulation si nécessaire
        if mode != self.mode:
            if mode not in _PHYSICS:
                raise ValueError(f"Mode inconnu : {mode!r}. Choisir parmi {list(_PHYSICS)}")
            self.mode = mode
            self._physics_step = _PHYSICS[mode]

        # Initialisation spécifique à certaines parties
        if mode == "partie2":
            trafalgar.select_leader(self.school)

        if mode == "partie2_bis":
            trafalgar_2.initialize_school(self.school, self.config)
            trafalgar_2.select_leader(self.school)

        # Boucle de simulation
        for _ in range(self.config.n_steps):
            self.step()
            if callback is not None:
                if callback(self) is False:
                    break
