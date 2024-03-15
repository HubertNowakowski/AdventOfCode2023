import re
import functools


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

def steps_to_next_end(node, instr_start):
    global node_dict
    current_node = node
    step_counter = 0
    
    move = instructions[(instr_start+step_counter)%len(instructions)]
    current_node = node_dict[current_node.get_next(move)]
    step_counter += 1

    while not current_node.is_endnode():
        move = instructions[(instr_start+step_counter)%len(instructions)]
        current_node = node_dict[current_node.get_next(move)]
        step_counter += 1
    return step_counter, current_node

# helper math functions
def gcd(a,b):
    while b:
        a,b = b, a%b
    return a
def lcm(a,b):
    return a*b // gcd(a,b)


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

    path_lengths = [steps_to_next_end(node, 0) for node in current_nodes]
    print(path_lengths)
    path_lengths2 = [steps_to_next_end(node, start) for start, node in path_lengths]
    print(path_lengths2)

    # if path length from A->Z and then Z->Z is the same then we can calculate LCM and be done
    path_check = [pl1[0]==pl2[0] for pl1, pl2 in zip(path_lengths, path_lengths2)]
    print(path_check)
    # all true (i also see that its the same end node, end nodes loop)
    if all(path_check):
        lengths = [l for l, node in path_lengths]
        LCM = functools.reduce(lambda x, y: lcm(x, y), lengths)
        print(LCM)
    else:
        print("Path length A->Z and Z->Z is not always equal")
