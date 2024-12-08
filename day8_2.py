import os
import itertools

script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d8_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d8.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
antenas_map = []
with open(file_path, 'r') as file:
    for line in file.readlines():
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
    # print(antennas)
    return antennas


def outside_map(i, j, max_i, max_j):
    return i < 0 or j < 0 or i >= max_i or j >= max_j


def get_combination_antinodes(c1, c2, max_i, max_j):
    i1, j1 = c1
    i2, j2 = c2
    di = i1 - i2
    dj = j1 - j2

    def get_side_antinodes(i, j, di, dj):
        antinodes = []
        while not outside_map(i, j, max_i, max_j):
            antinodes.append((i, j))
            i, j = (i + di, j + dj)

        return antinodes
    

    final_antinodes = [] 
    final_antinodes.extend(get_side_antinodes(*c1, di, dj))
    final_antinodes.extend(get_side_antinodes(*c2, -di, -dj))

    return final_antinodes


def get_same_frequency_antinodes(antennas, max_i, max_j):
    # print(f"antennas {antennas}")
    # print(type(antennas))
    antenna_name, coords = antennas
    combinations = itertools.combinations(coords, r=2)
    antinodes_list = []
    [antinodes_list.extend(get_combination_antinodes(c1, c2, max_i, max_j)) for c1, c2 in combinations]
    return antinodes_list
        

def solve1(map):
    antinodes = []
    max_i = len(map)
    max_j = len(map[0])
    for antennas in find_antennas(map).items():
        # print(f"0antennas {antennas}")
        antinodes.extend(get_same_frequency_antinodes(antennas, max_i, max_j))
    return antinodes

print("-"*100)    
print(f"Result2: {len(set(solve1(antenas_map)))}")
    
# # print(f"result1: {solve1(content)}")
