# <========== Import ==========>

from __future__ import annotations

# <========== Class ==========>

class Bankroll:

    # <----- init ----->

    def __init__(self: Bankroll, x: int = 0) -> None: self.__value: int  = x

    # <----- getter ----->

    @property
    def bankroll(self: Bankroll) -> int: return self.__value

    # <----- setter ----->

    @bankroll.setter
    def bankroll(self: Bankroll, newBankroll: int) -> None: self.__value = newBankroll

    # <----- operateur ----->

    def __iadd__(self: Bankroll, x:int) -> Bankroll: return Bankroll(self.__value + x)

    def __add__(self: Bankroll, x: int) -> Bankroll: return Bankroll(self.__value + x)

    def __isub__(self: Bankroll, x:int) -> Bankroll: return Bankroll(self.__value - x)

    def __sub__(self: Bankroll, x: int) -> Bankroll: return Bankroll(self.__value - x)

    # <----- comparateur ----->

    def __eq__(self: Bankroll, other: Bankroll) -> bool: return self.__value == other.__value

    def __ne__(self: Bankroll, other: Bankroll) -> bool: return self.__value != other.__value
    
    def __lt__(self: Bankroll, other: Bankroll) -> bool: return self.__value < other.__value
    
    def __gt__(self: Bankroll, other: Bankroll) -> bool: return self.__value > other.__value
    
    def __le__(self: Bankroll, other: Bankroll) -> bool: return self.__value <= other.__value
    
    def __ge__(self: Bankroll, other: Bankroll) -> bool: return self.__value >= other.__value

    # <----- str ----->

    def __str__(self: Bankroll) -> str: return f"bankroll is {self.__value}$."
        
