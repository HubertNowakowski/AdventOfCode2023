import re

class Draw:
    def __init__(self, colors : str):
        if (match := re.search(r"(\d+)\sred", colors)) is not None:
            self.red = int(match.group(1))
        else: self.red = 0
        if (match := re.search(r"(\d+)\sgreen", colors)) is not None:
            self.green = int(match.group(1))
        else: self.green = 0
        if (match := re.search(r"(\d+)\sblue", colors)) is not None:
            self.blue = int(match.group(1))
        else: self.blue = 0

    def __repr__(self) -> str:
        return f"[{self.red}, {self.green}, {self.blue}]"
    

class Game:
    def __init__(self, line : str):
        self.text = line
        match = re.search(r"Game\s(\d+):(.*)", line)
        # first regex match is Game ID, 2nd match is all draws after ':'
        self.id = int(match.group(1))   
        self.draw_list = [Draw(x) for x in match.group(2).split(';')]
        self.red_max = max([ d.red for d in self.draw_list ])
        self.green_max = max([ d.green for d in self.draw_list ])
        self.blue_max = max([ d.blue for d in self.draw_list ])
    
    def add_draw(self, draw : Draw) -> None:
        self.draw_list.append(draw)
        self.red_max = max([self.red_max, draw.red])
        self.green_max = max([self.green_max, draw.green])
        self.blue_max = max([self.blue_max, draw.blue])
    
    def __repr__(self) -> str:
        return f"\nid {self.id};\t[{self.red_max}, {self.green_max}, {self.blue_max}]"
    
    def is_valid(self, red_max : int, green_max : int, blue_max : int) -> bool:
        return ( self.red_max <= red_max ) \
            &  ( self.green_max <= green_max ) \
            &  ( self.blue_max <= blue_max )
    
    def get_id(self) -> int:
        return self.id
    
    def power(self) -> int:
        return self.red_max * self.green_max * self.blue_max


if __name__ == '__main__':
    input_file  = "./DAY 2/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    # Part one - valid games
    red_max = 12
    green_max = 13
    blue_max = 14

    games_list = [ Game(l) for l in lines]
    valid_games = [ Game(l).is_valid(red_max, green_max, blue_max) for l in lines]
    id_sum = 0
    for game in games_list:
        if game.is_valid(red_max, green_max, blue_max):
            id_sum += game.get_id()

    # print(games_list)
    # print(valid_games)
    print(id_sum)

    # Part two - power of set
    ### I already had calculated the max color number for each game to check validity ->
    ### the max number is also the minimal number of cubes required

    games_powers = [ g.power() for g in games_list]
    print(sum(games_powers))


