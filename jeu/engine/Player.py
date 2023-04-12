# <========== Import ==========>

from __future__ import annotations

from Bankroll import Bankroll
from Hand import Hand

# <========== Class ==========>

class Player:
    
    # <----- init ----->
    
    def __init__(self: Player, name: str, hand: Hand | None = None, bankroll: int = 100) -> None:
        self.__name: str = name
        self.__bankroll: Bankroll = Bankroll(bankroll)
        self.__bet: int = 0
        if isinstance(hand, Hand): self.__hand: Hand = hand
        else: self.__hand: Hand = Hand([])
        self.__action: str = ''
    
    # <----- getter -----> 
    
    @property
    def name(self: Player) -> str: return self.__name
    
    @property
    def bankroll(self: Player) -> Bankroll: return self.__bankroll
    
    @property
    def bet(self: Player) -> int: return self.__bet
    
    @property
    def hand(self: Player) -> Hand: return self.__hand
    
    @property
    def action(self: Player) -> str: return self.__action
    
    # <----- setter ----->
    
    @name.setter
    def name(self: Player, new_name: str) -> None: self.__name = new_name
    
    @bankroll.setter
    def bankroll(self: Player, new_bankroll: int) -> None: self.__bankroll = Bankroll(new_bankroll)

    @bet.setter
    def bet(self: Player, new_bet: int) -> None: self.__bet = new_bet
    
    @hand.setter
    def hand(self: Player, new_hand: Hand) -> None: self.__hand = new_hand
    
    @action.setter
    def action(self: Player, new_action: str) -> None: self.__action = new_action