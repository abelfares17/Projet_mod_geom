# Modélisation d'un Banc de Poissons

Projet de modélisation géométrique implémentant un système de particules
simulant le comportement collectif d'un banc de poissons en 3D.

Le modèle est décomposé en cinq parties :

| Partie | Sujet | État |
|--------|-------|------|
| 1 | Mouvement aléatoire | CHECK |
| 2 | Effet Trafalgar (propagation de comportement) | TODO |
| 3 | Règles comportementales d'Aoki (répulsion / alignement / attraction) | TODO |
| 4 | Influence de la densité (6 voisins topologiques via KDTree) | TODO |
| 5 | Réseau d'influence visuel (cône de vision 60°) | TODO |

---

## Installation

Cloner le dépôt puis, depuis la racine du projet :

**macOS / Linux**
```bash
make install
```

---

## Lancer une simulation

**macOS / Linux**
```bash
make run-p1   # Partie 1 — Mouvement aléatoire
make run-p2   # Partie 2 — Effet Trafalgar
make run-p2-bis # Partie 2 bis - Effet Trafalgar plus visible
make run-p3   # Partie 3 - Règles comportementales d'Aoki
make run-p4   # Partie 4 - Influence de la densité sur les règles comportementales d'Aoki
```

---

## Nettoyage

```bash
make clean   # supprime .venv et les __pycache__
```

---

## Structure du projet

```
src/
├── config.py                  # Tous les paramètres en un seul endroit
├── core/
│   ├── fish.py                # Classe Fish (position, vitesse, couleur)
│   ├── school.py              # Classe School (collection de poissons)
│   └── simulation.py          # Moteur de simulation (dispatch physique)
├── physics/
│   ├── movement.py            # Partie 1 : mouvement aléatoire   CHECK
│   ├── trafalgar.py           # Partie 2 : effet Trafalgar       TODO
│   ├── aoki.py                # Partie 3 : règles d'Aoki         TODO
│   ├── density.py             # Partie 4 : densité / KDTree      TODO
│   └── visual_network.py      # Partie 5 : réseau visuel         TODO
└── visualization/
    └── renderer.py            # Rendu 3D Matplotlib (cross-platform)

simulations/
├── partie1_mouvement_aleatoire.py
└── partie2_trafalgar.py
```

---

## Ajouter une nouvelle partie

1. Implémenter `step(school, config)` dans le module `src/physics/` correspondant.
2. Créer le script d'entrée dans `simulations/`.
3. Le dispatcher dans `src/core/simulation.py` reconnaît automatiquement le nouveau mode.

---

## Dépendances

| Package | Usage |
|---------|-------|
| `numpy` | Calculs vectoriels (positions, vitesses, forces) |
| `matplotlib` | Rendu 3D temps-réel (cross-platform, pas d'OpenGL requis) |
| `scipy` | KDTree pour la recherche efficace de voisins (Partie 4+) |
