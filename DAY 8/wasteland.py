import re


class Node():
    def __init__(self, name: str, left: str, right: str) -> None:
        self.name = name
        self.left = left
        self.right = right
    
    def __repr__(self) -> str:
        return f"{self.name} = ({self.left}, {self.right})\n"


if __name__ == "__main__":

    input_file  = "./DAY 8/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
    instructions = lines[0].strip()
    # lines = lines[2:10]

    node_dict = { match[0]:Node(match[0], match[1], match[2]) \
                 for l in lines for match in re.findall(r"([A-Z]+)\s=\s\(([A-Z]+),\s([A-Z]+)\)", l.strip()) }
   
    # part one
    current_node = 'AAA'
    end_node = 'ZZZ'
    step_counter = 0

    print(f"start node: {current_node}")
    while current_node != end_node:
        move = instructions[step_counter%len(instructions)]
        # print( f"step: {step_counter} -> {move}" )
        if move == 'L': current_node = node_dict[current_node].left
        elif move == 'R': current_node = node_dict[current_node].right
        else: 
            raise ValueError
        step_counter += 1

    print(f"end node: {current_node}\nsteps taken: {step_counter}")

        
