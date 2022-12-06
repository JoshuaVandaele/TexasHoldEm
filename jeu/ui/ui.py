from abc import ABC, abstractmethod

import pygame
from typing_extensions import Self


class UI(ABC):
    """Abstract class for UI elements 
    """

    def __init__(self: Self, screen: pygame.surface.Surface, detection_offset: tuple[float, float] = (0, 0)) -> None:
        """Button UI elements

        Args:
            screen (pygame.surface.Surface): Screen to update the element on
        """
        self.screen = screen
        self.detection_offset: tuple[float, float] = detection_offset

    @abstractmethod
    def update(self: Self, event: pygame.event.Event) -> None:
        """Updates the element according to a give event.

        Args:
            event (pygame.event.Event): Event to process
        """
        pass

    @abstractmethod
    def update_render(self):
        """Updates the element on screen
        """
        pass
