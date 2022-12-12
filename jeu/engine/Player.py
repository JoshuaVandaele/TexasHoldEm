# <========== Import ==========>

from __future__ import annotations

from jeu.engine.Bankroll import Bankroll
from jeu.engine.Hand import Hand

# <========== Class ==========>

class Player:
    
    # <----- init ----->
    
    def __init__(self: Player, name: str, id: int, hand: Hand, bankroll: int) -> None:
        self.__name: str = name
        self.__id = id
        self.__bankroll: Bankroll = Bankroll(bankroll)
        self.__bet: int = 0
        self.__hand: Hand = hand
    
    # <----- getter -----> 
    
    @property
    def name(self: Player) -> str: return self.__name

    @property
    def id(self: Player) -> int: return self.__id
    
    @property
    def bankroll(self: Player) -> Bankroll: return self.__bankroll
    
    @property
    def bet(self: Player) -> int: return self.__bet
    
    @property
    def hand(self: Player) -> Hand: return self.__hand
    
    # <----- setter ----->
    
    @name.setter
    def name(self: Player, new_name: str) -> None: self.__name = new_name

    @id.setter
    def id(self: Player, new_id: int) -> None: self.__id = new_id
    
    @bankroll.setter
    def bankroll(self: Player, new_bankroll: int) -> None: self.__bankroll = Bankroll(new_bankroll)
    
    @bet.setter
    def bet(self: Player, new_bet: int) -> None: self.__bet = new_bet
    
    @hand.setter
    def hand(self: Player, new_hand: Hand) -> None: self.__hand = new_hand