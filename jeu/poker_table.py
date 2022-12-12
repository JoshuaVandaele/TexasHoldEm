import pygame
from jeu.ui.button import Button
from jeu.ui.ui import UI
from jeu.utils.font_manager import FontManager

from jeu.utils.assets_import import resource_path
from jeu.ui.popup import Popup
from jeu.ui.int_textbox import Int_Textbox

from jeu.engine.Dealer import Dealer
from jeu.engine.Card import Card
from jeu.engine.Deck import Deck
from jeu.engine.Player import Player
from jeu.engine.Board import Board
from jeu.engine.Hand import Hand

current_dealer: int = 0
current_player: int = 0

list_players: list[Player] = []
list_players_font: list[pygame.surface.Surface] = []
list_players_hand: list[list[pygame.surface.Surface]] = []

def next_dealer() -> None:
    global current_dealer
    global list_players
    
    current_dealer += 1
    if current_dealer == len(list_players): current_dealer = 0
    
def next_player() -> None:
    global current_player
    global list_players
    
    current_player += 1
    if current_player == len(list_players): current_player = 0

def who_next_player() -> int:
    global current_player
    global list_players
    
    if current_player + 1 == len(list_players): return 0
    return current_player + 1
    
def poker_table(screen: pygame.surface.Surface, players_list: list[Player] | None = None, blind: int = 100 ) -> None:
    
    global current_dealer
    global current_player
    global list_players
    global list_players_font
    global list_players_hand
    
    # <===== BACKGROUND =====>
    
    pygame.display.set_caption("Texas Hold'Em")
    menu_font: FontManager = FontManager("jeu/assets/fonts/Truculenta.ttf")
    background: pygame.surface.Surface = pygame.image.load("jeu/assets/images/backgound_poker.jpeg")
    
    h: Hand = Hand([Card(2, 'spade'), Card(2, 'heart')])
    h2: Hand = Hand([Card(3, 'diamond'), Card(3, 'club')])
    
    if players_list == None: list_players = [Player('USERNAME00',0 , h, blind), Player('USERNAME01',1 , h2, blind)]
    else: players_list = [Player('USERNAME00',0 , h, blind), Player('USERNAME01',1 , h2, blind)]
    
    board: Board = Board([Card(1, 'spade'), Card(13, 'spade'), Card(12, 'spade'), Card(11, 'spade'), Card(10, 'spade')])
    
    dealer: Dealer = Dealer(Deck(), list_players, board)

    list_players_font = [menu_font.get_font(50).render(player.name, True, "#EEEEEE") for player in list_players]
    list_players_hand = [[pygame.image.load(f"jeu/assets/images/card/{player.hand.cards[0].suit}/{player.hand.cards[0].value}.png"),pygame.image.load(f"jeu/assets/images/card/{player.hand.cards[1].suit}/{player.hand.cards[1].value}.png")] for player in dealer.players]
    
    
    # < ===== BOARD =====>
    
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
    
    # <===== BOARD CHIP =====>
    
    board_chip: pygame.surface.Surface = pygame.image.load("jeu/assets/images/chip.png")
    rect_board_chip: pygame.rect.Rect = board_chip.get_rect(center = (1280 / 2 + 350, 720 / 2))
    
    text_current_blind: pygame.surface.Surface = menu_font.get_font(25).render('Current Blind:', True, "#EEEEEE")
    rect_current_blind: pygame.rect.Rect = text_current_blind.get_rect(center = (1280 / 2 + 350, 720 / 2 + 75))
    
    # <===== PLAYERS_TOKEN RECT LIST =====>
    
    players_token_rect: list[tuple[pygame.surface.Surface, pygame.rect.Rect]] = []
    
    # <===== PLAYER 1 =====>
    
    text_j1: pygame.surface.Surface = list_players_font[current_player]
    rect_j1: pygame.rect.Rect = text_j1.get_rect(center = (1280 - 1105, 720 - 45))
    
    rect_card_j1_1: pygame.rect.Rect = list_players_hand[current_player][0].get_rect(center = (1280 / 2 - 75, 720 - 65))
    rect_card_j1_2: pygame.rect.Rect = list_players_hand[current_player][1].get_rect(center = (1280 / 2 + 75, 720 - 65))
    
    dealer_token_j1: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Dealer_Token.png")
    rect_j1_dealer: pygame.rect.Rect = dealer_token_j1.get_rect(center = (1280 / 2 - 225, 720 - 75))
    
    bankroll_j1: pygame.surface.Surface = pygame.image.load("jeu/assets/images/chip.png")
    rect_bankroll_j1: pygame.rect.Rect = bankroll_j1.get_rect(center = (1280 / 2 + 225, 720 - 75))
    
    
    players_token_rect.append((dealer_token_j1, rect_j1_dealer))
    
    # <===== PLAYER 2 =====>
    
    text_j2: pygame.surface.Surface = list_players_font[who_next_player()]
    rect_j2: pygame.rect.Rect = text_j2.get_rect(center = (1280 - 175, 720 - 675))
    
    card_j2_1: pygame.surface.Surface = pygame.image.load("jeu/assets/images/card/card_back.png")
    rect_card_j2_1: pygame.rect.Rect = card_j2_1.get_rect(center = (1280 / 2 - 75, 65))
    card_j2_2: pygame.surface.Surface = pygame.image.load("jeu/assets/images/card/card_back.png")
    rect_card_j2_2: pygame.rect.Rect = card_j2_2.get_rect(center = (1280 / 2 + 75, 65))
    
    dealer_token_2: pygame.surface.Surface = pygame.image.load("jeu/assets/images/Dealer_Token.png")
    rect_j2_token: pygame.rect.Rect = dealer_token_2.get_rect(center = (1280 / 2 + 225, 75))
    
    bankroll_j2: pygame.surface.Surface = pygame.image.load("jeu/assets/images/chip.png")
    rect_bankroll_j2: pygame.rect.Rect = bankroll_j2.get_rect(center = (1280 / 2 - 225, 75))
    
    players_token_rect.append((dealer_token_2, rect_j2_token))
    
    # <===== Table =====>
    
    table: pygame.surface.Surface = pygame.image.load("jeu/assets/images/poker_table.jpg")
    rect_table: pygame.rect.Rect = table.get_rect(center = (1280 / 2, 720 / 2))
    
    # <===== Bet Popup =====>
    
    bet_font: FontManager = FontManager(resource_path("jeu/assets/fonts/Truculenta.ttf"))
    bet_popup: Popup = Popup(screen, "Bet", (screen.get_width() * 0.4, screen.get_height() * 0.4), "#0575BB")
    
    bet_textbox = Int_Textbox(
        screen = bet_popup.surface,
        position = (bet_popup.surface.get_size()[0]//2, 225 / 1.5 + 10),
        placeholder_text = "Bet Value",
        font = bet_font.get_font(75),
        size = (370, 100)
    )
    
    def bet_handler() -> None:
        global list_players
        global text_chip_value
        global rect_chip_value
        
        if bet_textbox.text != None and int(bet_textbox.text) <= list_players[current_player].bankroll.bankroll and int(bet_textbox.text) >= dealer.blind:
            list_players[current_player].bankroll.bankroll -= int(bet_textbox.text)
            dealer.blind = int(bet_textbox.text)
            dealer.total_blind += int(bet_textbox.text) 
            bet_textbox.text = ''
            text_chip_value = menu_font.get_font(25).render(str(dealer.total_blind), True, "#EEEEEE")
            rect_chip_value = text_chip_value.get_rect(center = (1280 / 2 + 350, 720 / 2))
            
            bet_popup.active = False
    
            swap_player()
            
    done_button = Button(
        screen = bet_popup.surface,
        image = pygame.image.load("jeu/assets/images/Play Rect.png"),
        position = (bet_popup.surface.get_size()[0] // 2, bet_popup.surface.get_size()[1] // 2 + 100),
        text = "Done",
        font = bet_font.get_font(30),
        color = "#000000",
        hover_color = "#555555",
        action = bet_handler,
        enforced_size = (120, 35)
    )
            
    bet_popup.add_ui_element(bet_textbox)
    bet_popup.add_ui_element(done_button)
    
    # <===== SWAP BUTTON =====>
    
    def swap_player() -> None:
        next_dealer()
        next_player()
    
    # <===== CHECK BUTTON =====>
    
    check_button = Button(
        screen=screen,
        image=pygame.image.load("jeu/assets/images/Play Rect.png"),
        position=(1280 - 82, 720 / 2 - 90),
        text="Check",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = next_dealer,
        enforced_size = (120, 35)
    )
    
    # <===== BET BUTTON =====>
    
    bet_button = Button(
        screen=screen,
        image=pygame.image.load("jeu/assets/images/Play Rect.png"),
        position=(1280 - 83, 720 / 2 - 30),
        text="Bet",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = lambda: bet_popup.run(),
        enforced_size = (120, 35)
    )
    
    # <===== All IN BUTTON =====>
    
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
    
    # <===== PASS BUTTON =====>
    
    pass_button = Button(
        screen=screen,
        image=pygame.image.load("jeu/assets/images/Play Rect.png"),
        position=(1280 - 83, 720 / 2 + 90),
        text="Pass",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = swap_player,
        enforced_size = (120, 35)
    )
    
    # <===== MENU BETTONS =====>
    
    menu_buttons: tuple[UI, ...] = (check_button, bet_button, all_in_button, pass_button)
    
    # <===== WHILE =====>
    
    while True:
        screen.blit(background, (0, 0))
        
        screen.blit(table, rect_table)
        
        screen.blit(board_flop_1, rect_board_flop_1)
        screen.blit(board_flop_2, rect_board_flop_2)
        screen.blit(board_flop_3, rect_board_flop_3)
        screen.blit(board_turn, rect_board_turn)
        screen.blit(board_river, rect_board_river)
        
        screen.blit(board_chip, rect_board_chip)
        screen.blit(menu_font.get_font(25).render(str(dealer.total_blind), True, "#EEEEEE"), menu_font.get_font(25).render(str(dealer.total_blind), True, "#EEEEEE").get_rect(center = (1280 / 2 + 350, 720 / 2)))
        screen.blit(text_current_blind, rect_current_blind)
        screen.blit(menu_font.get_font(25).render(str(dealer.blind), True, "#EEEEEE"), menu_font.get_font(25).render(str(dealer.blind), True, "#EEEEEE").get_rect(center = (1280 / 2 + 350, 720 / 2 + 110)))
        
        screen.blit(bankroll_j1, rect_bankroll_j1)
        screen.blit(card_j2_1, rect_card_j2_1)
        screen.blit(card_j2_2, rect_card_j2_2)
        screen.blit(bankroll_j2, rect_bankroll_j2)
        
        screen.blit(list_players_hand[current_player][0], rect_card_j1_1)
        screen.blit(list_players_hand[current_player][1], rect_card_j1_2)
        
        screen.blit(players_token_rect[current_dealer][0], players_token_rect[current_dealer][1])
        
        screen.blit(list_players_font[current_player], rect_j1)
        screen.blit(list_players_font[who_next_player()], rect_j2)
        
        screen.blit(menu_font.get_font(25).render(str(list_players[current_player].bankroll.bankroll), True, "#EEEEEE"), menu_font.get_font(25).render(str(list_players[current_player].bankroll.bankroll), True, "#EEEEEE").get_rect(center = (1280 / 2 + 225, 720 - 75)))
        screen.blit(menu_font.get_font(25).render(str(list_players[who_next_player()].bankroll.bankroll), True, "#EEEEEE"), menu_font.get_font(25).render(str(list_players[who_next_player()].bankroll.bankroll), True, "#EEEEEE").get_rect(center = (1280 / 2 - 225, 75)))
        
        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT: quit()
        
            for button in menu_buttons: button.update(event)  # type: ignore
        for button in menu_buttons: button.update_render()
        
        pygame.display.update()