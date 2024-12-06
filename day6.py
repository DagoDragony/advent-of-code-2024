import os

import numpy as np

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d6_example1.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
lab_map = {}
with open(file_path, 'r') as file:
    lab_map = [line.strip() for line in file.readlines()]

for line in lab_map:
    print(line)


# # print(f"result2: {solve2(content)}")
