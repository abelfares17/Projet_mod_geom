"""Rendu 3D temps-réel avec Matplotlib."""

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from ..core.school import School

class Renderer3D:
    
    "Initialisation du Renderer3D."
    def __init__(self, zone_limit: float, show_velocities: bool = True, title: str = "Banc de poissons"):
        self.zone_limit = zone_limit
        self.show_velocities = show_velocities
        self.title = title

        self.fig = plt.figure(figsize=(8, 7))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self._setup_axes()

        self._fish_collection = None
        self._quiver = None
        self._open = True

        plt.ion()
        plt.show()
        self.fig.canvas.mpl_connect("close_event", self._on_close)

    "Mise en place des limites et étiquettes des axes."
    def _setup_axes(self) -> None:
        lim = self.zone_limit
        self.ax.set_xlim(-lim, lim)
        self.ax.set_ylim(-lim, lim)
        self.ax.set_zlim(-lim, lim)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

    _TRIS_PER_FISH = 10

    def _make_fish_verts(
        self,
        positions: np.ndarray,
        velocities: np.ndarray,
        colors: list,
        size: float,
    ) -> tuple[list, list]:
        verts: list = []
        face_colors: list = []

        for pos, vel, color in zip(positions, velocities, colors):
            norm = np.linalg.norm(vel)
            fwd = vel / norm if norm > 1e-10 else np.array([1., 0., 0.])

            # Repère local orthonormé (fwd, right, up)
            ref   = np.array([0., 0., 1.]) if abs(fwd[2]) < 0.9 else np.array([1., 0., 0.])
            right = np.cross(fwd, ref);  right /= np.linalg.norm(right)
            up    = np.cross(right, fwd)

            s = size
            # Points du corps
            nose = pos + fwd   * s
            top  = pos + up    * s * 0.28
            bot  = pos - up    * s * 0.28
            rgt  = pos + right * s * 0.32
            lft  = pos - right * s * 0.32
            tail = pos - fwd   * s * 0.7   # jonction corps-queue

            # Points de la nageoire caudale (fourche)
            cf_top = pos - fwd * s * 1.4 + up * s * 0.45
            cf_mid = pos - fwd * s * 1.1           # creux du V
            cf_bot = pos - fwd * s * 1.4 - up * s * 0.45

            fish_tris = [
                # Demi-avant (4 faces — nez = apex)
                [nose, top, rgt],
                [nose, rgt, bot],
                [nose, bot, lft],
                [nose, lft, top],
                # Demi-arrière (4 faces — queue = apex)
                [tail, top, rgt],
                [tail, rgt, bot],
                [tail, bot, lft],
                [tail, lft, top],
                # Nageoire caudale (2 faces)
                [tail, cf_top, cf_mid],
                [tail, cf_mid, cf_bot],
            ]

            verts.extend([[p.tolist() for p in tri] for tri in fish_tris])
            face_colors.extend([color] * self._TRIS_PER_FISH)

        return verts, face_colors

    "Mise à jour de la visualisation."
    def update(self, school: School, step: int) -> None:
        if not self._open:
            return

        pos = school.positions   # (N, 3)
        vel = school.velocities  # (N, 3)

        if self._fish_collection is not None:
            self._fish_collection.remove()
        if self._quiver is not None:
            self._quiver.remove()
            self._quiver = None

        size = self.zone_limit * 0.04
        verts, face_colors = self._make_fish_verts(pos, vel, school.colors, size)
        self._fish_collection = Poly3DCollection(
            verts,
            facecolors=face_colors,
            edgecolors="k",
            linewidths=0.2,
            alpha=0.85,
        )
        self.ax.add_collection3d(self._fish_collection)

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

    "Gestion de la fermeture de la fenêtre pour arrêter la simulation proprement."
    def _on_close(self, event) -> None:
        self._open = False

    "Indique si la fenêtre de rendu est toujours ouverte."
    def is_open(self) -> bool:
        return self._open

    "Ferme la fenêtre de rendu et libère les ressources associées."
    def close(self) -> None:
        self._open = False
        plt.ioff()
        plt.close(self.fig)
