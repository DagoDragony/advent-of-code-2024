import os
import itertools
from collections import defaultdict

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d10_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d10.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
        topographic_map = [line.strip() for line in file]

for line in topographic_map:
    print(line)

direction = [
      (-1, 0),
      (1, 0),
      (0, -1),
      (0, 1)
]

def is_outside_map(c, max):
    i, j = c
    mi, mj = max
    return i < 0 or i >= mi or j < 0 or j >= mj 

def get_all_trailheads(map):
      return [(i, j) for i, row in enumerate(map) for j, s in enumerate(row) if s == "0"]



def get_trailhead_score(start, map):
    i, j = start
    for h in range(10):
        moves = [(i+di, j+dj) for di, dj in direction]





def solve2(map):
    trailheads = get_all_trailheads(map)
    return sum([get_trailhead_score(c, map) for c in trailheads])

print(f"Result: {solve2(topographic_map)}")


