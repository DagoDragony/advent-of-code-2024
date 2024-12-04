import os
import re
from dataclasses import dataclass

from itertools import tee, islice

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d4_example1.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
puzzle_map = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        puzzle_map.append(line.strip())

print(puzzle_map)

def get_coords_to_check(puzzle_map, coord):
    max_i = len(puzzle_map[0])
    max_j = len(puzzle_map)
    coords = [(coord[0] + i, coord[1] + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if not(i == 0 and j == i)]
    return [ c for c in coords if c[0] < max_i and c[1] < max_j]


get_coords_to_check(puzzle_map)


# def find_words(i, puzzle_input):
#     if puzzle_input[i] == 'X':



# def solve1(puzzle_input):



# print(f"result1: {solve1(content)}")
# print(f"result2: {solve2(content)}")
