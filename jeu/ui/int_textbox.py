from __future__ import annotations

import pygame

from jeu.ui.textbox import Textbox

class Int_Textbox(Textbox):
    
    def __init__(self: Textbox, screen: pygame.surface.Surface, position: tuple[float, float], placeholder_text: str, font: pygame.font.Font, size: tuple[float, float], text_color: str = "Black", background_color: str = "White", placeholder_color: str = "#E4E4E4", replacement_char: str | None = None, detection_offset: tuple[float, float] = ...) -> None:
        super().__init__(screen, position, placeholder_text, font, size, text_color, background_color, placeholder_color, replacement_char, detection_offset)
        
    def _process_input(self, event: pygame.event.Event) -> None:
        match (event.key):
            case pygame.K_BACKSPACE:
                return super()._process_input(event)
            case pygame.K_ESCAPE:
                return super()._process_input(event)
            
        if event.unicode in ['0','1','2','3','4','5','6','7','8','9']:
            return super()._process_input(event)
                
            

