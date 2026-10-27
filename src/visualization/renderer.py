"""Rendu 3D temps-réel avec Matplotlib."""

import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
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
        self._title_artist = self.ax.set_title(self.title)

        self._fish_collection = None
        self._quiver = None
        self._last_colors = None
        self._bg = None
        self._view_state = None
        self._open = True

        plt.show(block=False)
        self.fig.canvas.mpl_connect("close_event", self._on_close)
        self.fig.canvas.mpl_connect("resize_event", self._on_invalidate_bg)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

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
    ) -> tuple[np.ndarray, list]:
        norms = np.linalg.norm(velocities, axis=1, keepdims=True)
        fwd = np.where(norms > 1e-10, velocities / np.maximum(norms, 1e-10), np.array([1.0, 0.0, 0.0]))

        # Repère local orthonormé (fwd, right, up) vectorisé
        ref = np.where(np.abs(fwd[:, 2:3]) < 0.9, np.array([0.0, 0.0, 1.0]), np.array([1.0, 0.0, 0.0]))
        right = np.cross(fwd, ref)
        right /= np.linalg.norm(right, axis=1, keepdims=True)
        up = np.cross(right, fwd)

        s = size
        # Points du corps
        nose = positions + fwd   * s
        top  = positions + up    * (s * 0.28)
        bot  = positions - up    * (s * 0.28)
        rgt  = positions + right * (s * 0.32)
        lft  = positions - right * (s * 0.32)
        tail = positions - fwd   * (s * 0.7)   # jonction corps-queue

        # Points de la nageoire caudale (fourche)
        cf_top = positions - fwd * (s * 1.4) + up * (s * 0.45)
        cf_mid = positions - fwd * (s * 1.1)           # creux du V
        cf_bot = positions - fwd * (s * 1.4) - up * (s * 0.45)

        tris = np.empty((len(positions), self._TRIS_PER_FISH, 3, 3), dtype=float)
        # Demi-avant (4 faces — nez = apex)
        tris[:, 0] = np.stack([nose, top, rgt], axis=1)
        tris[:, 1] = np.stack([nose, rgt, bot], axis=1)
        tris[:, 2] = np.stack([nose, bot, lft], axis=1)
        tris[:, 3] = np.stack([nose, lft, top], axis=1)
        # Demi-arrière (4 faces — queue = apex)
        tris[:, 4] = np.stack([tail, top, rgt], axis=1)
        tris[:, 5] = np.stack([tail, rgt, bot], axis=1)
        tris[:, 6] = np.stack([tail, bot, lft], axis=1)
        tris[:, 7] = np.stack([tail, lft, top], axis=1)
        # Nageoire caudale (2 faces)
        tris[:, 8] = np.stack([tail, cf_top, cf_mid], axis=1)
        tris[:, 9] = np.stack([tail, cf_mid, cf_bot], axis=1)

        verts = tris.reshape(-1, 3, 3)
        face_colors = [c for color in colors for c in (color,) * self._TRIS_PER_FISH]
        return verts, face_colors

    @staticmethod
    def _make_quiver_segments(positions: np.ndarray, velocities: np.ndarray, length: float, arrow_length_ratio: float = 0.3) -> np.ndarray:
        norms = np.linalg.norm(velocities, axis=1, keepdims=True)
        uvw = np.where(norms > 0, velocities / np.maximum(norms, 1e-12), velocities)
        tip = positions + uvw * length
        shafts = np.stack([tip, positions], axis=1)

        x = uvw[:, 0]
        y = uvw[:, 1]
        xy_norm = np.linalg.norm(uvw[:, :2], axis=1)
        x_p = np.divide(y, xy_norm, where=xy_norm != 0, out=np.zeros_like(x))
        y_p = np.divide(-x, xy_norm, where=xy_norm != 0, out=np.ones_like(x))
        rangle = math.radians(15)
        c = math.cos(rangle)
        s = math.sin(rangle)
        r13 = y_p * s
        r32 = x_p * s
        r12 = x_p * y_p * (1 - c)
        Rpos = np.array([
            [c + (x_p ** 2) * (1 - c), r12, r13],
            [r12, c + (y_p ** 2) * (1 - c), -r32],
            [-r13, r32, np.full_like(x_p, c)],
        ])
        Rneg = Rpos.copy()
        Rneg[[0, 1, 2, 2], [2, 2, 0, 1]] *= -1
        Rpos_vecs = np.einsum("ij...,...j->...i", Rpos, uvw)
        Rneg_vecs = np.einsum("ij...,...j->...i", Rneg, uvw)
        alen = length * arrow_length_ratio
        head1 = np.stack([tip, tip - Rpos_vecs * alen], axis=1)
        head2 = np.stack([tip, tip - Rneg_vecs * alen], axis=1)
        return np.concatenate([shafts, head1, head2], axis=0)

    def _get_view_state(self) -> tuple:
        return (
            self.ax.elev,
            self.ax.azim,
            getattr(self.ax, "roll", 0.0),
            self.fig.bbox.bounds,
        )

    def _on_invalidate_bg(self, event) -> None:
        self._bg = None

    def _capture_background(self) -> None:
        artists = [a for a in (self._fish_collection, self._quiver, self._title_artist) if a is not None]
        for a in artists:
            a.set_visible(False)
        self.fig.canvas.draw()
        self._bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        self._view_state = self._get_view_state()
        for a in artists:
            a.set_visible(True)

    "Mise à jour de la visualisation."
    def update(self, school: School, step: int) -> None:
        if not self._open:
            return

        pos = school.positions   # (N, 3)
        vel = school.velocities  # (N, 3)
        colors = school.colors

        size = self.zone_limit * 0.04
        verts, face_colors = self._make_fish_verts(pos, vel, colors, size)

        if self._fish_collection is None:
            self._fish_collection = Poly3DCollection(
                verts,
                facecolors=face_colors,
                edgecolors="k",
                linewidths=0.2,
                alpha=0.85,
            )
            self.ax.add_collection3d(self._fish_collection)
            self._last_colors = list(colors)
        else:
            self._fish_collection.set_verts(verts)
            if colors != self._last_colors:
                self._fish_collection.set_facecolor(face_colors)
                self._last_colors = list(colors)

        if self.show_velocities:
            scale = self.zone_limit * 0.08
            segments = self._make_quiver_segments(pos, vel, scale)
            if self._quiver is None:
                self._quiver = Line3DCollection(
                    segments,
                    colors="gray",
                    alpha=0.35,
                    linewidths=1.0,
                )
                self.ax.add_collection3d(self._quiver)
            else:
                self._quiver.set_segments(segments)

        self._title_artist.set_text(f"{self.title} — étape {step}")

        # Si l'utilisateur fait tourner la vue 3D à la souris, redessiner normalement
        if getattr(self.ax, "_button_pressed", None) is not None:
            self._bg = None
            self.fig.canvas.draw()
            self.fig.canvas._draw_pending = False
            self.fig.canvas.flush_events()
            return

        if self._bg is None or self._view_state != self._get_view_state():
            self._capture_background()

        self.fig.canvas.restore_region(self._bg)
        z_fish = self._fish_collection.do_3d_projection()
        if self._quiver is not None:
            z_quiv = self._quiver.do_3d_projection()
            if z_quiv < z_fish:
                self.ax.draw_artist(self._quiver)
                self.ax.draw_artist(self._fish_collection)
            else:
                self.ax.draw_artist(self._fish_collection)
                self.ax.draw_artist(self._quiver)
        else:
            self.ax.draw_artist(self._fish_collection)
        self.ax.draw_artist(self._title_artist)
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas._draw_pending = False
        self.fig.canvas.flush_events()

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
