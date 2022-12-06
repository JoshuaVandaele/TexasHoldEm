import sys

import pygame
from jeu.ui.button import Button
from jeu.ui.popup import Popup
from jeu.ui.textbox import Textbox
from jeu.ui.ui import UI
from jeu.utils.font_manager import FontManager


def login_screen(screen: pygame.surface.Surface):
    """Login screen

    Args:
        screen (pygame.surface.Surface): Screen to display the menu on
    """
    login_font: FontManager = FontManager("jeu/assets/fonts/Truculenta.ttf")

    # Initializing on-screen elements #
    login_popup: Popup = Popup(screen, "Account", (500, 580), "#0575BB")

    def login_handler():
        """Action ran when the login button is clicked
        """
        print(f"Login! User:'{username_textbox.text}', Password:'{password_textbox.text}'")
        login_popup.active = False

    def register_handler():
        """Action ran when the register button is clicked
        """
        print(f"Register! User:'{username_textbox.text}', Password:'{password_textbox.text}'")
        login_popup.active = False

    username_textbox = Textbox(
        screen=login_popup.surface,
        position=(login_popup.surface.get_size()[0]//2, 225),
        placeholder_text="Username",
        font=login_font.get_font(75),
        size=(370, 100)
    )
    password_textbox = Textbox(
        screen=login_popup.surface,
        position=(login_popup.surface.get_size()[0]//2, 350),
        placeholder_text="Password",
        font=login_font.get_font(75),
        size=(370, 100),
        replacement_char="*"
    )
    login_button = Button(
        screen=login_popup.surface,
        image=pygame.image.load("jeu/assets/images/Login Rect.png"),
        position=(login_popup.surface.get_size()[0]//2*0.5, 500),
        text="Login",
        font=login_font.get_font(50),
        color="#000000",
        hover_color="#555555",
        action=login_handler
    )
    register_button = Button(
        screen=login_popup.surface,
        image=pygame.image.load("jeu/assets/images/Login Rect.png"),
        position=(login_popup.surface.get_size()[0]//2*1.5, 500),
        text="Register",
        font=login_font.get_font(50),
        color="#000000",
        hover_color="#555555",
        action=register_handler
    )

    login_popup.add_ui_element(username_textbox)
    login_popup.add_ui_element(password_textbox)
    login_popup.add_ui_element(register_button)
    login_popup.add_ui_element(login_button)

    login_popup.run()
