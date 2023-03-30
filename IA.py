# <========== import ==========>

from __future__ import annotations

from Hand import Hand
from Board import Board
from Dealer import Dealer
from Player import Player
from Card import Card
from IA_Proba import *

class IA(Player):
    
    def __init__(self: Player, hand: Hand | None = None, bankroll: int = 100) -> None:
        super().__init__("IA", hand, bankroll)
        
    def decision(self: IA, board: list[Card], phase: int, current_dealer: bool) -> str:
        """Return the action for the IA

        Args:
            hand (list[Card]): Hand of the IA
            board (list[Card]): Board on the field
            phase (int): Phase of the round
            current_dealer (int): If the IA is the current dealer

        Returns:
            str: Action
        """
        proba_out: float = get_proba_out(self.__hand.cards, board, phase)
        hand_power: int = get_hand_power(self.__hand.cards, board)
        
        if hand_power == 10: 
            if phase == 0: ...
            else: ...
        else:
            return 'fold'
        
if __name__ == "__main__":

    dealer: Dealer = Dealer([Player('IA')], 10)
    dealer.distribute(True)
    
    
    print(dealer.board)
    print(dealer.players[0].hand)