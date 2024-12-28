import os
import os
from functools import cache
from typing import Tuple, List, TypeAlias, Dict
from itertools import pairwise

DAY = 21
FILE_PATH_EXAMPLE = f"inputs/input_d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/input_d{DAY}.txt"


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

	possible_paths = [path + "A" for path in move(initial, final, (di, dj), "", empty_space)]
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


@cache
def get_shortest_path(code: str, depth: int, number_pad = False) -> int:
	"""
	Go to location
	Press A to confirm this location
	If location is right already, just press A
 	"""
	result = 0

	for b1, b2 in pairwise("A" + code):
		paths = NUMBER_KEYBOARD_PATHS[(b1, b2)] if number_pad else ARROW_KEYBOARD_PATHS[(b1, b2)]
		
		if depth == 0:
			result += min(len(path) for path in paths)
		else:
			result += min(get_shortest_path(path, depth - 1) for path in paths) 
	return result


def main():
	codes = get_input(FILE_PATH_MAIN)

	shortest_paths = []
	for row in codes:
		print(row)
		shortest = get_shortest_path(row, 25, True)
		print("shortest", shortest)
		shortest_paths.append((row, shortest))

	results = []
	for cmd, min_path in shortest_paths:
		cmd_number = int(cmd[:-1])
		results.append(cmd_number * min_path)
	print("Result: ", sum(results))

if __name__ == "__main__":
	main()