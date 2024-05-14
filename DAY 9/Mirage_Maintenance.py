import re
import pandas as pd
import numpy as np


if __name__ == "__main__":

    input_file  = "./DAY 9/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    # part 1
    sum_predictions = 0
    for ii, line in enumerate(lines):
        # print(f"## {ii} ##")
        sequence = np.fromstring(line, dtype=int, sep=' ')
        prediction = 0
        
        seq_list = []
        while any(sequence) != 0:
            seq_list.append(sequence)
            # print(sequence)
            prediction += sequence[-1]
            sequence = np.diff(sequence)
            # if sequence[-1] == 5: print(ii)
        # print(seq_list)
        # print(ii, prediction)
        sum_predictions += prediction

    print(f"Sum of predictions: {sum_predictions}")
