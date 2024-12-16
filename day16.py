import os
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum

# FILE_PATH = 'inputs/input_d16_example1.txt'
# FILE_PATH = 'inputs/input_d16_example2.txt'
FILE_PATH = 'inputs/input_d16.txt'

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
	key = (position, direction)
	if key in cache:
		if cache[key].state == State.NO_PATH:
			return None
		if cache[key].state == State.REACHED_END and cache[key].value < score:
			return cache[key].value

	# cache.add((position, direction))
	i, j = position
	if (i, j) in visited:
		return None
	visited.add((i, j))

	# print("moved into", position)
	# print("found", map[i][j])
	match map[i][j]:
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

if __name__ == "__main__":
	main()
