import os
import sys
from ascii_art import game_title, game_over, about  # Import des ASCII arts

# -------------------------
# Fonctions utilitaires
# -------------------------

def clear_screen():
    """Efface l'écran du terminal, compatible avec Windows et Unix/Linux/Mac."""
    os_system = os.name
    if os_system == 'nt':  # Si c'est Windows
        os.system('cls')
    else:  # Si c'est un système Unix-like (Linux/MacOS)
        os.system('clear')

def move_cursor_to_bottom():
    """Positionne le curseur sur la dernière ligne du terminal."""
    terminal_height = os.get_terminal_size().lines
    sys.stdout.write(f"\033[{terminal_height};1H")  # Positionne le curseur sur la dernière ligne
    sys.stdout.flush()

def get_input(prompt):
    """Affiche une invite en bas de l'écran et retourne l'entrée de l'utilisateur."""
    move_cursor_to_bottom()  # Déplacer le curseur avant de demander l'entrée
    return input(prompt)

# -------------------------
# Fonctions de centrage du texte
# -------------------------

def center_text(text):
    """Centre le texte sur l'écran en fonction de la taille du terminal."""
    terminal_width = os.get_terminal_size().columns
    terminal_height = os.get_terminal_size().lines
    lines = text.split('\n')
    centered_lines = [line.center(terminal_width) for line in lines]
    
    # Calculer l'espace vertical pour centrer verticalement
    text_height = len(centered_lines)
    vertical_padding = (terminal_height - text_height) // 2

    centered_text = '\n' * vertical_padding + '\n'.join(centered_lines)
    return centered_text

def center_text_above(art, text_box):
    """
    Centre l'art ASCII juste au-dessus du menu ou du texte encadré.
    
    art : str
        Le texte ASCII à afficher au-dessus.
    text_box : str
        Le texte encadré qui sera centré en dessous.
    """
    terminal_width = os.get_terminal_size().columns
    terminal_height = os.get_terminal_size().lines

    # Calcul des hauteurs des éléments
    art_lines = art.split('\n')
    text_box_lines = text_box.split('\n')
    total_height = len(art_lines) + len(text_box_lines)
    
    # Calcul du padding vertical pour que tout soit centré globalement
    vertical_padding = (terminal_height - total_height) // 2

    # Centrage horizontal
    centered_art = '\n'.join(line.center(terminal_width) for line in art_lines)
    centered_text_box = '\n'.join(line.center(terminal_width) for line in text_box_lines)

    return '\n' * vertical_padding + centered_art + '\n' + centered_text_box

# -------------------------
# Fonctions d'affichage des menus et informations
# -------------------------

def draw_box(text):
    """Encadre le texte fourni avec un joli cadre."""
    lines = text.strip().split('\n')
    max_length = max(len(line) for line in lines)
    border = f"╔{'═' * (max_length + 2)}╗"

    framed_lines = [f"║ {line.ljust(max_length)} ║" for line in lines]
    bottom_border = f"╚{'═' * (max_length + 2)}╝"

    return f"{border}\n" + "\n".join(framed_lines) + f"\n{bottom_border}"

def display_menu():
    """Affiche le menu principal du jeu avec un cadre."""
    clear_screen()
    
    menu_text = """
1. Create a New Game
2. Load Saved Game
3. About
4. Exit
    """
    
    # Encadrer le menu
    menu_box = draw_box(menu_text)
    # Art ASCII juste au-dessus du menu
    print(center_text_above(game_title(), menu_box))

def display_help():
    """Affiche le menu d'aide encadré."""
    help_text = """
Game Help:
- Use 'z' or 'go north' to move north.
- Use 's' or 'go south' to move south.
- Use 'q' or 'go west' to move west.
- Use 'd' or 'go east' to move east.
- Type 'help' to see this help message again.
- Type 'quit' to exit the game.
    """
    
    clear_screen()
    print(center_text(draw_box(help_text)))

def display_game_over():
    """Affiche un message de fin de jeu encadré."""
    clear_screen()
    
    game_over_box = draw_box(game_over())
    print(center_text(game_over_box))  # ASCII art juste au-dessus
    get_input("\nPress Enter to exit...")

def display_about():
    """Affiche les informations 'About' encadrées."""
    clear_screen()

    about_box = draw_box(about())
    
    print(center_text(about_box))  # ASCII art juste au-dessus
    get_input("\nPress Enter to return...")

def player_info(player):
    """Affiche les informations du joueur dans un format stylisé."""
    # Préparer le texte d'information du joueur
    info_text = f"""
    {player.name} - Level {player.level}
    HP: {player.hp}/{player.max_hp}
    Attack: {player.attack}
    Defense: {player.defense}
    XP: {player._experience}/{player.experience_to_next_level()}
    """

    # Encadrer l'information avec un joli cadre
    print(draw_box(info_text))

