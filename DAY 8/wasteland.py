import re


class Node():
    def __init__(self, name: str, left: str, right: str) -> None:
        self.name = name
        self.left = left
        self.right = right
    
    def __repr__(self) -> str:
        return f"{self.name} = ({self.left}, {self.right})\n"
    
    def is_endnode(self) -> bool:
        return self.name[2] =='Z'
    
    def get_next(self, move: str) -> str:
        if move == 'L': 
            return self.left
        elif move == 'R': 
            return self.right


if __name__ == "__main__":

    input_file  = "./DAY 8/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
    instructions = lines[0].strip()

    node_dict = { match[0]:Node(match[0], match[1], match[2]) \
                 for l in lines for match in re.findall(r"([A-Z0-9]+)\s=\s\(([A-Z0-9]+),\s([A-Z0-9]+)\)", l.strip()) }
   
    # part one
    # current_node = 'AAA'
    # end_node = 'ZZZ'
    # step_counter = 0

    # print(f"start node: {current_node}")
    # while current_node != end_node:
    #     move = instructions[step_counter%len(instructions)]
    #     # print( f"step: {step_counter} -> {move}" )
    #     if move == 'L': current_node = node_dict[current_node].left
    #     elif move == 'R': current_node = node_dict[current_node].right
    #     else: 
    #         raise ValueError
    #     step_counter += 1

    # print(f"end node: {current_node}\nsteps taken: {step_counter}")

    # part two
    # print(node_dict)
    current_nodes = [node_dict[key] for key in node_dict.keys() if key[2]=='A']
    print(current_nodes)

    step_counter = 0

    while not all([n.is_endnode() for n in current_nodes]):
        move = instructions[step_counter%len(instructions)]
        if step_counter%1e9 == 0: 
            print( f"step: {step_counter} -> {move} || {[n.is_endnode() for n in current_nodes]} || {[n.name for n in current_nodes]}" )
        current_nodes = [node_dict[node.get_next(move)] for node in current_nodes]
        step_counter += 1
    print(current_nodes)
    print(f"steps taken: {step_counter}")
        
