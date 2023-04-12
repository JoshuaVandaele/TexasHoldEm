# <========== import ==========>

from __future__ import annotations
from random import randint, choice

from Hand import Hand
from Board import Board
from Dealer import Dealer
from Player import Player
from Card import Card
from Bankroll import Bankroll
from IA_Proba import *


class IA(Player):

    def __init__(self: Player, hand: Hand | None = None, bankroll: int = 100) -> None:
        super().__init__("IA", hand, bankroll)

    # <----- getter ----->

    @property
    def name(self: IA) -> str: return super().name

    @property
    def bankroll(self: IA) -> Bankroll: return super().bankroll

    @property
    def bet(self: IA) -> int: return super().bet

    @property
    def hand(self: IA) -> Hand: return super().hand

    @property
    def action(self: IA) -> str: return super().action

    # <----- setter ----->

    @name.setter
    def name(
        self: IA, new_name: str) -> None: object.__getattribute__(self, '_find')(new_name)

    @bankroll.setter
    def bankroll(self: IA, new_bankroll: Bankroll | int) -> None:
        if isinstance(new_bankroll, int):
            object.__getattribute__(self, '_find')(Bankroll(new_bankroll))
        else:
            object.__getattribute__(self, '_find')(new_bankroll)

    @bet.setter
    def bet(self: IA, new_bet: int) -> None: object.__getattribute__(self,
                                                                     '_find')(new_bet)

    @hand.setter
    def hand(
        self: IA, new_hand: Hand) -> None: object.__getattribute__(self, '_find')(new_hand)

    @action.setter
    def action(
        self: IA, new_action: str) -> None: object.__getattribute__(self, '_find')(new_action)

    # <----- IA decision ----->

    def generate_bet_value(self: IA, current_bet: int) -> int:
        if current_bet >= self.bankroll.bankroll:
            return self.bankroll.bankroll
        return randint(current_bet, self.bankroll.bankroll)

    def decision(self: IA, board: list[Card], phase: int, current_dealer: bool, total_blind: int, blind: int, can_check: bool = False) -> tuple[str, int]:
        """Return the action for the IA

        Args:
            hand (list[Card]): Hand of the IA
            board (list[Card]): Board on the field
            phase (int): Phase of the round
            current_dealer (int): If the IA is the current dealer

        Returns:
            tuple[str, int] : (Action, Value)
        """
        proba_out: float = get_proba_out(self.__hand.cards, board, phase)
        hand_power: int = get_hand_power(self.__hand.cards, board)
        pot_odds: float = get_pot_odds(total_blind, blind)

        tuple_choice: tuple[str, int] = ('fold', 0)

        # if royal flush
        if hand_power == 10:
            if current_dealer:
                tuple_choice = ('raise', self.generate_bet_value(blind))
            else:
                tuple_choice = choice(
                    [('call', 0), ('raise', self.generate_bet_value(blind))])

        elif proba_out >= 50:
            if current_dealer:
                tuple_choice = ('check', self.generate_bet_value(blind))
            else:
                if can_check:
                    tuple_choice = choice(
                        [('check', 0), ('raise', self.generate_bet_value(blind))])
                else:
                    tuple_choice = choice(
                        [('call', 0), ('raise', self.generate_bet_value(blind))])

        elif proba_out >= 25:
            if can_check:
                tuple_choice = ('check', 0)
            elif hand_power >= 5:
                tuple_choice = ('call', 0)

        self.action = tuple_choice[0]
        return tuple_choice


if __name__ == "__main__":

    dealer: Dealer = Dealer([Player('IA')], 10)
    dealer.distribute(True)

    print(dealer.board)
    print(dealer.players[0].hand)
