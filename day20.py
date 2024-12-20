import os
from dataclasses import dataclass
from typing import Tuple, List, Iterable
from enum import Enum
import time
import heapq

DAY = 20
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


def get_input(file_path) -> List[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    with open(full_path, 'r') as file:
        return file.read().splitlines()


def is_outside(pos, boundaries):
	i, j = pos
	len_i, len_j = boundaries
	return i < 0 or j < 0 or i >= len_i or j > len_j


def get_all_direction(pos, map):
	i, j = pos
	all_directions =  [(i + di, j + dj) for di, dj in ALL_DIRECTIONS]
	valid_directions = [direction for direction in all_directions if not is_outside(direction, (len(map), len(map-1)))]
	return valid_directions


def get_shortest_paths(start, end, map):
    """
    Dijkstra again
    """

    heap = [(0, start)]
    while heap:
		
    print("")


def find_tile(wanted_tile, map):
	for i, row in enumerate(map):
		for j, tile in enumerate(row):
			if tile == wanted_tile:
				return (i, j)
	raise Exception(f"Couldn't find {wanted_tile} in map")


def main():
	race_map = get_input(FILE_PATH_EXAMPLE)
	for row in race_map:
		print(row)
	start = find_tile("S")
	end = find_tile("E")
	paths = get_shortest_paths(start, end, paths)

if __name__ == "__main__":
	main()
