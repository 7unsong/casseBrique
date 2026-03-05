# Casse Brique

**Auteurs :** DURAND Guillian & SONG Yun  
**Dépôt Git :** [https://github.com/7unsong/casseBrique.git](https://github.com/7unsong/casseBrique.git)  
**Langage :** Python  

---

## Règles du jeu

Le jeu **Casse-Brique** reprend les principes classiques du genre :

- Le joueur contrôle une raquette (paddle) horizontale en bas de l’écran.  
- Une balle rebondit sur les murs, la raquette et les briques.  
- Chaque brique détruite rapporte des points.  
- Le joueur dispose d’un nombre limité de vies.  
- La partie est **gagnée** lorsque toutes les briques sont détruites.  
- La partie est **perdue** lorsque toutes les vies sont épuisées.

---

## Bonus

Certaines briques spéciales (en texture diamant) contiennent un **bonus** :
- Lorsqu’elles sont détruites, le bonus est ajouté à une file d’attente.
- Le bonus agrandit temporairement la raquette de **50 pixels** pendant **15 secondes**.
- Les bonus ne se cumulent pas : un seul agrandissement peut être actif à la fois.

---

## Spécificités de l’implémentation

Ce projet respecte la contrainte du TP demandant l’utilisation d’une **liste**, d’une **pile** et d’une **file** :

| Structure de données | Classe / Emplacement | Rôle dans le jeu |
|-----------------------|----------------------|------------------|
| **Liste** | `Bricks` (dans `MyWindow`) | Contient toutes les briques encore présentes à l’écran. Chaque brique supprimée est retirée de la liste. |
| **Pile (Stack)** | `LifeStack` | Gère les vies du joueur. Chaque vie perdue correspond à un `pop()`, et chaque vie gagnée à un `push()`. |
| **File (Queue)** | `BonusQueue` | Gère les bonus en attente. Chaque bonus obtenu est ajouté avec `enqueue()` et appliqué dans l’ordre d’obtention. |

Autres caractéristiques :
- Gestion visuelle des vies via des cœurs affichés en haut à gauche.
- Score affiché en temps réel.
- Écran de **victoire** ("YOU WIN!") quand toutes les briques sont détruites.
- Écran de **défaite** ("GAME OVER") quand toutes les vies sont perdues.
- Bouton **Restart** permettant de recommencer une partie immédiatement.

---

## Commandes

| Action | Touche |
|--------|--------|
| Démarrer / relancer la balle | `Espace` |
| Déplacer la raquette à gauche | `←` (Flèche gauche) |
| Déplacer la raquette à droite | `→` (Flèche droite) |
| Quitter le jeu | Bouton “Quitter” |

---

## Architecture générale du code

- `MyWindow` : fenêtre principale, gère l’interface graphique, le score, les vies et la détection de victoire/défaite.  
- `Ball` : gère les déplacements, rebonds et collisions avec les briques et la raquette.  
- `Brick` : représente une brique du jeu (normale ou bonus).  
- `Paddle` : gère la raquette, ses déplacements et sa largeur (modifiée par les bonus).  
- `LifeStack` : implémentation de la pile pour les vies.  
- `BonusQueue` : implémentation de la file pour les bonus.  

---

## Objectif pédagogique

Ce projet met en pratique la programmation orientée objet et l’intégration de **structures de données abstraites** (liste, pile, file) dans une application graphique interactive.  
Il illustre également la gestion des événements et des collisions dans un jeu en temps réel.

---

© 2025 — Projet Casse-Brique développé par **DURAND Guillian & SONG Yun**
