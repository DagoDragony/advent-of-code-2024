import os
from dataclasses import dataclass
from typing import Tuple, List, Iterable, TypeAlias, Dict
from enum import Enum
import time
from heapq import heappush, heappop
from itertools import groupby
from collections import Counter

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

Coord: TypeAlias = tuple[int, int]


def get_input(file_path) -> List[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    with open(full_path, 'r') as file:
        return file.read().splitlines()


def is_outside(pos: Tuple[int, int], boundaries: Tuple[int, int]):
	i, j = pos
	len_i, len_j = boundaries
	return i < 0 or j < 0 or i >= len_i or j >= len_j

def get_all_adjacent(pos, map):
	i, j = pos
	adjacent_tiles =  [(i + di, j + dj) for di, dj in ALL_DIRECTIONS]
	valid_directions = [tile for tile in adjacent_tiles if not is_outside(tile, (len(map), len(map[0])))]
	return valid_directions

def move_to_direction(pos, direction):
	i, j = pos
	di, dj = direction
	return (i + di, j + dj)


def get_shortest_paths(start, end, map) -> Dict[Coord, int]:
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

    shortest_path = set()
    current_pos = end
    visited = set()
    while True:
        shortest_path.add(current_pos)
        current_pos
        if current_pos == start:
            break
        value = shortest[current_pos]
        all_adjacent = get_all_adjacent(current_pos, map)
        next_shortest = [pos for pos in all_adjacent if not pos in visited and pos in shortest and shortest[pos] < value]
        current_pos = next_shortest[0]

	
    return (shortest_path, shortest)
		

def find_tile(wanted_tile, map):
	for i, row in enumerate(map):
		for j, tile in enumerate(row):
			if tile == wanted_tile:
				return (i, j)
	raise Exception(f"Couldn't find {wanted_tile} in map")


def get_savings(map, shortest_paths, min_saving, max_cheat_len):
	path_tiles = []
	for i, row in enumerate(map):
		for j, s in enumerate(row):
			if s == "#":
				continue

			for direction in ALL_DIRECTIONS:
				if map[i + direction[0]][j + direction[1]] == "#":
					path_tiles.append(((i, j), direction))

	already_checked_cheat = set()
	savings = []
	def check_all_cheats(start_pos, i_range, j_range):
		si, sj = start_pos
		for di in i_range:
			for dj in j_range:
				ei, ej = si + di, sj + dj
				end_pos = (ei, ej)
				distance = abs(di) + abs(dj)

				if is_outside(end_pos, (len(map), len(map[0]))) or map[ei][ej] == "#" or distance > max_cheat_len or (start_pos, end_pos) in already_checked_cheat:
					continue

				saved = shortest_paths[end_pos] - shortest_paths[start_pos] - distance
				if saved >= min_saving:
					savings.append(saved)

				already_checked_cheat.add((start_pos, end_pos))


	full_cheat_range = range(-max_cheat_len, max_cheat_len + 1)
	# forward_cheat_range = range(1, max_cheat_len+1)
	# backwards_cheat_range = range(-max_cheat_len, 0)
	forward_cheat_range = full_cheat_range
	backwards_cheat_range = full_cheat_range
	for pos, direction in path_tiles:
		if direction == DOWN:
			check_all_cheats(pos, forward_cheat_range, full_cheat_range)

		if direction == UP:
			check_all_cheats(pos, backwards_cheat_range, full_cheat_range)

		if direction == RIGHT:
			check_all_cheats(pos, full_cheat_range, forward_cheat_range)

		if direction == LEFT:
			check_all_cheats(pos, full_cheat_range, backwards_cheat_range)
	
	return savings


def main():
	race_map = get_input(FILE_PATH_MAIN)
	start = find_tile("S", race_map)
	end = find_tile("E", race_map)

	_, shortest_paths = get_shortest_paths(start, end, race_map)

	savings_for_len_2 = get_savings(race_map, shortest_paths, 100, 2)
	print("Result1:", len(savings_for_len_2))
	savings_for_len_20 = get_savings(race_map, shortest_paths, 100, 20)
	print("Result2:", len(savings_for_len_20))

if __name__ == "__main__":
	main()
