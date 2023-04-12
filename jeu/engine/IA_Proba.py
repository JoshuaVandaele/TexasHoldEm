# <========== Local Import ==========>

from jeu.engine.Card import Card
from jeu.engine.Deck import Deck

# <========== Out Table ==========>

# use for out proba
out_table: list = [
    # %T     %R     %T+R
    [0,     0,     0    ], # 0 Out
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

# <========== Check Hand Combination ==========>

def is_highest_card(cards: list[Card]) -> int:
    """Return the highest card value in a list of cards

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        int: Highest card value
    """
    
    cards.sort(reverse=True)
    cards_list: list[int] = [card.value for card in cards]    
    while cards_list[-1] == 1 and sum(cards_list) != len(cards_list):
        cards_list.insert(0, 1)
        del cards_list[-1]

    return cards_list[0]
    
def is_one_pair(cards: list[Card]) -> int | None:
    """Return the value of the highest pair or None if the list
    doesn't have pair 

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        int | None: Highest pair value or None
    """

    occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
    pair: int = 0

    for tuple_card in occurence:
        if tuple_card[1] == 2 and (pair == 0 or tuple_card[0] > pair):
            pair = tuple_card[0]
            del occurence[occurence.index(tuple_card)]

    return pair if pair != 0 else None
        
def is_two_pairs(cards: list[Card]) -> tuple[int, int] | None:
    """Return the values of the highest pairs in order of stonger
    or None if the list doesn't have two pairs

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        tuple[int, int] | None: Highest pairs values or None
    """


    occurence: list[tuple[int, int]] = Card.sort_occurence(cards)

    pair: list[int] = []
    to_del: list[tuple[int, int]] = []

    for tuple_card in occurence:
        if tuple_card[1] == 2:
            pair.append(tuple_card[0])
            to_del.append(tuple_card)

    for value in to_del: occurence[occurence.index(value)]

    return (pair[0], pair[1]) if len(pair) >= 2 else None
        
def is_three_of_kind(cards: list[Card]) -> int | None:
    """Return the values of the highest three of kind
    or None if the list doesn't have three of kind

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        int | None: Three of kind values or None
    """

    occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
    three_of_kind: int = 0


    for tuple_card in reversed(occurence):
        if tuple_card[1] == 3 and (three_of_kind == 0 or (tuple_card[0] > three_of_kind or tuple_card[0] == 1)):
            three_of_kind = tuple_card[0]

    return three_of_kind if three_of_kind != 0 else None

def is_straight(cards: list[Card]) -> int | None:
    """ Return the highest value of a straight
    or None if the list doesn't have straight
    
    Args:
        cards (list[Card]): List of cards to check

    Returns:
        int | None: Highest straight value or None
    """
                
    cards.sort(reverse = True)

    if 1 in cards and 13 in cards and 12 in cards and 11 in cards and 10 in cards: return 1

    compteur: int = 0
    highest_value: int = 0

    for i, card in enumerate(cards):
        if i < len(cards) - 1:
            if card - 1 == cards[i+1]:
                compteur += 1
                if highest_value == 0:
                    highest_value = card.value
            else:
                compteur = 0
                highest_value = 0

    return highest_value if compteur >= 4 else None
    
def is_flush(cards: list[Card]) -> tuple[int, int, int, int, int] | None:
    """Return flush values from cards list in order of power
    or None if the list doesn't have flush

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        tuple[int, int, int, int, int] | None: Flush values or None
    """
            
    cards.sort(reverse=True)

    while cards[-1].value == 1 and sum(card.value for card in cards) != len(cards):
        cards.insert(0, cards[-1])
        del cards[-1]

    suit: list[str] = []
    value: list[list[int]] = []

    for card in cards:
        if card.suit not in suit:
            suit.append(card.suit)
            value.append([card.value])
        else:
            value[suit.index(card.suit)].append(card.value)

    return next((tuple(v[:5]) for v in value if len(v) >= 5), None)

def is_four_of_kind(cards: list[Card]) -> int | None:
    """Return value of four of kind
    or None if list doesn't have four of kind

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        int | None: Four of kind value or None
    """
    
    occurence: list[tuple[int, int]] = Card.sort_occurence(cards)

    four_of_kind: int = 0

    for tuple_card in occurence:
        if tuple_card[1] == 4:
            four_of_kind = tuple_card[0]
            del occurence[occurence.index(tuple_card)]

    return four_of_kind if four_of_kind != 0 else None
    

def is_full_house(cards: list[Card]) -> tuple[int, int] | None:
    """Return the values of full house
    or None if list doesn't have full house

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        tuple[int, int] | None: Full house values or None
    """

    occurence:  list[tuple[int, int]] = Card.sort_occurence(cards)

    three_of_kind: int = 0
    pair: int = 0

    for tuple_card in occurence:
        if tuple_card[1] == 3 and (three_of_kind == 0 or tuple_card[0] > three_of_kind):
            three_of_kind = tuple_card[0]
        elif tuple_card[1] == 2 and (pair == 0 or tuple_card[0] > pair):
            pair = tuple_card[0]

    return (three_of_kind, pair) if three_of_kind != 0 and pair != 0 else None

def is_straight_flush(cards: list[Card]) -> int | None:
    """Return the highest straight flush value
    or None if the list doesn't have straight flush

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        int | None: Highest straight flush value or None
    """

    card_value: list[list[int]] = []
    card_suit: list[str] = []

    for card in sorted(cards, reverse = True):
        if card.suit not in card_suit:
            card_suit.append(card.suit)
            card_value.append([card.value])
        else:
            card_value[card_suit.index(card.suit)].append(card.value)

    compteur: int = 0
    highest_value: int = 0

    for j, value in enumerate(card_value):
        if len(value) > 4:
            for i, card in enumerate(value):
                if 1 in value and 13 in value and 12 in value and 11 in value and 10 in value:
                    return 1

                if i < len(value) - 1:
                    if card - 1 == value[i+1]: compteur += 1
                    if highest_value == 0: highest_value = card

                elif compteur < 4:
                    compteur = 0
                    highest_value = 0

            if compteur >= 4:
                return highest_value

    return None

def is_royal_straight_flush(cards: list[Card]) -> bool:
    """Return if the deck contains a royal straight flush

    Args:
        cards (list[Card]): List of cards to check

    Returns:
        bool: If deck contains a royal straight flush
    """
    
    card_suit: list[str] = []
    card_value: list[list[int]] = []

    for card in sorted(cards, reverse=True):
        if card.suit not in card_suit:
            card_suit.append(card.suit)
            card_value.append([card.value])
        else:
            card_value[card_suit.index(card.suit)].append(card.value)

    for value in card_value:
        if 1 in value and 13 in value and 12 in value and 11 in value and 10 in value:
            return True

    return False
    
def complet_hand(current_hand: list[int], cards: list[Card]) -> list:
    """Complete the hand with the most powerfull cards

    Args:
        current_hand (list): hand of the IA
        cards (list[Card]): list of cards to check

    Returns:
        list[int]: The hand completed
    """
    
    # remove card use in hand
    for card in reversed(cards[:]):
        if card.value in current_hand:
            del cards[cards.index(card)]

    # complete the hand with most powerfull cards
    for _ in range(len(cards)):
        highest_card: int = is_highest_card(cards)
        current_hand.append(highest_card)

        for card in cards:
            if card.value == highest_card:
                del cards[cards.index(card)]
                break

    # remove card useless in hand
    if current_hand[0] == 8: max_card: int = 2
    elif current_hand[0] in [3, 4]: max_card: int = 3
    elif current_hand[0] == 2: max_card: int = 4
    else: max_card: int = 5

    while len(current_hand[1:]) > max_card:
        del current_hand[-1]

    return current_hand
    
def get_best_combination(cards: list[Card]) -> list:
    """Return the power of the hand and
    best combination you can have with a cards list
    
    Args:
        cards (list[Card]): List of cards to check

    Returns:
        list: hand power + hand composition
    """

    if is_royal_straight_flush(cards):
        return [10] 

    elif (straight_flush := is_straight_flush(cards)) != None:
        return [9, straight_flush]

    elif (four_of_kind := is_four_of_kind(cards)) != None:
        return complet_hand([8, four_of_kind], cards)

    elif (full_house := is_full_house(cards)) != None:
        return [7, full_house[0], full_house[1]]

    elif (flush := is_flush(cards)) != None:
        return [6] + list(flush)

    elif (straight := is_straight(cards)) != None:
        return [5, straight]

    elif (three_of_kind := is_three_of_kind(cards)) != None:
        return complet_hand([4, three_of_kind], cards)

    elif (two_pairs := is_two_pairs(cards)) != None:
        return complet_hand([3, two_pairs[0], two_pairs[1]], cards)

    elif (one_paire := is_one_pair(cards)) != None:
        return complet_hand([2, one_paire], cards)

    return complet_hand([1], cards)
            
def better_hand(hand1: list[Card], hand2: list[Card], board: list[Card]) -> bool:
    """Check if the first hand ws better than the second

    Args:
        hand1 (list[Card]): First hand
        hand2 (list[Card]): Second hand
        board (list[Card]): Board on the field

    Returns:
        bool: If hand was better
    """
    best_hand1: list = get_best_combination(hand1 + board)
    best_hand2: list = get_best_combination(hand2 + board)

    if best_hand1[0] > best_hand2[0]: return True
    elif best_hand1[0] < best_hand2[0]: return False

    size: int = min(len(best_hand2), len(best_hand1))
    for i in range(size):
        if i +1 == size:
            if best_hand1[i] == best_hand2[i]: return False
            elif best_hand1[i] > best_hand2[i]: return True

    return False

def count_out(hand: list[Card], board: list[Card]) -> int:
    """Return the out count.
    An out is a card that improves our game.
    For earch card in the deck,
    if hand + board + card more powerfull than hand + board -> out += 1

    Args:
        hand (list[Card]): Hand of the IA
        board (list[Card]): Board on the field

    Returns:
        int: Out count
    """
    deck: list [Card] = []
    d: Deck = Deck()

    deck.extend(card for card in d.cards if not card.exit_in(hand + board))
    out: int = sum(bool(better_hand(hand + [card], hand, board)) for card in deck)
    return out

def get_proba_out(hand: list[Card], board: list[Card], phase: int) -> float:
    """Return the probability for the next cards was a out

    Args:
        hand (list[Card]): Hand of the IA
        board (list[Card]): Board on the field
        phase (int): Phase for the flop, turn and river

    Returns:
        float: Probability for out
    """
    global out_table
    out: int = count_out(hand, board)
    return (out/(52-5+phase-1))*100 if out > len(out_table) else out_table[count_out(hand, board) - 1][phase - 2]

def get_hand_power(hand: list[Card], board: list[Card]) -> int:
    """Return the hand power

    Args:
        hand (list[Card]): Hand of the IA
        board (list[Card]): Board on the field

    Returns:
        int: Power of the hand
    """
    return get_best_combination(hand + board)[0]

def get_pot_odds(total_blind: int, blind: int) -> float:
    """Returns the pot odds on percentage

    Args:
        total_blind (int): the pot value
        blind (int): the current blind for call

    Returns:
        float: pot odds
    """
    return blind / total_blind * 100

# <========== Main ==========>

if __name__ == "__main__":
    
    hand: list[Card] = [Card(10,"carreau"), Card(11,"coeur")]
    board: list[Card] = [Card(5,"coeur"), Card(4,"carreau"), Card(3,"trefle")]
    
    print(get_proba_out(hand, board, 0))