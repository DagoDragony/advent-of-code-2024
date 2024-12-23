import os
from dataclasses import dataclass, field
from typing import Tuple, List, Iterable, Dict
from enum import Enum
from collections import defaultdict
import time
import heapq

FILE_PATH_EXAMPLE = 'inputs/input_d19_example1.txt'
FILE_PATH_MAIN = 'inputs/input_d19.txt'


@dataclass
class Trie:
	nodes: Dict[str, Tuple['Trie', bool]] = field(default_factory=dict)

	# def __str__(self):
	# 	"\n".join([
	# 		f"{self.nodes.keys()}"

	# 		])



	def add(self, design):
		last_trie = self
		for i,  strip in enumerate(design):
			last_strip = (len(design) - 1) == i
			next_trie, next_stop = last_trie.nodes[strip] if strip in last_trie.nodes else (Trie(), False)

			if last_strip:
				last_trie.nodes[strip] = (next_trie, True)
			else:
				last_trie.nodes[strip] = (next_trie, next_stop)
			
			last_trie = next_trie


@dataclass
class UnsenTowels:
	towels: Iterable[str]
	designs: Iterable[str]


def get_input(file_path) -> 'UnsenTowels':
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)
	with open(full_path, 'r') as file:
		lines = file.read().splitlines()
		return UnsenTowels(
			lines[0].split(", "),
			lines[2:]
		)

cache = {}
def is_design_possible(design, trie):
	# print("trie.nodes.keys", trie.nodes.keys())
	# print("design", design)
	if design in cache:
		return cache[design]

	designs_to_check = []
	
	if not design:
		return True

	last_trie = trie
	for i, strip in enumerate(design):
		if strip in last_trie.nodes:
			next_trie, stop = last_trie.nodes[strip]
			if stop:
				next_design = design[(i+1):]
				designs_to_check.append(next_design)

			last_trie = next_trie	
		else:
			break
	
	while designs_to_check:
		design_to_check = designs_to_check.pop()
		if is_design_possible(design_to_check, trie):
			cache[design_to_check] = True
			return True
		else:
			cache[design_to_check] = False
	return False


def main():
	unsen_towels = get_input(FILE_PATH_MAIN)
	print(unsen_towels)
	trie = Trie()
	for towel in unsen_towels.towels:
		trie.add(towel)
	
	print(trie.nodes.keys())

	possible_designs = []
	for i, design in enumerate(unsen_towels.designs):
		result = is_design_possible(design, trie)
		possible_designs.append(result)
		print(f"{i} {design} {result}")

	print(f"Result1: {sum(possible_designs)}")


if __name__ == "__main__":
	main()
