import os
from typing import List, AnyStr
# from itertools import distinct_permutations
from more_itertools import distinct_permutations
import itertools
import sys
import re

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d8_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d8.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
antenas_map = []
with open(file_path, 'r') as file:
    for line in file.readlines():
        # print(line)
        antenas_map.append(line.strip())

for line in antenas_map:
    print(line)

def find_antennas(map):
    antennas = {}
    for i in range(len(map)):
        for j in range(len(map[0])):
            symbol = map[i][j]
            if symbol.isalnum():
                if symbol in antennas:
                    antennas[symbol].append((i, j))
                else:
                    antennas[symbol] = [(i, j)]
    print(antennas)
    return antennas


def outside_map(i, j, max_i, max_j):
    return i < 0 or j < 0 or i >= max_i or j >= max_j


def get_combination_antinodes(c1, c2):
    i1, j1 = c1
    i2, j2 = c2
    di = i1 - i2
    dj = j1 - j2
    return [(i1 + di, j1 + dj), (i2 - di, j2 - dj)]


def get_same_frequency_antinodes(antennas):
    print(antennas)
    for antenna_name, coords  in antennas:
        combinations = itertools.combinations(coords, r=2)
        for c1, c2 in combinations:
            get_combination_antinodes(c1, c2)

def solve1(map):
    antinodes = []
    max_i = len(map)
    max_j = len(map[0])
    for antennas in find_antennas(map):
        antinodes.extend(get_same_frequency_antinodes(antennas))

    return [coord for coord in antinodes if not outside_map(coord, max_i, max_j)]

            
find_antennas(antenas_map) 

print(solve1(antenas_map))

print("-"*100)    
print(f"Result: ")
    

# # print(f"result1: {solve1(content)}")
