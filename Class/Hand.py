# <========== import ==========>

from __future__ import annotations

from Card import Card
# <========== class ==========>

class Hand:
    
    # <----- init ----->
    
    def __init__(self: Hand, cards: list[Card]) -> None:
        self.__cards: list[Card] = cards
        
    # <----- getter ----->
    
    @property
    def cards(self: Hand) -> list[Card]: return self.__cards
    
    # <----- setter ----->
    
    @cards.setter
    def cards(self: Hand, newCards: list[Card]) -> None: self.__cards = newCards
    
    # <----- getKicker ----->
    
    def get_kicker(self: Hand) -> Card:
        if self.__cards[0] > self.__cards[1]: return self.__cards[0]
        else: return self.__cards[1]
        