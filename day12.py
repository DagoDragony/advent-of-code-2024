import os
import itertools
from collections import defaultdict, deque

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d12_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d12.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
    garden = [line.strip() for line in file] 

print("Garden")
print("-" * 100)
for row in garden:
    print(row)
