import os
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum
import time
import sys
import heapq


sys.setrecursionlimit(10000)

# FILE_PATH = 'inputs/input_d16_example1.txt'
FILE_PATH = 'inputs/input_d16_example2.txt'
# FILE_PATH = 'inputs/input_d16.txt'

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

EAST_DIRECTION = (0, 1)
ROTATE_CLOCKWISE = {
	UP: RIGHT,
	RIGHT: DOWN,
	DOWN: LEFT,
	LEFT: UP 
}
ROTATE_COUNTERCLOCKWISE = {
	UP: LEFT,
	LEFT: DOWN,
	DOWN: RIGHT,
	RIGHT:  UP
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
price = {}
def make_a_move(pos, direction, map, visited, score):
	i, j = pos
	symbol = map[i][j]
	if symbol == '#':
		return None

	if pos in price:
		if price[pos] > score:
			# add cheaper score to this cell
			price[pos] = score
		else:
			return None
	else:
		price[pos] = score

	match symbol:
		case "E":
			# cache[key] = NodeStatus(State.REACHED_END, score)
			return
		case v if v != "#":
			clockwise = ROTATE_CLOCKWISE[direction]
			counterclockwise = ROTATE_COUNTERCLOCKWISE[direction]
			make_a_move(next_tile(pos, direction), direction, map, visited.copy(), score + 1),
			make_a_move(next_tile(pos, clockwise), clockwise, map, visited.copy(), score + 1000 + 1),
			make_a_move(next_tile(pos, counterclockwise), counterclockwise, map, visited.copy(), score + 1000 + 1),
			return
		case _:
			return

def get_all_direction(pos):
	i, j = pos
	return [(i + di, j + dj) for di, dj in ALL_DIRECTIONS]

# visited = set()
def walk_to_bests(pos, path, final_score, map):
	i, j = pos
	price[pos] == 0
	if map[i][j] == "E":
		return path

	def check_if_valid(new_pos):
		result = new_pos in price and price[new_pos] < final_score # and not pos in visited
		# if result:
		# 	print("position to go", new_pos, price.get(new_pos))
		return result
	
	all_directions = get_all_direction(pos)
	positions_to_go = [ new_pos for new_pos in all_directions if check_if_valid(new_pos)]
	# time.sleep(0.5)

	success_paths = filter(lambda x: x != None, [walk_to_bests(pos_to_go, path | { pos }, final_score, map) for pos_to_go in positions_to_go])
	if not success_paths:
		return None
	else:
		return [position for path in success_paths for position in path]
	

def get_best_paths_tile_count(start, end, map):
	visited = set()

	def check_if_valid(new_pos):
		result = new_pos in price and not new_pos in visited
		# if result:
		# 	print("position to go", new_pos, price.get(new_pos))
		return result

	def walk(pos):
		print("pos", pos)
		visited.add(pos)
		all_directions = get_all_direction(pos)
		positions_to_go = [new_pos for new_pos in all_directions if check_if_valid(new_pos)]
		print("positions_to_go", positions_to_go)
		for ptg in positions_to_go:
			print(ptg, price[ptg])
		if not positions_to_go:
			return
		# print("positions_to_go", positions_to_go)

		minimum_price = min([price[ptg] for ptg in positions_to_go])
		print("minimum_price", minimum_price)
		final_positions_to_go = [ptg for ptg in positions_to_go if price[ptg] == minimum_price]
		for fptg in final_positions_to_go:
			walk(fptg)

	walk(end)
	
	return visited

# def get_adjacent(start, end, map):
# 	i, j = start

# 	for


# 	while True:
		




# def get_price_path(start, max_boundary):
# 	i, j = start







# 	adj = {}
# 	# visited = {}
# 	for y in range(max_boundary + 1):
# 		for x in range(max_boundary + 1):
# 			adj[(x, y)] = (w, get_all_direction((x, y), max_boundary))
# 			# visited.add((x, y))
# 	# print("adj", adj)

# 	shortest = {}
# 	minHeap = [[0, start]]
# 	while minHeap:
# 		# print("minHeap", minHeap)
# 		w1, n1 = heapq.heappop(minHeap)
# 		if n1 in shortest:
# 			continue
# 		shortest[n1] = w1
		

# 		# print("n1", n1, "w1", w1)
# 		# print(f"adj[{n1}]", adj[n1])
# 		for n2 in adj[n1]:
# 			if n2 not in shortest:
# 				heapq.heappush(minHeap, [w1 + 1, n2])
	
# 	return shortest


def get_score(map):
	start = (len(map)-2, 1)
	print("start", start)
	end = (1, len(map)-2)
	print("end", end)
	make_a_move(start, EAST_DIRECTION, [list(row) for row in map], set(), 0)

	final_price = price[end]
	best_paths = get_best_paths_tile_count(start, end, map)
	tile_count = len(best_paths)

	for i, row in enumerate(map):
		line = ""
		for j, s in enumerate(row):
			if (i, j) in best_paths:
				line += "^"
			else:
				line += s
		print(line)

	print("--- price")
	for key, value in sorted(price.items()):
		print(key, "->", value)
	print("---")

	return (final_price, tile_count)

def main():
	race_map = get_map(FILE_PATH)
	for row in race_map:
		print(row)
	price, tile_count = get_score(race_map)
	print(f"Result1: {price}")
	print(f"Result2: {tile_count}")


if __name__ == "__main__":
	main()
