# RPG Game - Aventure & Combat en Python

Bienvenue dans le monde de **RPG Game**, un jeu de rôle textuel développé en Python où tu incarnes un héros dans sa quête pour vaincre des ennemis, améliorer ses compétences et découvrir des trésors cachés ! Explore des cartes générées aléatoirement, affronte des monstres puissants, améliore ton équipement, et deviens le héros légendaire de ce monde fantastique.

## Table des matières

- [Introduction](#introduction)
- [Concept du jeu](#concept-du-jeu)
- [Fonctionnalités](#fonctionnalités)
- [Code et architecture](#code-et-architecture)
- [Installation](#installation)
- [Lancer le jeu](#lancer-le-jeu)

## Introduction

Le jeu RPG Game est une aventure textuelle où le joueur prend le rôle d'un personnage (le héros) et interagit avec différents éléments de l'environnement du jeu, principalement des combats au tour par tour contre des ennemis, la collecte de ressources et l'amélioration des compétences. Le joueur évolue au fur et à mesure qu'il vainc des ennemis et remporte des victoires, gagnant des points d'expérience (XP) qui lui permettent de monter en niveau, améliorer ses statistiques et débloquer de nouvelles compétences.

L'objectif principal est de survivre aux différents combats, résoudre des énigmes et compléter des quêtes tout en progressant dans l'histoire. L'environnement est dynamique, avec des ennemis et des boss à vaincre, ainsi que des éléments de jeu tels que des objets et des trésors cachés.

## Concept du jeu

### Objectifs
- **Survivre aux combats** : En affrontant des ennemis de plus en plus forts, en utilisant des objets et en améliorant tes compétences.
- **Monter en niveau** : Gagner des XP pour améliorer les statistiques du personnage et débloquer de nouvelles capacités.
- **Explorer le monde** : Découvrir des trésors cachés, interagir avec différents personnages et vaincre des boss redoutables.
- **Terminer la quête** : Compléter l'histoire principale en battant les boss finaux et en accomplissant les missions secondaires.

### Mécanismes du jeu
- **Combat au tour par tour** : Le joueur et l'ennemi agissent chacun leur tour, avec des options pour attaquer, utiliser des objets ou fuir le combat.
- **Système de statistiques** : Chaque personnage (joueur et ennemi) a des statistiques qui influencent ses performances en combat (HP, attaque, défense, etc.).
- **Système de loot** : Les ennemis laissent tomber des objets et des équipements qui permettent au joueur d'améliorer ses statistiques et d'accéder à de nouvelles compétences.
- **Système de niveau** : Le joueur monte en niveau en accumulant des XP, ce qui permet d'améliorer ses statistiques et d'acquérir de nouvelles capacités.

## Fonctionnalités

### Fonctionnalités principales
- **Combat dynamique** : Système de combat avec des coups critiques, esquive et gestion de la santé.
- **Exploration** : Le joueur peut se déplacer sur une carte et interagir avec des ennemis ou des objets.
- **Inventaire** : Le joueur peut ramasser des objets et les utiliser durant les combats ou pour améliorer ses capacités.
- **Montée en niveau** : Chaque victoire contre un ennemi permet au joueur de gagner de l'XP et d'améliorer ses statistiques.
- **Gestion des objets** : Système d'utilisation d'objets avec des effets variés, tels que des potions de soins, des objets qui boostent les attaques, etc.
- **Fuite des combats** : Le joueur peut tenter de fuir un combat si la situation devient trop risquée.
- **Boss fights** : Des combats contre des ennemis particulièrement puissants marquent des moments clés du jeu.
- **Interface texte** : Le jeu se joue entièrement dans le terminal avec des affichages textuels pour chaque action du joueur.

### Fonctionnalités supplémentaires
- **Système de sauvegarde** : Le jeu permet de sauvegarder l'état actuel du joueur pour reprendre la partie ultérieurement.

## Code et architecture

Le projet est développé en Python et utilise une structure modulaire pour organiser le code. Voici un aperçu de l'architecture du jeu :

### Fichiers principaux
- **`main.py`** : Point d'entrée du jeu, gère le menu principal et lance la boucle de jeu.
- **`battle.py`** : Contient la logique des combats (attaques, défenses, coups critiques, etc.).
- **`map.py`** : Définit la carte du jeu, la génération des zones, la gestion des ennemis et des boss.
- **`player.py`** : Contient la classe `Player`, qui gère les statistiques et les actions du joueur.
- **`enemy.py`** : Contient la classe `Enemy`, qui gère les ennemis et leurs actions.
- **`inventory.py`** : Gère l'inventaire du joueur, les objets collectés et leur utilisation.
- **`game.py`** : Gère la logique de jeu générale, y compris les déplacements du joueur et les événements aléatoires.
- **`save_load.py`** : Gère la sauvegarde et le chargement des données de jeu.
- **`ascii_art.py`** : Contient des éléments graphiques ASCII pour l'affichage dans le terminal.
- **`ui_manager.py`** : Gère l'interface utilisateur du jeu (affichage des menus, états de santé, etc.).

### Dossier `assets`
Le dossier `assets` contient des fichiers de données et des configurations pour les ennemis et les objets :

- **`enemies_data.json`** : Données des ennemis du jeu.
- **`items_data.json`** : Données des objets et équipements dans le jeu.

### Dossier `game`
Le dossier `game` contient les modules relatifs à la logique du jeu, tels que les classes pour les personnages, ennemis, objets et la gestion des combats.

### Dossier `saves`
Le dossier `saves` contient les sauvegardes du joueur. Les données sont stockées pour permettre de reprendre une partie là où elle a été laissée.

## Installation

### Prérequis
Avant de commencer, assurez-vous d'avoir Python installé sur votre machine. Vous pouvez vérifier cela en tapant :

```bash
python --version
```

### Installer le jeu

1. Clonez le dépôt du projet :

```bash
git clone https://github.com/LucasGYnov/RPGPython.git
cd rpg-game
```


Pour démarrer le jeu, exécutez le fichier principal :

```bash
python main.py
```
