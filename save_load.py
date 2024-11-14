import pickle
import os

import ui_manager  # Importer le module UI


SAVE_DIRECTORY = "saves"  # Dossier pour stocker les sauvegardes

def save_game(player, game_map, save_name):
    """Sauvegarde l'état du joueur, de la carte et de la position actuelle dans un fichier pickle."""
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)  # Créer le dossier de sauvegarde si nécessaire

    save_file = os.path.join(SAVE_DIRECTORY, f"{save_name}.pkl")
    data = {
        "player": player,
        "game_map": game_map,
        "current_position": game_map.get_player_position(),  # Sauvegarder la position actuelle
    }

    try:
        with open(save_file, "wb") as file:
            pickle.dump(data, file)  # Sauvegarder les données dans le fichier
    except Exception as e:
        print(f"Failed to save the game: {e}")  # Gestion des erreurs lors de la sauvegarde

def load_game():
    """Charge l'état du joueur, de la carte et de la position actuelle à partir d'un fichier pickle."""
    if not os.path.exists(SAVE_DIRECTORY):
        print("\nNo saved games found.")
        input("\nPress Enter to return to the main menu...")
        return None, None, None, None

    save_files = [f for f in os.listdir(SAVE_DIRECTORY) if f.endswith(".pkl")]
    if not save_files:
        print("\nNo saved games found.")
        input("\nPress Enter to return to the main menu...")
        return None, None, None, None

    print("\nSelect a saved game:")
    for idx, save_file in enumerate(save_files, start=1):
        print(f"{idx}. {save_file[:-4]}")  # Affiche le nom de la sauvegarde sans l'extension

    try:
        choice = int(input("\nEnter the number of the game to load: "))
        if 1 <= choice <= len(save_files):
            selected_file = save_files[choice - 1]
            save_path = os.path.join(SAVE_DIRECTORY, selected_file)

            with open(save_path, "rb") as file:
                data = pickle.load(file)  # Charger les données du fichier
                print(f"\nGame loaded successfully from {selected_file}!")
                ui_manager.clear_screen()
                save_name = os.path.splitext(selected_file)[0]  # Récupérer le nom sans extension
                return data["player"], data["game_map"], data["current_position"], save_name
        else:
            print("\nInvalid choice.")
            input("\nPress Enter to return to the main menu...")
            return None, None, None, None
    except Exception as e:
        print(f"\nFailed to load the game: {e}")
        input("\nPress Enter to return to the main menu...")
        return None, None, None, None
