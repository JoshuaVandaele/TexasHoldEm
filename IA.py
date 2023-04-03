# <========== import ==========>

from __future__ import annotations
from random import randint

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
    def name(self: IA, new_name: str) -> None: object.__getattribute__(self, '_find')(new_name)
    
    @bankroll.setter
    def bankroll(self: IA, new_bankroll: Bankroll | int) -> None:
        if isinstance(new_bankroll, int): object.__getattribute__(self, '_find')(Bankroll(new_bankroll))
        else: object.__getattribute__(self, '_find')(new_bankroll)
    
    @bet.setter
    def bet(self: IA, new_bet: int) -> None: object.__getattribute__(self, '_find')(new_bet)
    
    @hand.setter
    def hand(self: IA, new_hand: Hand) -> None: object.__getattribute__(self, '_find')(new_hand)   
    
    @action.setter
    def action(self: IA, new_action: str) -> None: object.__getattribute__(self, '_find')(new_action)
    
    # <----- IA decision ----->
    
    def generate_bet_value(self: IA) -> int:...
        
    def decision(self: IA, board: list[Card], phase: int, current_dealer: bool, total_blind: int, blind: int) -> tuple(str|int) | None:
        """Return the action for the IA

        Args:
            hand (list[Card]): Hand of the IA
            board (list[Card]): Board on the field
            phase (int): Phase of the round
            current_dealer (int): If the IA is the current dealer

        Returns:
            tuple(str|int) | None: (Action, Value) or None (fold)
        """
        proba_out: float = get_proba_out(self.__hand.cards, board, phase)
        hand_power: int = get_hand_power(self.__hand.cards, board)
        pot_odds: float = get_pot_odds(total_blind, blind)
        
        if hand_power == 10: 
            if phase == 0 and current_dealer: return ('raise', self.generate_bet_value())
        elif proba_out >= 50: ...
        elif proba_out >= 25: ...
    
        return None
        
if __name__ == "__main__":

    dealer: Dealer = Dealer([Player('IA')], 10)
    dealer.distribute(True)
    
    
    print(dealer.board)
    print(dealer.players[0].hand)