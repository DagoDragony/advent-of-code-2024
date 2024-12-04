import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d4_example1_custom.txt')
file_path = os.path.join(script_dir, 'inputs/input_d4_example1.txt')

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

count = check_XMAS(0, 4, puzzle_map)
print(f"count: {count}")

# def find_words(i, puzzle_input):
#     if puzzle_input[i] == 'X':



# def solve1(puzzle_input):



# print(f"result1: {solve1(content)}")
# print(f"result2: {solve2(content)}")
