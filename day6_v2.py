import os
from collections import defaultdict

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/d6_example1.txt')
file_path = os.path.join(script_dir, 'inputs/d6.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
    lab_map = [line.strip() for line in file]

for line in lab_map:
    print(line)

def get_current_position(map):
    for i, row in enumerate(map):
        for j, symbol in enumerate(row):
            if symbol == '^':
                return (i, j)

def outside_map(i, j, map):
    return i < 0 or j < 0 or i >= len(map) or j >= len(map[0])

righ_changes = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}

obstacle_symbols = set()
obstacle_symbols.add("#")
obstacle_symbols.add("O")

def print_map(map):
    for l in map:
        print(l)

def process_path_history(c, direction, path_history):
    if c in  path_history and direction in path_history[c]:
        return True
    else:
        path_history[c].add(direction)
    return False

def is_loop_walk(i, j, map):
    path_history = defaultdict(set)
    direction = (-1, 0)
    path_history[(i, j)].add(direction)
    while(True):
        ni, nj = move(i, j, direction)
        if outside_map(ni, nj, map):
            break
        elif map[ni][nj] in obstacle_symbols:
            direction = righ_changes[direction]
            if process_path_history((i, j), direction, path_history):
                return path_history

            i, j = move(i, j, direction)

            if process_path_history((i, j), direction, path_history):
                return path_history
        else:
            i, j = (ni, nj)
            if process_path_history((i, j), direction, path_history):
                return path_history
    return {}


def move(i, j, direction):
    return (i + direction[0], j + direction[1])


def get_initial_path(i, j, map):
    direction = (-1, 0)
    passed_path = set([(i, j)])
    while(True):
        ni, nj = move(i, j, direction)
        if outside_map(ni, nj, map):
            break
        elif map[ni][nj] in obstacle_symbols:
            direction = righ_changes[direction]
            i, j = move(i, j, direction)
            passed_path.add((i, j))
        else:
            i, j = (ni, nj)
            passed_path.add((i, j))
    return passed_path


def add_obstacle(i, j, map):
    new_map = list(map)
    new_line = list(map[i])
    new_line[j] = "O"
    new_map[i] = "".join(new_line) 
    return new_map

def get_map_combinations(si, sj, map, path):
    return [add_obstacle(i, j, map) for i, j in path if not (i == si and j == sj)]

def print_infinite_path(path, m):
    # print(path)
    for i, row in enumerate(m):
        line = list(row)
        for j, symbol in enumerate(row):
            # print(line)
            if (i, j) in path:
                h = list(path[(i, j)])
                im, jm = 0, 0
                for c in h:
                    hi, hj = c
                    im += abs(hi)
                    jm += abs(hj)
                    # print(im, jm)
                if im != 0 and jm != 0:
                    line[j] = "+"
                elif im != 0:
                    line[j] = "|"
                elif jm != 0:
                    line[j] = "-"
                else:
                    line[j] = "8"
        print("".join(line))
    print()


def solve2(start, map, path):
    start_i, start_j = start
    inifinite_loops = 0
    for m in get_map_combinations(start_i, start_j, map, path):
        # print("Combination")
        # print_map(m)
        infinite_path = is_loop_walk(start_i, start_j, m)
        if len(infinite_path) > 0:
            inifinite_loops += 1
            # print_infinite_path(infinite_path, m)
    return inifinite_loops


start_i, start_j = get_current_position(lab_map)
current_path = get_initial_path(start_i, start_j, lab_map)
print("-"*100)    
print(f"Result1: {len(current_path)}")

result2 = solve2((start_i, start_j), lab_map, current_path)

print(f"Result2: {result2}")

# print_map(lab_map)
# # print(f"result2: {solve2(content)}")
