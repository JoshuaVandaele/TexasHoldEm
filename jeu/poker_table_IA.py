# <========== Import ==========>

import pygame
import sys

# <========== Local Import ==========>
from jeu.ui.button import Button
from jeu.ui.ui import UI
from jeu.utils.font_manager import FontManager

from jeu.utils.assets_import import resource_path
from jeu.ui.popup import Popup
from jeu.ui.int_textbox import Int_Textbox

from jeu.engine.Dealer import Dealer
from jeu.engine.Card import Card
from jeu.engine.Player import Player
from jeu.engine.IA import IA
from jeu.engine.Hand import Hand

# <========== Global Variables ==========>

current_dealer: int = 0
current_phase: int = 0

# <========== Quit ==========>


def quit():
    """Quits the program
    """
    pygame.quit()
    sys.exit()

# <========== Next Dealer ===========>


def next_dealer(nbr_players: int) -> None:
    """Set the next dealer
    """
    global current_dealer

    current_dealer = (current_dealer + 1) % nbr_players

# <========== who next dealer ==========>


def who_next_dealer(nbr_players: int) -> int:
    """Return the index of the next dealer

    Returns:
        int: index of the next dealer
    """
    global current_dealer

    return (current_dealer + 1) % nbr_players

# <========== poker_table_IA ===========>


