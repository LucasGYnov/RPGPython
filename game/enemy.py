import json
import random
from game.character import Character
from game.item import Item  # Classe Item avec gestion des niveaux

class Enemy(Character):
    def __init__(self, name, level=1, enemy_type="Basic", spawn_chance=0.1, available_items=None):
        """
        Initialise un ennemi avec des caractéristiques spécifiques en fonction de son type et niveau.

        :param name: Nom de l'ennemi.
        :param level: Niveau de l'ennemi.
        :param enemy_type: Type de l'ennemi (terrestre, aérien, etc.).
        :param spawn_chance: Chance d'apparition de l'ennemi.
        :param available_items: Liste d'objets possibles à drop par cet ennemi.
        """
        super().__init__(name, level)  # Appel du constructeur de la classe parente (Character)
        self._enemy_type = enemy_type
        self.spawn_chance = spawn_chance
        self.available_items = available_items if available_items else []  # Liste d'objets possibles à drop
        self.set_attributes()  # Définir les caractéristiques de l'ennemi

    def set_attributes(self, base_hp=100):
        """Définit les caractéristiques de l'ennemi en fonction de son niveau et type."""
        base_attack = 10

        # Si c'est un boss, on lui donne plus de HP que les ennemis classiques
        if self._enemy_type == "boss":
            self._hp = base_hp + (self._level - 1) * 50  # Exemple d'augmentation des HP pour un boss
            self._attack = 25 + (self._level - 1) * 2
        elif self._enemy_type == "terrestre":
            self._hp = base_hp + (self._level - 1) * 25
            self._attack = base_attack + (self._level - 1) * 2
        elif self._enemy_type == "aérien":
            self._hp = base_hp + (self._level - 1) * 15
            self._attack = base_attack + (self._level - 1) * 4
        else:  # Type par défaut ou "Basic"
            self._hp = base_hp + (self._level - 1) * 20
            self._attack = base_attack + (self._level - 1) * 2

        self._max_hp = self._hp  # Mise à jour des HP max


    def drop_loot(self):
        """
        Détermine quel loot l'ennemi laisse tomber en fonction des objets disponibles et des chances.
        Retourne un à trois objets (Item) obtenus de manière aléatoire.
        """
        loot = []

        # Ouvre et charge le fichier JSON contenant les objets à loot
        try:
            with open('assets/items_data.json', 'r') as file:
                items_data = json.load(file)
        except FileNotFoundError:
            print("Erreur : Le fichier items_data.json est introuvable.")
            return None
        except json.JSONDecodeError:
            print("Erreur : Le fichier JSON est malformé.")
            return None

        # Sélectionne entre 1 et 3 objets à loot
        number_of_items_to_drop = random.randint(2, 4)

        # Filtrer les objets disponibles selon les chances de drop
        possible_items = []
        for item_data in items_data:
            item = Item(**item_data)  # Crée l'objet Item à partir des données JSON
            item_level = item.level
            chance = self.calculate_drop_chance(item_level)  # Calcule les chances de drop pour l'objet

            # Si l'objet passe le test de probabilité, l'ajouter à la liste possible
            if random.random() < chance:
                possible_items.append(item)

        # Choisir entre 1 et 3 objets au hasard parmi les objets possibles
        if possible_items:
            chosen_items = random.sample(possible_items, min(len(possible_items), number_of_items_to_drop))
            loot.extend(chosen_items)

            # Afficher les objets choisis
            print(f"{self.name} dropped: {[item.name for item in loot]}")
            return loot  # Retourne la liste des objets choisis

        # Si aucun objet n'a été sélectionné, afficher un message
        print(f"{self.name} dropped no loot.")
        return None

    def calculate_drop_chance(self, item_level):
        """
        Calcule les chances de loot en fonction du niveau de l'ennemi et du niveau de l'objet.
        :param item_level: Niveau de l'objet à loot.
        :return: La probabilité que l'objet soit lâché par l'ennemi.
        """
        level_diff = item_level - self._level
        if level_diff == 0:  # Même niveau
            chance = 0.7
        elif level_diff < 0:  # Niveau de l'objet plus bas
            chance = 0.25
        elif level_diff > 0:  # Niveau de l'objet plus élevé
            chance = 0.05
        else:
            chance = 0.1  # Valeur par défaut si aucune condition n'est remplie
        return chance

    # --- Propriétés de l'ennemi ---
    @property
    def level(self):
        """Retourne le niveau de l'ennemi."""
        return self._level

    @property
    def max_hp(self):
        """Retourne les HP max de l'ennemi."""
        return self._max_hp

    @property
    def enemy_type(self):
        """Retourne le type d'ennemi."""
        return self._enemy_type

    # --- Méthodes de gestion de l'état de l'ennemi ---
    def take_damage(self, damage):
        """Réduit les HP de l'ennemi en fonction des dégâts reçus."""
        self._hp -= damage
        if self._hp < 0:
            self._hp = 0  # Empêche les HP négatifs

    def is_alive(self):
        """Vérifie si l'ennemi est encore en vie."""
        return self._hp > 0

    @staticmethod
    def load_enemies(filename, item_pool):
        """
        Charge les ennemis depuis un fichier JSON avec des informations sur le type, niveau, chances d'apparition et loot possible.
        :param filename: Le nom du fichier contenant les données des ennemis.
        :param item_pool: Liste d'objets disponibles pour être droppés par les ennemis.
        :return: Liste des ennemis chargés.
        """
        enemies = []
        try:
            with open(filename, 'r') as file:
                enemies_data = json.load(file)
                for enemy_info in enemies_data:
                    try:
                        name = enemy_info['name']
                        level = enemy_info.get('level', 1)  # Par défaut, niveau 1
                        enemy_type = enemy_info.get('type', "Basic")
                        spawn_chance = enemy_info.get('spawn_chance', 0.1)  # Par défaut, 10% de chance d'apparition
                        loot_table = enemy_info.get('loot_table', [])  # Liste d'objets possibles à loot

                        # Crée l'ennemi avec des objets à loot basés sur le loot pool
                        available_items = [
                            item for item in item_pool if abs(item.level - level) <= 1  # Items avec un niveau +-1 par rapport à l'ennemi
                        ]

                        enemy = Enemy(
                            name=name,
                            level=level,
                            enemy_type=enemy_type,
                            spawn_chance=spawn_chance,
                            available_items=available_items
                        )
                        enemies.append(enemy)
                    except KeyError as e:
                        print(f"Erreur dans les données de l'ennemi : clé manquante {e}")
                    except TypeError:
                        print("Erreur : Format des données de l'ennemi incorrect.")
        except FileNotFoundError:
            print("Erreur : Fichier des données des ennemis introuvable.")
        except json.JSONDecodeError:
            print("Erreur : Le fichier JSON est malformé.")
        
        return enemies

    def __str__(self):
        """Retourne une représentation sous forme de chaîne de l'ennemi."""
        return (f"{self.name} (Type: {self._enemy_type}, Level: {self._level}, "
                f"HP: {self._hp}/{self._max_hp}, Spawn Chance: {self.spawn_chance})")
