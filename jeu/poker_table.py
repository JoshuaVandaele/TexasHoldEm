# <========== import ==========>

import pygame
import sys
from jeu.ui.button import Button
from jeu.ui.ui import UI
from jeu.utils.font_manager import FontManager

from jeu.utils.assets_import import resource_path
from jeu.ui.popup import Popup
from jeu.ui.int_textbox import Int_Textbox

from jeu.engine.Dealer import Dealer
from jeu.engine.Card import Card
from jeu.engine.Player import Player
from jeu.engine.Hand import Hand


# <========== global variables ==========>

current_dealer: int = 0
current_player: int = 0

list_players: list[Player] = []
list_players_font: list[pygame.surface.Surface] = []
list_players_hand: list[list[pygame.surface.Surface]] = []
list_board_card: list[pygame.surface.Surface] = []

step_one: bool = True
step_two: bool = True
step_three: bool = True
step_four: bool = True
end_turn: bool = False
game_loop: bool = True

dealer: Dealer = Dealer([Player('init', Hand([Card(-1,'init')]), 0)], 0)

def quit():
    """Quits the program
    """
    pygame.quit()
    sys.exit()
        
# <========== next player ==========>
    
def next_player() -> None:
    """Set the next player
    """
    global current_player
    global list_players
    
    current_player = (current_player + 1) % len(list_players)
   
# <========== who next player ==========>

def who_next_player() -> int:
    """Return the index of the next player

    Returns:
        int: index of the next player
    """
    global current_player
    global list_players
    
    return (current_player + 1) % len(list_players)

# <========== next dealer ==========>
    
def next_dealer() -> None:
    """Set the next dealer
    """
    global current_dealer
    global list_players
    
    current_dealer = (current_dealer + 1) % len(list_players)
   
# <========== who next dealer ==========>

def who_next_dealer() -> int:
    """Return the index of the next dealer

    Returns:
        int: index of the next dealer
    """
    global current_dealer
    global list_players
    
    return (current_dealer + 1) % len(list_players)

# <========== poker table ==========>

