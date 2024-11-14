import sys
import os
from game.player import Player
from game.enemy import Enemy
from game.map import GameMap
from game.battle import Battle
import ui_manager  # Importer le module UI
import save_load  # Importer le module de sauvegarde/chargement

# --------- Fonction principale de gestion du menu ---------
def main_menu():
    """Affiche le menu principal et gère les choix de l'utilisateur."""
    while True:
        ui_manager.display_menu()  # Affiche le menu principal
        choice = ui_manager.get_input("> ")  # Demande à l'utilisateur son choix

        if choice == "1":
            start_new_game()  # Démarrer une nouvelle partie
        elif choice == "2":
            player, game_map, current_position, save_name = save_load.load_game()  # Charger une partie sauvegardée
            if player and game_map:
                game_loop(player, game_map, current_position, save_name)  # Lancer la boucle de jeu
            else:
                print("No saved game found or failed to load.")  # Si la sauvegarde échoue
        elif choice == "3":
            ui_manager.display_about()  # Afficher des informations sur le jeu
        elif choice == "4":
            print("Thank you for playing! See you soon.")  # Quitter le jeu
            sys.exit()
        else:
            print("Invalid option. Please choose a valid option.")  # Choix invalide

# --------- Fonction pour démarrer une nouvelle partie ---------
def start_new_game():
    """Démarre une nouvelle partie et sauvegarde immédiatement, en vérifiant si le nom de la sauvegarde existe déjà."""
    ui_manager.clear_screen()
    player_name = ui_manager.get_input("Enter your character's name: ")  # Demander le nom du joueur
    player = Player(player_name)  # Créer un joueur
    game_map = GameMap()  # Créer une carte de jeu
    current_position = game_map.start_location  # Position initiale du joueur

    while True:
        save_name = ui_manager.get_input("Enter a name for your save file: ")  # Demander un nom pour la sauvegarde
        save_file_path = os.path.join(save_load.SAVE_DIRECTORY, f"{save_name}.pkl")  # Vérifier si le fichier existe
        if os.path.exists(save_file_path):
            # Si le fichier existe déjà, demander à l'utilisateur s'il veut écraser
            overwrite = ui_manager.get_input(f"Save file '{save_name}' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite == 'y':
                save_load.save_game(player, game_map, save_name)  # Sauvegarder la partie
                break
            else:
                print("Please enter a different name for your save file.")  # Demander un autre nom
        else:
            save_load.save_game(player, game_map, save_name)  # Sauvegarder la partie
            break  # Sortir de la boucle une fois la sauvegarde effectuée

    ui_manager.clear_screen()
    print(f"Welcome, {player.name}! You find yourself in a mysterious forest.")
    game_loop(player, game_map, current_position, save_name)  # Lancer la boucle de jeu

# --------- Boucle principale du jeu ---------
def game_loop(player, game_map, current_position, save_name):
    """Boucle principale du jeu."""
    while player.is_alive():
        # Afficher la carte et les informations du joueur
        game_map.print_map(current_position)
        ui_manager.player_info(player)

        # Gérer les rencontres avec des ennemis
        if game_map.is_enemy_at(current_position):
            enemy = game_map.get_enemy(current_position)
            print(f"A wild {enemy.name} (Level {enemy.level}) appears!")
            print(f"{enemy.name}'s HP: {enemy.hp}/{enemy.max_hp}")

            battle = Battle(player, enemy)
            battle.start_battle()

            if not player.is_alive():
                break  # Fin de jeu si le joueur est mort
            else:
                game_map.clear_enemy(current_position)  # Enlever l'ennemi après la victoire

        # Gérer les objets à la position actuelle
        if game_map.is_item_at(current_position):
            player.pick_up_item(current_position[0], current_position[1], game_map)

            if not player.is_alive():
                break

        # Demander et exécuter l'action du joueur
        action = get_player_action()
        ui_manager.clear_screen()

        if action == 'quit':
            print("Exiting the game.")
            break
        elif action == 'go north':
            current_position = game_map.move_player(current_position, 'north')
        elif action == 'go south':
            current_position = game_map.move_player(current_position, 'south')
        elif action == 'go west':
            current_position = game_map.move_player(current_position, 'west')
        elif action == 'go east':
            current_position = game_map.move_player(current_position, 'east')

        # Sauvegarder automatiquement avec le nom de la sauvegarde en cours
        save_load.save_game(player, game_map, save_name)

    if not player.is_alive():
        ui_manager.display_game_over()  # Afficher l'écran de fin de jeu
        save_load.save_game(player, game_map, save_name)

# --------- Gestion des actions du joueur ---------
def get_player_action():
    """Demande l'action du joueur et gère les entrées invalides."""
    while True:
        action = ui_manager.get_input("What would you like to do? (Type 'help' for options): ").strip().lower()

        if action == 'help':
            ui_manager.display_help()
        elif action in ['z', 'go north']:
            return 'go north'
        elif action in ['s', 'go south']:
            return 'go south'
        elif action in ['q', 'go west']:
            return 'go west'
        elif action in ['d', 'go east']:
            return 'go east'
        elif action == 'quit':
            return 'quit'
        else:
            print("Invalid action. Please try again.")  # Entrée invalide

# --------- Point d'entrée principal ---------
if __name__ == "__main__":
    main_menu()  # Lancer le menu principal
