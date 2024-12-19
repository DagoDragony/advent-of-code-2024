import os
from dataclasses import dataclass
from typing import Tuple, List, Iterable
from enum import Enum
import time
import heapq

FILE_PATH_EXAMPLE = 'inputs/input_d19_example1.txt'
FILE_PATH_MAIN = 'inputs/input_d19.txt'

@dataclass
class UnsenTowels:
	towels: Iterable[str]
	designs: Iterable[str]


def get_input(file_path) -> List[Tuple[int, int]]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)
	with open(full_path, 'r') as file:
		lines = [line.split(",") for line in file.read().splitlines()]
		return UnsenTowels(
			lines[0],
			lines[2:]
		)


def main():
	unsen_towels = get_input(FILE_PATH_EXAMPLE)
	print(unsen_towels)


if __name__ == "__main__":
	main()
