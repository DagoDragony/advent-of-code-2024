import os
from dataclasses import dataclass
from typing import Tuple, List, Iterable, TypeAlias, Dict
from enum import Enum
import time
from heapq import heappush, heappop
from itertools import groupby

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

	empty_space = (3, 0)

	def get_path(initial, delta) -> str:
		di, dj = delta
		current_coord = initial
		while di != 0 and dj != 0:
			i, j = current_coord
			if di < 0:
				new_coord = (i + 1, j)
				if new_coord != empty_space:
					current_coord = new_coord
					di += 1

			


	return {(f, t): (ti - fi, tj - fj)  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items() if f != t}

NUMBER_KEYBOARD_PATHS = get_number_keyboard_paths()

def get_arrow_keyboard_paths():
	keypad_mappings = {
		"^": (0, 1),
		"A": (0, 2),
		"<": (1, 0),
		"v": (1, 1),
		">": (1, 2),
	}
	return {(f, t): (ti - fi, tj - fj)  for f, (fi, fj) in keypad_mappings.items() for t, (ti, tj) in keypad_mappings.items() if f != t}

ARROW_KEYBOARD_PATHS = get_arrow_keyboard_paths()

def direction_symbols(di, dj):
	si = "^" if di < 0 else "v"
	sj = "<" if dj < 0 else ">"
	return (si, sj)

def translate_number_keypad(symbols):
	result = ""
	# ????????
	previous_symbol = "A"
	for s in symbols:
		mi, mj = NUMBER_KEYBOARD_PATHS[(previous_symbol, s)]
		si, sj = direction_symbols(mi, mj)
		r = sj*abs(mj) + si*abs(mi) +"A"
		# print(f"{previous_symbol} -> {s}:", mi, mj)
		# print("directions", si, sj)
		# print(r)
		result += r
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
			mi, mj = ARROW_KEYBOARD_PATHS[(previous_symbol, s)]
			si, sj = direction_symbols(mi, mj)
			r = sj*abs(mj) + si*abs(mi) +"A"
			if debug:
				print(f"{previous_symbol} -> {s}:", mi, mj)
				print("directions", si, sj)
				print(r)

			result += r
			previous_symbol = s

	return result




def main():
	codes = get_input(FILE_PATH_EXAMPLE)
	
	for row in [codes[0]]:
		print(row)
		lvl1 = translate_number_keypad(row)
		lvl2 = translate_arrow_keypad(lvl1)
		lvl3 = translate_arrow_keypad(lvl2, debug = True)
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
