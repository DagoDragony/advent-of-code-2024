import os
import re

from itertools import tee, islice

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_3_1_example.txt')
# file_path = os.path.join(script_dir, 'inputs/input_3_2_example.txt')
file_path = os.path.join(script_dir, 'inputs/input_d3.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
content = ""
with open(file_path, 'r') as file:
    content = file.read()
print(content)

mul_pattern = r"mul\((\d+),(\d+)\)"

def get_mul_result(report):
    raw_commands = re.findall(mul_pattern, report)
    # print(raw_commands)
    return sum([int(a) * int(b) for a, b in raw_commands])

def solve1(report):
    return get_mul_result(report)

def solve2(report):
    unfiltered_dos = report.split("do()")
    filtered_dos = "".join([unfiltered_do.split("don't")[0] for unfiltered_do in unfiltered_dos])
    return get_mul_result(filtered_dos)

print(f"result1: {solve1(content)}")
print(f"result2: {solve2(content)}")
