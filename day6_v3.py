import os
from collections import defaultdict

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d6.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d6.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
    lab_map = [line.strip() for line in file]

for line in lab_map:
    print(line)

def find_start(map):
    for i, line in enumerate(map):
        for j, s in enumerate(line):
            if s == "^":
                return (i, j)

direction_up = (-1, 0)
turn_righ = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0)
}

def outside(c, max):
    i, j = c
    mi, mj = max
    return i < 0 or j < 0 or i >= mi or j >= mj


def move(c, direction):
    i, j = c
    di, dj = direction
    return (i + di, j + dj)


def get_initial_path(start, map):
    i, j = start
    direction = direction_up
    visited = set([(i, j)])
    while True:
        ni, nj = move((i, j), direction)
        if outside((ni, nj), (len(map), len(map[0]))):
            break
        elif map[ni][nj] == "#":
            direction = turn_righ[direction]
            i, j = move((i, j), direction)
        else:
            i, j = ni, nj
        visited.add((i, j))
    return visited

start = find_start(lab_map)
print("start", start)
initial_path = get_initial_path(start, lab_map)
print("initial path length", len(initial_path))
