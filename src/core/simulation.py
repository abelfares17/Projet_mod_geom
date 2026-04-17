from typing import Callable, Optional

from ..config import SimConfig
from .school import School
from ..physics import movement, trafalgar, aoki, density, visual_network


_PHYSICS = {
    "partie1": movement.step,
    "partie2": trafalgar.step,
    "partie3": aoki.step,
    "partie4": density.step,
    "partie5": visual_network.step,
}


class Simulation:
    """Moteur de simulation — orchestre physique et rendu."""

    def __init__(self, config: SimConfig, mode: str = "partie1"):
        if mode not in _PHYSICS:
            raise ValueError(f"Mode inconnu : {mode!r}. Choisir parmi {list(_PHYSICS)}")
        self.config = config
        self.mode = mode
        self.school = School(config.n_fish, config.zone_limit, config.speed, config.seed)
        self.step_count = 0
        self._physics_step = _PHYSICS[mode]

    def step(self) -> None:
        self._physics_step(self.school, self.config)
        self.step_count += 1

    def run(self, mode, callback: Optional[Callable] = None) -> None:
        if mode == "partie2":
            trafalgar._select_leader(self.school, self.config)
        for _ in range(self.config.n_steps):
            self.step(self.step_count)
            if callback:
                callback(self)