def poker_table(screen: pygame.surface.Surface, players_list: list[str], bankroll: int = 1000, big_blind: int = 100) -> None:
    """Game screen, to play the game of Poker Texas Hold'em

    Args:
        screen (pygame.surface.Surface): Screen to display the game onto
        players_list (list[str]): List of player names
        bankroll (int, optional): The base value of bankroll for earch player. Defaults to 1000.
        big_blind (int, optional): The base value for big blind. Defaults to 100.
    """
    
    global current_dealer
    global current_player
    global list_players
    global list_players_font
    global list_players_hand
    global list_board_card
    global dealer
    global step_one
    global step_two
    global step_three
    global step_four
    global end_turn
    global game_loop


    # <----- BACKGROUND ----->

    pygame.display.set_caption("Texas Hold'Em")
    menu_font: FontManager = FontManager(resource_path("jeu/assets/fonts/Truculenta.ttf"))
    background: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/backgound_poker.jpeg"))

    # setup the dealer class
    dealer = Dealer([Player(player, Hand([Card(-1,'init'),Card(-1,'init')]), bankroll) for player in players_list], big_blind)
    dealer.distribute(shuffle = True)

    # setup the board card and player list
    list_board_card = [pygame.image.load(resource_path("jeu/assets/images/card/card_back.png"))] * 5
    list_players = list(dealer.players)
    list_players_font = [menu_font.get_font(50).render(player, True, "#EEEEEE") for player in players_list]
    list_players_hand = [[pygame.image.load(resource_path(f"jeu/assets/images/card/{player.hand.cards[0].suit}/{player.hand.cards[0].value}.png")),pygame.image.load(resource_path(f"jeu/assets/images/card/{player.hand.cards[1].suit}/{player.hand.cards[1].value}.png"))] for player in dealer.players]

    # setup the big and small blind
    list_players[current_dealer].bankroll.bankroll -= int(big_blind / 2)
    list_players[who_next_dealer()].bankroll.bankroll -= big_blind

    # <----- BOARD CHIP ----->

    # setup the chip png
    board_chip: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/chip.png"))
    rect_board_chip: pygame.rect.Rect = board_chip.get_rect(center = (1280 / 2 + 350, 720 / 2))

    # setup the text for the current blind
    text_current_blind: pygame.surface.Surface = menu_font.get_font(25).render('Current Blind:', True, "#EEEEEE")
    rect_current_blind: pygame.rect.Rect = text_current_blind.get_rect(center = (1280 / 2 + 350, 720 / 2 + 75))

    # <----- PLAYERS TOKEN RECT LIST ----->

    # setup the list of tuple[surface, rect]
    players_token_rect: list[tuple[pygame.surface.Surface, pygame.rect.Rect]] = []

    # <----- PLAYER 1 ----->

    # setup the current player name
    text_j1: pygame.surface.Surface = list_players_font[current_player]
    rect_j1: pygame.rect.Rect = text_j1.get_rect(center = (1280 - 1105, 720 - 45))

    # setup the current player hand
    rect_card_j1_1: pygame.rect.Rect = list_players_hand[current_player][0].get_rect(center = (1280 / 2 - 75, 720 - 65))
    rect_card_j1_2: pygame.rect.Rect = list_players_hand[current_player][1].get_rect(center = (1280 / 2 + 75, 720 - 65))

    # setup the current player dealer token
    dealer_token_j1: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/Dealer_Token.png"))
    rect_j1_dealer: pygame.rect.Rect = dealer_token_j1.get_rect(center = (1280 / 2 - 225, 720 - 75))

    # setup the current player bankroll
    bankroll_j1: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/chip.png"))
    rect_bankroll_j1: pygame.rect.Rect = bankroll_j1.get_rect(center = (1280 / 2 + 225, 720 - 75))

    # add the token to the list for display
    players_token_rect.append((dealer_token_j1, rect_j1_dealer))

    # <----- PLAYER 2 ----->

    # setup the next player name
    text_j2: pygame.surface.Surface = list_players_font[who_next_player()]
    rect_j2: pygame.rect.Rect = text_j2.get_rect(center = (1280 - 175, 720 - 675))

    # setup the next player hand
    card_j2_1: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/card/card_back.png"))
    rect_card_j2_1: pygame.rect.Rect = card_j2_1.get_rect(center = (1280 / 2 - 75, 65))
    card_j2_2: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/card/card_back.png"))
    rect_card_j2_2: pygame.rect.Rect = card_j2_2.get_rect(center = (1280 / 2 + 75, 65))

    # setup the next player dealer token
    dealer_token_2: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/Dealer_Token.png"))
    rect_j2_token: pygame.rect.Rect = dealer_token_2.get_rect(center = (1280 / 2 + 225, 75))

    # setup the next player bankroll
    bankroll_j2: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/chip.png"))
    rect_bankroll_j2: pygame.rect.Rect = bankroll_j2.get_rect(center = (1280 / 2 - 225, 75))

    # add the token to the list for display
    players_token_rect.append((dealer_token_2, rect_j2_token))

    # <-----  Table ----->

    # setup the poker table
    table: pygame.surface.Surface = pygame.image.load(resource_path("jeu/assets/images/poker_table.jpg"))
    rect_table: pygame.rect.Rect = table.get_rect(center = (1280 / 2, 720 / 2))

    # <----- REVEAL FLOP ----->

    def reveal_flop() -> None:
        """Reveal the flop (the first three cards) on the board
        change the png of back card by the value in the list_board_card
        """
        list_board_card[0] = pygame.image.load(resource_path(f"jeu/assets/images/card/{dealer.board.cards[0].suit}/{dealer.board.cards[0].value}.png"))
        list_board_card[1] = pygame.image.load(resource_path(f"jeu/assets/images/card/{dealer.board.cards[1].suit}/{dealer.board.cards[1].value}.png"))
        list_board_card[2] = pygame.image.load(resource_path(f"jeu/assets/images/card/{dealer.board.cards[2].suit}/{dealer.board.cards[2].value}.png"))

    # <----- REVEAL TURN ----->

    def reveal_turn() -> None:
        """Reveal the turn (the fourth) on the board
        change the png of back card by the value in the list_board_card
        """
        list_board_card[3] = pygame.image.load(resource_path(f"jeu/assets/images/card/{dealer.board.cards[3].suit}/{dealer.board.cards[3].value}.png"))

    # <----- REVEAL RIVER ----->

    def reveal_river() -> None:
        """Reveal the river (the last) on the board
        change the png of back card by the value in the list_board_card
        """
        list_board_card[4] = pygame.image.load(resource_path(f"jeu/assets/images/card/{dealer.board.cards[4].suit}/{dealer.board.cards[4].value}.png"))

    # <----- Raise Popup ----->

    # setup the popup
    bet_font: FontManager = FontManager(resource_path("jeu/assets/fonts/Truculenta.ttf"))
    bet_popup: Popup = Popup(screen, "Raise", (screen.get_width() * 0.4, screen.get_height() * 0.4), "#0575BB")

    # setup the textbox
    bet_textbox = Int_Textbox(
        screen = bet_popup.surface,
        position = (bet_popup.surface.get_size()[0]//2, 225 / 1.5 + 10),
        placeholder_text = "Raise Value",
        font = bet_font.get_font(75),
        size = (370, 100)
    )

    # <----- bet_handler ----->

    def bet_handler() -> None:
        """check the value in the textbox and if
        the value is valid, set the player bankroll and dealer total blind for raise
        """
        global list_players
        global text_chip_value
        global rect_chip_value
        global dealer

        # check value in textbox
        if (
            bet_textbox.text != ''
            and bet_textbox.text != None
            and int(bet_textbox.text)
            <= list_players[current_player].bankroll.bankroll
            and (int(bet_textbox.text) >= dealer.blind * 2)
        ):
            # set the player bankroll and bet 
            list_players[current_player].bankroll.bankroll -= int(bet_textbox.text)
            list_players[current_player].bet += int(bet_textbox.text)

            # set the dealer current and total blind
            dealer.blind = int(bet_textbox.text)
            dealer.total_blind += int(bet_textbox.text)
            dealer.players[current_player].action = 'raise'

            # disable the popup
            bet_popup.active = False

            # swap the current and next player
            swap_player()

        # reset the textbox value 
        bet_textbox.text = ''

    # <----- check handler -----> 

    def check_handler() -> None:
        """Set the current player action to check if condition is valid
        """
        # check condition
        if dealer.players[who_next_player()].action in ['check', '']:
            # set the current player action
            dealer.players[current_player].action = 'check'
            # swap the current and next player
            swap_player()

    # <----- done button ----->

    # setup the done button
    done_button = Button(
        screen = bet_popup.surface,
        image = pygame.image.load(resource_path("jeu/assets/images/Action.png")),
        position = (bet_popup.surface.get_size()[0] // 2, bet_popup.surface.get_size()[1] // 2 + 100),
        text = "Done",
        font = bet_font.get_font(30),
        color = "#000000",
        hover_color = "#555555",
        action = bet_handler,
        enforced_size = (120, 35)
    )

    # add the button to ui  
    bet_popup.add_ui_element(bet_textbox)
    bet_popup.add_ui_element(done_button)


    # <----- PASS HANDLER ----->

    def fold_handler() -> None:
        """Set the current player action to fold
        """
        dealer.players[current_player].action = 'fold'
        swap_player()

    # <----- CALL HANDLER ----->

    def call_handler() -> None:
        """Set the current player action to call if condition is valid
        """
        # calculate the blind value for call
        blind: int = list_players[who_next_player()].bet - list_players[current_player].bet

        # if blind is positive
        if blind > 0:

            dealer.players[current_player].action = 'call'
            dealer.total_blind += blind 

            list_players[current_player].bet = list_players[who_next_player()].bet
            list_players[current_player].bankroll.bankroll -= blind

            swap_player()

        elif blind != 0:
            dealer.players[current_player].action = 'call'
            dealer.total_blind += list_players[current_player].bankroll.bankroll

            list_players[current_player].bet = list_players[current_player].bankroll.bankroll
            list_players[current_player].bankroll.bankroll -= list_players[current_player].bankroll.bankroll

            swap_player()


    # <-----  SWAP BUTTON ----->

    def swap_player() -> None:
        """Swap the current and next player
        """
        next_dealer()
        next_player()

    # <----- give bankroll ----->

    def give_bankroll(winner: int) -> None:
        """give the dealer class bankroll to a player

        Args:
            winner (int): index of the winner round in the list
        """
        dealer.players[winner].bankroll.bankroll += dealer.total_blind
        dealer.total_blind = 0

    # <----- split ----->

    def split(list_winner: list[int]) -> None:
        """split the dealer class bankroll  to player's

        Args:
            list_winner (list[int]): list of player's index for split the bankroll
        """
        give_value: int = dealer.total_blind // len(list_winner)
        for player in dealer.players: player.bankroll.bankroll += give_value

        # if value is odd
        give_value = dealer.total_blind % len(list_winner)
        dealer.players[who_next_dealer()].bankroll.bankroll += give_value
        dealer.total_blind = 0

    # <----- CHECK BUTTON ----->

    # setup the check button
    check_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Action.png")),
        position=(1280 - 82, 720 / 2 - 90),
        text="Check",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = check_handler,
        enforced_size = (120, 35)
    )

    # <----- BET BUTTON ----->

    # setup the bet button
    bet_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Action.png")),
        position=(1280 - 83, 720 / 2 - 30),
        text="Raise",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = lambda: bet_popup.run(),
        enforced_size = (120, 35)
    )

    # <----- CALL BUTTON ----->

    # setup the call button
    call_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Action.png")),
        position=(1280 - 83, 720 / 2 + 30),
        text="Call",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = call_handler,
        enforced_size = (120, 35)
    )

    # <----- PASS BUTTON ----->

    # setup the pass button
    fold_button = Button(
        screen=screen,
        image=pygame.image.load(resource_path("jeu/assets/images/Action.png")),
        position=(1280 - 83, 720 / 2 + 90),
        text="Fold",
        font=menu_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action = fold_handler,
        enforced_size = (120, 35)
    )

    # <----- MENU BETTONS ----->

    # add button
    menu_buttons: tuple[UI, ...] = (check_button, bet_button, call_button, fold_button)

    # <----- CHECK STEP ONE ----->

    def check_step() -> None:
        """Check if the step was ending or not for reveal card or decide who is the round winner
        """
        global dealer
        global current_player
        global list_players
        global step_one
        global end_turn
        global step_one
        global step_two
        global step_three
        global step_four

        # if player fold
        if dealer.players[who_next_player()].action == 'fold':

            give_bankroll(current_player)

            for player in dealer.players: player.action = ""
            end_turn = True

        elif dealer.players[who_next_player()].action == 'check' and dealer.players[current_player].action == 'check':
            
            if step_one: 
                step_one = False
                reveal_flop()
                swap_player()

            elif step_two:
                step_two = False
                reveal_turn()

            elif step_three: 
                step_three = False
                reveal_river()

            elif step_four: 
                step_four = False
                end_turn = True

                winner: int = (dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players)
                if winner == -1:
                    split(list(range(len(dealer.players))))
                else: give_bankroll((dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players))


            for player in dealer.players: player.action = ""

        elif dealer.players[who_next_player()].action == 'check':
            
            # if the current player call
            if dealer.players[current_player].action == 'call':
                
                for player in dealer.players: player.action = ""

                if step_one: 
                    step_one = False
                    reveal_flop()
                    swap_player()

                elif step_two:
                    step_two = False
                    reveal_turn()

                elif step_three: 
                    step_three = False
                    reveal_river()

                elif step_four:
                    step_four = False
                    end_turn = True

                    winner: int = (dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players)
                    if winner == -1:
                        split(list(range(len(dealer.players))))
                    else: give_bankroll((dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players))

        elif dealer.players[who_next_player()].action == 'call' and dealer.players[current_player].action == 'raise':
            for player in dealer.players: player.action = ""

            if dealer.players[current_player].bankroll.bankroll == 0 or dealer.players[who_next_player()].bankroll.bankroll == 0:

                step_one = False
                step_two = False
                step_three = False
                step_four = False
                end_turn = True

                winner: int = (dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players)
                if winner == -1:
                    split(list(range(len(dealer.players))))
                else: give_bankroll((dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players))

            else:

                if step_one: 
                    step_one = False
                    reveal_flop()

                elif step_two:
                    step_two = False
                    reveal_turn()

                elif step_three: 
                    step_three = False
                    reveal_river()

                elif step_four:
                    step_four = False
                    end_turn = True

                    winner: int = (dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players)
                    if winner == -1:
                        split(list(range(len(dealer.players))))
                    else: give_bankroll((dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players))

        # if one of player have a empty bankroll
        if dealer.players[who_next_player()].action == 'raise' and dealer.players[current_player].bankroll.bankroll == 0:
            reveal_flop()
            reveal_river()
            reveal_turn()

            end_turn = True

            winner: int = (dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players)
            if winner == -1:
                split(list(range(len(dealer.players))))
            else: give_bankroll((dealer.compare_hand(current_player, who_next_player()) + 1) % len(dealer.players))


                

    # <----- WHILE ----->

    # game loop
    while game_loop:
        # display all element

        screen.blit(background, (0, 0))

        screen.blit(table, rect_table)

        screen.blit(list_board_card[0], list_board_card[0].get_rect(center = (1280 / 2, 720 /2 - 100)))
        screen.blit(list_board_card[1], list_board_card[1].get_rect(center = (1280 / 2 - 200, 720 /2 - 100)))
        screen.blit(list_board_card[2], list_board_card[2].get_rect(center = (1280 / 2 + 200, 720 /2 - 100)))
        screen.blit(list_board_card[3], list_board_card[3].get_rect(center = (1280 / 2 - 100, 720 /2 + 100)))
        screen.blit(list_board_card[4], list_board_card[4].get_rect(center = (1280 / 2 + 100, 720 /2 + 100)))

        screen.blit(board_chip, rect_board_chip)

        screen.blit(bankroll_j1, rect_bankroll_j1)
        screen.blit(card_j2_1, rect_card_j2_1)
        screen.blit(card_j2_2, rect_card_j2_2)
        screen.blit(bankroll_j2, rect_bankroll_j2)

        screen.blit(list_players_hand[current_player][0], rect_card_j1_1)
        screen.blit(list_players_hand[current_player][1], rect_card_j1_2)

        screen.blit(players_token_rect[current_dealer][0], players_token_rect[current_dealer][1])

        screen.blit(list_players_font[current_player], rect_j1)
        screen.blit(list_players_font[who_next_player()], rect_j2)

        # call check step
        check_step()

        # if is the end of turn
        if end_turn:

            # reset field and player's card's
            dealer.distribute(shuffle = True)
            list_players_hand = [[pygame.image.load(resource_path(f"jeu/assets/images/card/{player.hand.cards[0].suit}/{player.hand.cards[0].value}.png")),pygame.image.load(resource_path(f"jeu/assets/images/card/{player.hand.cards[1].suit}/{player.hand.cards[1].value}.png"))] for player in dealer.players]
            list_board_card = [pygame.image.load(resource_path("jeu/assets/images/card/card_back.png"))] * 5
            next_dealer()

            if current_dealer != current_dealer: swap_player()
            dealer.blind = 0

            # setup the blind            
            if list_players[current_dealer].bankroll.bankroll >= big_blind :
                dealer.total_blind += big_blind
                list_players[current_dealer].bankroll.bankroll -= big_blind
            else:
                dealer.total_blind += list_players[current_dealer].bankroll.bankroll
                list_players[current_dealer].bankroll.bankroll = 0 



            if list_players[who_next_dealer()].bankroll.bankroll >= big_blind // 2:
                dealer.total_blind += big_blind // 2
                list_players[who_next_dealer()].bankroll.bankroll -= big_blind // 2
            else:
                dealer.total_blind += list_players[who_next_dealer()].bankroll.bankroll
                list_players[who_next_dealer()].bankroll.bankroll = 0 

            # update the screen
            pygame.display.update()
        # display the bankroll value
        screen.blit(menu_font.get_font(25).render(str(dealer.total_blind), True, "#EEEEEE"), menu_font.get_font(25).render(str(dealer.total_blind), True, "#EEEEEE").get_rect(center = (1280 / 2 + 350, 720 / 2)))
        screen.blit(text_current_blind, rect_current_blind)
        screen.blit(menu_font.get_font(25).render(str(dealer.blind), True, "#EEEEEE"), menu_font.get_font(25).render(str(dealer.blind), True, "#EEEEEE").get_rect(center = (1280 / 2 + 350, 720 / 2 + 110)))
        # display the player's bankroll
        screen.blit(menu_font.get_font(25).render(str(list_players[current_player].bankroll.bankroll), True, "#EEEEEE"), menu_font.get_font(25).render(str(list_players[current_player].bankroll.bankroll), True, "#EEEEEE").get_rect(center = (1280 / 2 + 225, 720 - 75)))
        screen.blit(menu_font.get_font(25).render(str(list_players[who_next_player()].bankroll.bankroll), True, "#EEEEEE"), menu_font.get_font(25).render(str(list_players[who_next_player()].bankroll.bankroll), True, "#EEEEEE").get_rect(center = (1280 / 2 - 225, 75)))   

        # if end of the round   
        if end_turn:

            # reset the value of step checker
            step_one = True
            step_two = True
            step_three = True
            step_four = True

            end_turn = False


            for player in dealer.players:

                # if player have empty bankroll
                if player.bankroll.bankroll <= 0:
                    # reset the end popup
                    end_popup = Popup(
                    screen=screen,
                    title="Game Over",
                    size=(1280//1.9, 720//1.5),
                    color="#0575BB"
                    )

                    end_label: pygame.surface.Surface = menu_font.get_font(75).render("Game Over", True, "white")
                    end_rect: pygame.rect.Rect = end_label.get_rect(center=(end_popup.surface.get_size()[0]//2, end_popup.surface.get_size()[1]//2*0.8))
                    end_popup.elements.pop(0)

                    def end_button_handler() -> None:
                        global game_loop

                        end_popup.active = False
                        game_loop = False


                    end_popup_quit = Button(
                    screen = end_popup.surface,
                    image=None,
                    position=(end_popup.surface.get_size()[0]//2, end_popup.surface.get_size()[1]//1.2),
                    text="QUIT",
                    font=menu_font.get_font(48),
                    color="white",
                    hover_color="black",
                    action = end_button_handler,
                    )

                    end_popup.add_ui_element(end_popup_quit)
                    end_popup.run()


        # get event on the screen
        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT: quit()

            for button in menu_buttons: button.update(event)  # type: ignore
        for button in menu_buttons: button.update_render()

        pygame.display.update()
    