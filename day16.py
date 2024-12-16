import os
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum
import time
import sys


sys.setrecursionlimit(5000)

# FILE_PATH = 'inputs/input_d16_example1.txt'
FILE_PATH = 'inputs/input_d16_example2.txt'
# FILE_PATH = 'inputs/input_d16.txt'

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

EAST_DIRECTION = (0, 1)
ROTATE_CLOCKWISE = {
	UP: RIGHT,
	RIGHT: DOWN,
	DOWN: LEFT,
	LEFT: UP 
}
ROTATE_COUNTERCLOCKWISE = {
	UP: LEFT,
	LEFT: DOWN,
	DOWN: RIGHT,
	RIGHT:  UP
}

def get_map(file_path) -> List[str]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)
	with open(full_path, 'r') as file:
		return file.read().splitlines()


def next_tile(position, delta):
	i, j = position
	di, dj = delta
	return (i + di, j + dj)

class State(Enum):
    NO_PATH = 1
    BACK_IN_PATH = 2
    REACHED_END = 3

@dataclass
class NodeStatus:
    state: State
    value: int = 10**10

cache = {}
price = {}
def make_a_move(pos, direction, map, visited, score):
	i, j = pos
	symbol = map[i][j]
	if symbol == '#':
		return None

	if pos in price:
		if price[pos] > score:
			# add cheaper score to this cell
			price[pos] = score
		else:
			return None
	else:
		price[pos] = score

	match symbol:
		case "E":
			# cache[key] = NodeStatus(State.REACHED_END, score)
			return
		case v if v != "#":
			clockwise = ROTATE_CLOCKWISE[direction]
			counterclockwise = ROTATE_COUNTERCLOCKWISE[direction]
			make_a_move(next_tile(pos, direction), direction, map, visited.copy(), score + 1),
			make_a_move(next_tile(pos, clockwise), clockwise, map, visited.copy(), score + 1000 + 1),
			make_a_move(next_tile(pos, counterclockwise), counterclockwise, map, visited.copy(), score + 1000 + 1),
			return
		case _:
			return

def get_all_direction(pos):
	i, j = pos
	return [(i + di, j + dj) for di, dj in ALL_DIRECTIONS]


best_paths = set()
def walk_to_bests(pos, path, final_score, map):
	i, j = pos
	if map[i][j] == "E":
		return len(path)

	def check_if_valid(new_pos):
		ni, nj = new_pos
		checks = [
			new_pos in price,
			price[ni][nj] < final_score
		]
		return all(checks)
	
	all_directions = get_all_direction(pos)
	positions_to_go = [new_pos for new_pos in all_directions if check_if_valid(new_pos)]
	for pos_to_go in positions_to_go:
		walk_to_bests(pos_to_go, list(path) + pos + 1, final_score, map)





	walk_to_bests
	

def get_best_paths_tile_count(start, map): ...


def get_score(map):
	start = (len(map)-2, 1)
	print(map[start[0]][start[1]])
	end = (1, len(map)-2)
	print(map[end[0]][end[1]])
	make_a_move(start, EAST_DIRECTION, [list(row) for row in map], set(), 0)

	final_price = price[end]
	tile_count = final_price % 1000 + 1
	return (final_price, tile_count)

def main():
	race_map = get_map(FILE_PATH)
	for row in race_map:
		print(row)
	price, tile_count = get_score(race_map)
	print(f"Result1: {price}")
	print(f"Result2: {tile_count}")

if __name__ == "__main__":
	main()
