import os
from dataclasses import dataclass
from typing import Tuple, List
import sys

sys.setrecursionlimit(10000)


FILE_PATH = 'inputs/input_d16_example1.txt'
# FILE_PATH = 'inputs/input_d16_example2.txt'
# FILE_PATH = 'inputs/input_d16.txt'

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

cache = {}
def make_a_move(position, direction, map, visited, score):
	key = (position, direction)
	# if key in cache:
	# 	return cache[key]

	# cache.add((position, direction))
	i, j = position
	if (i, j) in visited:
		return None
	visited.add((i, j))

	# print("moved into", position)
	# print("found", map[i][j])
	match map[i][j]:
		case "E":
			# print("End")
			return score
		case v if v != "#":
			clockwise = ROTATE_CLOCKWISE[direction]
			counterclockwise = ROTATE_COUNTERCLOCKWISE[direction]
			possible_scores = [score for score in  [
				make_a_move(next_tile(position, direction), direction, map, set(visited), score + 1),
				make_a_move(next_tile(position, clockwise), clockwise, map, set(visited), score + 1000 + 1),
				make_a_move(next_tile(position, counterclockwise), counterclockwise, map, set(visited), score + 1000 + 1),
			] if score]
			# print("Scores", possible_scores)
			final_score = min(possible_scores) if possible_scores else None
			cache[key] = final_score
			return final_score
		case _:
			cache[key] = None
			return None

def get_score(map):
	start = (len(map)-2, 1)
	print(map[start[0]][start[1]])
	end = (1, len(map)-2)
	print(map[end[0]][end[1]])
	return make_a_move(start, EAST_DIRECTION, map, set(), 0)

def main():
	race_map = get_map(FILE_PATH)
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
