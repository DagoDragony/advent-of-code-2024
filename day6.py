import os

import numpy as np

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d6_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d6.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
lab_map = {}
with open(file_path, 'r') as file:
    lab_map = [line.strip() for line in file.readlines()]

for line in lab_map:
    print(line)

def get_current_position(map):
    for i in range(len(map)):
        for j in range (len(map[0])):
            if map[i][j] == '^':
                return (i, j)

def outside_map(i, j, map):
    return i < 0 or j < 0 or i >= len(map) or j >= len(map[0])

righ_changes = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}

def set_walked(i, j, map):
    line = list(map[i])
    line[j] = "X"
    map[i] = ''.join(line)
    # for l in map:
    #     print(l)

def count_walked(map):
    # print(map)
    return sum([True for i in range(len(map)) for j in range(len(map[0])) if map[i][j] == 'X'])

def print_map(map):
    for l in map:
        print(l)

def walk(map):
    i, j = get_current_position(map)
    already_walked = 0

    set_walked(i, j, map)
    direction = (-1, 0)
    while(True or already_walked > 1000000):
        ni, nj = (i + direction[0], j + direction[1])
        if outside_map(ni, nj, map):
            # print(ni, nj)
            break;
            # return already_walked
        elif map[ni][nj] == '#':
            # print("#", ni, nj)
            direction = righ_changes[direction]
            # print(direction)
            i, j = (i + direction[0], j + direction[1]) 
            if(map[i][j] != 'X'):
                already_walked += 1
            # print(i, j)
        else:
            i, j = (ni, nj)
            # print(i, j)
            if(map[i][j] != 'X'):
                already_walked += 1
        # print(already_walked)
        set_walked(i, j, map)
    
    return count_walked(map)
    # return already_walked

result = walk(lab_map)
print("-"*100)    

print_map(lab_map)
print(result)
# # print(f"result2: {solve2(content)}")
