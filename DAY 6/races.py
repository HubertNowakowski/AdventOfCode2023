import numpy as np
import math

def count_ways(t, max_d) -> int:
    p = np.arange(0,t+1,1)
    d = p*(t-p)
    return sum(d>max_d)

if __name__ == "__main__":
    input_file  = "./DAY 6/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    # part one
    times = [ int(x) for x in lines[0].split()[1:] ]
    dist_records = [ int(x) for x in lines[1].split()[1:] ]
    print ( *zip(times, dist_records) )
    ways_counts = [ count_ways(t,d) for t,d in zip(times, dist_records) ]
    print(np.prod(ways_counts))

    # part two
    time = int(''.join(lines[0].split()[1:]))
    distance = int(''.join(lines[1].split()[1:]))
    print(time, distance)
    # "brute force" counting the points returns 0
    # probably int overflow or smth similar
    # ways = count_ways(time, distance)
    # print(ways)

    # guess i have to actually solve the quadratic then
    p1 = time/2 - math.sqrt( time**2 - 4*distance )/2
    p2 = time/2 + math.sqrt( time**2 - 4*distance )/2
    print( int( np.floor(p2) - np.ceil(p1) +1))
