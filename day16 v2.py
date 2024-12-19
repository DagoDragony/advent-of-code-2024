from collections import defaultdict
from collections.abc import Iterable, Iterator
from heapq import heappop, heappush
from typing import TypeAlias, List
import os

# TODO: rewrite this again for training dijkstra

# FILE_PATH = 'inputs/input_d16_example1.txt'
# FILE_PATH = 'inputs/input_d16_example2.txt'
FILE_PATH = 'inputs/input_d16.txt'

RIGHT=(0, 1)
LEFT=(0, -1)
UP=(-1, 0)
DOWN=(1, 0)

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

Coord: TypeAlias = tuple[int, int]
Direction: TypeAlias = tuple[int, int]
Grid: TypeAlias = defaultdict[Coord, str]
PathState: TypeAlias = tuple[Coord, Direction]

def parse_input(lines: Iterable[str]) -> tuple[Grid, Coord, Coord]:
    grid: Grid = defaultdict(lambda: "#")
    start_pos, end_pos = None, None
    for i, row in enumerate(lines):
        for j, tile in enumerate(row):
            pos = (i, j)
            if tile == "S":
                start_pos = pos
            elif tile == "E":
                end_pos = pos
            grid[pos] = tile
    assert start_pos is not None and end_pos is not None
    return grid, start_pos, end_pos

def get_next_states(
        state: PathState,
        grid: Grid,
) -> Iterator[tuple[int, PathState]]:
    (i, j), direction = state
    (di, dj) = direction
    yield 1000, ((i, j), ROTATE_CLOCKWISE[direction])
    yield 1000, ((i, j), ROTATE_COUNTERCLOCKWISE[direction])
    next_node = (i + di, j + dj)
    if grid[next_node] != "#":
        yield 1, (next_node, direction)


def find_shortest_paths(
        start_state: PathState,
        end_pos: Coord,
		race_map: Grid
) -> tuple[int, Iterator[list[PathState]]]:
    costs: dict[PathState, int] = {}
    priority_queue: list[tuple[int, PathState]] = [(0, start_state)]
    prev_states: defaultdict[PathState, set[PathState]] = defaultdict(set)

    while priority_queue:
        cost, state = heappop(priority_queue)
        pos, *_ = state
        if pos == end_pos:
            break
        for weight, next_state in get_next_states(state, race_map):
            prev_cost = costs.get(next_state, float("inf"))
            next_cost = cost + weight
            if next_cost < prev_cost:
                costs[next_state] = next_cost
                heappush(priority_queue, (next_cost, next_state))
                prev_states[next_state] = {state}
            elif next_cost == prev_cost:
                prev_states[next_state].add(state)
    else:
        raise RuntimeError("no path exists!")

    start_node, *_ = start_state
    def walk(state: PathState) -> Iterator[list[PathState]]:
        node, *_ = state
        if node == start_node:
            yield [state]
            return
        for prev_state in prev_states[state]:
            for path in walk(prev_state):
                yield path + [state]

    last_state = state
    return cost, walk(last_state)


def get_input_lines(file_path) -> List[str]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)
	with open(full_path, 'r') as file:
		return file.read().splitlines()


def solve1(start_pos, end_pos, grid) -> int:
    cost, _ = find_shortest_paths((start_pos, (0, 1)), end_pos, grid)
    return cost


def solve2(start_pos, end_pos, grid) -> int:
    _, paths = find_shortest_paths((start_pos, (0, 1)), end_pos, grid)
    return len({pos for path in paths for pos, _ in path})


def main():
	race_map, start_pos, end_pos = parse_input(get_input_lines(FILE_PATH))
	# for row in race_map:
	# 	print(row)
	print(f"Result1: {solve1(start_pos, end_pos, race_map)}")
	print(f"Result2: {solve2(start_pos, end_pos, race_map)}")

if __name__ == "__main__":
	main()