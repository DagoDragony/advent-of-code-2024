import os
import re
from dataclasses import dataclass

from itertools import tee, islice

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d4_example1.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
content = ""
with open(file_path, 'r') as file:
    content = file.read()
print(content)

@dataclass
class Coord:
    i: int
    j: int

def get_coords_to_check

def find_words(i, puzzle_input):
    if puzzle_input[i] == 'X':



def solve1(puzzle_input):



print(f"result1: {solve1(content)}")
print(f"result2: {solve2(content)}")
