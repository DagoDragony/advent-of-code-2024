import os
import itertools
from collections import defaultdict

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d11_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d11.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
        initial_stones = [int(str_stone) for str_stone in file.read().strip().split(" ") ] 

def solve2(stones):
    stones_lists = [list(stone) for stone in stones]
    for i, stone in  stones_lists:
        if stone[0] == 0:
             stone[0] == 1
        elif (len(stone[0]) % 2 == 0):
            str_stone = stone[0]
            middle_index = str_stone / 2
            stones.extend([int(str_stone[middle_index:]), int(str_stone[:middle_index])])

        if len(stones)




print("Initial stones")
print(initial_stones)



