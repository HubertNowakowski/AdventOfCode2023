import re

def decode_line(line):
    digit_one = re.search(r'\d', line).group(0)
    digit_two = re.search(r'\d', line[::-1]).group(0)
    return 10*int(digit_one) + int(digit_two)


if __name__ == "__main__":
    input_file  = "./DAY 1/input.txt"
    with open(input_file, "r") as f:
        calibration_values = [ decode_line(l) for l in f]
    print(sum(calibration_values))
