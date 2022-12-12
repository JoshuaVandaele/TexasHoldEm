# <========== import ==========>

from __future__ import annotations

from jeu.engine.Card import Card
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
        