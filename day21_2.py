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


Coord: TypeAlias = tuple[int, int]

def get_input(file_path) -> List[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    with open(full_path, 'r') as file:
        return file.read().splitlines()

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
	return possible_paths


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
	return {(f, t): get_possible_paths((fi, fj), (ti, tj), (3, 0))  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items()}

NUMBER_KEYBOARD_PATHS = get_number_keyboard_paths()

def translate_number_keypad(symbols, debug = False):
	if debug:
		print(symbols)
	results = [""]
	previous_symbol = "A"
	for s in symbols:
		if previous_symbol == s:
			results = [r + "A" for r in results]
			continue 
		
		results = [r + path + "A" for path in NUMBER_KEYBOARD_PATHS[(previous_symbol, s)] for r in results]

		previous_symbol = s
	
	return set(results)




def collect_partitions(partitions):
	results = [""]

	for partition in partitions:
		results = [ r + part for part in partition for r in results]
	return results


# def get_shortest_combination(partitions):
# 	results = [0]

# 	for partition in partitions:
# 		results = list(set([ r + len(part) for part in partition for r in results]))
	
# 	return min(results)

def get_arrow_keyboard_paths():
	keypad_mappings = {
		"^": (0, 1),
		"A": (0, 2),
		"<": (1, 0),
		"v": (1, 1),
		">": (1, 2),
	}

	return {(f, t): get_possible_paths((fi, fj), (ti, tj), (0, 0))  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items()}


ARROW_KEYBOARD_PATHS = get_arrow_keyboard_paths()


def collect_path(previous_symbol, symbols) -> List[str]:
	results = []
	for s in symbols:
		if previous_symbol == s:
			results.append(["A"])
			continue 
		
		results.append(ARROW_KEYBOARD_PATHS[(previous_symbol, s)])

		previous_symbol = s

	return (previous_symbol, results)


def collect_full_paths(current_position, symbols, debug = False):
	if debug:
		print(symbols)
	results = [""]
	for s in symbols:
		if current_position == s:
			results = [r + "A" for r in results]
			continue 
		
		results = [r + path for path in NUMBER_KEYBOARD_PATHS[(current_position, s)] for r in results]

		current_position = s
	
	return results


# (current_position, path, indirection_count): length count
# cache = {}
def get_shortest_path(current_position, path_to_symbol, indirection_count) -> Tuple[str, int]:
	# Go to location
	# Press A to confirm this location
	# If location is right already, just press A
	if indirection_count == 0:
		return (path_to_symbol[-2], len(path_to_symbol))

	# key = (path_to_location, indirection_count)
	# if key in cache:
	# 	return cache[key]

	shortest_final_path = 0

	full_path = current_position + path_to_symbol

	for i in range(len(full_path) - 1):
		shortest_in_paths = 9999999999999999999999
		for path in ARROW_KEYBOARD_PATHS[(full_path[i], full_path[i+1])]:
			current_position, path_len = get_shortest_path(current_position, path, indirection_count - 1) 

			if path_len < shortest_in_paths:
				shortest_in_paths = path_len

		shortest_final_path += shortest_in_paths

	return shortest_final_path


def main():
	codes = get_input(FILE_PATH_MAIN)

	# shortest_paths = []
	# for row in codes:
	# 	lvl1_paths = list(translate_number_keypad(row))

	# 	lvl2_partitions_groups = [translate_arrow_keypad(path) for path in lvl1_paths]
	# 	lvl2_paths = [path for lvl2_partitions_group in lvl2_partitions_groups for path in collect_partitions(lvl2_partitions_group)] 
	# 	lvl3_partitions_groups = [ translate_arrow_keypad(path) for path in lvl2_paths]

	# 	min_path_len = min([get_shortest_combination(partitions_group) for partitions_group in lvl3_partitions_groups])
	# 	shortest_paths.append((row, min_path_len))


	# results = []
	# for cmd, min_path in shortest_paths:
	# 	cmd_number = int(cmd[:-1])
	# 	results.append(cmd_number * min_path)
	# print("Result1: ", sum(results))

	shortest_paths = []
	for row in codes[:1]:
		# lvl1_paths = list(translate_number_keypad(row))
		# shortest = [get_shortest_path("A", path, 2)[1] for path in lvl1_paths]
		# print(min(shortest))
		# for path in lvl1_paths:
		# 	print(path)

		# print("-" * 30)

		lvl1_paths = list(translate_number_keypad(row))
		for path in lvl1_paths:
			print(path)

		# final_partitions_groups = get_shortest_path("A", lvl1_paths, 2)

		# min_path_len = min([get_shortest_combination(partitions_group) for partitions_group in final_partitions_groups])
		# shortest_paths.append((row, min_path_len))


	# results = []
	# for cmd, min_path in shortest_paths:
	# 	cmd_number = int(cmd[:-1])
	# 	results.append(cmd_number * min_path)
	# print("Result1: ", sum(results))

if __name__ == "__main__":
	main()