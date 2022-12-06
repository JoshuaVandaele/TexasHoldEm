import pygame

from jeu.ui.popup import Popup
from jeu.utils.font_manager import FontManager
from jeu.utils.assets_import import resource_path


def options_screen(screen: pygame.surface.Surface):
    """Options screen

    Args:
        screen (pygame.surface.Surface): Screen to display the menu on
    """
    options_font: FontManager = FontManager(resource_path("jeu/assets/fonts/Truculenta.ttf"))

    # Initializing on-screen elements #
    options_popup: Popup = Popup(screen, "Options", (screen.get_width()*0.85, screen.get_height()*0.8), "#0575BB")

    options_popup.run()
