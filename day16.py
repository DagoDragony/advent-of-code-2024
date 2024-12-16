import os
from dataclasses import dataclass
from typing import Tuple, List

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d16_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d16.txt')


HORIZONTAL_EDGE_DIRECTION = {
    "[": 1,
    "]": -1
}
BOX_PARTS = set(["[", "]"])
DIRECTION_TRANSLATIONS = {
	"^": (-1, 0),
	"v": (1, 0),
	">": (0, 1),
	"<": (0, -1)
}
WIDEN_SYMBOL = {
	"#": "##",
	".": "..",
	"O": "[]",
	"@": "@.",
}

def find_robot(map):
	for i, row in enumerate(map):
		if '@' in row:
			return (i, row.index('@'))
	raise Exception("No robot found")

def get_map(file_path) -> List[str]:
	with open(file_path, 'r') as file:
		return file.read().splitlines()

def is_horizontal_direction(direction):
	return direction[1] != 0

def is_vertical_direction(direction):
	return direction[0] != 0

def move_boxes_horizontally(box_pos, dj, map):
	i, j = box_pos
	nj = j + 2 * dj

	dj2 = HORIZONTAL_EDGE_DIRECTION[map[i][j]]
	match map[i][nj]:
		case ".":
			map[i][j + dj + dj2] = map[i][j + dj]
			map[i][j + dj] = map[i][j]
			map[i][j] = "."
			return True
		case value if value in BOX_PARTS:
			move_boxes_horizontally((i, nj), dj, map)
			map[i][j + dj + dj2] = map[i][j + dj]
			map[i][j + dj] = map[i][j]
			map[i][j] = "."

# is there any max load?
def horizontal_move_possible_for_box(box_pos, dj, map):
	i, j = box_pos
	nj = j + 2 * dj
	match map[i][nj]:
		case "#":
			return False
		case ".":
			return True
		case value if value in BOX_PARTS:
			result = horizontal_move_possible_for_box((i, nj), dj, map)
			return result
		case value:
			raise Exception(f"Unknown symbol {map[i][nj]}")

def vertical_move_possible(tile_pos, di, map):
	i, j = tile_pos
	ni = i + di
	match map[ni][j]:
		case "#":
			return False
		case ".":
			return True
		case value if value in BOX_PARTS:
			jd = HORIZONTAL_EDGE_DIRECTION[value]
			return all([
				vertical_move_possible((ni, j), di, map),
				vertical_move_possible((ni, j + jd), di, map)
			])

def move_box_part(position, delta, map):
	i, j = position
	di, dj = delta
	map[i + di][j + dj] = map[i][j]
	map[i][j] = "."

def move_boxes_vertically(box_part_pos, di, map):
	i, j = box_part_pos
	ni = i + di
	if map[ni][j] in BOX_PARTS:
		dj2 = HORIZONTAL_EDGE_DIRECTION[map[ni][j]]
		move_boxes_vertically((ni, j), di, map)
		move_boxes_vertically((ni, j + dj2), di, map)
	move_box_part(box_part_pos, (di, 0), map)

def move_robot(robot_pos, move, map):
	i, j = robot_pos
	direction = DIRECTION_TRANSLATIONS.get(move)
	di, dj = direction
	ni, nj = i + di, j + dj
	match map[ni][nj]:
		case "#":
			return i, j
		case value if value in BOX_PARTS:
			horizontal_direction = is_horizontal_direction(direction)
			dj2 = HORIZONTAL_EDGE_DIRECTION[map[ni][nj]]
			if horizontal_direction:
				checks = [
					horizontal_move_possible_for_box((ni, nj), dj, map),
				]
				if all(checks):
					move_boxes_horizontally((ni, nj), dj, map)
					map[i][j] = "."
					map[ni][nj] = "@"
					return (ni, nj)
			else:
				# vertical direction
				checks = [
					vertical_move_possible((ni, nj), di, map),
					vertical_move_possible((ni, nj + dj2), di, map),
				]
				if all(checks):
					move_boxes_vertically((ni, nj), di, map)
					move_boxes_vertically((ni, nj+dj2), di, map)
					map[i][j] = "."
					map[ni][nj] = "@"
					return (ni, nj)
			return (i, j)
		case ".":
			map[i][j] = "."
			map[ni][nj] = "@"
			return (ni, nj)
		case _:
			raise Exception(f"Unexpected value {map[ni][nj]}")
    

def process_robot_moves(map, moves):
	robot_coords = find_robot(map)
	position = robot_coords
	for s in "".join(moves):
		position = move_robot(position, s, map)
	return map

def count_widened_GPS(map):
	for i, row in enumerate(map):
		for j, s in enumerate(row):
			if s == "[":
				yield i * 100 + j

def widen_input_data(map):
	widened_map = []
	for row in map:
		line = []
		for s in row:
			line.extend(WIDEN_SYMBOL.get(s))
		widened_map.append(line)
	return widened_map

def get_score(map):
	start = (len(map)-2, 1)
	print(map[start[0]][start[1]])
	end = (1, len(map)-2)
	print(map[end[0]][end[1]])

def main():
	race_map = get_map(file_path)
	for row in race_map:
		print(row)
	print(f"Result1: {get_score(race_map)}")

	# widened_input_data = widen_input_data(input_data.map)
	# for row in widened_input_data:
	# 	print("".join(row))
	# map_after_processing = process_robot_moves(widened_input_data, input_data.moves)
	# gps_sum = sum(count_widened_GPS(map_after_processing))
	# print(f"Result2: {gps_sum}")

if __name__ == "__main__":
    main()