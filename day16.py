import os
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum
import time

# FILE_PATH = 'inputs/input_d16_example1.txt'
FILE_PATH = 'inputs/input_d16_example2.txt'
# FILE_PATH = 'inputs/input_d16.txt'

RIGHT=(0, 1)
LEFT=(0, -1)
UP=(-1, 0)
DOWN=(1, 0)

EAST_DIRECTION = (0, 1)
ROTATE_CLOCKWISE = {
	(0, 1): (1, 0),
	(1, 0): (0, -1),
	(0, -1): (-1, 0),
	(-1, 0): (0, 1)
}
ROTATE_COUNTERCLOCKWISE = {
	(0, 1): (-1, 0),
	(-1, 0): (0, -1),
	(0, -1): (1, 0),
	(1, 0): (0, 1)
}

def get_map(file_path) -> List[str]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)
	with open(full_path, 'r') as file:
		return file.read().splitlines()


def next_tile(position, delta):
	i, j = position
	di, dj = delta
	return (i + di, j + dj)

class State(Enum):
    NO_PATH = 1
    BACK_IN_PATH = 2
    REACHED_END = 3

@dataclass
class NodeStatus:
    state: State
    value: int = 10**10

cache = {}

def make_a_move(position, direction, map, visited, score):
	# print("position", position)
	i, j = position
	symbol = map[i][j]
	if symbol == '#':
		return None

	key = (position, direction)
	if key in cache:
		# if cache[key].state == State.NO_PATH:
		# 	return None
		if cache[key].state == State.REACHED_END and cache[key].value < score:
			return cache[key].value

	# cache.add((position, direction))
	if position in visited:
		return None
	visited.add(position)

	# try:
	# 	symbol = map[i][j]
	# except Exception:
	# 	print((i, j))
	# 	print(len(map), len(map[0]))
	# 	print(map)
	# 	raise

	if symbol != 'E' and symbol != 'S':
		match direction:
			case v if v == LEFT:
				map[i][j] = ">"
				# print(">")
			case v if v == RIGHT:
				map[i][j] = "<"
				# print("<")
			case v if v == UP:
				map[i][j] = "^"
				# print("^")
			case v if v == DOWN:
				map[i][j] = "v"
				# print("v")
	
	for _, row in enumerate(map):
		line = ""
		for _, s in enumerate(row):
			line = line + s
		print(line)
	# time.sleep(0.5)

	# print("moved into", position)
	# print("found", map[i][j])
	match symbol:
		case "E":
			cache[key] = NodeStatus(State.REACHED_END, score)
			return score
		case v if v != "#":
			clockwise = ROTATE_CLOCKWISE[direction]
			counterclockwise = ROTATE_COUNTERCLOCKWISE[direction]
			possible_scores = [score for score in  [
				make_a_move(next_tile(position, direction), direction, map, visited.copy(), score + 1),
				make_a_move(next_tile(position, clockwise), clockwise, map, visited.copy(), score + 1000 + 1),
				make_a_move(next_tile(position, counterclockwise), counterclockwise, map, visited.copy(), score + 1000 + 1),
			] if score]
			# print("Scores", possible_scores)
			final_score = min(possible_scores) if possible_scores else None
			cache[key] = NodeStatus(State.BACK_IN_PATH)
			return final_score
		case _:
			cache[key] = NodeStatus(State.NO_PATH)
			return None

def make_a_move2(position, direction, map, visited, score):
	symbol = map[i][j]
	key = (position, direction)
	if symbol == '#':
		cache[key] = NodeStatus(State.NO_PATH)
		return None

	if key in cache:
		if cache[key].state == State.REACHED_END and cache[key].value < score:
			return cache[key].value

	# cache.add((position, direction))
	i, j = position
	if position in visited:
		return None
	visited.add((i, j))
	if symbol != 'E' and symbol != 'S':
		match direction:
			case v if v == LEFT:
				map[i][j] = ">"
				# print(">")
			case v if v == RIGHT:
				map[i][j] = "<"
				# print("<")
			case v if v == UP:
				map[i][j] = "^"
				# print("^")
			case v if v == DOWN:
				map[i][j] = "v"
				# print("v")

	for i, row in enumerate(map):
		line = ""
		for j, s in enumerate(row):
			line = line + s
			# if (i, j) in visited and not map[i][j] == 'E':
			# 	line = line + s
			# else:
		print(line)


	# print("moved into", position)
	# print("found", map[i][j])
	match symbol:
		case "E":
			cache[key] = NodeStatus(State.REACHED_END, score)
			return score
		case _:
			clockwise = ROTATE_CLOCKWISE[direction]
			counterclockwise = ROTATE_COUNTERCLOCKWISE[direction]
			possible_scores = [score for score in  [
				make_a_move(next_tile(position, direction), direction, map, visited.copy(), score + 1),
				make_a_move(next_tile(position, clockwise), clockwise, map, visited.copy(), score + 1000 + 1),
				make_a_move(next_tile(position, counterclockwise), counterclockwise, map, visited.copy(), score + 1000 + 1),
			] if score]
			# print("Scores", possible_scores)
			final_score = min(possible_scores) if possible_scores else None
			cache[key] = NodeStatus(State.BACK_IN_PATH)
			return final_score
		# case _:
		# 	return None

def get_score(map):
	start = (len(map)-2, 1)
	print(map[start[0]][start[1]])
	end = (1, len(map)-2)
	print(map[end[0]][end[1]])
	return make_a_move(start, EAST_DIRECTION, [list(row) for row in map], set(), 0)

def main():
	race_map = get_map(FILE_PATH)
	for row in race_map:
		print(row)
	print(f"Result1: {get_score(race_map)}")

if __name__ == "__main__":
	main()
