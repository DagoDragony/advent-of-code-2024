import os
from dataclasses import dataclass
from typing import Tuple, List, Iterable, TypeAlias, Dict
from enum import Enum
import time
from heapq import heappush, heappop
from itertools import groupby

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


def is_outside(pos, boundaries):
	i, j = pos
	len_i, len_j = boundaries
	return i < 0 or j < 0 or i >= len_i or j >= len_j

def get_all_adjacent(pos, map):
	i, j = pos
	adjacent_tiles =  [(i + di, j + dj) for di, dj in ALL_DIRECTIONS]
	valid_directions = [tile for tile in adjacent_tiles if not is_outside(tile, (len(map), len(map[0])))]
	return valid_directions


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
	Finds all walls that can be used for cheating
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


def main():
	race_map = get_input(FILE_PATH_MAIN)
	for row in race_map:
		print(row)
	start = find_tile("S", race_map)
	end = find_tile("E", race_map)

	shortest_path, shortest_paths = get_shortest_paths(start, end, race_map)
	# print("Shortest path", shortest_paths[end])
	# for i, row in enumerate(race_map):
	# 	line = ""
	# 	for j, s in enumerate(row):
	# 		if (i, j) in shortest_path:
	# 			line += "*"
	# 		else:
	# 			line += s
	# 	print(line)


	# dot_count = sum([1 for i, row in enumerate(race_map) for j, s in enumerate(row) if s == "."])
	# print("Dot count", dot_count)
	# for i, row in enumerate(race_map):
	# 	line = ""
	# 	for j, s in enumerate(row):
	# 		if (i, j) in shortest_path:
	# 			line += "*"
	# 		else:
	# 			line += s

	walkable_walls = get_walkable_walls(race_map)
	print("walkable walls", len(walkable_walls))
	saved = []
	for walkable_wall in walkable_walls:
		side1, side2 = walkable_wall
		if side1 in shortest_paths and side2 in shortest_paths:
			saved.append(abs(shortest_paths[side1] - shortest_paths[side2])-2)
	print("max_saved", max(saved))
	print("savings", saved)
	print("savings count", len(saved))
	print("Original path", shortest_paths[end])
	print("Result1:", len([s for s in saved if s >= 100]))
	print()
	# grouped = {key: list(group) for key, group in groupby(saved)}
	# print(grouped)
	# print(sorted(saved))
	# # print(shortest_paths)
	# # 9404 -- too high
	# 1552 -- too high


if __name__ == "__main__":
	main()
