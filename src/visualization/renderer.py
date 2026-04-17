"""Rendu 3D temps-réel avec Matplotlib (cross-platform, pas de dépendance OpenGL)."""

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — import requis pour projection='3d'
import numpy as np

from ..core.school import School


class Renderer3D:
    def __init__(self, zone_limit: float, show_velocities: bool = True, title: str = "Banc de poissons"):
        self.zone_limit = zone_limit
        self.show_velocities = show_velocities
        self.title = title

        self.fig = plt.figure(figsize=(8, 7))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self._setup_axes()

        self._scatter = None
        self._quiver = None

        plt.ion()
        plt.show()

    def _setup_axes(self) -> None:
        lim = self.zone_limit
        self.ax.set_xlim(-lim, lim)
        self.ax.set_ylim(-lim, lim)
        self.ax.set_zlim(-lim, lim)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

    def update(self, school: School, step: int) -> None:
        pos = school.positions   # (N, 3)
        vel = school.velocities  # (N, 3)

        if self._scatter is not None:
            self._scatter.remove()
        if self._quiver is not None:
            self._quiver.remove()
            self._quiver = None

        self._scatter = self.ax.scatter(
            pos[:, 0], pos[:, 1], pos[:, 2],
            c=school.colors, s=15, alpha=0.85, depthshade=True,
        )

        if self.show_velocities:
            scale = self.zone_limit * 0.08
            self._quiver = self.ax.quiver(
                pos[:, 0], pos[:, 1], pos[:, 2],
                vel[:, 0], vel[:, 1], vel[:, 2],
                length=scale, normalize=True, alpha=0.35, color="gray",
            )

        self.ax.set_title(f"{self.title} — étape {step}")
        self.fig.canvas.draw_idle()
        plt.pause(0.001)

    def close(self) -> None:
        plt.ioff()
        plt.show()
