import os
import os
from dataclasses import dataclass, field
from typing import Tuple, List, Iterable, TypeAlias, Dict
from enum import Enum
from collections import defaultdict
import time
from heapq import heappush, heappop
from itertools import groupby, permutations

DAY = 21
FILE_PATH_EXAMPLE = f"inputs/input_d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/input_d{DAY}.txt"

RIGHT=(0, 1)
LEFT=(0, -1)
UP=(-1, 0)
DOWN=(1, 0)

ALL_DIRECTIONS = [
	RIGHT,
	LEFT,
	UP,
	DOWN,
]


@dataclass
class Trie:
	nodes: Dict[str, Tuple['Trie', bool]] = field(default_factory=dict)


Coord: TypeAlias = tuple[int, int]


def get_input(file_path) -> List[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    with open(full_path, 'r') as file:
        return file.read().splitlines()


# def is_outside(pos, boundaries):
# 	i, j = pos
# 	len_i, len_j = boundaries
# 	return i < 0 or j < 0 or i >= len_i or j >= len_j


def get_all_adjacent(pos, map):
	i, j = pos
	adjacent_tiles =  [(i + di, j + dj) for di, dj in ALL_DIRECTIONS]
	valid_directions = [tile for tile in adjacent_tiles if not is_outside(tile, (len(map), len(map[0])))]
	return valid_directions


def get_shortest_paths(start, map) -> Dict[Coord, int]:
    """
    Dijkstra again
    """
    shortest = {}

    heap = [(0, start)]
    while heap:
        current_weight, coord = heappop(heap)
        if coord in shortest:
            pass
        shortest[coord] = current_weight
        
        all_adj = get_all_adjacent(coord, map)
        for  tile in all_adj:
            i, j = tile
            if not tile in shortest and not map[i][j] == "#":
                heappush(heap, (current_weight + 1,  tile))
    return shortest


DIRECTION_MAP = {
	(0, 1): ">",
	(0, -1): "<",
	(-1, 0): "^",
	(1, 0): "v"
}

empty_space = (3, 0)

def get_path(initial, final) -> str:
	(ii, ij), (fi, fj) = initial, final
	di, dj = (ii - fi, ij - fj)
	# print("-"*10)
	# print("from to", initial, final)
	# print("-"*10)

	def get_delta_i_step(di, pos) ->  Tuple[Tuple[int, int], int, str] | None:
		if di == 0:
			return None
		i, j = pos
		step =int((di * -1)/abs(di))
		new_coord = (i + step, j)
		if new_coord == empty_space:
			return None
		else:
			move_symbol = DIRECTION_MAP[(step, 0)]
			# print("symbol", move_symbol, "new di", di + step)
			return (new_coord, di + step, move_symbol)


	def get_delta_j_step(dj, pos) -> Tuple[Tuple[int, int], int, str] | None:
		if dj == 0:
			return None
		i, j = pos
		step = int((dj * -1)/abs(dj))
		new_coord = (i, j + step)
		if new_coord == empty_space:
			return None
		else:
			move_symbol = DIRECTION_MAP[(0, step)]
			# print("symbol", move_symbol, "new dj", dj + step)
			return (new_coord, dj + step, move_symbol)


	directions = ""
	current_coord = initial
	# print("di", di, "dj", dj)
	while di != 0 or dj != 0:
		changed = False
		symbol = "x"

		move_i = get_delta_i_step(di, current_coord)
		if not changed and move_i != None:
			new_coord, new_di, symbol = move_i
			di = new_di
			changed = True

		move_j = get_delta_j_step(dj, current_coord)
		if not changed and move_j != None:
			new_coord, new_dj, symbol = move_j
			dj = new_dj
			changed = True

		directions += symbol
		current_coord = new_coord
	# print("Directions", directions)
	
	return directions


def get_all_permutations(path) -> List[str]:
	all_permutations = [''.join(p) for p in permutations(path)]
	return all_permutations


def get_number_keyboard_paths() -> Dict[Tuple[str, str], str]:
	keypad_mappings = {
		"7": (0, 0),
		"8": (0, 1),
		"9": (0, 2),
		"4": (1, 0),
		"5": (1, 1),
		"6": (1, 2),
		"1": (2, 0),
		"2": (2, 1),
		"3": (2, 2),
		"0": (3, 1),
		"A": (3, 2),
	}
	return {(f, t): set(get_all_permutations(get_path((fi, fj), (ti, tj))))  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items() if f != t}

NUMBER_KEYBOARD_PATHS = get_number_keyboard_paths()

def get_arrow_keyboard_paths():
	keypad_mappings = {
		"^": (0, 1),
		"A": (0, 2),
		"<": (1, 0),
		"v": (1, 1),
		">": (1, 2),
	}

	return {(f, t): set(get_all_permutations(get_path((fi, fj), (ti, tj))))  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items() if f != t}


ARROW_KEYBOARD_PATHS = get_arrow_keyboard_paths()


def translate_number_keypad(symbols, debug = False):
	if debug:
		print(symbols)
	results = [""]
	previous_symbol = "A"
	for s in symbols:
		if previous_symbol == s:
			results = [r + "A" for r in results]
			continue 
		
		paths = [path + "A" for path in NUMBER_KEYBOARD_PATHS[(previous_symbol, s)]]
		results = [r + path for path in paths for r in results]

		previous_symbol = s
	
	return set(results)


def translate_arrow_keypad(symbols, debug = False):
	if debug:
		print(symbols)

	results = []
	previous_symbol = "A"
	for s in symbols:
		if previous_symbol == s:
			results.append(["A"])
			continue 
		
		paths = [path + "A" for path in ARROW_KEYBOARD_PATHS[(previous_symbol, s)]]
		results.append(paths)

		previous_symbol = s

	return results


def collect_partitions(partitions):
	results = [""]

	for partition in partitions:
		results = [ r + part for part in partition for r in results]
	return results


def get_shortest_combination(partitions):
	results = [0]

	for partition in partitions:
		results = list(set([ r + len(part) for part in partition for r in results]))
	
	return min(results)


def main():
	codes = get_input(FILE_PATH_EXAMPLE)

	# collected_partitions = collect_partitions([["A"], ["1", "2"], ["X", "Y"]])
	# print(collected_partitions)
	# for key, paths in NUMBER_KEYBOARD_PATHS.items():
	# 	print(key, paths)

	# for key, paths in ARROW_KEYBOARD_PATHS.items():
	# 	print(key, paths)

	for row in [codes[3]]:
		print(row)
		lvl1_paths = list(translate_number_keypad(row))
		print(lvl1_paths)
		# print("finished lvl1 with ", len(lvl1_paths))
		# print(lvl1_paths)
		# print(">> min lvl1", min(lvl1_paths, key=len))
		lvl2_partitions_groups = [translate_arrow_keypad(path) for path in lvl1_paths]
		# print("lvl2_partitions_groups_count", len(lvl2_partitions_groups))
		# print(lvl2_partitions_groups)

		lvl2_paths = [path for lvl2_partitions_group in lvl2_partitions_groups for path in collect_partitions(lvl2_partitions_group)] 
		# for row in lvl2_paths:
		# 	print(row)
		# print("lvl2_paths", lvl2_paths)
		# print("finished lvl2 with ", len(lvl2_paths))

	# 	print(lvl2_paths)
	# 	# # lvl2_min = min(lvl2_paths, key=len)
	# 	# # print(">> min lvl2", lvl2_min, "len", len(lvl2_min))
		lvl3_partitions_groups = [ translate_arrow_keypad(path) for path in lvl2_paths]
		min_path_len = min([get_shortest_combination(partitions_group) for partitions_group in lvl3_partitions_groups])
		print("Result", min_path_len)
		# lvl3_paths = [path3 for path in lvl2_paths for path3 in translate_arrow_keypad(path)]
		# lvl3_min = min(lvl3_paths, key=len)
	# 	# print(">> min lvl3", lvl3_min, "len", len(lvl3_min))
	# 	# # print(lvl3_paths)
	# 	# # print(">> min lvl3", min(lvl3_paths, key=len))

if __name__ == "__main__":
	main()