import numpy as np
import operator


class Hand:
    CARD_DICT = {
        'A': 14,
        'K': 13,
        'Q': 12,
        # 'J': 11, # his is now a JOKER
        'T': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
        'J': 1, # JOKER is last in order of cards
        'None': -1
    }

    HAND_DICT = {
        "5ofaKind": 6,
        "4ofaKind": 5,
        "FullHouse": 4,
        "3ofaKind": 3,
        "TwoPair": 2,
        "Pair": 1,
        "HighCard": 0,
        'None': -1
    }

    def __init__(self, cards : str, bid: int) -> None:
        self.bid = bid

        self.hand_type = 'None'
        self.first_card = 'None'
        self.first_card_count = 0
        self.second_card = 'None'
        self.second_card_count = 0
        
        for letter in Hand.CARD_DICT.keys():
            #adding exception for the jokers, so i dont get pairs of jokers
            if letter == 'J':
                continue

            count =cards.count(letter)
            if count > self.first_card_count:
                self.second_card_count = self.first_card_count
                self.second_card = self.first_card
                self.first_card_count = count
                self.first_card = letter

            elif count > self.second_card_count:
                self.second_card_count = count
                self.second_card = letter
        # before setting the hand_type we need to add JOKERS to first card (making the hand better)
        # but not if Jokers are the most occuring card 
        if self.first_card != 'J':
            self.first_card_count += cards.count('J')

        if self.first_card_count == 5: self.hand_type = "5ofaKind"
        elif self.first_card_count == 4: self.hand_type = "4ofaKind"
        elif self.first_card_count == 3 and self.second_card_count == 2: self.hand_type = "FullHouse"
        elif self.first_card_count == 3: self.hand_type = "3ofaKind"
        elif self.first_card_count == 2 and self.second_card_count == 2: self.hand_type = "TwoPair"
        elif self.first_card_count == 2: self.hand_type = "Pair"
        else: self.hand_type = "HighCard"
        
        self.cards = cards
        # self.cards = ''
        # if self.first_card != 'Null':
        #     self.cards += f'{np.char.multiply(self.first_card, self.first_card_count)}'
        # if self.second_card != 'Null':
        #     self.cards += f'{np.char.multiply(self.second_card, self.second_card_count)}'
        #     # print(self.cards)
        # self.cards += ''.join(sorted(cards.replace(self.first_card, '').replace(self.second_card, ''), key=lambda x: self.CARD_DICT[x], reverse=True))
        self.rank = 0
    
    def __repr__(self) -> str:
        return f"\n{self.cards} {self.first_card_count, self.first_card} {self.second_card_count, self.second_card} {self.hand_type} {self.rank}"
    
    def set_rank(self, rank):
        self.rank = rank
    
    def winnings(self):
        return self.bid * self.rank


if __name__ == "__main__":

    input_file  = "./DAY 7/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
        
    hands = [Hand(x[0], int(x[1])) for x in (l.strip().split(' ') for l in lines )]
    # print(hands)

    # sorting hands by hand_type,
    # then sorting by cards IN ORDER of the hand (no sorting here)
    hands_sorted = sorted(hands, key=lambda x: (Hand.HAND_DICT[x.hand_type],
                                                Hand.CARD_DICT[x.cards[0]], 
                                                Hand.CARD_DICT[x.cards[1]], 
                                                Hand.CARD_DICT[x.cards[2]], 
                                                Hand.CARD_DICT[x.cards[3]], 
                                                Hand.CARD_DICT[x.cards[4]], 
                                                ) )
    [h.set_rank(ii+1) for ii, h in enumerate(hands_sorted)]
    # print(hands_sorted)

    winnings = sum([h.winnings() for h in hands_sorted])
    print(winnings)

