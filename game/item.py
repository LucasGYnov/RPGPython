class Item:
    def __init__(self, name, effect, power, quantity=1, attack_bonus=0, level=1, boost=0):
        """
        Initializes an item with specific properties.

        :param name: Name of the item.
        :param effect: Effect of the item (heal, boost_attack, damage, boost_shield).
        :param power: Main power of the item.
        :param quantity: Quantity of items available (default is 1).
        :param attack_bonus: Attack bonus if applicable (default is 0).
        :param level: Level of the item (default is 1).
        :param boost: Percentage boost (used for effects like boost_attack) (default is 0).
        """
        self.name = name
        self.effect = effect
        self.power = power
        self.quantity = quantity
        self._attack_bonus = attack_bonus
        self.level = level
        self.boost = boost

    def use(self, player, enemy=None):
        """
        Uses the item on the player or enemy depending on its effect.

        :param player: The instance of the player using the item.
        :param enemy: (Optional) The instance of the targeted enemy.
        :return: True if the item was used, otherwise False.
        """
        # Check if the item has quantities available
        if self.quantity <= 0:
            print(f"No {self.name} left to use!")  # If the item is depleted
            return False

        # Logic based on the item's effect
        if self.effect == "heal":
            # Healing effect on the player
            player.heal(self.power)
            print(f"{player.name} recovers {self.power} HP!")

        elif self.effect == "boost_attack":
            # Apply a temporary boost to the player's attack
            if not player.has_boosted_attack:  # Check if attack is not already boosted
                player.apply_temporary_attack_boost(self.power)
                print(f"{player.name}'s attack will increase by {self.power}% on the next turn!")
            else:
                print(f"{player.name} already has an active attack boost!")

        elif self.effect == "damage" and enemy:
            # Apply damage to the enemy
            total_damage = round(self.power * (1 + player._temporary_attack_boost / 100))
            print(f"{player.name} uses {self.name} and deals {total_damage:.2f} damage to {enemy.name}!")
            enemy.take_damage(total_damage)

        elif self.effect == "boost_shield":
            # Apply a shield to the player
            shield_amount = self.power
            player.activate_shield(shield_amount)
            print(f"{player.name} gains a shield of {shield_amount} points!")

        # Reduce the item's quantity after use
        self.quantity -= 1
        return True

    def is_usable(self):
        """
        Checks if the item is still usable (if quantities remain).

        :return: True if the item can be used, otherwise False.
        """
        return self.quantity > 0

    def attack_bonus(self):
        """
        Returns the attack bonus of the item, if applicable.

        :return: The attack bonus of the item.
        """
        return self._attack_bonus

    def __str__(self):
        """
        Returns a textual representation of the item.

        :return: A string representing the item.
        """
        return (f"{self.name} (Effect: {self.effect}, Power: {self.power}, "
                f"Quantity: {self.quantity}, Level: {self.level})")
