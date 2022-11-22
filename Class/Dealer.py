# <========== import ==========>

from __future__ import annotations

from Card import Card
from Deck import Deck
from Player import Player
from Board import Board
from Hand import Hand

# <========= class ==========>


class Dealer:

    # <----- init ----->

    def __init__(self: Dealer, deck: Deck, players: list[Player], board: Board) -> None:
        self.__deck: Deck = deck
        self.__players: list[Player] = players.copy()
        self.__board: Board = board
        self.__blind: int = 0
        self.__total_blind: int = 0

    # <----- getter ----->

    @property
    def deck(self: Dealer) -> Deck: return self.__deck

    @property
    def players(self: Dealer) -> list[Player]: return self.__players

    @property
    def board(self: Dealer) -> Board: return self.__board
    
    @property
    def blind(self: Dealer) -> int: return self.__blind
    
    @property
    def total_blind(self: Dealer) -> int: return self.__total_blind
    
    # <----- setter ----->
    
    @blind.setter
    def blind(self: Dealer, new_blind: int) -> None: self.__blind = new_blind
    
    @total_blind.setter
    def total_blind(self: Dealer, new_total_blind: int) -> None: self.__total_blind = new_total_blind

    # <----- distribute ----->

    def distribute(self: Dealer, shuffle: bool = False) -> None:
        if shuffle:
            self.__deck.reset_deck()
            self.__deck.shuffle()

        for i in range(2):
            for player in self.__players:
                player.hand[i] = self.__deck.draw()

        self.__deck.burn()
        self.__board.cards = [self.__deck.draw() for i in range(3)]
        self.__deck.burn()
        self.__board.cards[3] = self.__deck.draw()
        self.__deck.burn()
        self.__board.cards[4] = self.__deck.draw()

    # <----- its_royal_straight_flush----->
    
    def its_royal_straight_flush(self: Dealer,  player_index: int) -> bool:
        card_suit: list[str] = []
        card_value: list[int] = []
        
        for card in sorted(self.__board.cards + self.__players[player_index].hand.cards, reverse=True):
            if card.suit not in card_suit:
                card_suit.append(card.suit)
                card_value.append([card.value])
            else:
                card_value[card_suit.index(card.suit)].append(card.value)
                
        for value in card_value:
            if 1 in value and 13 in value and 12 in value and 11 in value and 10 in value: return True
        
        return False
        
    
    # <----- its_straight_flush ----->
    
    def its_staight_flush(self: Dealer, player_index: int) -> bool | tuple[bool, int]:
        card_suit: list[str] = []
        card_value: list[int] = []
        
        for card in sorted(self.__board.cards + self.__players[player_index].hand.cards, reverse=True):
            if card.suit not in card_suit:
                card_suit.append(card.suit)
                card_value.append([card.value])
            else:
                card_value[card_suit.index(card.suit)].append(card.value)
        
        compteur = 0
        hight_value = None
        
        for value in card_value:
            if len(value) > 4:
                for i, card in enumerate(value):
                    if 1 in value and 13 in value and 12 in value and 11 in value and 10 in value: return (True,1)
                    else:
                        if i < len(value) - 1:
                            if card - 1 == value[i+1]:
                                compteur +=1
                            if hight_value == None: hight_value = card
                        elif compteur < 4:
                            compteur = 0
                            hight_value = None
        
                if compteur >= 4: return (True, hight_value)
                
        return False
                    
                        
    
    # <----- its_four_of_kind ----->
    
    def its_four_of_kind(self: Dealer, player_index: int) -> bool | tuple[bool]:
        cards: list[Card] = [card for card in (self.__board.cards + self.__players[player_index].hand.cards)]
        occurence: list[int] = Card.sort_occurence(cards)
        
        four_of_kind: int = None
        
        for tuple_card in occurence:
            if tuple_card[1] == 4:
                four_of_kind = tuple_card[0]
                del occurence[occurence.index(tuple_card)]
                
        if four_of_kind != None:
            if isinstance(occurence[0], tuple): return (True, four_of_kind, occurence[0][0])
            return (True, four_of_kind, occurence[0])
        return False
        
    # <----- its_full_house ----->
    
    def its_full_house(self: Dealer, player_index: int) -> bool | tuple[bool, int, int]:
        
        cards: list[Card] = [card for card in (self.__board.cards + self.__players[player_index].hand.cards)]
        occurence: list[int] = Card.sort_occurence(cards)
        
        three_of_kind: int = None
        pair: int = None
        
        for tuple_card in occurence:
            if tuple_card[1] == 3 and (three_of_kind == None or tuple_card[0] > three_of_kind):
                three_of_kind = tuple_card[0]
            elif tuple_card[1] == 2 and (pair == None or tuple_card[0] > pair):
                print("pair")
                pair = tuple_card[0]
                
        
        if three_of_kind != None and pair != None: return (True, three_of_kind, pair)
        return False
        
    
    # <----- its_flush ----->
    
    def its_flush(self: Dealer, player_index: int) -> bool | tuple[bool, int, int, int, int, int]:
        
        cards: list[Card] = [card for card in (self.__board.cards + self.__players[player_index].hand.cards)]
        cards.sort(reverse=True)
        
        suit: list[str] = []
        value: list[list[int]] = []
        
        for card in cards:
            if card.suit not in suit:
                suit.append(card.suit)
                value.append([card.value])
            else:
                value[suit.index(card.suit)].append(card.value)
        
        for v in value:
            if len(v) >= 5: return (True, v[0])
        return False
                
    

    
    # <----- its_straight ----->
    
    def its_straight(self: Dealer, player_index: int) -> bool | tuple[bool, int]:
        
        cards: list[int] = [card.value for card in (self.__board.cards + self.__players[player_index].hand.cards)]
        cards.sort(reverse=True)
        
        if 1 in cards and 13 in cards and 12 in cards and 11 in cards and 10 in cards: return (True,1)
            
        
        compteur: int = 0
        hight_value: int = None
        
        for i, card in enumerate(cards):
        
            if i < len(cards) - 1:
                if card - 1 == cards[i+1]:
                    compteur +=1
                    if hight_value == None: hight_value = card
                else:
                    compteur = 0
                    hight_value = None
        
        if compteur >= 4: return (True, hight_value)
        return False
    
    
    # <----- its_three_of_kind ----->
    
    def its_tree_of_kind(self: Dealer, player_index: int) -> bool | tuple(bool, int, int, int):
        
        cards: list[Card] = self.__board.cards + self.__players[player_index].hand.cards
        
        occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
        three_of_kind: int = None
        
        for tuple_card in occurence:
            if tuple_card[1] == 3 and (three_of_kind == None or tuple_card[0] > three_of_kind):
                three_of_kind = tuple_card[0]
                del occurence[occurence.index(tuple_card)]
        
        if three_of_kind != None: return (True, three_of_kind, occurence[0][0], occurence[1][0])
        else: return False
    
    # <----- its_two_pairs----->
    
    def its_two_pairs(self: Dealer, player_index: int) -> bool | tuple[bool, int, int, int]:
    
        cards: list[Card] = self.__board.cards + self.__players[player_index].hand.cards
        
        occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
        
        pair: list[int] = []; to_del: list[tuple[int, int]] = []
        
        for tuple_card in occurence:
            if tuple_card[1] == 2:
                pair.append(tuple_card[0])
                to_del.append(tuple_card)
        
        for value in to_del: occurence[occurence.index(value)]
        
        if len(pair) >= 2: return (True, pair[0], pair[1], occurence[0][0])
        else: return False
    
    # <----- its_one_pair ----->
    
    def its_one_pair(self: Dealer, player_index: int) -> bool | tuple[bool, int, int, int]:
            
        cards: list[Card] = self.__board.cards + self.__players[player_index].hand.cards
       
        occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
        
        pair: int = None
        
        for tuple_card in occurence:
            if tuple_card[1] == 2 and (pair == None or tuple_card[0] > pair):
                pair = tuple_card[0]
                del occurence[occurence.index(tuple_card)]
        
        if pair != None: return (True, pair, occurence[0][0], occurence[1][0], occurence[2][0])
        else: return False

    
    # <----- get_best_combination ----->

    def get_best_combination(self: Dealer, player_index: int) -> str: ...
    
if __name__ == "__main__":
    h: Hand = Hand([Card(2,'nuke'), Card(2,'nuke')])
    b: Board = Board([Card(1, 'spade'), Card(13, 'spade'), Card(12, 'spade'), Card(11, 'spade'), Card(10, 'spade')])
    p: Player = Player('silver', 1, h)
    d: Dealer = Dealer(Deck(), [p], b)
    
    print(d.its_royal_straight_flush(0))
    