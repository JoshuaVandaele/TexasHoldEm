# <========== Import ==========>

from __future__ import annotations

from random import shuffle
from typing import Final

from Card import Card

# <========== Class ==========>

class Deck:
    
    # <----- init ----->
    
    def __init__(self: Deck, numberOfCards: int = 52, suitList: list[str]|None = None) -> None:
        if suitList == None: suitList = ["Hearts","Diamonds","Clubs","Spades"]
        
        self.__SUIT_LIST: Final[list[str]] = suitList.copy()
        self.__NUMBER_OF_CARDS: Final[int] = numberOfCards
        self.__cards: list[Card] = []
        
        for suit in suitList:
            for i in range(1,int(numberOfCards/len(suitList))+1):
                self.__cards.append(Card(i,suit))
                
    # <----- getter ----->
    
    @property
    def SUIT_LIST(self: Deck) -> list[str]: return self.__SUIT_LIST.copy()
    
    @property
    def NUMBER_OF_CARDS(self: Deck) -> int: return self.__NUMBER_OF_CARDS
    
    @property
    def cards(self: Deck) -> list[Card]: return self.__cards.copy()
    
    # <----- shuffle ----->
    
    def shuffle(self: Deck) -> None: shuffle(self.__cards)
    
    # <----- draw ----->
    
    def draw(self: Deck) -> Card: return self.__cards.pop(0)
    
    # <----- burn ----->
    
    def burn(self: Deck) -> None: self.__cards.pop(0)
    
    # <----- resetDeck ----->
    
    def reset_deck(self: Deck) -> None: 
        self.__cards = []        
        for suit in self.__SUIT_LIST:
            for i in range(1,int(self.__NUMBER_OF_CARDS/len(self.__SUIT_LIST))+1):
                self.__cards.append(Card(i,suit))
    