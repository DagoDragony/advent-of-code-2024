import os
import itertools
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Tuple

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

@dataclass
class machine:
    button_a: Tuple[int, int]
    button_b: Tuple[int, int]
    prize: Tuple[int, int]

print("PROCESSING PART 1...")
def get_machine_behaviors(file_path):
    print(f"Reading file {file_path}")
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    machine_behaviors = [lines[i:i+n] for n in range(0, len(lines), 4)]
    machine_strings = [machine for machine in machine_behaviors]
    

    return garden


directions = {
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
}


def is_outside(i, j, mi, mj):
    return i < 0 or j < 0 or i >= mi or j >= mj


def get_cords_around(i, j, max):
    mi, mj = max
    return [(i + di, j + dj) for di, dj in directions if not is_outside(i + di, j + dj, mi, mj)]


def get_same_around(coord, name, used, garden):
    max = (len(garden), len(garden[0]))
    i, j = coord
    new_and_same_around = [(ni, nj) for ni, nj in get_cords_around(i, j, max) if not (ni, nj) in used and garden[ni][nj] == name]
    used.update(new_and_same_around)
    return new_and_same_around


def get_connected(coord, garden, name):
    used = set()
    used.add(coord)
    i, j = coord
    extensions = get_same_around((i, j), name, used, garden)
    while extensions:
        new_values = []
        for c in extensions:
            new_values.extend(get_same_around(c, name, used, garden))
        extensions = new_values
    return used

def get_regions(garden):
    used = set()
    regions = []
    for i, row in enumerate(garden):
        for j, symbol in enumerate(row):
            if not (i, j) in used:
                region = get_connected((i, j), garden, symbol)
                regions.append(region)
                used.update(region)
    return regions

def move_in_direction(c, d):
    i, j = c
    di, dj = d
    return (i+di, j+dj)


def get_down_coord(c):
    return move_in_direction(c, (1, 0))
def get_up_coord(c):
    return move_in_direction(c, (-1, 0))
def get_right_coord(c):
    return move_in_direction(c, (0, 1))
def get_left_coord(c):
    return move_in_direction(c, (0, -1))
    

def get_perimeter_and_area(region):
    area = len(region)
    perimeter = 0
    for i, j in region:
        outside_count = sum([1 for di, dj in directions if not (i+di, j+dj) in region])
        perimeter += outside_count
    return (perimeter, area)

def get_ranges(region):
    all_i = [i for i, _ in region]
    all_j = [j for _, j in region]
    return (min(all_i), max(all_i), min(all_j), max(all_j))

def get_perimeter_and_area_with_dicount(region, name):
    area = len(region)
    min_i, max_i, min_j, max_j = get_ranges(region)

    print("Region")
    print(region)

    up_count = 0
    down_count = 0
    left_count = 0
    right_count = 0
    for i in range(min_i, max_i + 1):
        has_last_up = False
        has_last_down = False
        for j in range(min_j, max_j + 1):
            if not (i, j) in region: 
                has_last_up = False
                has_last_down = False
                continue
            up = get_up_coord((i, j))
        
            if not up in region:
                if not has_last_up:
                    has_last_up = True
                    up_count += 1
            else:
                has_last_up = False
            
            down = get_down_coord((i, j))
        
            if not down in region:
                if not has_last_down:
                    has_last_down = True
                    down_count += 1
            else:
                has_last_down = False

        # if has_last_up:
        #     up_count += 1

        # if has_last_down:
        #     down_count += 1

    for j in range(min_j, max_j + 1):
        has_last_left = False
        has_last_right = False
        for i in range(min_i, max_i + 1):
            if not (i, j) in region: 
                has_last_left = False
                has_last_right = False
                continue
            left = get_left_coord((i, j))
            print((i, j))
        
            if not left in region:
                if not has_last_left:
                    has_last_left = True
                    left_count += 1
            else:
                has_last_left = False
                # print("Added left on", (i, j))
            
            right = get_right_coord((i, j))
        
            if not right in region:
                if not has_last_right:
                    has_last_right = True
                    right_count += 1
            else:
                has_last_right = False
                print("Added right on", (i, j))

        # if has_last_left:
        #     # print("2Added left on", (i, j))
        #     left_count += 1

        # if has_last_right:
        #     print("2Added right on", (i, j))
        #     right_count += 1
    
    print(f"name {name} up {up_count} down {down_count} left {left_count} right {right_count}")
    perimeter = up_count+right_count+left_count+down_count
    print("Perimeter", perimeter)
    return (perimeter, area)



# file_path = os.path.join(script_dir, 'inputs/input_d12_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d12_example0.txt')
file_path = os.path.join(script_dir, 'inputs/input_d12.txt')
garden = get_garden(file_path)
print("Garden")
print("-" * 100)
for row in garden:
    print(row)

regions = get_regions(garden)
# products_sum = 0
# for region in regions:
#     print(region)
#     i, j = next(iter(region))
#     name = garden[i][j]
#     perimeter, area = get_perimeter_and_area(region)
#     products_sum += perimeter * area
#     print(f"Name: {name}, P: {perimeter}, A: {area}, R: {perimeter*area}")

# print(f"Result1: {products_sum}")

products_sum = 0
for region in regions:
    print(region)
    i, j = next(iter(region))
    name = garden[i][j]
    perimeter, area = get_perimeter_and_area_with_dicount(region, name)
    products_sum += perimeter * area
    print(f"Name: {name}, P: {perimeter}, A: {area}, R: {perimeter*area}")

print(f"Result2: {products_sum}")