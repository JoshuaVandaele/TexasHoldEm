import sys

import pygame

from jeu.poker_table import poker_table
from jeu.login_screen import login_screen
from jeu.options_screen import options_screen
from jeu.ui.button import Button

from jeu.ui.ui import UI
from jeu.utils.assets_import import resource_path
from jeu.utils.font_manager import FontManager

MAX_SIZE = 25
MIN_SIZE = 2

def main_menu(screen: pygame.surface.Surface):
    """Main menu of the game.

    Args:
        screen (pygame.surface.Surface): Screen to display the menu on
    """
    clock: pygame.time.Clock = pygame.time.Clock()

    pygame.display.set_caption("Menu")

    menu_font: FontManager = FontManager(resource_path("jeu/assets/fonts/Truculenta.ttf"))

    uninteraction_timer = 0

    def quit():
        """Quits the program
        """
        pygame.quit()
        sys.exit()

    background: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/menu_background.png"))

    menu_text: pygame.surface.Surface = menu_font.get_font(
        100).render("MAIN MENU", True, "#EEEEEE")
    menu_rect: pygame.rect.Rect = menu_text.get_rect(center=(640, 75))

    play_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Play Rect.png")),
        position=(640, 250),
        text="PLAY",
        font=menu_font.get_font(75),
        color="#FFFFFF",
        hover_color="#d7fcd4",
        action=lambda: poker_table(screen, ["PLAYERNAME00", "PLAYERNAME01"])
    )
    options_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Options Rect.png")),
        position=(640, 400),
        text="OPTIONS",
        font=menu_font.get_font(75),
        color="#FFFFFF",
        hover_color="#d7fcd4",
        action=lambda: options_screen(screen)
    )
    quit_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Quit Rect.png")),
        position=(640, 550),
        text="QUIT",
        font=menu_font.get_font(75),
        color="#FFFFFF",
        hover_color="#d7fcd4",
        action=quit
    )

    def account_button_handler():
        nonlocal uninteraction_timer
        login_screen(screen)
        uninteraction_timer = 10

    account_button = Button(screen=screen, image=pygame.image.load(resource_path("jeu/assets/images/User.png")),
                            position=(1280-75, 75),
                            text=" ",
                            font=menu_font.get_font(75),
                            color="#FFFFFF",
                            hover_color="#FFFFFF",
                            action=account_button_handler
                            )
    # Store all UI elements in a list for easy access
    menu_buttons: tuple[UI, ...] = (account_button, play_button, options_button, quit_button)

    while True:
        if uninteraction_timer > 0:
            uninteraction_timer -= 1
        print(int(clock.get_fps()), end=" FPS    \r")
        # Blit the background to screen first /!\
        screen.blit(background, (0, 0))
        # Display all text on screen
        screen.blit(menu_text, menu_rect)

        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT:
                    quit()
                case pygame.MOUSEBUTTONDOWN:
                    # Clear FPS counter from console
                    print("            ", end="\r")
            # Update all UI elements
            for button in menu_buttons:
                if uninteraction_timer <= 0:
                    button.update(event)
        # Update all UI elements
        for button in menu_buttons:
            button.update_render()
        # Update the display
        pygame.display.update()
        # Tick the clock used to calculate the FPS
        clock.tick()
