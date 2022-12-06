from __future__ import annotations

from typing import Callable

import pygame
from jeu.ui.ui import UI


class Checkbox(UI):
    def __init__(self: Checkbox, screen: pygame.surface.Surface, position: tuple[float, float], checked_image: pygame.surface.Surface, unchecked_image: pygame.surface.Surface, text: str, font: pygame.font.Font, color: str, text_offset: int = 0, on_check: Callable = lambda: None, on_uncheck: Callable = lambda: None, checked: bool = False, detection_offset: tuple[float, float] = (0, 0)) -> None:
        """Checkbox which takes the value true or false.

        Args:
            screen (pygame.surface.Surface): Screen to update the checkbox on
            position (tuple[int, int]): X and Y position of the checkbox
            checked_image (pygame.surface.Surface): Image to use for the checkbox when it's checked
            unchecked_image (pygame.surface.Surface): Image to use for the checkbox when it's unchecked
            text (str): Text to display next to the checkbox.
            font (pygame.font.Font): Font to use for the text.
            color (str): Color of the text.
            text_offset (int, optional): offset of the text. Defaults to 0.
            on_check (Callable, optional): Function to run on check. Defaults to lambda:None.
            on_uncheck (Callable, optional): Function to run on uncheck. Defaults to lambda:None.
            checked (bool): Current state of the button. Defaults to False.
            detection_offset (tuple[float, float], optional): Offset for the mouse/checkbox interaction. Defaults to (0, 0).
        """
        super().__init__(screen, detection_offset)
        self.checked = checked
        self.checked_image = checked_image
        self.unchecked_image = unchecked_image
        self.position = position
        self.font = font
        self.color = color
        self.text = text
        self.text_render = self.font.render(self.text, True, self.color)
        self.on_check = on_check
        self.on_uncheck = on_uncheck
        self.rect = self.checked_image.get_rect(center=self.position)
        self.text_rect = self.text_render.get_rect(center=self.position)
        self.text_rect.left = int(position[0] + self.checked_image.get_width() + text_offset)

    def update_render(self: Checkbox) -> None:
        """Updates the checkbox's render
        """
        if self.checked:
            self.screen.blit(self.checked_image, self.rect)
        else:
            self.screen.blit(self.unchecked_image, self.rect)
        self.screen.blit(self.text_render, self.text_rect)

    def update(self: Checkbox, event: pygame.event.Event):
        """Updates the checkbox according to the given event.

        Args:
            event (pygame.event.Event): Event to check for
        """
        mouse_pos: tuple[float, float] = (pygame.mouse.get_pos()[0]-self.detection_offset[0], pygame.mouse.get_pos()[1]-self.detection_offset[1])
        match (event.type):
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouse_pos):
                    self.checked = not self.checked

                    if self.checked:
                        self.on_check()
                    else:
                        self.on_uncheck()
