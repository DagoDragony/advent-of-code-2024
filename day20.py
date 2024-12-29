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

def get_walkable_walls(map):
	"""
	Finds all walls that has path after it
	"""
	row_len = len(map[0])
	walkable_walls = []
	for i in range(1, len(map)-1):
		for j in range(1, row_len - 1):
			if map[i][j] != "#":
				continue

			added = 0
			# walkable horizontally
			if map[i][j -1] != "#" and map[i][j + 1] != "#":
				# if (i, j) == (1, 8):
				# 	print("Added horizontally")
				added += 1
				walkable_walls.append(((i, j - 1), (i, j + 1)))

			# walkable vertically
			if map[i-1][j] != "#" and map[i+1][j] != "#":
				# if (i, j) == (1, 8):
				# 	print("Added vertically")
				added += 1
				walkable_walls.append(((i - 1, j), (i + 1, j)))

			# if (i, j) == (1, 8):
			# 	print(f"symbol {(i, j)} {map[i][j]}")
			# 	print(f"horizontal left right {map[i][j - 1]} {map[i][j + 1]}")
			# 	print(f"vertical up down {map[i - 1][j]} {map[i + 1][j]}")

			if added > 1:
				raise Exception(f"{(i, j)} added {added}")
	return walkable_walls


def get_savings(map, shortest_paths, min_saving):
	"""
	get savings that are more or equal to min_saving
	"""
	cheat_starts_with_direction = []
	for i in range(1, len(map)-1):
		for j in range(1, len(map[0]) - 1):
			if map[i][j] != ".":
				continue

			for direction in ALL_DIRECTIONS:
				ai, aj = move_to_direction((i, j), direction)
				if map[ai][aj] == "#":
					cheat_starts_with_direction.append((i, j, direction))
	

	boundaries = (len(map), len(map[0]))
	saved = []
	checkable_locations = []

	def check_positions(start_pos, i_range, j_range):
		i, j = start_pos
		for di in i_range:
			for dj in j_range:
				end_pos = (i + di, j + dj)
				ni, nj = end_pos
				if not is_outside(end_pos, boundaries) and map[ni][nj] != "#":
					checkable_locations.append(((i, j), (di, dj)))
					shortest_paths[start_pos]
					start_shortest = shortest_paths[start_pos]
					end_shortest = shortest_paths[end_pos]
					if start_shortest > end_shortest:
						saving = start_shortest - end_shortest -2
						if saving >= min_saving:
							saved.append(saving)


	for i, j, direction in cheat_starts_with_direction:
		start_pos = (i, j)
		if direction == UP:
			check_positions(start_pos, range(-1, -21, -1), range(-21, 21))

		if direction == DOWN:
			check_positions(start_pos, range(1, 21), range(-21, 21))

		if direction == LEFT:
			check_positions(start_pos, range(-21, 21), range(-1, -21, -1))

		if direction == RIGHT:
			check_positions(start_pos, range(-21, 21), range(1, 21))

	return saved


def main():
	race_map = get_input(FILE_PATH_EXAMPLE)
	for row in race_map:
		print(row)
	start = find_tile("S", race_map)
	end = find_tile("E", race_map)

	_, shortest_paths = get_shortest_paths(start, end, race_map)

	walkable_walls = get_walkable_walls(race_map)
	print("walkable walls", len(walkable_walls))
	saved = []
	for walkable_wall in walkable_walls:
		side1, side2 = walkable_wall
		if side1 in shortest_paths and side2 in shortest_paths:
			saved.append(abs(shortest_paths[side1] - shortest_paths[side2])-2)
	print("max_saved", max(saved))
	# print("savings", saved)
	# print("savings count", len(saved))
	print("Original path", shortest_paths[end])
	print("Result1:", len([s for s in saved if s >= 100]))

	# print(get_savings(race_map, shortest_paths, 100))
	# print(get_savings(race_map, shortest_paths, 50))
	counts = Counter(get_savings(race_map, shortest_paths, 50))

	duplicates = sorted([ f"{item}: {count}" for item, count in counts.items() if count > 1 ])
	print(duplicates)


if __name__ == "__main__":
	main()
