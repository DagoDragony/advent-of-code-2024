import os
from dataclasses import dataclass
from typing import Tuple, List

script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d15_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d15_example2.txt')
file_path = os.path.join(script_dir, 'inputs/input_d15_example3.txt')
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

def move_boxes_horizontally(box_position, dj, map):
	print("box_position", box_position)
	i, j = box_position
	nj = j + 2 * dj

	dj2 = horizontal_edge_direction[value]
	match map[i][nj]:
		case ".":
			map[i][j + dj] = map[i][j]
			map[i][j + dj + dj2] = "]"
			map[i][j] = "."
			return True
		case value if value in box_parts:
			move_boxes_horizontally((i, nj), dj, map)
			map[i][j] = "."
			map[i][j + dj] = "["
			map[i][j + dj] = "["
			map[i][nj] = "]"

# is there any max load?
def horizontal_move_possible_for_box(box_position, dj, map):
	print("checking horizontal move")
	i, j = box_position
	nj = j + 2 * dj
	match map[i][nj]:
		case "#":
			print("# Impossible")
			return False
		case ".":
			print(". Possible")
			return True
		case value if value in box_parts:
			# dj = horizontal_edge_direction[value]
			print("Found box, checking further")
			result = horizontal_move_possible_for_box((i, nj), dj, map)
			print(result)
			return result
		case value:
			raise Exception(f"Unknown symbol {map[i][nj]}")

horizontal_edge_direction = {
    "[": 1,
    "]": -1
}
box_parts = set(["[", "]"])

def vertical_move_possible(tile_position, di, map):
	i, j = tile_position
	ni = i + di
	
	# edge = map[i][j]
	match map[ni][j]:
		case "#":
			return False
		case ".":
			return True
		case value if value in box_parts:
			jd = horizontal_edge_direction[value]
			checks = [
				vertical_move_possible((ni, j), di, map),
				vertical_move_possible((ni, j + jd), di, map)
			]
			
			return all(checks)


def move_boxes_vertically(box_position, di, map):
	print("box_position", box_position)
	i, j = box_position
	ni = i + di
	edge = map[i][j]
	match map[ni][j]:
		case "." if edge == "[":
			map[i][j] = "."
			map[i][j+1] = "."
			map[ni][j] = "["
			map[ni][j+1] = "]"
			return True
		case "." if edge == "]":
			map[i][j] = "."
			map[i][j-1] = "."
			map[ni][j-1] = "["
			map[ni][j] = "]"
			return True
		case "]":
			print("moving ]")
			move_boxes_horizontally((ni, j), di, map)
			map[i][j] = "."
			map[i][j-1] = "."
			map[ni][j] = "]"
			map[ni][j-1] = "["
		case "[":
			print("moving [")
			move_boxes_horizontally((ni, j), di, map)
			map[i][j] = "."
			map[i][j+1] = "."
			map[ni][j] = "["
			map[ni][j+1] = "]"

def move_robot(robot_position, move, map):
	i, j = robot_position
	direction = direction_translations.get(move)
	di, dj = direction
	ni, nj = i + di, j + dj
	match map[ni][nj]:
		case "#":
			return i, j
		case value if value in box_parts:
			horizontal_direction = is_horizontal_direction(direction)
			# j_direction = horizontal_edge_direction[map[ni][nj]]
			if horizontal_direction:
				print("Horizontal")
				if horizontal_move_possible_for_box((ni, nj), dj, map):
					move_boxes_horizontally((ni, nj), dj, map)
					print("moved horizontally")
					map[i][j] = "."
					map[ni][nj] = "@"
					return (ni, nj)
				else:
					print("Couldn't move horizontally")
			else:
				print("Vertical")
				if vertical_move_possible((ni, nj), di, map):
					move_boxes_vertically((ni, nj), di, map)
					print("moved vertically")
					map[i][j] = "."
					map[ni][nj] = "@"
					return (ni, nj)
				else:
					print("Couldn't move vertically")
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
	count = 0 
	for row in moves:
		for s in row:
			count += 1
			if count > 2:
				raise Exception("Stopped")
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
map_after_processing = process_robot_moves(widened_input_data, input_data.moves)
# for row in map_after_processing:
# 	print("".join(row))
# print("Result1: ", sum(count_GPS(map_after_processing)))