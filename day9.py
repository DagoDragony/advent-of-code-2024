import os
import itertools
from collections import defaultdict

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d9_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d9.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
        disk_map = file.read()

print(disk_map)

def expand_disk_map(map):
    expanded_disk_map = []
    for i, symbol in enumerate(map):
        nmb = int(symbol)
        if i % 2 == 0:
            expanded_disk_map.append([str(i // 2) for n in range(nmb)])
        else:
            expanded_disk_map.append(["." for n in range(nmb)])
    return expanded_disk_map

def compact_disk_map(expaded_disk_map):
    dm = list(expanded_disk_map)
    is_full = False
    i = 0
    empty_spaces = [(i, j) for i, block in enumerate(expanded_disk_map) for j in range(len(block)) if i % 2 == 1]
    numbers = list(reversed([(i, j) for i, block in enumerate(expanded_disk_map) for j in range(len(block)) if i % 2 == 0]))

    last_emptied = (9999999, 99999999)
    for i in range(len(empty_spaces)):
        ei, ej = empty_spaces[i]
        ni, nj = numbers[i]

        if expaded_disk_map[ni][nj] == '.':
            # print(ei, ej, ni, nj)
            break

        if last_emptied < (ei, ej):
            print("last_emptied < (ei, ej)")
            break
            lei, lej = last_emptied
            expanded_disk_map[lei][lej] = expaded_disk_map[ni][nj]
        else:
            expanded_disk_map[ei][ej] = expaded_disk_map[ni][nj]

        expanded_disk_map[ni][nj] = '.'
        last_emptied = (ni, nj)

        print("".join(["".join(ls) for i, ls in enumerate(expanded_disk_map)]))

# 00 998 111 888 2 777 333 6 44 6 555 566
expanded_disk_map = expand_disk_map(disk_map)
print(expanded_disk_map)
# print("".join(expanded_disk_map))
compact_disk_map(expanded_disk_map)
for l in expanded_disk_map:
    print(l)
print(expanded_disk_map)
            
print("-"*100)    
print(f"Result1: ")