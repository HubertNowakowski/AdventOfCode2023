import re
import sys
import numpy as np
from time import perf_counter
import gc


class MyRange():
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end
    
    def length(self):
        return self.end - self.start + 1

    def __repr__(self) -> str:
        return f" {self.start} {self.end}"
    
    def split_range(self, source_start, source_end, offset):
        # return self when nothing is mapped (start after map or end before map)
        if self.start > source_end or self.end < source_start:
            return [self], []
        
        unpammed_list = []
        mapped_list = []
        # if range start before map, then split the part before to the list (it stays unmapped)
        # and move the start of range that is to be mapped
        if self.start < source_start:
            unpammed_list.append(MyRange(self.start, source_start-1))
            self.start = source_start
        # same thing as above but on the other side of range
        if self.end > source_end:
            unpammed_list.append(MyRange(source_end+1, self.end))
            self.end = source_end
        
        # map the range
        if self.length() > 0:
            self.start = self.start + offset
            self.end = self.end + offset
            mapped_list.append(self)
        
        return unpammed_list, mapped_list


if __name__ == '__main__':
    input_file  = "./DAY 5/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
    # part two
    line_gen = (line for line in lines)
    # list of seeds
    line = next(line_gen)
    pattern = r"\b(\d+)\b"
    matches = re.findall(pattern, line)
    pairs = [(int(matches[ii]), int(matches[ii+1])) for ii in range(0, len(matches), 2) ]

    seed_ranges = [MyRange(p[0], p[0]+p[1]) for p in pairs]
    seed_ranges = sorted(seed_ranges, key=lambda x: x.start)
    next(line_gen, None)


    map_list = ["seed-to-soil",
                "soil-to-fertilizer",
                "fertilizer-to-water",
                "water-to-light",
                "light-to-temperature",
                "temperature-to-humidity",
                "humidity-to-location",
                ]
    
    for m in map_list:
        next(line_gen, None) # line before x-to-y map
        mapped_ranges = []
        while (next_line:= next(line_gen, None)) != None:
            # after list of maps theres an empty line- i use it to break the loop
            if next_line == '\n':
                break
            dest_start, source_start, length = (int(x) for x in next_line.split())
            
            unmapped_ranges = []
            for sr in seed_ranges:
                unmapped, mapped = sr.split_range(source_start, source_start+length-1, dest_start-source_start)
                unmapped_ranges += unmapped
                mapped_ranges += mapped
            seed_ranges = unmapped_ranges
        seed_ranges = sorted(mapped_ranges + unmapped_ranges, key=lambda x: x.start)
    print(min([sr.start for sr in seed_ranges]))
   