# <========== import ==========>

from __future__ import annotations

from jeu.engine.Card import Card
from jeu.engine.Deck import Deck
from jeu.engine.Player import Player
from jeu.engine.Board import Board
from jeu.engine.Hand import Hand

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
        """ Distribute card with casino method

        Args:
            self (Dealer): self
            shuffle (bool, optional):for shuffle or the deck when you use the function. Defaults to False.
        """
        if shuffle:
            self.__deck.reset_deck()
            self.__deck.shuffle()

        for i in range(2):
            for player in self.__players:
                player.hand.cards.append(self.__deck.draw())

        self.__deck.burn()
        self.__board.cards = [self.__deck.draw() for i in range(3)]
        self.__deck.burn()
        self.__board.cards[3] = self.__deck.draw()
        self.__deck.burn()
        self.__board.cards[4] = self.__deck.draw()

    # <----- is_royal_straight_flush----->

    def is_royal_straight_flush(self: Dealer,  player_index: int) -> bool:
        """ Define if their have royal straight flush

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            bool: royal straight flush = True else False
        """
        card_suit: list[str] = []
        card_value: list[list[int]] = []

        for card in sorted(self.__board.cards + self.__players[player_index].hand.cards, reverse=True):
            if card.suit not in card_suit:
                card_suit.append(card.suit)
                card_value.append([card.value])
            else:
                card_value[card_suit.index(card.suit)].append(card.value)

        for value in card_value:
            if 1 in value and 13 in value and 12 in value and 11 in value and 10 in value:
                return True

        return False

    # <----- is_straight_flush ----->

    def is_straight_flush(self: Dealer, player_index: int) -> list:
        """ Define if their have straight flush

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: if their have straight flush = True + hand composition or False in a list
        """
        card_suit: list[str] = []
        card_value: list[list[int]] = []

        for card in sorted(self.__board.cards + self.__players[player_index].hand.cards, reverse=True):
            if card.suit not in card_suit:
                card_suit.append(card.suit)
                card_value.append([card.value])
            else:
                card_value[card_suit.index(card.suit)].append(card.value)

        compteur = 0
        highest_value = None

        for value in card_value:
            if len(value) > 4:
                for i, card in enumerate(value):
                    if 1 in value and 13 in value and 12 in value and 11 in value and 10 in value:
                        return [True, 1]
                    else:
                        if i < len(value) - 1:
                            if card - 1 == value[i+1]:
                                compteur += 1
                            if highest_value == None:
                                highest_value = card
                        elif compteur < 4:
                            compteur = 0
                            highest_value = None

                if compteur >= 4:
                    return [True, highest_value]

        return [False]

    # <----- is_four_of_kind ----->

    def is_four_of_kind(self: Dealer, player_index: int) -> list:
        """ Define if their have four of kind

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: if their have four of kind = True + hand composition or False in a list
        """
        cards: list[Card] = [card for card in (
            self.__board.cards + self.__players[player_index].hand.cards)]
        occurence: list[tuple[int, int]] = Card.sort_occurence(cards)

        four_of_kind: int | None = None

        for tuple_card in occurence:
            if tuple_card[1] == 4:
                four_of_kind = tuple_card[0]
                del occurence[occurence.index(tuple_card)]

        if four_of_kind != None:
            if isinstance(occurence[0], tuple):
                return [True, four_of_kind, occurence[0][0]]
            return [True, four_of_kind, occurence[0]]
        return [False]

    # <----- is_full_house ----->

    def is_full_house(self: Dealer, player_index: int) -> list:
        """ Define if their have full house

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: if their have full house = True + hand composition or False in a list
        """

        cards: list[Card] = [card for card in (self.__board.cards + self.__players[player_index].hand.cards)]
        occurence:  list[tuple[int, int]] = Card.sort_occurence(cards)

        three_of_kind: int | None = None
        pair: int | None = None

        for tuple_card in occurence:
            if tuple_card[1] == 3 and (three_of_kind == None or tuple_card[0] > three_of_kind):
                three_of_kind = tuple_card[0]
            elif tuple_card[1] == 2 and (pair == None or tuple_card[0] > pair):
                print("pair")
                pair = tuple_card[0]

        if three_of_kind != None and pair != None:
            return [True, three_of_kind, pair]
        return [False]

    # <----- is_flush ----->

    def is_flush(self: Dealer, player_index: int) -> list:
        """ Define if their have flush

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: if their have flush = True + hand composition or False in a list
        """

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
            if len(v) >= 5:
                return [True, v[0]]
        return [False]

    # <----- is_straight ----->

    def is_straight(self: Dealer, player_index: int) -> list:
        """ Define if their have straight

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: if their have straight = True + hand composition or False in a list
        """

        cards: list[int] = [card.value for card in (
            self.__board.cards + self.__players[player_index].hand.cards)]
        cards.sort(reverse=True)

        if 1 in cards and 13 in cards and 12 in cards and 11 in cards and 10 in cards:
            return [True, 1]

        compteur: int = 0
        highest_value: int | None = None

        for i, card in enumerate(cards):

            if i < len(cards) - 1:
                if card - 1 == cards[i+1]:
                    compteur += 1
                    if highest_value == None:
                        highest_value = card
                else:
                    compteur = 0
                    highest_value = None

        if compteur >= 4:
            return [True, highest_value]
        return [False]

    # <----- is_three_of_kind ----->

    def is_tree_of_kind(self: Dealer, player_index: int) -> list:
        """ Define if their have tree of kind

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: if their have tree of kind = True + hand composition or False in a list
        """

        cards: list[Card] = self.__board.cards + \
            self.__players[player_index].hand.cards

        occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
        three_of_kind: int | None = None

        for tuple_card in occurence:
            if tuple_card[1] == 3 and (three_of_kind == None or tuple_card[0] > three_of_kind):
                three_of_kind = tuple_card[0]
                del occurence[occurence.index(tuple_card)]

        if three_of_kind != None:
            return [True, three_of_kind, occurence[0][0], occurence[1][0]]
        else:
            return [False]

    # <----- is_two_pairs----->

    def is_two_pairs(self: Dealer, player_index: int) -> list:
        """ Define if their have two pairs

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: if their have two pairs = True + hand composition or False in a list
        """

        cards: list[Card] = self.__board.cards + \
            self.__players[player_index].hand.cards

        occurence: list[tuple[int, int]] = Card.sort_occurence(cards)

        pair: list[int] = []
        to_del: list[tuple[int, int]] = []

        for tuple_card in occurence:
            if tuple_card[1] == 2:
                pair.append(tuple_card[0])
                to_del.append(tuple_card)

        for value in to_del:
            occurence[occurence.index(value)]

        if len(pair) >= 2:
            return [True, pair[0], pair[1], occurence[0][0]]
        else:
            return [False]

    # <----- is_one_pair ----->

    def is_one_pair(self: Dealer, player_index: int) -> list:
        """ Define if their have one pair

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: if their have one pair = True + hand composition or False in a list
        """

        cards: list[Card] = self.__board.cards + \
            self.__players[player_index].hand.cards

        occurence: list[tuple[int, int]] = Card.sort_occurence(cards)

        pair: int | None = None

        for tuple_card in occurence:
            if tuple_card[1] == 2 and (pair == None or tuple_card[0] > pair):
                pair = tuple_card[0]
                del occurence[occurence.index(tuple_card)]

        if pair != None:
            return [True, pair, occurence[0][0], occurence[1][0], occurence[2][0]]
        else:
            return [False]

    def is_highest_card(self: Dealer, player_index: int) -> list[int]:
        """define the hand if you doesn't have combination

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list[int]: the hand composition
        """
        cards: list[int] = [card.value for card in self.__board.cards + self.__players[player_index].hand.cards]
        cards.sort(reverse=True)
        while cards[-1] == 1:
            cards.insert(0, 1)
            del cards[-1]

        return [cards[0], cards[1], cards[2], cards[3], cards[4]]

    # <----- get_best_combination ----->

    def get_best_combination(self: Dealer, player_index: int) -> list:
        """define the best combination

        Args:
            self (Dealer): self
            player_index (int): index for the hand you want to check

        Returns:
            list: list compose by hand power + hand composition
        """

        if self.is_royal_straight_flush(player_index):
            return [10]

        elif self.is_straight_flush(player_index)[0]:
            return [9] + self.is_straight_flush(player_index)[1:]

        elif self.is_four_of_kind(player_index)[0]:
            return [5] + self.is_four_of_kind(player_index)[1:]

        elif self.is_full_house(player_index)[0]:
            return [7] + self.is_straight(player_index)[1:]

        elif self.is_flush(player_index)[0]:
            return [6] + self.is_flush(player_index)[1:]

        elif self.is_straight(player_index)[0]:
            return [5] + self.is_straight(player_index)[1:]

        elif self.is_tree_of_kind(player_index)[0]:
            return [4] + self.is_tree_of_kind(player_index)[1:]

        elif self.is_two_pairs(player_index)[0]:
            return [3] + self.is_two_pairs(player_index)[1:]

        elif self.is_one_pair(player_index)[0]:
            return [2] + self.is_one_pair(player_index)[1:]

        else:
            return [1] + self.is_highest_card(player_index)

    # <----- compare_hand ----->

    def compare_hand(self: Dealer, player1_index: int, player2_index: int) -> int:
        """compare two hand

        Args:
            self (Dealer): self
            player1_index (int): player 1 you want to check
            player2_index (int): player 2 you want to check

        Returns:
            int: return the index of the best player hand or -1 if their are equals
        """
        player_1: list = self.get_best_combination(player1_index)
        player_2: list = self.get_best_combination(player2_index)

        for value_p1, value_p2 in zip(player_1, player_2):
            if value_p1 < value_p2:
                return player1_index
            elif value_p1 > value_p2:
                return player2_index

        return -1


if __name__ == "__main__":
    h: Hand = Hand([Card(2, 'nuke'), Card(2, 'nuke')])
    b: Board = Board([Card(1, 'spade'), Card(13, 'spade'), Card(
        12, 'spade'), Card(11, 'spade'), Card(10, 'spade')])
    p: Player = Player('silver', 1, h)
    d: Dealer = Dealer(Deck(), [p], b)

    print(d.is_royal_straight_flush(0))