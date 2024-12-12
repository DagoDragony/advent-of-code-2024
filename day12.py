import os
import itertools
from collections import defaultdict, deque

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

print("PROCESSING PART 1...")
def get_garden(file_path):
    print(f"Reading file {file_path}")
    with open(file_path, 'r') as file:
        garden = [line.strip() for line in file] 
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



def get_perimeter_and_area(region):
    area = len(region)
    perimeter = 0
    for i, j in region:
        outside_count = sum([1 for di, dj in directions if not (i+di, j+dj) in region])
        perimeter += outside_count
    return (perimeter, area) 


# file_path = os.path.join(script_dir, 'inputs/input_d12_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d12.txt')
garden = get_garden(file_path)
print("Garden")
print("-" * 100)
for row in garden:
    print(row)

regions = get_regions(garden)
products_sum = 0
for region in regions:
    print(region)
    i, j = next(iter(region))
    name = garden[i][j]
    perimeter, area = get_perimeter_and_area(region)
    products_sum += perimeter * area
    print(f"Name: {name}, P: {perimeter}, A: {area}, R: {perimeter*area}")

print(f"Result1: {products_sum}")