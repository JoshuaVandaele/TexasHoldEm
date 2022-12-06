# <========== import ==========>

from __future__ import annotations

from Card import Card

# <========== class ==========>

class Board:
    
    # <----- init ----->
    
    def __init__(self: Board, cards: list[Card]) -> None:
        self.__cards: list[Card] = cards
    
    # <----- getter ----->
    
    @property
    def cards(self: Board) -> list[Card]: return self.__cards
    
    # <----- setter ----->
    
    @cards.setter
    def cards(self: Board, newCards: list[Card]) -> None: self.__cards = newCards
    
    # <----- getFlop ----->
    
    def get_flop(self: Board) -> list[Card]: return self.__cards[:3]
    
    # <----- getTurn ----->
    
    def get_turn(self: Board) -> Card: return self.__cards[3]
    
    # <----- getRiver ----->
    
    def get_river(self: Board) -> Card: return self.__cards[4]
        