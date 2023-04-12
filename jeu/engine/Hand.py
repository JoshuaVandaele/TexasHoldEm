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
    
    # <----- str ----->
    
    def __str__(self: Hand) -> str: return f"({self.cards[0]}; {self.cards[1]})"
    
    # <----- repr ----->

    def __repr__(self: Hand) -> str: return f"({self.cards[0]}; {self.cards[1]})"
        
        