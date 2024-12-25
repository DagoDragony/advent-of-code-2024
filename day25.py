import os
from typing import Tuple, List, Dict, TypeAlias
from collections import defaultdict, Counter
from itertools import combinations, groupby
from dataclasses import dataclass
from collections import deque

DAY = 25
FILE_PATH_EXAMPLE = f"inputs/input_d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/input_d{DAY}.txt"

@dataclass
class Lock:
    pins: List[int]

@dataclass
class Key:
    pins: List[int]


def get_input(file_path) -> Tuple[List[Key], List[Lock]]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)

	with open(full_path, 'r') as file:
		all_content = file.read()
		entities = all_content.split("\n\n")
		keys = []
		locks = []
		for entity in entities:
			key_schema = entity.splitlines()
			if all(symbol == "#" for symbol in key_schema[0]):
				heights = []
				for j in range(len(key_schema[0])):
					new_height = 0
					for i in range(1, len(key_schema)):
						if key_schema[i][j] == "#":
							new_height += 1
					heights.append(new_height)
				locks.append(heights)
				# lock
			else:
				heights = []
				for j in range(len(key_schema[0])):
					new_height = 0
					for i in range(len(key_schema) - 1):
						if key_schema[i][j] == "#":
							new_height += 1
					heights.append(new_height)
				keys.append(heights)
		return (keys, locks)


def main():
	keys, locks = get_input(FILE_PATH_MAIN)
	print("Keys")
	for key in keys:
		print(key)
	print("Locks")
	for lock in locks:
		print(lock)

	perfectly_fitting = 0
	for lock in locks:
		for key in keys:
			if all(key[i]+ lock[i] <= 5 for i in range(len(lock))):
				perfectly_fitting += 1
	print("Result1:", perfectly_fitting)




		
if __name__ == "__main__":
	main()