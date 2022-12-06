import pygame

class FontManager:
    def __init__(self, font: str) -> None:
        """

        Args:
            font (str): Path of the font
        """
        self.font = font
    
    def get_font(self, size: int) -> pygame.font.Font:  # Returns Press-Start-2P in the desired size
        """Returns the desired font in the desired size

        Args:
            size (int): Size of the font

        Returns:
            pygame.font.Font: Font
        """
        return pygame.font.Font(self.font, size)