class Character:
    def __init__(self, name, level=1):
        """
        Initialise un personnage avec des attributs de base.
        
        :param name: Nom du personnage.
        :param level: Niveau initial du personnage (par défaut 1).
        """
        self.name = name
        self._level = level
        self._max_hp = 100 + (level - 1) * 20  # Les HP max augmentent avec le niveau
        self._hp = self._max_hp
        self._attack = 10 + (level - 1) * 3  # L'attaque augmente avec le niveau
        self._defense = 5 + (level - 1) * 2  # La défense augmente avec le niveau
        self._experience = 0  # XP initiale
        self.points_to_allocate = 0  # Points d'amélioration pour stats
        self._temporary_attack_boost = 0  # Boost temporaire d'attaque
        self._damage_reduction = 0  # Réduction des dégâts via bouclier

    # --- Propriétés de l'objet ---
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self._max_hp))  # S'assure que HP ne dépasse pas les limites

    @property
    def max_hp(self):
        return self._max_hp

    @property
    def attack(self):
        return self._attack + self._temporary_attack_boost  # Prend en compte le boost temporaire d'attaque

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        """Setter pour la défense. Personnalisation possible selon règles du jeu."""
        self._defense = value

    @property
    def level(self):
        return self._level

    # --- Méthodes de gestion des statistiques ---
    def take_damage(self, amount):
        """Applique des dégâts après réduction par la défense et le bouclier actif."""
        
        # Réduction via bouclier (si actif)
        if self._damage_reduction > 0:
            reduced_damage = amount * (1 - self._damage_reduction / 100)
            print(f"{self.name}'s shield reduces the damage by {self._damage_reduction}%.")
            
            # Bouclier consommé après cette attaque
            self._damage_reduction = 0  
        else:
            reduced_damage = amount

        # Réduction via défense
        reduced_damage -= self.defense  # La défense absorbe directement les dégâts
        
        # Ne pas descendre en-dessous d'un minimum viable de dégâts (1)
        final_damage = max(int(reduced_damage), 1)
        
        # Appliquer les dégâts
        self.hp -= final_damage
        print(f"{self.name} takes {final_damage} damage! Remaining HP: {self.hp}/{self.max_hp}")

        if self.hp <= 0:
            print(f"{self.name} is defeated!")




    def heal(self, amount):
        """Soigne le personnage en ajoutant de la vie."""
        self.hp += amount
        print(f"{self.name} recovers {amount} HP! Current HP: {self.hp}/{self.max_hp}")

    def attack_target(self, target):
        """Inflige des dégâts à une cible."""
        damage = max(self.attack, 1)  # L'attaque ne peut pas être inférieure à 1
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")
        target.take_damage(damage)
        self.reset_attack_boost()  # Réinitialise le boost d'attaque après l'attaque

    # --- Système d'expérience ---
    def gain_experience(self, xp):
        """Ajoute de l'XP et gère les passages de niveau."""
        self._experience += xp
        print(f"{self.name} gained {xp} XP! Current XP: {self._experience}/{self.experience_to_next_level()}")
        
        # Passage au niveau supérieur si suffisamment d'XP
        while self._experience >= self.experience_to_next_level():
            self.level_up()

    def experience_to_next_level(self):
        """Calcule l'XP nécessaire pour passer au niveau suivant."""
        return 100 + (self._level - 1) * 50  # XP nécessaire pour atteindre le niveau suivant

    def level_up(self):
        """Augmente le niveau et distribue des points d'amélioration."""
        self._level += 1
        self.points_to_allocate += 3  # Distribution des points d'amélioration
        self._max_hp += 20  # Augmente les HP max au niveau supérieur
        self._hp = self._max_hp  # Rétablit les HP à leur maximum
        self._attack += 5  # Augmente l'attaque
        self._defense += 2  # Augmente la défense

        print(f"{self.name} leveled up to Level {self._level}!")
        print(f"New stats - Max HP: {self._max_hp}, Attack: {self._attack}, Defense: {self._defense}.")
        print(f"Points available to allocate: {self.points_to_allocate}")

    def allocate_points(self, attack_points=0, defense_points=0, hp_points=0):
        """Alloue des points d'amélioration pour les statistiques."""
        total_points = attack_points + defense_points + hp_points
        if total_points > self.points_to_allocate:
            print("Not enough points to allocate!")
            return

        self._attack += attack_points
        self._defense += defense_points
        self._max_hp += hp_points * 10  # Chaque point de HP augmente de 10
        self.hp = self._max_hp
        self.points_to_allocate -= total_points
        print(f"{self.name}'s stats updated: Attack: {self._attack}, Defense: {self._defense}, Max HP: {self._max_hp}.")

    # --- Gestion des boosts ---
    def apply_temporary_attack_boost(self, boost_amount):
        """Applique un boost temporaire d'attaque."""
        self._temporary_attack_boost += boost_amount
        print(f"{self.name} receives a temporary attack boost of {boost_amount}!")

    def reset_attack_boost(self):
        """Réinitialise le boost temporaire d'attaque."""
        if self._temporary_attack_boost > 0:
            print(f"{self.name}'s attack boost of {self._temporary_attack_boost} is reset.")
        self._temporary_attack_boost = 0

    def activate_shield(self, reduction):
        """Active un bouclier réduisant les dégâts subis."""
        self._damage_reduction = reduction
        print(f"{self.name} activates a shield reducing damage by {reduction}%!")

    def deactivate_shield(self):
        """Désactive le bouclier."""
        if self._damage_reduction > 0:
            print(f"{self.name}'s shield deactivates.")
        self._damage_reduction = 0

    # --- État du personnage ---
    def is_alive(self):
        """Vérifie si le personnage est encore en vie."""
        return self.hp > 0

    def __str__(self):
        """Affiche les statistiques actuelles du personnage sous forme lisible."""
        return (f"{self.name} (Level: {self.level}, HP: {self.hp}/{self.max_hp}, "
                f"Attack: {self.attack}, Defense: {self.defense}, "
                f"XP: {self._experience}/{self.experience_to_next_level()})")
