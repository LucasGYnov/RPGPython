import random
from game.character import Character
from game.inventory import Inventory
from game.item import Item

class Player(Character):
    def __init__(self, name, level=1):
        """
        Initialise le joueur avec un inventaire et des boosts temporaires.
        
        :param name: Nom du joueur.
        :param level: Niveau initial du joueur.
        """
        super().__init__(name, level)
        self.inventory = Inventory()
        self.add_starter_items()  # Ajoute des objets de départ à l'inventaire
        self._temporary_attack_boost = 0  # Augmentation temporaire d'attaque
        self._damage_reduction = 0  # Réduction des dégâts (bouclier)
        self.attack_boost_active = False  # Statut du boost d'attaque
        self.has_boosted_attack = False  # Vérifie si un boost d'attaque a déjà été appliqué
        self.has_used_attack_boost = False  # Empêche l'utilisation répétée du boost d'attaque dans un même tour

    def add_starter_items(self):
        """
        Ajoute les objets de départ uniquement si l'inventaire est vide.
        """
        if not self.inventory.items:  # Vérifie si l'inventaire est vide
            starter_items = [
                Item(name="Noob's Dagger", effect="damage", power=10, quantity=1, level=1),
                Item(name="Minor Health Potion", effect="health_boost", power=20, quantity=1, level=1),
                Item(name="Wooden Shield", effect="boost_shield", power=15, quantity=1, level=1)
            ]
            for item in starter_items:
                self.inventory.add_item(item)

    def pick_up_item(self, x, y, game_map):
        """Ramasser un objet à la position (x, y) sur la carte."""
        if game_map.is_item_at((x, y)):  # Vérifier si un objet est présent à cette position
            item = game_map.get_item((x, y))  # Obtenir l'objet à cette position
            self.inventory.add_item(item)  # Ajouter l'objet à l'inventaire
            game_map.clear_item((x, y))  # Retirer l'objet de la carte
            print(f"\nYou have picked up \033[92m{item.name}\033[0m.")

    # --- Méthodes de combat ---
    def attack_enemy(self, enemy, power=None):
        """
        Attaque un ennemi. Utilise une puissance spécifique ou l'attaque standard.
        
        :param enemy: Cible de l'attaque.
        :param power: Puissance d'attaque personnalisée (si fournie).
        """
        damage = power if power else self.calculate_attack_power()

        # Applique des boosts d'objets de l'inventaire
        for item in self.inventory.items:
            if item.effect == "boost_attack" and item.quantity > 0 and not self.has_used_attack_boost:
                damage *= (1 + item.power / 100)
                print(f"{item.name} boost applied: +{item.power}% damage.")
                item.quantity -= 1  # Décrémente la quantité de l'objet utilisé
                self.has_used_attack_boost = True  # Empêche l'utilisation répétée dans le même tour
                break  # Un seul boost d'objet par attaque

        # Inflige les dégâts à l'ennemi
        print(f"{self.name} attacks {enemy.name} for {damage:.2f} damage!")
        enemy.take_damage(damage)

        # Réinitialise le boost temporaire après l'attaque
        self.reset_attack_boost()

    def calculate_attack_power(self):
        """
        Calcule la puissance d'attaque avec un facteur aléatoire.
        
        :return: Puissance d'attaque calculée.
        """
        return (self.attack + self._temporary_attack_boost) * random.uniform(0.9, 1.1)

    def apply_temporary_attack_boost(self, boost_percentage):
        """Applique un boost temporaire à l'attaque du joueur."""
        if not self.has_boosted_attack:
            self._temporary_attack_boost += boost_percentage
            self.has_boosted_attack = True  # Le boost a été appliqué une seule fois
            print(f"{self.name}'s attack is boosted by {boost_percentage}%!")

    def reset_attack_boost(self):
        """Réinitialise le boost temporaire d'attaque après utilisation."""
        if self._temporary_attack_boost > 0:
            print(f"Temporary attack boost of {self._temporary_attack_boost} is reset.")
        self._temporary_attack_boost = 0
        self.has_boosted_attack = False  # Réinitialise également l'indicateur

    # --- Utilisation d'un objet d'inventaire ---
    def use_item_from_inventory(self, item_name, enemy=None):
        """
        Utilise un objet spécifique de l'inventaire.
        
        :param item_name: Nom de l'objet à utiliser.
        :param enemy: Ennemi contre lequel l'objet est utilisé (si applicable).
        """
        item = self.inventory.get_item_by_name(item_name)
        if item:
            # Boost d'attaque (uniquement si le boost n'a pas été utilisé pendant ce tour)
            if item.effect == "boost_attack" and not self.has_used_attack_boost:
                self.apply_temporary_attack_boost(item.power)
                print(f"Temporary attack boost of {item.power}% applied!")
            
            # Application de l'effet du bouclier
            elif item.effect == "boost_shield":
                self.activate_shield(item.power)
            
            # Application des soins
            elif item.effect == "heal":
                self.heal(item.power)
            
            # Application des dégâts d'un objet (type "damage")
            elif item.effect == "damage":
                damage = item.power
                
                # Si un boost d'attaque est actif, appliquez-le aux dégâts de l'objet
                if self.attack_boost_active:
                    damage *= (1 + self._temporary_attack_boost / 100)
                    print(f"Boosted damage with {item.name}: {damage:.2f}")
                
                # Appliquer les dégâts à l'ennemi
                if enemy:
                    enemy.take_damage(damage)
                    print(f"{self.name} uses {item.name} and deals {damage:.2f} damage!")
            
            # Après utilisation, consomme l'objet et met à jour l'inventaire
            self.inventory.consume_item(item_name)


    def activate_shield(self, power):
        """Active un bouclier de protection pour réduire les dégâts d'une seule attaque."""
        self._damage_reduction = power
        self.shield_active = True  # Indique que le bouclier est actif
        print(f"{self.name}'s shield is active, reducing damage by {power}% for the next attack.")


    def heal(self, amount):
        """Soigne le joueur de l'amount spécifié de points de vie."""
        self.hp = min(self.hp + amount, self.max_hp)  # Ne pas dépasser le maximum de points de vie
        print(f"{self.name} heals for {amount} points. Current HP: {self.hp}/{self.max_hp}")

    # --- Réinitialisation de l'état de boost après chaque tour ---
    def end_turn(self):
        """Réinitialise l'état du joueur à la fin de chaque tour."""
        self.has_used_attack_boost = False  # Permet la réutilisation d'une potion après le tour
        self._damage_reduction = 0  # Réinitialise la réduction des dégâts (bouclier)

    def restore_health_on_victory(self):
        """
        Restaure la santé du joueur après une victoire.
        """
        heal_amount = 25  # Points de vie à restaurer (ajustable)
        self.hp = min(self.hp + heal_amount, self.max_hp)  # Ne pas dépasser les points de vie maximum
        print(f"{self.name} restores {heal_amount} health on victory. Current HP: {self.hp}/{self.max_hp}")
