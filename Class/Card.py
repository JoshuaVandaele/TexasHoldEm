# <========== Import ==========>

from __future__ import annotations

# <========== Class ==========>

class Card:
    
    # <----- init ----->
    
    def __init__(self: Card, value: int, suit: str) -> None:
        self.__value: int = value
        self.__suit: str = suit
        
    # <----- getter ----->
    
    @property
    def value(self: Card) -> int: return self.__value
    
    @property
    def suit(self: Card) -> str: return self.__suit
    
    # <----- comparator ----->
    
    def __eq__(self: Card, other: Card | int) -> bool: 
        if isinstance(other, Card): return self.__value == other.__value
        return self.__value == other

    def __ne__(self: Card, other: Card | int) -> bool: 
        if isinstance(other, Card): return self.__value != other.__value
        return self.__value == other
    
    def __lt__(self: Card, other: Card | int) -> bool: 
        if self.__value == 1: return False
        elif isinstance(other, Card): return self.__value < other.__value
        return self.__value < other
    
    def __gt__(self: Card, other: Card | int) -> bool: 
        if self.__value == 1: return True
        elif isinstance(other, Card): return self.__value > other.__value
        return self.__value > other
    
    def __le__(self: Card, other: Card | int) -> bool:
        if self == other: return True
        return self < other

    def __ge__(self: Card, other: Card | int) -> bool:
        if self == other: return True
        return self > other

        
    # <----- operateur ----->
    
    def __iadd__(self: Card, x: int) -> Card: return Card(self.__value + x, self.__suit)

    def __add__(self: Card, x: int) -> Card: return Card(self.__value + x, self.__suit)
    
    def __isub__(self: Card, x: int) -> Card: return Card(self.__value - x, self.__suit)

    def __sub__(self: Card, x: int) -> Card: return Card(self.__value - x, self.__suit)
    
    # <----- sameSuit ----->
    
    def same_suit(self: Card, other: Card) -> bool: return self.__suit == other.__suit
    
    # <----- str ----->
    
    def __str__(self: Card) -> str: return f"{self.__value} of {self.__suit}"
    
    # <----- repr ----->
    
    def __repr__(self: Card) -> str: return f"{self.__value} of {self.__suit}"
        
    
    # <----- sort_occurence ----->
    
    @staticmethod
    def sort_occurence(cards: list[Card]) -> list[tuple[int, int]]:
        occurence: list[tuple(int, int)] = []
        
        for card in cards:
            if (card.value, cards.count(card)) not in occurence:
                occurence.append((card.value, cards.count(card)))
        
        occurence.sort(key = lambda x: x[0], reverse = True)
        if occurence[-1][0] == 1:
            occurence.insert(0,occurence[-1])
            del occurence[-1]
            
        return occurence