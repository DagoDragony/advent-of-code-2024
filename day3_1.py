import os
import re

from itertools import tee, islice

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_3_1_example.txt')
file_path = os.path.join(script_dir, 'inputs/input_3_1.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
content = ""
with open(file_path, 'r') as file:
    content = file.read()
# print(content)

def solve1(content):
    pattern = r"mul\((\d+),(\d+)\)"
    raw_commands = re.findall(pattern, content)
    # print(raw_commands)
    return sum([int(a) * int(b) for a, b in raw_commands])

def isdont(it):
    for c in "don't()":
        if(it)


def solve1_v2(content):
    it = iter(content)
    iter1, iter2 = tee(it, 2)
    # even_chars = islice(iter1, 5)
    isdont(tee(content))




print(f"result1: {solve1(content)}")
