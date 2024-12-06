import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d6_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d6.txt')

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

def count_walked(map):
    # print(map)
    return sum([True for i in range(len(map)) for j in range(len(map[0])) if map[i][j] == 'X'])

def print_map(map):
    for l in map:
        print(l)

def process_path_history(c, direction, path_history):
    if c in  path_history:
        if direction in path_history[c]:
            return True
        else:
            path_history[c].add(direction)
    else:
        path_history[c] = set(direction)
    return False

def is_loop_walk(i, j, map):
    path_history = {}
    direction = (-1, 0)
    path_history[(i, j)] = set(direction)
    while(True):
        ni, nj = (i + direction[0], j + direction[1])
        if outside_map(ni, nj, map):
            # print(ni, nj)
            break;
        elif map[ni][nj] == '#' or map[ni][nj] == 'O':
            # print("#", ni, nj)
            direction = righ_changes[direction]
            # print(direction)
            i, j = (i + direction[0], j + direction[1]) 

            if process_path_history((i, j), direction, path_history):
                return path_history
            # print(i, j)
        else:
            i, j = (ni, nj)
            # print(i, j)
            if process_path_history((i, j), direction, path_history):
                return path_history
    return {}


def get_initial_path(i, j, map):
    direction = (-1, 0)
    passed_path = set()
    passed_path.add((i, j))
    while(True):
        ni, nj = (i + direction[0], j + direction[1])
        if outside_map(ni, nj, map):
            # print(ni, nj)
            break;
        elif map[ni][nj] == '#' or map[ni][nj] == 'O':
            # print("#", ni, nj)
            direction = righ_changes[direction]
            # print(direction)
            i, j = (i + direction[0], j + direction[1]) 
            if(map[i][j] != 'X'):
                passed_path.add((i, j))
            # print(i, j)
        else:
            i, j = (ni, nj)
            # print(i, j)
            if(map[i][j] != 'X'):
                passed_path.add((i, j))
        # print(already_walked)

    return passed_path

start_i, start_j = get_current_position(lab_map)
current_path = get_initial_path(start_i, start_j, lab_map)
print("-"*100)    
print(len(current_path))

def add_obstacle(i, j, map):
    # print(map)
    new_map = list(map)
    new_line = list(map[i])
    new_line[j] = "O"
    new_map[i] = "".join(new_line) 
    return new_map

def get_map_combinations(si, sj, map, path):
    return [add_obstacle(i, j, map) for i, j in path if i != si and j != sj]

def print_infinite_path(path, m):
    for i in range(len(m)):
        line = list(m[i])
        for j in range(len(line)):
            if (i, j) in path:
                line[j] = "X"
        print("".join(line))
    print()

inifinite_loops = 0
for m in get_map_combinations(start_i, start_j, lab_map, current_path):
    infinite_path = is_loop_walk(start_i, start_j, m)
    if len(infinite_path):
        inifinite_loops += 1
        print_infinite_path(infinite_path, m)

# inifinite_loops = sum([is_loop_walk(start_i, start_j, m) for m in get_map_combinations(start_i, start_j, lab_map, current_path)])
print(inifinite_loops)


# possible_location_of_obstacle = [(i, j) for i in range(len(lab_map)) for j in range(len(lab_map[0])) if lab_map[i][j] == "."]




# print_map(lab_map)
# # print(f"result2: {solve2(content)}")
