from Card import Card

def is_highest_card(cards: list[Card]) -> int:
    
    cards.sort(reverse=True)
    cards_list: list[int] = [card.value for card in cards]
    
    while cards_list[-1] == 1:
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

    if pair == 0: return pair
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

    for tuple_card in occurence:
        if tuple_card[1] == 3 and (three_of_kind == 0 or tuple_card[0] > three_of_kind):
            three_of_kind = tuple_card[0]
            del occurence[occurence.index(tuple_card)]

    if three_of_kind == 0: return three_of_kind
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
    
def is_flush(cards: list[Card]) -> tuple[int, str] | None:
            
    cards.sort(reverse=True)
    
    suit: list[str] = []
    value: list[list[int]] = []
    
    for card in cards:
        if card.suit not in suit:
            suit.append(card.suit)
            value.append([card.value])
        else:
            value[suit.index(card.suit)].append(card.value)
            
    for i, v in enumerate(value):
        if len(v) >= 5: return v[0], suit[i]
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

    print(card_value)
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
    
def get_best_combination(cards: list[Card]) -> list:

        if is_royal_straight_flush(cards) != None:
            return [10] 

        elif (straight_flush := is_straight_flush(cards)) != None:
            return [9, straight_flush[0]]

        elif (four_of_kind := is_four_of_kind(cards)) != None:
            res: list = [8, four_of_kind]
            
            for card in cards:
                if card.value == res[-1]:
                    del card
            
            if cards != []: res.append(is_highest_card(cards))
            
            return res
        
        elif (full_house := is_full_house(cards)) != None:
            return [7, full_house[0], full_house[1]]

        elif (flush := is_flush(cards)) != None:
            return [6, flush]

        elif (straight := is_straight(cards)) != None:
            return [5, straight]

        elif (three_of_kind := is_three_of_kind(cards)) != None:
            res: list =  [4, three_of_kind]
            
            for card in cards:
                if card.value == res[-1]:
                    del card
            
            # to do
        elif is_two_pairs(cards) != None:
            return [3] #to do

        elif is_one_pair(cards) != None:
            return [2] #to do

        else:
            return [1] #to do
    
if __name__ == "__main__":
    print(is_straight_flush([Card(1,"heart"),Card(9,"spade"),Card(13,"spade"),Card(12,"spade"),Card(11,"spade"),Card(10,"spade")]))