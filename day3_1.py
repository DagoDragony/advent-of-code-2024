import os
import re

from itertools import tee, islice

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_3_1_example.txt')
file_path = os.path.join(script_dir, 'inputs/input_3_1_example.txt')

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

def solve2(content):
    start_pattern = r"^(.*?)(don't()|do())"
    do_patern = r"do\(\).*?(don't()|$)"
    start = re.findall(start_pattern, content)
    dos = re.findall(start_pattern, content)
    print(f"Start {start}")
    print(f"Do's {dos}")



print(f"result1: {solve1(content)}")
print(f"result2: {solve2(content)}")
