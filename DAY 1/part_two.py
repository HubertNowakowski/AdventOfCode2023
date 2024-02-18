import re
from part_one import decode_line


def replace_numbers(line : str, p, d : dict):
    return  p.sub(lambda x: d[x.group()], line)


def improved_decode_line(line: str, d: dict):
    line_forward = line
    line_backward = line[::-1]
    
    first_string_num = re.search(r"" + "|".join(d.keys()), line)
    if first_string_num is not None:
        line_forward = line_forward.replace(first_string_num.group(0), d[first_string_num.group(0)])
    digit_one = digit_one = re.search(r'\d', line_forward).group(0)
    
    last_string_num = re.search(r"" + "|".join([key[::-1] for key in d.keys()]), line[::-1])
    if last_string_num is not None:
        line_backward = line_backward.replace(last_string_num.group(0), d[last_string_num.group(0)[::-1]])
    digit_two = re.search(r'\d', line_backward).group(0)
    return 10*int(digit_one) + int(digit_two)


if __name__ == "__main__":
    # dict mapping digits to their spelling
    numbers_dict = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }


    input_file  = "./DAY 1/input.txt"
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    calibration_values = [ improved_decode_line(l, numbers_dict) for l in lines]
    print(sum(calibration_values))

