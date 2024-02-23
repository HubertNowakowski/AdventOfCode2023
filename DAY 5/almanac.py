import re
import sys
import numpy as np
from time import perf_counter
import gc


class Seed:
    def __init__(self, id : int) -> None:
        # if parameters arent mapped they they correspond to same destination
        # so i start with all marameres as seed id and update when needed
        self.id = id
        self.soil = id
        self.fertilizer = id
        self.water = id
        self.light = id
        self.temperature = id
        self.humidity = id
        self.location = id
    
    def __repr__(self) -> str:
        return f"\n{self.id, self.soil, self.fertilizer, self.water, self.light, self.temperature, self.humidity, self.location}"
    
    def update_soil(self, soil_id : int, seed_id : int, range : int):
        # update soil only if seed is in specified range
        if seed_id <= self.id < seed_id + range:
            self.soil = soil_id + (self.id - seed_id)

    # generalised func for setting atribute, i keep the soil example above just as a reminder/test
    def update_attribute(self, dest_attr : str, source_attr : str, destination : int, source : int, range : int) -> bool:
        if source <= getattr(self, source_attr) < source + range:
            setattr(self, dest_attr, destination + getattr(self, source_attr)  - source )
            return 1
        return 0


def update_seeds(seed_list : list[Seed], lines) -> None:
    line_gen = (line for line in lines)

    update_flags = np.zeros(len(seed_list))
    next(line_gen, None) # seed-to-soil map
    while (next_line:= next(line_gen, None)) != None:
        # after list of maps theres an empty line- i use it to break the loop
        if next_line == '\n':
            break
        # for every line update the soil of seeds based on map
        for ii, seed in enumerate(seed_list):
            #if seed was already updated, go to next one (no overlaping ranges, no multiple updates)
            if update_flags[ii] == 1:
                continue
            update_flags[ii] = seed.update_attribute('soil', 'id', *[int(x) for x in next_line.split()])
    # update attributes that didnt map
    for ii, seed in enumerate(seed_list):
        if update_flags[ii] == 0:
            seed.soil = seed.id
        
    # next us the cascade update of attributes
    # it could be automated further with regex to get (destination)-(source) map
    
    update_flags = np.zeros(len(seed_list))
    next(line_gen, None) #soil-to-fertilizer map
    while (next_line:= next(line_gen, None)) != None:
        if next_line == '\n':
            break
        for ii, seed in enumerate(seed_list):
            if update_flags[ii] == 1:
                continue
            update_flags[ii] = seed.update_attribute('fertilizer', 'soil', *[int(x) for x in next_line.split()])
    for ii, seed in enumerate(seed_list):
        if update_flags[ii] == 0:
            seed.fertilizer = seed.soil

    update_flags = np.zeros(len(seed_list))
    next(line_gen, None) # fertilizer-to-water map:
    while (next_line:= next(line_gen, None)) != None:
        if next_line == '\n':
            break
        for ii, seed in enumerate(seed_list):
            if update_flags[ii] == 1:
                continue
            update_flags[ii] = seed.update_attribute('water', 'fertilizer', *[int(x) for x in next_line.split()])
    for ii, seed in enumerate(seed_list):
        if update_flags[ii] == 0:
            seed.water = seed.fertilizer

    update_flags = np.zeros(len(seed_list))
    next(line_gen, None) # water-to-light map:
    while (next_line:= next(line_gen, None)) != None:
        if next_line == '\n':
            break
        for ii, seed in enumerate(seed_list):
            if update_flags[ii] == 1:
                continue
            update_flags[ii] = seed.update_attribute('light', 'water', *[int(x) for x in next_line.split()])
    for ii, seed in enumerate(seed_list):
        if update_flags[ii] == 0:
            seed.light = seed.water

    update_flags = np.zeros(len(seed_list))
    next(line_gen, None) # light-to-temperature map:
    while (next_line:= next(line_gen, None)) != None:
        if next_line == '\n':
            break
        for ii, seed in enumerate(seed_list):
            if update_flags[ii] == 1:
                continue
            update_flags[ii] = seed.update_attribute('temperature', 'light', *[int(x) for x in next_line.split()])
    for ii, seed in enumerate(seed_list):
        if update_flags[ii] == 0:
            seed.temperature = seed.light   

    update_flags = np.zeros(len(seed_list))
    next(line_gen, None) # temperature-to-humidity map:
    while (next_line:= next(line_gen, None)) != None:
        if next_line == '\n':
            break
        for ii, seed in enumerate(seed_list):
            if update_flags[ii] == 1:
                continue
            update_flags[ii] = seed.update_attribute('humidity', 'temperature', *[int(x) for x in next_line.split()])
    for ii, seed in enumerate(seed_list):
        if update_flags[ii] == 0:
            seed.humidity = seed.temperature

    update_flags = np.zeros(len(seed_list))
    next(line_gen, None) # humidity-to-location map:
    while (next_line:= next(line_gen, None)) != None:
        if next_line == '\n':
            break
        for ii, seed in enumerate(seed_list):
            if update_flags[ii] == 1:
                continue
            update_flags[ii] = seed.update_attribute('location', 'humidity', *[int(x) for x in next_line.split()])
    for ii, seed in enumerate(seed_list):
        if update_flags[ii] == 0:
            seed.location = seed.humidity

if __name__ == "__main__":

    input_file  = "./DAY 5/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    # part one
    
    # read file line by line 
    # depending on contents of the line proces next n lines (thats why i need generator)
    # the maps in almanac seem to be in same order in input as in example
    line_gen = (line for line in lines)

    # list of seeds
    line = next(line_gen)
    seed_list = [Seed(int(id)) for id in re.search(r"^seeds:\s(.*)\n", line).group(1).split()]
    update_seeds(seed_list, lines[2:])
    print(min( [seed.location for seed in seed_list] ))

    # # part two
    # line_gen = (line for line in lines)
    # # list of seeds
    # line = next(line_gen)
    # pattern = r"\b(\d+)\b"
    # matches = re.findall(pattern, line)
    # pairs = [(int(matches[ii]), int(matches[ii+1])) for ii in range(0, len(matches), 2) ]
    
    # # print(sum([p[1] for p in pairs])*sys.getsizeof(Seed(1))/(1e9))
    # # with my solution creating all seeds at once would take up 93 gigs of RAM
    # # but I'm looking for minimum location
    # # so i will try a generator of all seed id's and check one by one comparing to current minimum
    # minimum_location = np.iinfo(int).max # set to very high number so every other location is smaller

    # print('create seed_id_gen')
    # seed_id_gen = (ii for p in pairs for ii in range(p[0], p[0]+p[1]))

    # t0 = perf_counter()
    # print('process seeds')
    # while (seed_id := next(seed_id_gen, None)) != None:
    #     t1 = perf_counter()
    #     seed_list = [Seed(seed_id)] + [Seed(seed_id:=next(seed_id_gen, None)) for ii in range(0, 1_000_000) if seed_id is not None]
    #     if seed_list[-1].id is None: seed_list = seed_list[:-1]
    #     print('\tupdating batch of seeds')
    #     # print(seed_list)
    #     update_seeds(seed_list, lines[2:])
    #     minimum_location = np.min([minimum_location] + [seed.location for seed in seed_list])
    #     t2 = perf_counter()
    #     print(f"{minimum_location} ({round((t2-t1)/60,2)} min)")
    #     del seed_list
    #     gc.collect()
    # t2 = perf_counter()
    # print(f"{minimum_location} ({round((t2-t0)/60/60,2)} hours)")