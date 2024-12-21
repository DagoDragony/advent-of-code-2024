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


# def get_shortest_paths(start, map) -> Dict[Coord, int]:
#     """
#     Dijkstra again
#     """
#     shortest = {}

#     heap = [(0, start)]
#     while heap:
#         current_weight, coord = heappop(heap)
#         if coord in shortest:
#             pass
#         shortest[coord] = current_weight
        
#         all_adj = get_all_adjacent(coord, map)
#         for  tile in all_adj:
#             i, j = tile
#             if not tile in shortest and not map[i][j] == "#":
#                 heappush(heap, (current_weight + 1,  tile))
#     return shortest


DIRECTION_MAP = {
	(0, 1): ">",
	(0, -1): "<",
	(-1, 0): "^",
	(1, 0): "v"
}



def move(current, final, delta, path, empty_space) -> List[str]:
	if current == empty_space:
		return []
	
	if current == final:
		# print("current == final")
		if delta != (0, 0):
			raise Exception("failing")
		return [path]
	
	if delta == (0, 0):
		return []

	i, j = current
	di, dj = delta

	if di == 0:
		di_move = []
	else:
		di_step = int((di * -1)/abs(di))
		move_symbol = DIRECTION_MAP[(di_step, 0)]
		# print("i move_symbol", move_symbol)
		new_coord = (i + di_step, j)
		di_move = move(new_coord, final, (di + di_step, dj), path+move_symbol, empty_space)
	
	if dj == 0:
		dj_move = []
	else:
		dj_step = int((dj * -1)/abs(dj))
		move_symbol = DIRECTION_MAP[(0, dj_step)]
		# print("j move_symbol", move_symbol)
		new_coord = (i, j + dj_step)
		dj_move = move(new_coord, final, (di, dj + dj_step), path+move_symbol, empty_space)

	return di_move + dj_move


def get_possible_paths(initial, final, empty_space) -> str:
	(ii, ij), (fi, fj) = initial, final
	di, dj = (ii - fi, ij - fj)

	possible_paths = [path for path in move(initial, final, (di, dj), "", empty_space)]
	# print("possible paths", possible_paths)
	return possible_paths


# def get_all_permutations(path) -> List[str]:
# 	all_permutations = [''.join(p) for p in permutations(path)]
# 	return all_permutations


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
	return {(f, t): get_possible_paths((fi, fj), (ti, tj), (3, 0))  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items() if f != t}

NUMBER_KEYBOARD_PATHS = get_number_keyboard_paths()

def get_arrow_keyboard_paths():
	keypad_mappings = {
		"^": (0, 1),
		"A": (0, 2),
		"<": (1, 0),
		"v": (1, 1),
		">": (1, 2),
	}

	return {(f, t): get_possible_paths((fi, fj), (ti, tj), (0, 0))  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items() if f != t}


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
	codes = get_input(FILE_PATH_MAIN)

	# collected_partitions = collect_partitions([["A"], ["1", "2"], ["X", "Y"]])
	# print(collected_partitions)
	# for key, paths in NUMBER_KEYBOARD_PATHS.items():
	# 	print(key, paths)

	# for key, paths in ARROW_KEYBOARD_PATHS.items():
	# 	print(key, paths)

	shortest_paths = []
	for row in codes:
		# print(row)
		lvl1_paths = list(translate_number_keypad(row))
		# print(lvl1_paths)
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

		# print(lvl2_paths)
		# # lvl2_min = min(lvl2_paths, key=len)
		# # print(">> min lvl2", lvl2_min, "len", len(lvl2_min))
		lvl3_partitions_groups = [ translate_arrow_keypad(path) for path in lvl2_paths]
		min_path_len = min([get_shortest_combination(partitions_group) for partitions_group in lvl3_partitions_groups])
		# print("Result", min_path_len)
		shortest_paths.append((row, min_path_len))
		# lvl3_paths = [path3 for path in lvl2_paths for path3 in translate_arrow_keypad(path)]
		# lvl3_min = min(lvl3_paths, key=len)
	# # 	# print(">> min lvl3", lvl3_min, "len", len(lvl3_min))
	# # 	# # print(lvl3_paths)
	# # 	# # print(">> min lvl3", min(lvl3_paths, key=len))

	results = []
	for cmd, min_path in shortest_paths:
		cmd_number = int(cmd[:-1])
		results.append(cmd_number * min_path)
	print("Result1: ", sum(results))

if __name__ == "__main__":
	main()