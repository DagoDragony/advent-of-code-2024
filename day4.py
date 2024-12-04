import os

import numpy as np

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d4_example1_custom.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d4_example1_custom2.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d4_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d4.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
puzzle_map = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        puzzle_map.append(line.strip())

print(puzzle_map)


def get_coords_to_check(oi, oj, puzzle_map):
    max_i = len(puzzle_map)
    max_j = len(puzzle_map[0])
    coords = [(oi + i, oj + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == 0 and j == i)]
    result = [(ci, cj) for ci, cj in coords if ci >= 0 and cj >= 0 and ci < max_i and cj < max_j]
    # print(result)
    return result

def find_letter_arround(i, j, letter, puzzle):
    around_coords = get_coords_to_check(i, j, puzzle_map)
    result = [(ni, nj) for ni, nj in around_coords if puzzle[ni][nj] == letter]
    # print(f"{letter} {result}")
    return result

def check_XMAS(i, j, puzzle):
    found = 0
    if puzzle[i][j] == 'X':
        print(f"found X {i} {j}")
        print("------------------")
        foundM = find_letter_arround(i, j, 'M', puzzle)
        print(f"found M {foundM}")
        print("------------------")
        foundM = find_letter_arround(i, j, 'M', puzzle)
        for mi, mj in foundM:
            # print(f"MIJ {mi} {mj}")
            foundA = find_letter_arround(mi, mj, 'A', puzzle)
            print(f"found A {foundA}")
            print("------------------")
            foundM = find_letter_arround(i, j, 'M', puzzle)
            for ai, aj in foundA:
                foundS = find_letter_arround(ai, aj, 'S', puzzle)
                print(f"found S {foundS}")
                print("------------------")
                found += len(foundS)
    return found

# count = sum([check_XMAS(i, j, puzzle_map) for i in range(len(puzzle_map)) for j in range(len(puzzle_map[0]))])
# print(f"count: {count}")

# right = (0, 1)
# left = (0, -1)
# up = (-1, 0)
# down = (1, 0)
# ne = (-1, 1)
# nw = (-1, -1)
# se = (1, 1)
# sw = (1, -1)
xmas_letters = "XMAS"
all_directions = [
    (0, 1),
    (0, -1),
    (1, 0),
    (1, 1),
    (1, -1),
    (-1, 0),
    (-1, 1),
    (-1, -1)
]

def check_in_direction(i, j, direction, puzzle):
    max_i = len(puzzle)
    max_j = len(puzzle[0])
    def valid_coord(_i, _j):
        return _i >= 0 and _i < max_i and _j >= 0 and _j < max_j

    print(f"Direction {direction}")
    i_shift, j_shift = direction
    for index in range(1, 4):
        ni, nj = (i + index * i_shift, j + index * j_shift )
        if not valid_coord(ni, nj):
            return False
        print((ni, nj), puzzle[ni][nj])
        if puzzle[ni][nj] != xmas_letters[index]:
            return False
    print("Found")
    return True
        
def check_XMAS(i, j, puzzle):
    print(xmas_letters[0])
    if puzzle[i][j] == xmas_letters[0]:
        return sum([check_in_direction(i, j, direction, puzzle)  for direction in all_directions])
    return 0

count = sum(check_XMAS(i, j, puzzle_map) for i in range(len(puzzle_map)) for j in range(len(puzzle_map[0])))
print(f"result1: {count}")


correct_combs = [
    "MMSS",
    "SMMS",
    "SSMM",
    "MSSM",
]

def is_right_comb(i, j, puzzle):
    comb = puzzle[i-1][j-1] + puzzle[i-1][j+1] + puzzle[i+1][j+1] + puzzle[i+1][j-1]
    print(comb)
    if comb in correct_combs:
        return True
    return False

def solve2(puzzle):
    a_coords = [(i, j) for i in range(1, len(puzzle) - 1) for j in range(1, len(puzzle[0]) - 1) if puzzle[i][j] == "A"]
    print(a_coords)
    return sum([is_right_comb(i, j, puzzle) for i, j in a_coords])
    

print(f"result2: {solve2(puzzle_map)}")


# def get_coords_to_check2(i, j, puzzle_map):
#     max_i = len(puzzle_map)
#     max_j = len(puzzle_map[0])
#     def valid_coord(_i, _j):
#         return _i >= 0 and _i < max_i and _j >= 0 and _j < max_j

#     horizonal_right = [(i, j + s) for s in range(1, 4) if valid_coord(i, j+s)]
#     horizonal_left = [(i, j - s) for s in range(1, 4) if valid_coord(i, j -s)]



#     coords = [(oi + i, oj + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == 0 and j == i)]
#     result = [(ci, cj) for ci, cj in coords if ci >= 0 and cj >= 0 and ci < max_i and cj < max_j]
#     # print(result)
#     return result

# count = check_XMAS(0, 4, puzzle_map)
# print(f"count: {count}")

# print(np.add((1, 2), (3, 4)))

# def find_words(i, puzzle_input):
#     if puzzle_input[i] == 'X':



# def solve1(puzzle_input):



# print(f"result1: {solve1(content)}")
# print(f"result2: {solve2(content)}")
