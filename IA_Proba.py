from Card import Card

def is_highest_card(cards: list[Card]) -> int:
    
    cards.sort(reverse=True)
    cards_list: list[int] = [card.value for card in cards]    
    while cards_list[-1] == 1 and sum(cards_list) != len(cards_list):
        cards_list.insert(0, 1)
        del cards_list[-1]

    return cards_list[0]
    
def is_one_pair(cards: list[Card]) -> int | None:

    occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
    pair: int = 0

    for tuple_card in occurence:
        if tuple_card[1] == 2 and (pair == 0 or tuple_card[0] > pair):
            pair = tuple_card[0]
            del occurence[occurence.index(tuple_card)]

    if pair != 0: return pair
    return None
        
def is_two_pairs(cards: list[Card]) -> tuple[int, int] | None:

    occurence: list[tuple[int, int]] = Card.sort_occurence(cards)

    pair: list[int] = []
    to_del: list[tuple[int, int]] = []

    for tuple_card in occurence:
        if tuple_card[1] == 2:
            pair.append(tuple_card[0])
            to_del.append(tuple_card)

    for value in to_del: occurence[occurence.index(value)]

    if len(pair) >= 2: return pair[0], pair[1]
    return None
        
def is_three_of_kind(cards: list[Card]) -> int | None:

    occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
    three_of_kind: int = 0
    
    
    for tuple_card in reversed(occurence):
        if tuple_card[1] == 3 and (three_of_kind == 0 or (tuple_card[0] > three_of_kind or tuple_card[0] == 1)):
            three_of_kind = tuple_card[0]

    if three_of_kind != 0: return three_of_kind
    return None

def is_straight(cards: list[Card]) -> int | None:
                
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
                
    if compteur >= 4: return highest_value
    return None
    
def is_flush(cards: list[Card]) -> tuple[int] | None:
            
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
            
    for i, v in enumerate(value):
        if len(v) >= 5: return tuple(card_value for card_value in v[:5])
    return None

def is_four_of_kind(cards: list[Card]) -> int | None:
    
    occurence: list[tuple[int, int]] = Card.sort_occurence(cards)
    
    four_of_kind: int = 0
    
    for tuple_card in occurence:
        if tuple_card[1] == 4:
            four_of_kind = tuple_card[0]
            del occurence[occurence.index(tuple_card)]
            
    if four_of_kind != 0: return four_of_kind
    return None
    

def is_full_house(cards: list[Card]) -> tuple[int, int] | None:

    occurence:  list[tuple[int, int]] = Card.sort_occurence(cards)
    
    three_of_kind: int = 0
    pair: int = 0
    
    for tuple_card in occurence:
        if tuple_card[1] == 3 and (three_of_kind == 0 or tuple_card[0] > three_of_kind):
            three_of_kind = tuple_card[0]
        elif tuple_card[1] == 2 and (pair == 0 or tuple_card[0] > pair):
            pair = tuple_card[0]
            
    if three_of_kind != 0 and pair != 0: return three_of_kind, pair
    return None

def is_straight_flush(cards: list[Card]) -> tuple[int, str] | None:

    card_value: list[list[int]] = []
    card_suit: list[str] = []
    
    for card in sorted(cards, reverse = True):
        if card.suit not in card_suit:
            card_suit.append(card.suit)
            card_value.append([card.value])
        else:
            card_value[card_suit.index(card.suit)].append(card.value)

    compteur: int = 0
    highest_value: tuple[int, str] = (0, "")

    for j, value in enumerate(card_value):
        if len(value) > 4:
            for i, card in enumerate(value):
                if 1 in value and 13 in value and 12 in value and 11 in value and 10 in value:
                    return 1, card_suit[j]
                
                else:    
                    if i < len(value) - 1:
                        if card - 1 == value[i+1]: compteur += 1
                        if highest_value[0] == 0: highest_value = (card, card_suit[j])
                            
                    elif compteur < 4:
                        compteur = 0
                        highest_value = (0, "")
            
            if compteur >= 4:
                return highest_value
        
    return None

def is_royal_straight_flush(cards: list[Card]) -> str | None:
        card_suit: list[str] = []
        card_value: list[list[int]] = []

        for card in sorted(cards, reverse=True):
            if card.suit not in card_suit:
                card_suit.append(card.suit)
                card_value.append([card.value])
            else:
                card_value[card_suit.index(card.suit)].append(card.value)

        for i, value in enumerate(card_value):
            if 1 in value and 13 in value and 12 in value and 11 in value and 10 in value:
                return card_suit[i]

        return None
    
def complet_hand(current_hand: list, cards: list[Card]) -> list:
    
    # remove card use in hand
    for card in reversed(cards[:len(cards)]):
        if card.value in current_hand:
            del cards[cards.index(card)]
    
    # complete the hand with most powerfull cards      
    for i in range(len(cards)):
        highest_card: int = is_highest_card(cards)
        current_hand.append(highest_card)
        
        for card in cards:
            if card.value == highest_card:
                del cards[cards.index(card)]
                break
        
    # remove card useless in hand
    if current_hand[0] == 8: max_card: int = 2
    elif current_hand[0] == 3: max_card: int = 3
    elif current_hand[0] == 4: max_card: int = 3
    elif current_hand[0] == 2: max_card: int = 4
    else: max_card: int = 5
    
    while len(current_hand[1:]) > max_card:
        del current_hand[-1]
    
    return current_hand
    
def get_best_combination(cards: list[Card]) -> list:

        if is_royal_straight_flush(cards) != None:
            return [10] 

        elif (straight_flush := is_straight_flush(cards)) != None:
            return [9, straight_flush[0]]

        elif (four_of_kind := is_four_of_kind(cards)) != None:
            return complet_hand([8, four_of_kind], cards)
        
        elif (full_house := is_full_house(cards)) != None:
            return [7, full_house[0], full_house[1]]

        elif (flush := is_flush(cards)) != None:
            return [6] + [value for value in flush]

        elif (straight := is_straight(cards)) != None:
            return [5, straight]

        elif (three_of_kind := is_three_of_kind(cards)) != None:
            return complet_hand([4, three_of_kind], cards)
        
        elif (two_pairs := is_two_pairs(cards)) != None:
            return complet_hand([3, two_pairs[0], two_pairs[1]], cards)

        elif (one_paire := is_one_pair(cards)) != None:
            return complet_hand([2, one_paire], cards)
        
        else:
            return complet_hand([1], cards)
            
def better_hand(hand1: list[Card], hand2: list[Card], board: list[Card]) -> bool:
    best_hand1: list = get_best_combination(hand1 + board)
    best_hand2: list = get_best_combination(hand2 + board)
    
    if best_hand1[0] > best_hand2[0]: return True
    elif best_hand1[0] < best_hand2[0]: return False
    
    size: int = len(best_hand2) if len(best_hand2) < len(best_hand1) else len(best_hand1)
    for i in range(size):
        if i +1 == size:
            if best_hand1[i] == best_hand2[i]: return False
            if best_hand1 > best_hand2: return True
            
    
if __name__ == "__main__":
    print(get_best_combination([Card(13,"Heart"),Card(9,"Heart"),Card(12,"Heart"),Card(11,"Heart"),Card(10,"Heart"),Card(7,"spade")]))