def poker_table_IA(screen: pygame.surface.Surface, player_name: str, bankroll: int = 1000, big_blind: int = 100) -> None:

    # global variables
    global current_dealer
    global current_phase

    # local varaibles
    game_loop: bool = True
    to_display: list[tuple[pygame.surface.Surface,
                           tuple[int, int] | pygame.rect.Rect]] = []

    # setup the dealer class
    dealer = Dealer([Player(player_name, bankroll=bankroll),
                    IA(bankroll=bankroll)], big_blind)
    dealer.distribute(shuffle=True)

    # <----- Background ----->

    pygame.display.set_caption("Texas Hold'Em")
    menu_font: FontManager = FontManager(
        resource_path("jeu/assets/fonts/Truculenta.ttf"))

    # add background to display
    to_display.append((pygame.image.load(
        resource_path("jeu/assets/images/backgound_poker.jpeg")), (int(0), int(0))))

    # <----- Table On Field ----->

    to_display.append((table := pygame.image.load(
        resource_path("jeu/assets/images/poker_table.jpg")),
        table.get_rect(center=(1280 / 2, 720 / 2))
    ))

    # <----- Cards On Field ----->

    list_board_card: list[pygame.surface.Surface] = [pygame.image.load(resource_path(
        "jeu/assets/images/card/card_back.png"))] * 5
    list_players_font: list[pygame.surface.Surface] = [menu_font.get_font(50).render(
        player.name, True, "#EEEEEE") for player in dealer.players]

    # setup the big and small blind
    dealer.players[current_dealer].bankroll.bankroll -= int(big_blind / 2)
    dealer.players[who_next_dealer(
        len(dealer.players))].bankroll.bankroll -= big_blind

    list_players_hand = [[pygame.image.load(resource_path(f"jeu/assets/images/card/{player.hand.cards[0].suit}/{player.hand.cards[0].value}.png")), pygame.image.load(
        resource_path(f"jeu/assets/images/card/{player.hand.cards[1].suit}/{player.hand.cards[1].value}.png"))] for player in dealer.players]

    # <----- REVEAL FLOP - --- ->

    def reveal_flop() -> None:
        """Reveal the flop (the first three cards) on the board
        change the png of back card by the value in the list_board_card
        """
        for i in range(3):
            list_board_card[i] = pygame.image.load(resource_path(
                f"jeu/assets/images/card/{dealer.board.cards[i].suit}/{dealer.board.cards[i].value}.png"))

    # <----- REVEAL TURN ----->

    def reveal_turn() -> None:
        """Reveal the turn (the fourth) on the board
        change the png of back card by the value in the list_board_card
        """
        list_board_card[3] = pygame.image.load(resource_path(
            f"jeu/assets/images/card/{dealer.board.cards[3].suit}/{dealer.board.cards[3].value}.png"))

    # <----- REVEAL RIVER ----->

    def reveal_river() -> None:
        """Reveal the river (the last) on the board
        change the png of back card by the value in the list_board_card
        """
        list_board_card[4] = pygame.image.load(resource_path(
            f"jeu/assets/images/card/{dealer.board.cards[4].suit}/{dealer.board.cards[4].value}.png"))

    # <----- Board Chip ----->

    # setup the chip png
    to_display.append((board_chip := pygame.image.load(
        resource_path("jeu/assets/images/chip.png")),
        board_chip.get_rect(center=(1280 / 2 + 350, 720 / 2)))

    )

    # setup the text for the current blind
    to_display.append((text_current_blind := menu_font.get_font(
        25).render('Current Blind:', True, "#EEEEEE"),
        text_current_blind.get_rect(
        center=(1280 / 2 + 350, 720 / 2 + 75))))

    # <----- Raise Popup ----->

    # setup the popup
    bet_font: FontManager = FontManager(
        resource_path("jeu/assets/fonts/Truculenta.ttf"))
    bet_popup: Popup = Popup(
        screen, "Raise", (screen.get_width() * 0.4, screen.get_height() * 0.4), "#0575BB")

    # setup the textbox
    bet_textbox = Int_Textbox(
        screen=bet_popup.surface,
        position=(bet_popup.surface.get_size()[0]//2, 225 / 1.5 + 10),
        placeholder_text="Raise Value",
        font=bet_font.get_font(75),
        size=(370, 100)
    )

    # <----- bet_handler ----->

    def bet_handler() -> None:
        """check the value in the textbox and if
        the value is valid, set the player bankroll and dealer total blind for raise
        """

        # check value in textbox
        if bet_textbox.text != '':
            if bet_textbox.text != None and int(bet_textbox.text) <= dealer.players[0].bankroll.bankroll:
                if (int(bet_textbox.text) >= dealer.blind * 2):

                    # set the player bankroll and bet
                    dealer.players[0].bankroll.bankroll -= int(
                        bet_textbox.text)
                    dealer.players[0].bet += int(bet_textbox.text)

                    # set the dealer current and total blind
                    dealer.blind = int(bet_textbox.text)
                    dealer.total_blind += int(bet_textbox.text)
                    dealer.players[0].action = 'raise'

                    # disable the popup
                    bet_popup.active = False

        # reset the textbox value
        bet_textbox.text = ''

    # <----- check handler ----->

    def check_handler() -> None:
        """Set the current player action to check if condition is valid
        """
        # check condition
        if dealer.players[1].action == 'check' or dealer.players[1].action == '':
            # set the current player action
            dealer.players[0].action = 'check'

    # <----- done button ----->

    # setup the done button
    done_button = Button(
        screen=bet_popup.surface,
        image=pygame.image.load(resource_path("jeu/assets/images/Action.png")),
        position=(bet_popup.surface.get_size()[
                  0] // 2, bet_popup.surface.get_size()[1] // 2 + 100),
        text="Done",
        font=bet_font.get_font(30),
        color="#000000",
        hover_color="#555555",
        action=bet_handler,
        enforced_size=(120, 35)
    )

    # add the button to ui
    bet_popup.add_ui_element(bet_textbox)
    bet_popup.add_ui_element(done_button)

    # <----- PASS HANDLER ----->

    def fold_handler() -> None:
        """Set the current player action to fold
        """
        dealer.players[0].action = 'fold'

    # <----- CALL HANDLER ----->

    def call_handler() -> None:
        """Set the current player action to call if condition is valid
        """
        # calculate the blind value for call
        blind: int = dealer.players[1].bet - dealer.players[0].bet

        # if blind is positive
        if blind > 0:

            dealer.players[0].action = 'call'
            dealer.total_blind += blind

            dealer.players[0].bet = dealer.players[1].bet
            dealer.players[0].bankroll.bankroll -= blind

        elif blind != 0:
            dealer.players[0].action = 'call'
            dealer.total_blind += dealer.players[0].bankroll.bankroll

            dealer.players[0].bet = dealer.players[0].bankroll.bankroll
            dealer.players[0].bankroll.bankroll -= dealer.players[0].bankroll.bankroll
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
        for player in dealer.players:
            player.bankroll.bankroll += give_value

        # if value is odd
        give_value = dealer.total_blind % len(list_winner)
        dealer.players[1].bankroll.bankroll += give_value
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
        action=check_handler,
        enforced_size=(120, 35)
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
        action=lambda: bet_popup.run(),
        enforced_size=(120, 35)
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
        action=call_handler,
        enforced_size=(120, 35)
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
        action=fold_handler,
        enforced_size=(120, 35)
    )

    # <----- CHECK STEP ONE ----->

    def check_step() -> None:
        """Check if the step was ending or not for reveal card or decide who is the round winner
        """
        global current_phase

        # if player fold
        if dealer.players[1].action == 'fold':

            give_bankroll(0)

            for player in dealer.players:
                player.action = ""
            current_phase = 5

        # if player's check
        elif dealer.players[1].action == 'check' and dealer.players[0].action == 'check':

            if current_phase == 1:
                current_phase += 1
                reveal_flop()

            elif current_phase == 2:
                current_phase += 1
                reveal_turn()

            elif current_phase == 3:
                current_phase += 1
                reveal_river()

            elif current_phase == 4:
                current_phase += 1

                winner: int = (dealer.compare_hand(
                    0, 1) + 1) % len(dealer.players)
                if winner == -1:
                    split([i for i in range(len(dealer.players))])
                else:
                    give_bankroll((dealer.compare_hand(
                        0, 1) + 1) % len(dealer.players))

            for player in dealer.players:
                player.action = ""

        # if the forward player check
        elif dealer.players[0].action == 'check':

            # if the current player call
            if dealer.players[1].action == 'call':

                for player in dealer.players:
                    player.action = ""

                if current_phase == 1:
                    current_phase += 1
                    reveal_flop()

                elif current_phase == 2:
                    current_phase += 1
                    reveal_turn()

                elif current_phase == 3:
                    current_phase += 1
                    reveal_river()

                elif current_phase == 4:
                    current_phase += 1

                    winner: int = (dealer.compare_hand(
                        0, 1) + 1) % len(dealer.players)
                    if winner == -1:
                        split([i for i in range(len(dealer.players))])
                    else:
                        give_bankroll((dealer.compare_hand(
                            0, 1) + 1) % len(dealer.players))

        # if the forward player call and the current player raise
        elif dealer.players[1].action == 'call' and dealer.players[1].action == 'raise':
            for player in dealer.players:
                player.action = ""

            if dealer.players[1].bankroll.bankroll == 0 or dealer.players[0].bankroll.bankroll == 0:

                current_phase = 5

                winner: int = (dealer.compare_hand(
                    0, 1) + 1) % len(dealer.players)
                if winner == -1:
                    split([i for i in range(len(dealer.players))])
                else:
                    give_bankroll((dealer.compare_hand(
                        0, 1) + 1) % len(dealer.players))

            else:

                if current_phase == 1:
                    current_phase += 1
                    reveal_flop()

                elif current_phase == 2:
                    current_phase += 1
                    reveal_turn()

                elif current_phase == 3:
                    current_phase += 1
                    reveal_river()

                elif current_phase == 4:
                    current_phase += 1

                    winner: int = (dealer.compare_hand(
                        0, 1) + 1) % len(dealer.players)
                    if winner == -1:
                        split([i for i in range(len(dealer.players))])
                    else:
                        give_bankroll((dealer.compare_hand(
                            0, 1) + 1) % len(dealer.players))

        # if one of player have a empty bankroll
        if dealer.players[1].action == 'raise' and dealer.players[1].bankroll.bankroll == 0:
            reveal_flop()
            reveal_river()
            reveal_turn()

            current_phase = 5

            winner: int = (dealer.compare_hand(
                0, 1) + 1) % len(dealer.players)
            if winner == -1:
                split([i for i in range(len(dealer.players))])
            else:
                give_bankroll((dealer.compare_hand(
                    0, 1) + 1) % len(dealer.players))

    menu_buttons: tuple[UI, ...] = (
        check_button, bet_button, call_button, fold_button)

    to_display.append((player_name_surface := list_players_font[0],
                       player_name_surface.get_rect(center=(1280 - 1105, 720 - 45))))

    to_display.append((bankroll_j1 := pygame.image.load(
        resource_path("jeu/assets/images/chip.png")),
        bankroll_j1.get_rect(center=(1280 / 2 + 225, 720 - 75))))

    to_display.append((bankroll_j2 := pygame.image.load(
        resource_path("jeu/assets/images/chip.png")),
        bankroll_j2.get_rect(center=(1280 / 2 - 225, 75))))

    to_display.append((text_j2 := list_players_font[1],
                       text_j2.get_rect(center=(1280 - 175, 720 - 675))))

    while game_loop:

        # display all element
        for display in to_display:
            screen.blit(display[0], display[1])

        # display the dealer token
        if current_dealer == 0:
            screen.blit(dealer_token_j1 := pygame.image.load(
                resource_path("jeu/assets/images/Dealer_Token.png")),
                dealer_token_j1.get_rect(center=(1280 / 2 - 225, 720 - 75)))
        else:
            screen.blit(dealer_token_j1 := pygame.image.load(
                resource_path("jeu/assets/images/Dealer_Token.png")),
                dealer_token_j1.get_rect(center=(1280 / 2 + 225, 75)))

        # display cards on the table
        screen.blit(list_board_card[0], list_board_card[0].get_rect(
            center=(1280 / 2 - 200, 720 / 2 - 100)))
        screen.blit(list_board_card[1], list_board_card[1].get_rect(
            center=(1280 / 2, 720 / 2 - 100)))
        screen.blit(list_board_card[2], list_board_card[2].get_rect(
            center=(1280 / 2 + 200, 720 / 2 - 100)))
        screen.blit(list_board_card[3], list_board_card[3].get_rect(
            center=(1280 / 2 - 100, 720 / 2 + 100)))
        screen.blit(list_board_card[4], list_board_card[4].get_rect(
            center=(1280 / 2 + 100, 720 / 2 + 100)))

        # display player cards
        screen.blit(card_1 := pygame.image.load(resource_path(f"jeu/assets/images/card/{dealer.players[0].hand.cards[0].suit}/{dealer.players[0].hand.cards[0].value}.png")),
                    card_1.get_rect(center=(1280 / 2 - 75, 720 - 65)))
        screen.blit(card_2 := pygame.image.load(resource_path(f"jeu/assets/images/card/{dealer.players[0].hand.cards[1].suit}/{dealer.players[0].hand.cards[1].value}.png")),
                    card_2.get_rect(center=(1280 / 2 + 75, 720 - 65)))

        # display AI cards
        screen.blit(card_IA := pygame.image.load(resource_path("jeu/assets/images/card/card_back.png")),
                    card_IA.get_rect(center=(1280 / 2 + 75, 65)))
        screen.blit(card_IA,
                    card_IA.get_rect(center=(1280 / 2 - 75, 65)))

        # display the bankroll value
        screen.blit(menu_font.get_font(25).render(str(dealer.total_blind), True, "#EEEEEE"), menu_font.get_font(
            25).render(str(dealer.total_blind), True, "#EEEEEE").get_rect(center=(1280 / 2 + 350, 720 / 2)))
        screen.blit(text_current_blind,
                    text_current_blind.get_rect(
                        center=(1280 / 2 + 350, 720 / 2 + 75)))
        screen.blit(menu_font.get_font(25).render(str(dealer.blind), True, "#EEEEEE"), menu_font.get_font(
            25).render(str(dealer.blind), True, "#EEEEEE").get_rect(center=(1280 / 2 + 350, 720 / 2 + 110)))

        # display the player's bankroll
        screen.blit(menu_font.get_font(25).render(str(dealer.players[0].bankroll.bankroll), True, "#EEEEEE"), menu_font.get_font(
            25).render(str(dealer.players[0].bankroll.bankroll), True, "#EEEEEE").get_rect(center=(1280 / 2 + 225, 720 - 75)))
        screen.blit(menu_font.get_font(25).render(str(dealer.players[1].bankroll.bankroll), True, "#EEEEEE"), menu_font.get_font(
            25).render(str(dealer.players[1].bankroll.bankroll), True, "#EEEEEE").get_rect(center=(1280 / 2 - 225, 75)))

        # get event on the screen
        for event in pygame.event.get():
            match (event.type):
                case pygame.QUIT: quit()

            for button in menu_buttons:
                button.update(event)
        for button in menu_buttons:
            button.update_render()

        pygame.display.update()
