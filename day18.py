import os
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum
import time
import heapq

FILE_PATH_EXAMPLE = 'inputs/d18_example1.txt'
FILE_PATH_MAIN = 'inputs/d18.txt'

def get_input(file_path) -> List[Tuple[int, int]]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)
	with open(full_path, 'r') as file:
		coord_lists = [line.split(",") for line in file.read().splitlines()]
		return [(int(coord[0]), int(coord[1])) for coord in coord_lists]

def fall(count, byte_coords):
	return byte_coords[:count]


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

def is_outside(pos, max_boundary):
	i, j = pos
	return i < 0 or j < 0 or i > max_boundary or j > max_boundary

def get_all_direction(pos, max_boundary, corrupted):
	i, j = pos
	all_directions =  [(i + di, j + dj) for di, dj in ALL_DIRECTIONS]
	valid_directions = [direction for direction in all_directions if not is_outside(direction, max_boundary) and not direction in corrupted]
	# print(f"{(i, j)} valid directions", valid_directions)

	return valid_directions


def shortest_path(start, max_boundary, corrupted):
	adj = {}
	# visited = {}
	for y in range(max_boundary + 1):
		for x in range(max_boundary + 1):
			adj[(x, y)] = get_all_direction((x, y), max_boundary, corrupted)
			# visited.add((x, y))
	# print("adj", adj)

	shortest = {}
	minHeap = [[0, start]]
	while minHeap:
		# print("minHeap", minHeap)
		w1, n1 = heapq.heappop(minHeap)
		if n1 in shortest:
			continue
		shortest[n1] = w1
		

		# print("n1", n1, "w1", w1)
		# print(f"adj[{n1}]", adj[n1])
		for n2 in adj[n1]:
			if n2 not in shortest:
				heapq.heappush(minHeap, [w1 + 1, n2])
	
	return shortest

def solve1(byte_coords, bytes_to_fall, max_boundary):
	# print(byte_coords)
	fallen_bytes = set(fall(bytes_to_fall, byte_coords))
	# print(fallen_bytes)
	# for y in range(max_boundary + 1):
	# 	line = ""
	# 	for x in range(max_boundary + 1):
	# 		if (x, y) in fallen_bytes:
	# 			line += "#"
	# 		else:
	# 			line += "."
	# 	print(line)

	shortest_paths = shortest_path((0, 0), max_boundary, fallen_bytes)
	final_coord = (max_boundary, max_boundary)
	return shortest_paths.get(final_coord, None)
	# print(shortest_path((0, 0), max_boundary, fallen_bytes)[max_boundary, max_boundary])


def main():
	# print(solve1(get_input(FILE_PATH_EXAMPLE), bytes_to_fall=12, max_boundary=6))
	# print(solve1(get_input(FILE_PATH_MAIN), bytes_to_fall=1024, max_boundary=70))

	first_failed = None
	# i = 0
	i = 2910
	bytes = get_input(FILE_PATH_MAIN)
	while not first_failed:
		print(i)
		result = solve1(bytes, bytes_to_fall=i+1, max_boundary=70)
		# print("result", result)
		if result == None:
			first_failed = bytes[i]
		i += 1
	print(first_failed)


	# first_failed = None
	# i = 0
	# bytes = get_input(FILE_PATH_EXAMPLE)
	# print(bytes)
	# while not first_failed:
	# 	print(i)
	# 	result = solve1(bytes, bytes_to_fall=i+1, max_boundary=6)
	# 	# print("result", result)
	# 	if result == None:
	# 		first_failed = bytes[i]
	# 	i += 1
	# print(first_failed)

	
	# print(solve1(get_input(FILE_PATH_MAIN), bytes_to_fall=2912, max_boundary=70))
	# just solved using binary search manually
	# print(f"Result2 {get_input(FILE_PATH_MAIN)[2912]}")


if __name__ == "__main__":
	main()
