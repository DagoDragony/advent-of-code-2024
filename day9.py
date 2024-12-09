import os
import itertools
from collections import defaultdict

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d8_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d8.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
        disk_map = file.read()

print(disk_map)
def find_antennas(map):
    antennas = defaultdict(list)
    for i, row in enumerate(map):
        for j, symbol in enumerate(row):
            if symbol.isalnum():
                antennas[symbol].append((i, j))
    return antennas


def outside_map(i, j, max_i, max_j):
    return i < 0 or j < 0 or i >= max_i or j >= max_j


def get_combination_antinodes(c1, c2):
    i1, j1 = c1
    i2, j2 = c2
    di, dj = i1 - i2, j1 - j2
    return [(i1 + di, j1 + dj), (i2 - di, j2 - dj)]


def get_same_frequency_antinodes(antennas):
    _, coords = antennas
    combinations = itertools.combinations(coords, r=2)
    antinodes_list = []
    [antinodes_list.extend(get_combination_antinodes(c1, c2)) for c1, c2 in combinations]
    return antinodes_list
        

def solve1(map):
    antinodes = []
    max_i, max_j = len(map), len(map[0])
    for antennas in find_antennas(map).items():
        antinodes.extend(get_same_frequency_antinodes(antennas))

    return [coord for coord in antinodes if not outside_map(*coord, max_i, max_j)]
            
print("-"*100)    
print(f"Result1: {len(set(solve1(antenas_map)))}")