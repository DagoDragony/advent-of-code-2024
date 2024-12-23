import os
import os
from typing import Tuple, List, Dict
from collections import defaultdict

DAY = 23
FILE_PATH_EXAMPLE = f"inputs/input_d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/input_d{DAY}.txt"


def get_input(file_path) -> List[str]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)

	def normalize(a, b):
		return (min(a, b), max(a, b))

	with open(full_path, 'r') as file:
		return [ normalize(*line.split('-'))  for line in file.read().splitlines()]


def main():
	connections = get_input(FILE_PATH_EXAMPLE)
	pairs = defaultdict(set)
	for a, b in connections:
		pairs[a].add(b)
	
	found_LAN_parties = []
	for pc, connections in pairs.items():
		for 

	print(connections)





if __name__ == "__main__":
	main()