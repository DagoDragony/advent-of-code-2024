import os
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum
import time
import heapq

FILE_PATH = 'inputs/input_d18_example1.txt'
# FILE_PATH = 'inputs/input_d18.txt'

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
	return [direction for direction in all_directions if not is_outside(direction, max_boundary) and not direction in corrupted]

def shortest_path(start, max_boundary, corrupted):
	adj = {}
	for y in range(max_boundary + 1):
		for x in range(max_boundary + 1):
			for direction in get_all_direction(start, max_boundary, corrupted):
				print(direction)
				adj[(x, y)] = direction

	shortest = {}
	minHeap = [[0, start]]
	while minHeap:
		print("minHeap", minHeap)
		w1, n1 = heapq.heappop(minHeap)
		if n1 in shortest:
			continue
		shortest[n1] = w1

		print("n1", n1, "w1", w1)
		for n2 in adj[n1]:
			if n2 not in shortest:
				heapq.heappush(minHeap, [w1 + 1, n2])
	
	return shortest


def main():
	boundaries = (0, 6)
	byte_coords = get_input(FILE_PATH)
	print(byte_coords)
	fallen_bytes = set(fall(12, byte_coords))
	print(fallen_bytes)
	for y in range(boundaries[1] + 1):
		line = ""
		for x in range(boundaries[1] + 1):
			if (x, y) in fallen_bytes:
				line += "#"
			else:
				line += "."
		print(line)

	print(shortest_path((0, 0), 6, fallen_bytes))



if __name__ == "__main__":
	main()
