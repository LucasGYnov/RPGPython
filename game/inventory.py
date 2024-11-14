import random
import json
from game.item import Item

class Inventory:
    def __init__(self):
        """
        Initializes the inventory with starting items.
        """
        self.items = []  # List of items in the inventory

        #self.load_default_items()  # Load starting items

    # def load_default_items(self):
        """
        Loads default items from a JSON file and adds those specified in the `starter_items` list.
        """
        """ try:
            with open('assets/items_data.json', 'r') as file:
                items_data = json.load(file)
                
                # List of items to add by default
                starter_items = ["Noob's Dagger", "Minor Health Potion", "Wooden Shield"]

                # Filter and add specified starter items
                for item_info in items_data:
                    if item_info["name"] in starter_items:
                        item = Item(
                            name=item_info["name"],
                            effect=item_info["effect"],
                            power=item_info["power"],
                            quantity=item_info.get("quantity", 1),
                            level=item_info.get("level", 1),
                            boost=item_info.get("boost", 0)
                        )
                        self.add_item(item)  # Add item to inventory
        except FileNotFoundError:
            print("Error: items_data.json file not found.")
        except json.JSONDecodeError:
            print("Error: items_data.json file is malformed.") """

    def add_item(self, item):
        """
        Adds an item to the inventory or updates the quantity if the item already exists.
        
        :param item: The item to add to the inventory.
        """
        existing_item = next((i for i in self.items if i.name == item.name), None)

        if existing_item:
            existing_item.quantity += item.quantity
            print(f"{item.quantity}x {item.name} added. New quantity: {existing_item.quantity}.")
        else:
            self.items.append(item)

    def show_inventory(self):
        """
        Displays the current inventory with items and their quantities.
        """
        if not self.items:
            print("Your inventory is empty.")
            return

        print("Inventory:")
        print("--------------------------------------------------")
        print(f"{'No.':<4}{'Item Name':<22}{'Quantity':<10}{'Power/Effect':<15}")
        print("--------------------------------------------------")
        for i, item in enumerate(self.items, start=1):
            effect_display = f"{item.effect.capitalize()} ({item.power})" 
            print(f"{i:<4}{item.name:<22} x{item.quantity:<10}{effect_display:<15}")



    def get_item(self, item_index):
        """
        Retrieves an item from the inventory by its index.
        
        :param item_index: Index of the item (1-based).
        :return: The corresponding item or None if the index is invalid.
        """
        try:
            return self.items[item_index - 1]  # Convert 1-based index to 0-based
        except IndexError:
            print("Invalid index. No item found at this position.")
            return None

    def use_item(self, item_index, player, enemy=None):
        item = self.get_item(item_index)
        if item and item.is_usable():
            print(f"{player.name} uses {item.name}.")
            
            if item.effect == "damage" and enemy:
                # Appliquer les dégâts à l'ennemi
                enemy.hp -= item.power
                print(f"{player.name} deals {item.power:.2f} damage to {enemy.name}!")
            
            elif item.effect == "health_boost":
                # Soigner le joueur
                player.hp = min(player.max_hp, player.hp + item.power)
                print(f"{player.name} heals for {item.power} HP!")
            
            elif item.effect == "boost_shield":
                # Appliquer un boost temporaire au joueur
                player._damage_reduction += item.power
                print(f"{player.name}'s shield increased by {item.power} points!")

            item.quantity -= 1
            if item.quantity <= 0:
                self.items.remove(item)
                # print(f"{item.name} has been used up and removed.")
            return True
        else:
            print(f"{item.name} cannot be used right now.")
        return False


    def has_items(self):
        """
        Checks if the inventory contains any items.
        
        :return: True if the inventory contains items, otherwise False.
        """
        return len(self.items) > 0

    def clean_up_items(self):
        """
        Removes items with zero or negative quantity.
        """
        self.items = [item for item in self.items if item.quantity > 0]

    def drop_loot(self):
        """
        Generates random loot from the inventory, with reduced quantities.
        
        :return: List of `Item` objects with reduced quantities.
        """
        loot = []
        if not self.items:
            return loot

        num_items_to_drop = random.choice([1, 2])
        for _ in range(num_items_to_drop):
            item = random.choice(self.items)
            quantity = random.randint(1, item.quantity)
            loot_item = Item(
                name=item.name,
                effect=item.effect,
                power=item.power,
                quantity=quantity,
                level=item.level,
                boost=item.boost
            )
            loot.append(loot_item)
            item.quantity -= quantity
            if item.quantity <= 0:
                self.items.remove(item)

        return loot

    def remove_item(self, item_name, quantity=1):
        """
        Removes a specified quantity of an item from the inventory.
        
        :param item_name: Name of the item to remove.
        :param quantity: Quantity to remove.
        """
        for item in self.items:
            if item.name == item_name:
                item.quantity -= quantity
                if item.quantity <= 0:
                    self.items.remove(item)
                print(f"{quantity}x {item_name} removed.")
                return True
        return False

    def find_item(self, item_name):
        """
        Searches for a specific item in the inventory.
        
        :param item_name: Name of the item to search for.
        :return: The `Item` object if found, otherwise None.
        """
        for item in self.items:
            if item.name == item_name:
                return item
        print(f"Item {item_name} not found.")
        return None

    def __str__(self):
        """
        Returns a textual representation of the inventory.
        
        :return: String representing the inventory.
        """
        if not self.items:
            return "Empty inventory."
        return "\n".join(f"{item.name} (Quantity: {item.quantity})" for item in self.items)
