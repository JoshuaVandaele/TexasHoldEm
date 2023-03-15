# <========== import ==========>

from __future__ import annotations

from Hand import Hand
from Board import Board
from Dealer import Dealer
from Player import Player
from Card import Card

out_table: list = [
    # %T     %R     %T+R
    [2.130, 2.170, 4.260], # 1 Out
    [4.260, 4.350, 8.420], # 2 Outs
    [6.380, 6.520, 12.49], # 3 Outs
    [8.510, 8.700, 16.47], # 4 Outs
    [10.64, 10.87, 20.35], # 5 Outs
    [12.77, 13.04, 24.14], # 6 Outs
    [14.89, 15.22, 27.84], # 7 Outs
    [17.02, 17.39, 31.45], # 8 Outs
    [19.15, 19.57, 34.97], # 9 Outs
    [21.28, 21.74, 38.39], # 10 Outs
    [23.40, 23.91, 41.72], # 11 Outs
    [25.53, 26.09, 44.96], # 12 Outs
    [27.66, 28.26, 48.10], # 13 Outs
    [29.79, 30.43, 51.16], # 14 Outs
    [31.91, 32.61, 54.12], # 15 Outs
    [34.04, 34,78, 56.98], # 16 Outs
    [36.17, 36.96, 59.76], # 17 Outs
    [38.30, 39.13, 62.44], # 18 Outs
    [40.43, 41.30, 65.03], # 19 Outs
    [42.55, 43.48, 67.53], # 20 Outs
    [44.68, 45.65, 69.94], # 21 Outs
    [46.81, 47.83, 72.25]] # 22 Outs

# <========== variables global ==========>

phase: int = 3
number_of_cards: int = 52

# <========== known cards ==========>

def known_cards(ia_hand: Hand, board: Board) -> list[Card]:
    cards_known: list[Card] = ia_hand.cards
    if phase >= 1: cards_known += board.get_flop()
    if phase >= 2: cards_known += [board.get_river()]
    if phase >= 3: cards_known += [board.get_turn()]
    
    return cards_known
    
# <========== value occurence ==========>

def value_occurence(ia_hand: Hand, board: Board) -> list[tuple[int, int]]:
    
    cards: list[Card] = known_cards(ia_hand, board)
    
    value_knows: list[int] = []
    value_counter: list[int] = []
    
    for card in cards:
        if card.value not in value_knows:
            value_knows.append(card.value)
            value_counter.append(1)
        else: value_counter[value_knows.index(card.value)] += 1
            
    return list(zip(value_knows, value_counter))

# <========== suit occurence global ==========>

def suit_occurence(ia_hand: Hand, board: Board) -> list[tuple[str, int]]:
    
    cards: list[Card] = known_cards(ia_hand, board)
    
    suit_knows: list[str] = []
    suit_counter: list[int] = []
    
    for card in cards:
        if card.suit not in suit_knows:
            suit_knows.append(card.suit)
            suit_counter.append(1)
        else: suit_counter[suit_knows.index(card.suit)] += 1
            
    return list(zip(suit_knows, suit_counter))    
    
class IA(Player):
    
    def __init__(self: Player, hand: Hand | None = None, bankroll: int = 100) -> None:
        super().__init__("IA", hand, bankroll)
        

        
if __name__ == "__main__":

    dealer: Dealer = Dealer([Player('IA')], 10)
    dealer.distribute(True)
    
    
    print(dealer.board)
    print(dealer.players[0].hand)