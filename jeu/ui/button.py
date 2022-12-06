from __future__ import annotations

from typing import Callable

import pygame

from jeu.ui.ui import UI


class Button(UI):
    def __init__(self: Button, screen: pygame.surface.Surface, image: pygame.surface.Surface | None, position: tuple[float, float], text: str, font: pygame.font.Font, color: str, hover_color: str, action: Callable = lambda: None, detection_offset: tuple[float, float] = (0, 0)) -> None:
        """Button UI elements

        Args:
            screen (pygame.surface.Surface): Screen to update the button on
            image (pygame.surface.Surface | None): Image to use as background
            position (tuple[int, int]): X and Y position of the button
            text (str): Text to display on the button
            font (pygame.font.Font): Font to use for the text
            color (str): Color of the text
            hover_color (str): Color of the text when hovering
            action (Callable): Function to call upon button click
            detection_offset (tuple[float, float]): Offset for the mouse/button interaction
        """
        super().__init__(screen)
        self.image = image
        self.position = position
        self.font = font
        self.color, self.hover_color = color, hover_color
        self.text = text
        self.text_render = self.font.render(self.text, True, self.color)
        self.action = action
        self.detection_offset = detection_offset
        if not self.image:
            self.image = self.text_render
        self.rect = self.image.get_rect(center=self.position)
        self.text_rect = self.text_render.get_rect(center=self.position)

    def update_render(self: Button) -> None:
        """Updates the button's render
        """
        if self.image:
            self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_render, self.text_rect)

    def update(self: Button, event: pygame.event.Event):
        """Updates the button according to the given event.

        Args:
            event (pygame.event.Event): Event to check for
        """
        mouse_pos: tuple[float, float] = (pygame.mouse.get_pos()[0]-self.detection_offset[0], pygame.mouse.get_pos()[1]-self.detection_offset[1])
        match (event.type):
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouse_pos):
                    self.action()
                    return True
            case pygame.MOUSEMOTION:
                if self.rect.collidepoint(mouse_pos):
                    self.text_render = self.font.render(
                        self.text, True, self.hover_color)
                else:
                    self.text_render = self.font.render(
                        self.text, True, self.color)

        return False
