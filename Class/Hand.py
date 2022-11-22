# <========== import ==========>

from __future__ import annotations

from Card import Card
# <========== class ==========>

class Hand:
    
    # <----- init ----->
    
    def __init__(self: Hand, cards: tuple[Card * 2]) -> None:
        self.__cards: tuple[Card * 2] = cards
        
    # <----- getter ----->
    
    @property
    def cards(self: Hand) -> tuple[Card * 2]: return self.__cards
    
    # <----- setter ----->
    
    @cards.setter
    def cards(self: Hand, newCards: tuple[Card * 2]) -> None: self.__cards = newCards
    
    # <----- getKicker ----->
    
    def get_kicker(self: Hand) -> Card:
        if self.__cards[0] > self.__cards[1]: return self.__cards[0]
        else: return self.__cards[1]
        