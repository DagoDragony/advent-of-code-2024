import os
from dataclasses import dataclass
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


def is_outside(pos, boundaries):
	i, j = pos
	len_i, len_j = boundaries
	return i < 0 or j < 0 or i >= len_i or j >= len_j

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
	current_coord = initial
	# print("-"*10)
	# print("from to", initial, final)
	# print("-"*10)

	def get_delta_i_step(di, pos) ->  Tuple[Tuple[int, int], int, str] | None:
		if di == 0:
			return None
		i, j = pos
		step =int((di * -1)/abs(di))
		new_coord = (i + step, j)
		# print("new_coord", new_coord)
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
		# print("new_coord", new_coord)
		if new_coord == empty_space:
			return None
		else:
			move_symbol = DIRECTION_MAP[(0, step)]
			# print("symbol", move_symbol, "new dj", dj + step)
			return (new_coord, dj + step, move_symbol)


	directions = ""
	# print("di", di, "dj", dj)
	while di != 0 or dj != 0:
		changed = False

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



		if not changed:
			raise Exception("Not changed!")

		directions += symbol
		current_coord = new_coord
	# print("Directions", directions)
	return directions


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



	return {(f, t): get_all_permutations(get_path((fi, fj), (ti, tj)))  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items() if f != t}

NUMBER_KEYBOARD_PATHS = get_number_keyboard_paths()

def get_all_permutations(path):
	all_permutations = [''.join(p) for p in permutations(path)]
	return all_permutations

def get_arrow_keyboard_paths():
	keypad_mappings = {
		"^": (0, 1),
		"A": (0, 2),
		"<": (1, 0),
		"v": (1, 1),
		">": (1, 2),
	}

	return {(f, t): get_all_permutations(get_path((fi, fj), (ti, tj)))  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items() if f != t}

ARROW_KEYBOARD_PATHS = get_arrow_keyboard_paths()

def direction_symbols(di, dj):
	si = "^" if di < 0 else "v"
	sj = "<" if dj < 0 else ">"
	return (si, sj)


def translate_number_keypad(symbols, debug = False):
	result = defaultdict(lambda: "")
	# ????????
	previous_symbol = "A"
	for s in symbols:
		for i, path in enumerate(NUMBER_KEYBOARD_PATHS[(previous_symbol, s)]):
			r = path + "A"
			if debug:
				print(f"{previous_symbol} -> {s}:", r)
			r[i] += r
			# print(r)
			previous_symbol = s
	return result


def translate_arrow_keypad(symbols, debug = False):
	# print(symbols)
	result = ""
	# ????????
	previous_symbol = "A"
	for s in symbols:
		if debug:
			print("Symbol", s)
			print("--------------------")
		if previous_symbol == s:
			result += "A"
			if debug:
				print("Same as previous")
		else:
			path = ARROW_KEYBOARD_PATHS[(previous_symbol, s)]
			r = path+"A"
			if debug:
				print(f"{previous_symbol} -> {s}:", r)

			result += r
			previous_symbol = s

	return result


def main():
	codes = get_input(FILE_PATH_EXAMPLE)

	row = codes[0]

	number_keyboard_paths = get_number_keyboard_paths()
	arrow_keyboard_paths = get_arrow_keyboard_paths()

	for (fr, to), path in number_keyboard_paths.items():

		

	for row in codes:
		print(row)
		lvl1_paths = translate_number_keypad(row)
		# print(NUMBER_KEYBOARD_PATHS)
		lvl2 = translate_arrow_keypad(lvl1)
		lvl3 = translate_arrow_keypad(lvl2)
		print("lvl1", lvl1, len(lvl1))
		print("lvl2", lvl2, len(lvl2))
		print("lvl3", lvl3, len(lvl3))
		# result = ""
		# for s in row:
		# 	mi, mj = number_keyboard_paths[(previous_symbol, s)]
		# 	si, sj = direction_symbols(mi, mj)
		# 	r = sj*abs(mj) + si*abs(mi) +"A"
		# 	# print(f"{previous_symbol} -> {s}:", mi, mj)
		# 	# print("directions", si, sj)
		# 	# print(r)
		# 	result += r
		# 	# print(r)
		# 	previous_symbol = s
		# print("lvl1:", result)
		


			





if __name__ == "__main__":
	main()
