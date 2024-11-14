import random

# Définition des constantes globales
CRIT_BASE_CHANCE = 0.1  # Chance de coup critique de base
EVASION_BASE_CHANCE = 0.05  # Chance d'esquive de base
RUN_CHANCE = 0.5  # Chance de réussite de fuite de base

class Battle:
    def __init__(self, player, enemy):
        """Initialise le combat entre un joueur et un ennemi."""
        self.player = player
        self.enemy = enemy
        self.temp_attack_boost = 0  # Boost temporaire de l'attaque du joueur
        self.boost_active = False   # État du boost d'attaque du joueur
        self.run_attempts = 0  # Compteur pour suivre les tentatives de fuite

    # --- Début du combat ---
    def start_battle(self):
        """Démarre le combat jusqu'à ce que le joueur ou l'ennemi soit vaincu."""
        while self.player.is_alive() and self.enemy.is_alive():
            self.show_health_status()  # Affiche l'état de santé
            print()  # Ligne vide pour la clarté
            valid_action = False  # Indique si une action valide a été effectuée

            while not valid_action:
                action = input("Choose your action (attack/use/run): ").strip().lower()

                if action == "attack":
                    self.player_turn()  # Attaque du joueur
                    valid_action = True
                elif action == "use":
                    cancel_action = self.handle_item_use()  # Utilisation d'un objet, retourne True si l'utilisateur annule
                    if cancel_action:
                        print("\nReturning to the action menu...\n")
                        break  # Sortir de la boucle et redonner les choix au joueur
                    valid_action = True
                elif action == "run":
                    if self.run_away():
                        print(f"\n\033[92m{self.player.name} escaped!\033[0m\n")
                        return
                    else:
                        print(f"\n\033[91m{self.player.name} failed to escape.\033[0m\n")
                        valid_action = True  # Tentative de fuite valide
                else:
                    print("\033[93mInvalid action. Please choose again.\033[0m\n")

            # L'ennemi attaque après l'action du joueur, si le joueur n'a pas annulé
            if self.enemy.is_alive() and valid_action:
                self.enemy_turn()

        # Conclusion du combat
        if self.player.is_alive():
            print(f"\n\033[92m{self.player.name} has defeated {self.enemy.name}!\033[0m\n")
            self.reward_player()  # Récompense après victoire
        else:
            print(f"\n\033[91m{self.enemy.name} has defeated {self.player.name}!\033[0m\n")

    # --- Actions du joueur ---
    def player_turn(self):
        """Effectue l'attaque du joueur avec calcul de coup critique."""
        attack_with_boost = self.player.attack + self.temp_attack_boost
        
        # Chance de coup critique ajustée selon le niveau et la différence d'attaque
        crit_chance = self.calculate_crit_chance(self.player, self.enemy)
        is_crit = random.random() < crit_chance
        
        damage = self.calculate_damage(attack_with_boost, crit_chance=crit_chance if is_crit else 0)

        self.enemy.take_damage(damage)
        
        if is_crit:
            print(f"\033[93mCritical hit!\033[0m {self.player.name} deals \033[91m{damage}\033[0m damage to {self.enemy.name}!")
        else:
            print(f"\n{self.player.name} attacks {self.enemy.name} for \033[91m{damage}\033[0m damage.\n")
        
        self.reset_attack_boost()  # Réinitialisation après application


    def handle_item_use(self):
        """Permet au joueur d'utiliser un objet pendant le combat ou de revenir en arrière."""
        while True:
            self.player.inventory.show_inventory()  # Affiche l'inventaire du joueur
            print("\nType 'cancel' to go back to attacking.\n")  # Ajout d'une option pour annuler

            try:
                item_index = input("Enter the number of the item you want to use: ").strip().lower()

                if item_index == "cancel":  # Si l'utilisateur tape "cancel", on annule l'utilisation de l'objet
                    print("\nReturning to attack...\n")
                    return True  # Retourne True pour signaler l'annulation

                item_index = int(item_index)  # Convertir l'entrée en entier

                if item_index < 1 or item_index > len(self.player.inventory.items):
                    print("\033[93mInvalid index. Try again.\033[0m\n")
                    continue

                item = self.player.inventory.get_item(item_index)
                if item:
                    # Application de l'effet de l'objet
                    if item.effect == "boost_attack":
                        print(f"\n\033[94mAttack boosted by {item.power}!\033[0m\n")
                        self.player.apply_temporary_attack_boost(item.power)
                        self.temp_attack_boost = item.power
                    elif item.effect == "damage":
                        print(f"\nUsing {item.name}! {self.player.name} uses {item.name} and deals {item.power} damage.")
                        self.enemy.take_damage(item.power)  # dégâts fixes, cohérent via take_damage.
                    elif item.effect == "health_boost":
                        print(f"\nUsed \033[94m{item.name}\033[0m to heal \033[92m{item.power}\033[0m HP!")
                        self.player.hp += item.power  # Restauration de la santé

                    # Mise à jour de l'inventaire
                    self.player.inventory.use_item(item_index, self.player)  # Utilisation de l'objet
                    if item.quantity <= 0:
                        self.player.inventory.remove_item(item.name)  # Retirer l'objet épuisé
                        print(f"\033[91m{item.name} has been used up and removed.\033[0m\n")
                    break  # Terminer la boucle une fois l'objet utilisé
            except ValueError:
                print("\033[93mInvalid input. Please enter a number or 'cancel' to go back.\033[0m\n")


    def reset_attack_boost(self):
        """Réinitialise le boost temporaire d'attaque du joueur."""
        if self.temp_attack_boost > 0:
            print("\033[94mAttack boost reset.\033[0m\n")
        self.temp_attack_boost = 0

    # --- Actions de l'ennemi ---
    def enemy_turn(self):
        """Effectue l'attaque de l'ennemi avec esquive possible."""
        if self.player_evades():
            print(f"\n\033[93m{self.player.name} evades the attack!\033[0m\n")
        else:
            attack_power = self.enemy.attack
            damage = self.calculate_damage(attack_power)

            self.player.take_damage(damage)
            # print(f"\n{self.enemy.name} attacks {self.player.name} for \033[91m{damage}\033[0m damage.\n")


    # --- Calculs de dégâts et autres ---
    def calculate_damage(self, attack, crit_chance=0):
        """Calcule les dégâts avec possibilité de coup critique."""
        base_damage = attack  # attaque d'entrée ou boostée
        variation = random.uniform(0.9, 1.2)  # Ajoute de la variation réaliste aux dégâts

        # Coup critique
        if random.random() < crit_chance:
            base_damage *= 2
            print("\033[93mCritical hit!\033[0m")
        
        # Calcul du total des dégâts avec la variation
        damage = int(base_damage * variation)

        # Minimum damage assurée de l'attaque doit être au moins 1
        return max(damage, 1)

    def calculate_crit_chance(self, attacker, defender):
        """Calcule la chance de coup critique."""
        crit_chance = CRIT_BASE_CHANCE + (attacker.level * 0.01) + (attacker.attack - defender.attack) * 0.005
        return min(crit_chance, 0.5)

    def player_evades(self):
        """Détermine si le joueur esquive l'attaque ennemie.""" 
        evade_chance = EVASION_BASE_CHANCE + (self.player.level * 0.01) + (self.player.attack - self.enemy.attack) * 0.005
        return random.random() < evade_chance

    def run_away(self):
        """Tente de fuir le combat avec un maximum de 3 tentatives."""
        if self.run_attempts >= 3:
            print("\033[93mThe monster took pity on you. He let you go...\033[0m\n")
            return True  # Fuite automatique après 3 essais

        # Calcul des chances de fuite en fonction du niveau
        run_chance = RUN_CHANCE + (self.player.level - self.enemy.level) * 0.05
        success = random.random() < run_chance

        self.run_attempts += 1  # Incrémente le compteur de tentatives

        if not success:
            damage = max(self.enemy.attack - self.player.defense, 1)  # Dégâts reçus si la fuite échoue
            self.player.take_damage(damage)
            print(f"\033[91m{self.enemy.name} hits you while you try to escape! You take {damage} damage.\033[0m\n")
            print(f"Escape attempt {self.run_attempts}/3 failed.\n")
        else:
            print(f"\033[92mYou successfully escape !\033[0m\n")
        
        return success

    # --- Récompenses et état du joueur ---
    def reward_player(self):
        """Récompense le joueur après la victoire dans le combat."""
        xp_reward = self.enemy.level * 10
        self.player.gain_experience(xp_reward)  # Gain d'XP
        self.player.heal(20)  # Restauration de la santé
        print(f"\n\033[92m{self.player.name} gained {xp_reward} XP!\033[0m")
        print(f"Health restored. {self.player.name} healed \033[92m20\033[0m HP.\n")

    def show_health_status(self):
        """Affiche l'état des points de vie des deux combattants."""
        print(f"{self.player.name}: \033[92m{self.player.hp}/{self.player.max_hp}\033[0m HP")
        print(f"{self.enemy.name}: \033[91m{self.enemy.hp}/{self.enemy.max_hp}\033[0m HP\n")

