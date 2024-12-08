import os
from typing import List, AnyStr
# from itertools import distinct_permutations
from more_itertools import distinct_permutations
import itertools
import sys
import re

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


            
find_antennas(antenas_map) 

print("-"*100)    
print(f"Result: ")
    

# # print(f"result1: {solve1(content)}")
