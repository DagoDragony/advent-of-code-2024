import os
from dataclasses import dataclass
from typing import Tuple, List

script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d15_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d15_example2.txt')
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

def get_input_data(file_path) -> 'InputData':
	with open(file_path, 'r') as file:
		return InputData.parse(file.read())

direction_translations = {
	"^": (-1, 0),
	"v": (1, 0),
	">": (0, 1),
	"<": (0, -1)
}

def is_horizontal_direction(direction):
	return direction[1] != 0

def is_vertical_direction(direction):
	return direction[0] != 0

def move_boxes_horizontally(box_position, direction, load = 1):
	if load > 2:
		return False
	i, j = box_position
	di, dj = direction
	ni, nj = i + 2 * di, j + 2 * dj
	match map[ni][nj]:
		case "#":
			return False
		case ".":
			map[i][j] = "."
			map[i + di][j + dj] = "["
			map[ni][nj] = "]"
			return True
		case "[":
			if move_boxes_horizontally((ni, nj), direction, map, load+1):
				map[i][j] = "."
				map[i + di][j + dj] = "["
				map[ni][nj] = "]"
				return True
			else:
				return False

def move_boxes_vertically(box_position, di, map, load=1):
	if load > 2:
		return False
	i, j = box_position
	ni = i + di
	edge = map[i][j]
	match map[ni][nj]:
		case "#":
			return False
		case "." if edge == "[":
			map[i][j] = "."
			map[i][j+1] = "."
			map[ni][j] = "["
			map[ni][j+1] = "]"
			return True
		case "." if edge == "]":
			map[i][j] = "."
			map[i][j-1] = "."
			map[ni][j] = "]"
			map[ni][j+1] = "["
			return True
		case "]":
			if move_boxes_horizontally((ni, j), di, map, load+1):
				map[i][j] = "."
				map[i][j-1] = "."
				map[i + di][j + dj] = "["
				map[ni][nj] = "]"
				return True
			else:
				return False
		case "[":
			if move_boxes_horizontally((ni, nj), direction, map, load+1):
				map[i][j] = "."
				map[i + di][j + dj] = "["
				map[ni][nj] = "]"
				return True
			else:
				return False

def move_boxes(box_position, direction, map) -> bool:
	i, j = box_position
	di, dj = direction
	ni, nj = i + 2 * di, j + 2 * dj
	match map[ni][nj]:
		case "#":
			return False
		case ".":
			map[i][j] = "."
			map[i][j] = "."
			map[ni][nj] = "O"
			return True
		case "[":
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
    

def process_robot_moves(map, moves):
	robot_coords = find_robot(map)
	print("Initial robot coords", robot_coords)
	position = robot_coords
	for row in moves:
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

widen_symbol = {
	"#": "##",
	".": "..",
	"O": "[]",
	"@": "@.",
}

def widen_input_data(map):
	widened_map = []
	for row in map:
		line = []
		for s in row:
			line.extend(widen_symbol.get(s))
		widened_map.append(line)
	return widened_map

    
input_data = get_input_data(file_path)
widened_input_data = widen_input_data(input_data.map)
for row in widened_input_data:
	print("".join(row))
map_after_processing = process_robot_moves(input_data)
# for row in map_after_processing:
# 	print("".join(row))
# print("Result1: ", sum(count_GPS(map_after_processing)))

