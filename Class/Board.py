# <========== import ==========>

from __future__ import annotations

from Card import Card

# <========== class ==========>

class Board:
    
    # <----- init ----->
    
    def __init__(self: Board, cards: list[Card * 5]) -> None:
        self.__cards: list[Card * 5] = cards
    
    # <----- getter ----->
    
    @property
    def cards(self: Board) -> tuple[Card * 5]: return self.__cards
    
    # <----- setter ----->
    
    @cards.setter
    def cards(self: Board, newCards: tuple[Card * 5]) -> None: self.__cards = newCards
    
    # <----- getFlop ----->
    
    def get_flop(self: Board) -> tuple[Card * 3]: return self.__cards[:3]
    
    # <----- getTurn ----->
    
    def get_turn(self: Board) -> Card: return self.__cards[3]
    
    # <----- getRiver ----->
    
    def get_river(self: Board) -> Card: return self.__cards[4]
        