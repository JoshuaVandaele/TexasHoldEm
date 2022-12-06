import pygame
from jeu.ui.button import Button
from jeu.ui.ui import UI
from jeu.utils.font_manager import FontManager

def poker_table(screen: pygame.surface.Surface, player_1: str = 'PLAYERNAME00', player_2: str = 'PLAYERNAME01'):

    pygame.display.set_caption("Game")
    menu_font: FontManager = FontManager("jeu/assets/fonts/Truculenta.ttf")
    
    # background
    background: pygame.surface.Surface = pygame.image.load("jeu/assets/images/backgound_poker.jpeg")
    
    # board
    board_flop_1: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_board_flop_1: pygame.rect.Rect = board_flop_1.get_rect(center = (1280 / 2, 720 /2 - 100))
    
    board_flop_2: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_board_flop_2: pygame.rect.Rect = board_flop_2.get_rect(center = (1280 / 2 - 200, 720 /2 - 100))
    
    board_flop_3: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_board_flop_3: pygame.rect.Rect = board_flop_3.get_rect(center = (1280 / 2 + 200, 720 /2 - 100))
    
    board_turn: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_board_turn: pygame.rect.Rect = board_turn.get_rect(center = (1280 / 2 - 100, 720 /2 + 100))
    
    board_river: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_board_river: pygame.rect.Rect = board_river.get_rect(center = (1280 / 2 + 100, 720 /2 + 100))
    
    # board chip
    board_chip: pygame.surface.Surface = pygame.image.load("jeu/assets/images/chip.png")
    rect_board_chip: pygame.rect.Rect = board_chip.get_rect(center = (1280 / 2 + 350, 720 / 2))
    text_chip_value: pygame.surface.Surface = menu_font.get_font(25).render('0', True, "#EEEEEE")
    rect_chip_value: pygame.rect.Rect = text_chip_value.get_rect(center = (1280 / 2 + 350, 720 / 2))
    
    text_current_blind: pygame.surface.Surface = menu_font.get_font(25).render('Current Blind:', True, "#EEEEEE")
    rect_current_blind: pygame.rect.Rect = text_current_blind.get_rect(center = (1280 / 2 + 350, 720 / 2 + 75))
    text_current_blind_value: pygame.surface.Surface = menu_font.get_font(25).render('0', True, "#EEEEEE")
    rect_current_blind_value: pygame.rect.Rect = text_current_blind_value.get_rect(center = (1280 / 2 + 350, 720 / 2 + 110))
    
    # player 1 name
    text_player_1: pygame.surface.Surface = menu_font.get_font(50).render(player_1, True, "#EEEEEE")
    rect_player_1: pygame.rect.Rect = text_player_1.get_rect(center = (1280 - 1105, 720 - 45))
    
    # player 1 hand
    card_j1_1: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_card_j1_1: pygame.rect.Rect = card_j1_1.get_rect(center = (1280 / 2 - 75, 720 - 65))
    
    card_j1_2: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_card_j1_2: pygame.rect.Rect = card_j1_2.get_rect(center = (1280 / 2 + 75, 720 - 65))
    
    # dealer token 1
    dealer_token_1: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Dealer_Token.png")
    rect_dealer_token_1: pygame.rect.Rect = dealer_token_1.get_rect(center = (1280 / 2 - 225, 720 - 75))
    
    # chip j1
    chip_j1: pygame.surface.Surface = pygame.image.load("jeu/assets/images/chip.png")
    rect_chip_j1: pygame.rect.Rect = chip_j1.get_rect(center = (1280 / 2 + 225, 720 - 75))
    text_chip_j1_value: pygame.surface.Surface = menu_font.get_font(25).render('100', True, "#EEEEEE")
    rect_chip_j1_value: pygame.rect.Rect = text_chip_j1_value.get_rect(center = (1280 / 2 + 225, 720 - 75))
    
    # player 2 name
    text_player_2: pygame.surface.Surface = menu_font.get_font(50).render(player_2, True, "#EEEEEE")
    rect_player_2: pygame.rect.Rect = text_player_2.get_rect(center = (1280 - 175, 720 - 675))
    
    # player 2 hand
    card_j2_1: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_card_j2_1: pygame.rect.Rect = card_j2_1.get_rect(center = (1280 / 2 - 75, 65))
    
    card_j2_2: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Card/card_back.png")
    rect_card_j2_2: pygame.rect.Rect = card_j2_2.get_rect(center = (1280 / 2 + 75, 65))
    
    # dealer token 1
    dealer_token_2: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Dealer_Token.png")
    rect_dealer_token_2: pygame.rect.Rect = dealer_token_2.get_rect(center = (1280 / 2 + 225, 75))
    
    # chip j2
    chip_j2: pygame.surface.Surface = pygame.image.load("jeu/assets/images/chip.png")
    rect_chip_j2: pygame.rect.Rect = chip_j2.get_rect(center = (1280 / 2 - 225, 75))
    text_chip_j2_value: pygame.surface.Surface = menu_font.get_font(25).render('100', True, "#EEEEEE")
    rect_chip_j2_value: pygame.rect.Rect = text_chip_j2_value.get_rect(center = (1280 / 2 - 225, 75))
    
    # table
    table: pygame.surface.Surface = pygame.image.load("jeu/assets/images/poker_table.jpg")
    rect_table: pygame.rect.Rect = table.get_rect(center = (1280 / 2, 720 / 2))
    
    # check button

    check_button = Button(
        screen=screen,
        image=pygame.image.load("jeu/assets/images/Play Rect.png"),
        position=(1280 - 82, 720 / 2 - 90),
        text="Check",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = lambda: print("Check"),
        enforced_size = (120, 35)
    )
    
    bet_button = Button(
        screen=screen,
        image=pygame.image.load("jeu/assets/images/Play Rect.png"),
        position=(1280 - 83, 720 / 2 - 30),
        text="Bet",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = lambda: print("Bet"),
        enforced_size = (120, 35)
    )
    
    all_in_button = Button(
        screen=screen,
        image=pygame.image.load("jeu/assets/images/Play Rect.png"),
        position=(1280 - 83, 720 / 2 + 30),
        text="All In",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = lambda: print("All In"),
        enforced_size = (120, 35)
    )
    
    pass_button = Button(
        screen=screen,
        image=pygame.image.load("jeu/assets/images/Play Rect.png"),
        position=(1280 - 83, 720 / 2 + 90),
        text="Pass",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = lambda: print("Pass"),
        enforced_size = (120, 35)
    )

    menu_buttons: tuple[UI, ...] = (check_button, bet_button, all_in_button, pass_button)
    
    while True:
        screen.blit(background, (0, 0))
        
        screen.blit(table, rect_table)
        screen.blit(board_flop_1, rect_board_flop_1)
        screen.blit(board_flop_2, rect_board_flop_2)
        screen.blit(board_flop_3, rect_board_flop_3)
        screen.blit(board_turn, rect_board_turn)
        screen.blit(board_river, rect_board_river)
        screen.blit(board_chip, rect_board_chip)
        screen.blit(text_chip_value, rect_chip_value)
        screen.blit(text_current_blind, rect_current_blind)
        screen.blit(text_current_blind_value, rect_current_blind_value)
        
        screen.blit(text_player_1, rect_player_1)
        screen.blit(card_j1_1, rect_card_j1_1)
        screen.blit(card_j1_2, rect_card_j1_2)
        screen.blit(dealer_token_1, rect_dealer_token_1)
        screen.blit(chip_j1, rect_chip_j1)
        screen.blit(text_chip_j1_value, rect_chip_j1_value)

        screen.blit(text_player_2, rect_player_2)
        screen.blit(card_j2_1, rect_card_j2_1)
        screen.blit(card_j2_2, rect_card_j2_2)
        screen.blit(dealer_token_2, rect_dealer_token_2)
        screen.blit(chip_j2, rect_chip_j2)
        screen.blit(text_chip_j2_value, rect_chip_j2_value)

        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT: quit()
        
            for button in menu_buttons: button.update(event)
        for button in menu_buttons: button.update_render()
        
        pygame.display.update()
        
if __name__ == "__main__":

    pygame.init()

    screen: pygame.surface.Surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE | pygame.SCALED)
    
    poker_table(screen)