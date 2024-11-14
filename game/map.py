import random
import json
from game.enemy import Enemy
from game.item import Item


class GameMap:
    def __init__(self, size=12):
        """Initialisation du jeu avec une carte de taille définie et les différents éléments du jeu."""
        self.size = size
        self.start_location = (0, 0)  # Emplacement de départ du joueur
        self.boss_location = (size - 1, size - 1)  # Emplacement du boss
        self.locations = self.generate_map()  # Génération de la carte
        self.enemy_data = self.load_enemy_data()  # Chargement des données des ennemis
        self.item_data = self.load_item_data()  # Chargement des données des objets
        self.spawn_enemies()  # Spawning des ennemis sur la carte
        self.spawn_items()  # Spawning des objets sur la carte
        self.spawn_boss()  # Spawning du boss
        self.current_position = (0, 0)  # Position initiale du joueur
        
        # Initialize the region descriptions as an instance attribute
        self.region_descriptions = {
                "forest": "You are surrounded by ancient trees. The air smells of moss and damp earth.",
                "mountain": "Rocky cliffs loom overhead. The path is steep and treacherous.",
                "swamp": "The ground squelches beneath your feet. You hear the distant croak of frogs.",
                "plains": "Open fields stretch as far as the eye can see. The wind whispers through the grass."
            }

    def get_player_position(self):
        """Retourne la position actuelle du joueur."""
        return self.current_position

    def set_player_position(self, x, y):
        """Met à jour la position du joueur si elle est valide."""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.current_position = (x, y)
        else:
            print("Position invalide.")

    def spawn_boss(self):
        """Spawne un boss puissant à l'emplacement du boss."""
        boss_data = {
            "name": "Goblin Overlord",
            "level": 10,
            "type": "boss",
            "spawn_chance": 1.0,  # Le boss est toujours présent
            "available_items": []  # Liste d'objets que le boss peut avoir (optionnelle)
        }
        self.locations[self.boss_location]['enemy'] = Enemy(
            name=boss_data["name"],
            level=boss_data["level"],
            enemy_type=boss_data["type"],
            spawn_chance=boss_data["spawn_chance"],
            available_items=boss_data["available_items"]
        )

    def load_item_data(self):
        """Charge les données des objets depuis un fichier JSON."""
        try:
            item_file_path = "assets/items_data.json"
            with open(item_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Erreur : Fichier de données des objets introuvable.")
        except json.JSONDecodeError as e:
            print(f"Erreur : Problème de format JSON dans le fichier des objets. {e}")
        return []

    def spawn_items(self):
        """Spawne un nombre limité d'objets sur la carte avec une densité contrôlée."""
        total_max_items = self.size
        items_placed = 0
        max_items_per_region = round(total_max_items / 4)  # Limite d'objets par région

        # Définition des régions de la carte
        regions = [
            [(x, y) for x in range(0, self.size // 2) for y in range(0, self.size // 2)],
            [(x, y) for x in range(0, self.size // 2) for y in range(self.size // 2, self.size)],
            [(x, y) for x in range(self.size // 2, self.size) for y in range(0, self.size // 2)],
            [(x, y) for x in range(self.size // 2, self.size) for y in range(self.size // 2, self.size)],
        ]

        item_types = self.load_item_data()

        # Assurer que chaque type d'objet apparaît au moins une fois
        for item in item_types:
            if items_placed >= total_max_items:
                break

            region_index = random.choice(range(len(regions)))
            region = regions[region_index]

            while region:
                position = random.choice(region)
                if self.is_valid_spawn_location(position):
                    new_item = Item(
                        name=item['name'],
                        effect=item['effect'],
                        power=item['power'],
                        quantity=item['quantity'],
                        level=item['level']
                    )
                    self.place_item(position[0], position[1], new_item)
                    region.remove(position)  # Retirer la position de la région
                    items_placed += 1
                    break  # Passer à l'objet suivant

        # Compléter les régions avec des objets jusqu'à la limite maximale
        for region in regions:
            region_items = 0
            while region and region_items < max_items_per_region and items_placed < total_max_items:
                position = random.choice(region)
                if self.is_valid_spawn_location(position):
                    chosen_item = random.choice(item_types)
                    item = Item(
                        name=chosen_item["name"],
                        effect=chosen_item["effect"],
                        power=chosen_item["power"],
                        quantity=chosen_item["quantity"],
                        level=chosen_item["level"]
                    )
                    self.place_item(position[0], position[1], item)
                    region.remove(position)
                    region_items += 1
                    items_placed += 1

    def place_item(self, x, y, item):
        """Place un objet sur une case spécifique de la carte."""
        if (x, y) not in self.locations:
            self.locations[(x, y)] = {}
        self.locations[(x, y)]['item'] = item  # Ajoute l'objet à cette case

    def is_item_at(self, position):
        """Vérifie s'il y a un objet à la position donnée."""
        return self.locations.get(position, {}).get("item") is not None

    def get_item(self, position):
        """Retourne l'objet à la position donnée."""
        return self.locations.get(position, {}).get("item")

    def clear_item(self, position):
        """Supprime l'objet de la position donnée après qu'il ait été récupéré."""
        if position in self.locations:
            self.locations[position]["item"] = None

    def load_enemy_data(self):
        """Charge les données des ennemis depuis un fichier JSON."""
        try:
            enemy_file_path = "assets/enemies_data.json"
            with open(enemy_file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Erreur : Fichier de données des ennemis introuvable.")
            return []

    def generate_map(self):
        """Génère la carte avec des descriptions de régions et initialise les cases."""
        map_grid = {}
        region_descriptions = {
            (0, 0): "forest",
            (0, 1): "swamp",
            (1, 0): "plains",
            (1, 1): "mountain"
        }

        for x in range(self.size):
            for y in range(self.size):
                # Déterminer le type de région pour chaque case
                region_type = region_descriptions.get((x // (self.size // 2), y // (self.size // 2)), "unknown")
                if (x, y) == self.start_location:
                    description = "You are at the entrance of a dark forest."
                elif (x, y) == self.boss_location:
                    description = "This is the lair of the final boss!"
                else:
                    description = f"The area is a {region_type}. " + random.choice([
                        "You hear faint noises.",
                        "The path ahead looks challenging.",
                        "It's eerily quiet."
                    ])
                map_grid[(x, y)] = {"description": description, "enemy": None, "item": None}

        return map_grid



    def spawn_enemies(self):
        """Spawne les ennemis sur la carte avec une densité contrôlée et garantit que chaque type d'ennemi apparaît au moins une fois."""
        max_enemies_per_region = round(self.size / 2)  # Nombre maximum d'ennemis par région
        enemies_per_region = {
            (0, 0): 0,  # Comptage des ennemis dans chaque région
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 0
        }

        # Définition des régions de la carte
        regions = [
            [(x, y) for x in range(0, self.size // 2) for y in range(0, self.size // 2)],  # Région 1 (Haut-Gauche)
            [(x, y) for x in range(0, self.size // 2) for y in range(self.size // 2, self.size)],  # Région 2 (Haut-Droite)
            [(x, y) for x in range(self.size // 2, self.size) for y in range(0, self.size // 2)],  # Région 3 (Bas-Gauche)
            [(x, y) for x in range(self.size // 2, self.size) for y in range(self.size // 2, self.size)],  # Région 4 (Bas-Droite)
        ]

        # Liste de tous les types d'ennemis
        enemy_types = [enemy for enemy in self.enemy_data]

        # Assurer que chaque type d'ennemi apparaît au moins une fois dans une position valide
        for enemy in enemy_types:
            region_index = random.choice(range(len(regions)))  # Choix d'une région aléatoire
            region = regions[region_index]
            
            while region:
                position = random.choice(region)  # Choix d'une position aléatoire dans la région
                if self.is_valid_spawn_location(position):  # Vérifier la validité de la position
                    # Création et ajout de l'ennemi à la position
                    self.locations[position]['enemy'] = Enemy(
                        name=enemy['name'],
                        level=enemy['level'],
                        enemy_type=enemy['type']
                    )
                    region.remove(position)  # Retirer la position de la région
                    break  # Passer à l'ennemi suivant

        # Remplir la carte avec des ennemis supplémentaires selon les contraintes
        for region in regions:
            for _ in range(max_enemies_per_region):  # Limite d'ennemis par région
                if not region:
                    continue  # Passer à la région suivante si la région est vide

                position = random.choice(region)  # Choisir une position aléatoire
                if self.is_valid_spawn_location(position):  # Vérifier si la position est valide
                    self.place_enemy(*position)  # Placer l'ennemi
                    region.remove(position)  # Retirer la position de la région

    def place_enemy(self, x, y):
        """Place un ennemi à une position donnée selon la probabilité de spawn de chaque ennemi."""
        # Liste des ennemis qui peuvent apparaître à la position actuelle en fonction de la probabilité de spawn
        possible_enemies = [enemy for enemy in self.enemy_data if random.random() < enemy["spawn_chance"]]
        
        if possible_enemies:  # Si des ennemis peuvent apparaître
            chosen_enemy = random.choice(possible_enemies)  # Choisir un ennemi aléatoirement
            # Création et ajout de l'ennemi à la carte
            enemy = Enemy(
                name=chosen_enemy["name"],
                level=chosen_enemy["level"],
                enemy_type=chosen_enemy["type"]
            )
            self.locations[(x, y)]['enemy'] = enemy  # Ajout de l'ennemi à la position

    def is_valid_spawn_location(self, position):
        """Vérifie si la position est valide pour l'apparition d'un ennemi.
        Les ennemis doivent être au moins à 2 cases de la position de départ du joueur."""
        x, y = position
        # Eviter que l'ennemi n'apparaisse à la position de départ du joueur
        if position == self.start_location:
            return False

        # Vérifier que l'ennemi est à au moins 2 cases du joueur
        player_x, player_y = self.start_location
        if abs(x - player_x) < 2 and abs(y - player_y) < 2:
            return False

        # Vérifier les cases adjacentes pour s'assurer qu'il n'y a pas d'ennemi déjà présent
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_x, neighbor_y = x + dx, y + dy
                if 0 <= neighbor_x < self.size and 0 <= neighbor_y < self.size:
                    if self.locations[(neighbor_x, neighbor_y)]['enemy'] is not None:
                        return False  # Retourne False si un ennemi est déjà présent dans les cases voisines
        return True  # La position est valide

    def is_enemy_at(self, position):
        """Vérifie s'il y a un ennemi à la position spécifiée."""
        return self.locations.get(position, {}).get("enemy") is not None

    def get_enemy(self, position):
        """Retourne l'ennemi présent à la position spécifiée."""
        return self.locations.get(position, {}).get("enemy")

    def clear_enemy(self, position):
        """Supprime l'ennemi de la position spécifiée après qu'il a été vaincu."""
        if position in self.locations:
            self.locations[position]["enemy"] = None  # Suppression de l'ennemi

    def get_location_description(self, position):
        """Retourne la description de la position actuelle et affiche les détails de l'ennemi s'il y en a."""
        description = self.locations.get(position, {}).get("description", "Lieu introuvable.")
        enemy = self.locations[position].get("enemy")
        if enemy:
            description += f" Vous voyez un {enemy.name} ici !"  # Ajout des détails de l'ennemi
        return description

    def get_region(self, position):
        """Retourne le type de la région (forêt, marais, plaine, montagne) en fonction de la position."""
        x, y = position
        if x < self.size // 2 and y < self.size // 2:
            return "forest"
        elif x < self.size // 2 and y >= self.size // 2:
            return "swamp"
        elif x >= self.size // 2 and y < self.size // 2:
            return "plains"
        else:
            return "mountain"
    
    

    def move_player(self, current_position, direction):
        """Déplace le joueur dans une direction donnée et retourne la nouvelle position."""
        x, y = current_position
        directions = {
            'north': (-1, 0),
            'south': (1, 0),
            'west': (0, -1),
            'east': (0, 1)
        }
        dx, dy = directions.get(direction, (0, 0))
        new_position = (x + dx, y + dy)

        if new_position in self.locations:
            self.set_player_position(*new_position)  # Met à jour la position du joueur
            # Affichage de la région d'entrée
            old_region = self.get_region(current_position)
            new_region = self.get_region(new_position)

            if old_region != new_region:
                print(f"You have entered a new region: \033[95m{self.region_descriptions[new_region]}\033[0m")
            return new_position
        else:
            print("You can't go that way.")
            return current_position

    def print_map(self, player_position):
        """Displays the map with the player's position and enemies, using emojis according to their level."""

         # Explanation legend
        print("\nLegend for enemies by level:")
        print("👺 Level 1 |👹 Level 2 | 🧌 Level 3 |🐉 Level 4 | 🦖 Level 5")

        print("\nEnemies are huge, so you can spot them from far away, but the items are tiny!")
        print("To find items, you will need to explore every corner of the map.")

        for x in range(self.size):
            for y in range(self.size):
                if (x, y) == player_position:
                    print("🧑", end=" ")  # Player representation
                elif (x, y) == self.boss_location:
                    print("👑", end=" ")  # Boss representation
                elif self.locations[(x, y)]['enemy'] is not None:
                    enemy = self.locations[(x, y)]['enemy']
                    # Choose emoji based on the enemy's level
                    if enemy.level == 3:
                        print("👺", end=" ")  # Level 3
                    elif enemy.level == 4:
                        print("👹", end=" ")  # Level 4
                    elif enemy.level == 5:
                        print("🧌", end=" ")  # Level 5
                    elif enemy.level == 6:
                        print("🐉", end=" ")  # Level 6
                    elif enemy.level == 7:
                        print("🦖", end=" ")  # Level 7 (for example, a dinosaur for a strong enemy)
                    else:
                        print("❓", end=" ")  # Unknown or undefined enemy level
                else:
                    # Display regions of the map
                    if x < self.size // 2 and y < self.size // 2:
                        print("🟩", end=" ")  # Forest
                    elif x < self.size // 2 and y >= self.size // 2:
                        print("🟧", end=" ")  # Swamp
                    elif x >= self.size // 2 and y < self.size // 2:
                        print("🟪", end=" ")  # Plains
                    else:
                        print("🟦", end=" ")  # Mountains
            print()  # New line after each row of the map
        print()  # New line after each row of the map





