import os
import itertools
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Tuple, List
import re
from math import prod
import copy

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d15_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d15.txt')

@dataclass
class RobotData:
	initial_location: Tuple[int, int]
	velocity: Tuple[int, int]

	def __str__(self):
		return f"p={self.initial_location} v={self.velocity}"

	def __iter__(self):
		return iter((self.initial_location[0], self.initial_location[1], self.velocity[0], self.velocity[1]))

@dataclass
class InputData:
	map: List[List[str]]
	moves: List[str]

	def print(self):
		for line in self.map:
			print(line)
		print()
		for line in self.moves:
			print(line)
		print
 
	@staticmethod
	def parse(str) -> 'InputData':
		map_str, moves_str = str.split("\n\n")
		map = [line.strip() for line in map_str.split("\n")]
		moves = moves_str.strip().split("\n")
		return InputData(map, moves)

def find_robot(map):
	for i, line in enumerate(map):
		for j, s in enumerate(line):
			if s == '@':
				return (i, j)
	raise Exception("No robot found")

print("PROCESSING PART 1...")
def get_input_data(file_path) -> 'InputData':
	with open(file_path, 'r') as file:
		return InputData.parse(file.read())

direction_translations = {
	"^": (-1, 0),
	"v": (1, 0),
	">": (0, 1),
	"<": (0, -1)
}

def move_boxes(box_position, direction, map) -> bool:
	i, j = box_position
	di, dj = direction
	ni, nj = i + di, j + dj
	match map[ni][nj]:
		case "#":
			return False
		case ".":
			map[i][j] = "."
			map[ni][nj] = "O"
			return True
		case "O":
			if move_boxes((ni, nj), direction, map):
				map[i][j] = "."
				map[ni][nj] = "O"
				return True
			else:
				return False

def move_robot(position, move, map):
	i, j = position
	direction = direction_translations.get(move)
	di, dj = direction
	ni, nj = i + di, j + dj
	match map[ni][nj]:
		case "#":
			return i, j
		case "O":
			if move_boxes((ni, nj), direction, map):
				map[i][j] = "."
				map[ni][nj] = "@"
				return (ni, nj)
			else:
				return (i, j)
		case ".":
			map[i][j] = "."
			map[ni][nj] = "@"
			return (ni, nj)
		case _:
			raise Exception(f"Unexpected value {map[ni][nj]}")
    

def process_robot_moves(input: 'InputData'):
	robot_coords = find_robot(input.map)
	print("Initial robot coords", robot_coords)
	map = [list(row) for row in input.map]
	position = robot_coords
	for row in input.moves:
		for s in row:
			position = move_robot(position, s, map)
			print("Move", s)
			for row in map:
				print("".join(row))
	return map

def count_GPS(map):
    for i, row in enumerate(map):
        for j, s in enumerate(row):
			if s == "O":
				yield i * 100 + j 
    
# box = "O"
# empty_space = "."
# robot = "@"
# wall = "#"

input_data = get_input_data(file_path)
input_data.print()
map_after_processing = process_robot_moves(input_data)
for row in map_after_processing:
	print("".join(row))

