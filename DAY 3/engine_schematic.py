import re


def has_symbol(character : str) -> bool:
    # strip to remove the pesky line breaks from lines
    return re.search('[^\.|\d]', character.strip()) != None


class Number:
    # this is probably not the best practice, because changing the schematic will move around parts
    # but for this task it should work; every number comes from the same schematic and it shouldn't change
    schematic = []

    def __init__(self, value : int, line : int, start : int, end : int):
        self.value = value
        self.line = line
        self.startidx = start
        self.endidx = end
    
    def __repr__(self) -> str:
        return f"{self.value}, {self.line} [{self.startidx}, {self.endidx}] {self.is_part_num()}\n"
    
    def is_part_num(self) -> int:
        # if the number is at the line edge I will compare with the 1st/last digit of the number 
        start = max(0, self.startidx-1)
        end = min(len(Number.schematic[self.line])-1, self.endidx)

        # symbol before number
        if has_symbol(Number.schematic[self.line][start]):
            return True
        # symbol after number
        if has_symbol(Number.schematic[self.line][end]):
            return True
        # symbol in line above number
        if self.line > 0 and has_symbol(Number.schematic[self.line-1][start:end+1]):
            return True
        # symbol in line below number
        if self.line < len(Number.schematic)-1 and has_symbol(Number.schematic[self.line+1][start:end+1]):
            return True
        # no symbols around
        return False
    
    #defne reverse add, so i can summ all part numbers
    def __radd__(self, other):
        return self.value + other


class Star:

    def __init__(self, line : int, position : int, part_numbers : list[Number]) -> None:
        self.line = line
        self.position = position
        # find all numbers that are connected to the star '*'
        self.parts = [n.value for n in part_numbers if (
            (self.line-1 <= n.line <= self.line+1 ) 
            and (
                ( n.startidx-2 < self.position ) 
                and ( n.endidx+1 > self.position ))
            )]

    def gear_ratio(self) -> int:
        # if theres only 2 it is a gear and i return the power
        if len(self.parts) == 2:
            return self.parts[0] * self.parts[1]
            # return (self.parts[0], self.parts[1], self.parts[0] * self.parts[1])
        return 0
    
    def __repr__(self) -> str:
        return f"{self.line} {self.position} {self.parts}\n"
        

if __name__ == '__main__':

    input_file  = "./DAY 3/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()

    # part one
    Number.schematic = lines

    numbers_list = [ Number(int(m.group()), ii, m.start(), m.end()) for ii, l in enumerate(Number.schematic) for m in re.finditer(r"(\d+)", l.strip()) ]
    part_numbers = [n for n in numbers_list if n.is_part_num()]
    # print(numbers_list)
    num_sum = sum(part_numbers)
    print(num_sum)

    #part two
    star_list = [ Star(ii, m.start(), part_numbers) for ii, l in enumerate(Number.schematic) for m in re.finditer(r"(\*)", l.strip()) ]
    gear_ratios = [s.gear_ratio() for s in star_list]
    # print(star_list) 
    # print(gear_ratios)
    print(sum(gear_ratios))
