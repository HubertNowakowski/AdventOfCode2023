import re
import numpy as np


class Card:
    def __init__(self, id : str, winning_numbers : str, numbers : str) -> None:
        self.id = int(id)
        self.winning_numbers = set([n for n in winning_numbers.split()])
        self.numbers = set([n for n in numbers.strip().split()])
        self.copies = 1
        self.wins = self.numbers.intersection(self.winning_numbers) # [n for n in self.numbers if np.isin(n, self.winning_numbers)]
        if len(self.wins)>0:
            self.points = 2**(len(self.wins)-1)
        else:
            self.points = 0

    def add_copies(self, num: int=1) -> None:
        self.copies += num
    
    def process_rules(self, cards : list) -> None:
        for number in range(self.id, self.id + len(self.wins), 1):
            cards[number].add_copies(self.copies)

    def __repr__(self) -> str:
        return f"\n{self.id} {self.copies}: {self.winning_numbers} | {self.numbers} || {self.wins} -> {self.points}"


if __name__ == '__main__':
    
    input_file  = "./DAY 4/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
        
    # part one
    scratch_cards = [Card(match[0], match[1], match[2]) \
                     for l in lines for match in re.findall(r"Card\s+(\d+):\s(.*)\s\|\s(.*)", l)  ]
    # print(scratch_cards)
    print(sum([sc.points for sc in scratch_cards]))

    # part two
    for sc in scratch_cards:
        sc.process_rules(scratch_cards)
    # print(scratch_cards)
    print(sum([sc.copies for sc in scratch_cards]))
    
