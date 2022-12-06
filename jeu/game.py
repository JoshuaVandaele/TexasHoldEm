"""
TODO None of this is final, \
UI Elements are to be moved accordingly with what will be decided in the future; \
For now, we are just implementing their potential look and functionality.
"""

import pygame
from jeu.utils.font_manager import FontManager
from jeu.utils.assets_import import resource_path
import time

def formatted_score(score: int) -> str:
    return f"{score:03d}"

def formatted_time(time_in_seconds: int) -> str:
    minutes = time_in_seconds // 60
    seconds = time_in_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def get_timer_label(start_time_in_seconds: float, font: FontManager):
    time_elapsed_in_seconds = int(time.time() - start_time_in_seconds)
    timer_label: pygame.surface.Surface = font.get_font(75).render(formatted_time(time_elapsed_in_seconds), True, "#EEEEEE")
    timer_rect: pygame.rect.Rect = timer_label.get_rect(center=(640, 50))
    return (timer_label, timer_rect)

def get_score_label(score: int, font: FontManager, player1: bool):
    if player1:
        xpos: int = 100
        color: str = "#0000FF"
    else:
        xpos: int = 1280-100
        color: str = "#FF0000"
    player_score_label: pygame.surface.Surface = font.get_font(75).render(f"{score:03d}", True, color)
    player_score_rect: pygame.rect.Rect = player_score_label.get_rect(center=(xpos, 650))
    return (player_score_label, player_score_rect)

def game(screen: pygame.surface.Surface, size: tuple[int, int] = (10, 10)):
    """Game screen

    Args:
        screen (pygame.surface.Surface): Screen to display the game on
    """
    clock: pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Pipopipette")

    game_font: FontManager = FontManager(resource_path("jeu/assets/fonts/Truculenta.ttf"))

    background: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/game_background.png"))

    labels: dict[str, tuple[pygame.surface.Surface, pygame.rect.Rect]] = {}
    start_time_in_seconds: float = time.time()

    player1_label: pygame.surface.Surface = game_font.get_font(33).render("Playername01", True, "#EEEEEE")
    player1_rect: pygame.rect.Rect = player1_label.get_rect(center=(100, 593))
    player2_label: pygame.surface.Surface = game_font.get_font(33).render("Playername02", True, "#EEEEEE")
    player2_rect: pygame.rect.Rect = player2_label.get_rect(center=(1280-100, 593))

    labels["timer"] =  get_timer_label(time.time(), game_font)
    labels["player1"] = (player1_label, player1_rect)
    labels["player2"] = (player2_label, player2_rect)
    labels["player1_score"] = get_score_label(0, game_font, True)
    labels["player2_score"] = get_score_label(0, game_font, False)

    started = False

    while True:
        if started:
            labels["timer"] = get_timer_label(start_time_in_seconds, game_font)
            labels["player1_score"] = get_score_label(0, game_font, True)
            labels["player2_score"] = get_score_label(5, game_font, False)
        print(int(clock.get_fps()), end=" FPS    \r")
        screen.blit(background, (0, 0))
        for surface, rect in labels.values():
            screen.blit(surface, rect)

        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT:
                    quit()
                case pygame.MOUSEBUTTONDOWN:
                    if not started:
                        started = True
                        start_time_in_seconds = time.time()
                    # Clear FPS counter from console
                    print("            ", end="\r")

        pygame.display.update()
        clock.tick()
