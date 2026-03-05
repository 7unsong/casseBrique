# Casse Brique — Ajouts

**Auteur :** DURAND Guillian  
**Dépôt Git :** [https://github.com/7unsong/casseBrique.git](https://github.com/7unsong/casseBrique.git)  
**Modifié le :** 5 mars 2026  

---

## Modes de jeu

Un sélecteur de mode a été ajouté en bas de l'écran, à côté des boutons Jouer et Quitter. Trois modes sont disponibles :

- **Classique** : le mode d'origine, inchangé.
- **Survie** : la vitesse de la balle augmente progressivement. En cas de perte de vie, la vitesse est réinitialisée et repart de zéro au prochain lancer.
- **Endless** : lorsque toutes les briques sont détruites, une nouvelle vague apparaît immédiatement sans interrompre la balle. Le numéro de vague est affiché brièvement à l'écran. Il n'y a pas d'écran de victoire.

---

## Mode Survie — détails

| Paramètre | Valeur |
|-----------|--------|
| Intervalle d'accélération | 5 secondes |
| Multiplicateur par palier | ×1.08 |
| Vitesse maximale | 35 px/frame |
| Vitesse du paddle | vitesse balle × 1.4 |

- La vitesse courante est affichée en temps réel en haut à droite de l'écran.
- Le paddle accélère proportionnellement à la balle pour rester jouable.
- À chaque perte de vie, la vitesse est remise à 10 px/frame et l'accélération redémarre au prochain lancer.
- La condition de défaite reste la même : toutes les vies épuisées.

---

## Nouveaux bonus

Deux types de briques bonus sont désormais présents dans tous les modes :

| Texture | Bonus | Effet |
|---------|-------|-------|
| Or | Multi-balle | Fait apparaître une balle supplémentaire (orange). |
| Diamant | Agrandissement raquette | Agrandit la raquette de **50 pixels** pendant **15 secondes**. |

### Bonus multi-balle

- Chaque brique or détruite ajoute une balle supplémentaire en jeu.
- Les balles supplémentaires sont **orange** ; la balle principale reste **rouge**.
- Si une balle supplémentaire tombe, elle est détruite silencieusement, **sans perte de vie**.
- Si la balle principale tombe alors qu'il reste des balles supplémentaires, l'une d'elles prend sa place (devient rouge, hérite des vies) — **sans perte de vie**.
- Une vie n'est perdue que lorsque la dernière balle restante tombe.

---

## Briques multi-vie

Certaines briques (texture Nether Bricks) résistent à **2 coups** avant d'être détruites. Elles sont présentes dans tous les modes avec une probabilité de 15 %. Elles valent **200 points** à la destruction (100 × hp_max).

---

## Probabilités des briques

| Type | Probabilité | Points |
|------|-------------|--------|
| Bonus multi-balle (or) | 10 % | 100 |
| Bonus raquette (diamant) | 10 % | 100 |
| Brique solide — 2 PV (nether) | 15 % | 200 |
| Brique normale | 65 % | 100 |

---

© 2026 — Ajouts réalisés par **DURAND Guillian**