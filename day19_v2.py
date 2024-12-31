import os
from dataclasses import dataclass, field
from typing import Tuple, Iterable, Dict

FILE_PATH_EXAMPLE = 'inputs/d19_example1.txt'
FILE_PATH_MAIN = 'inputs/d19.txt'

@dataclass
class Trie:
	nodes: Dict[str, Tuple['Trie', bool]] = field(default_factory=dict)

	def add(self, design) -> None:
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
def get_possible_variations(design, trie) -> int:
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
	
	possible_options = 0
	while designs_to_check:
		design_to_check = designs_to_check.pop()
		result = get_possible_variations(design_to_check, trie)
		possible_options += result
	cache[design] = possible_options

	return possible_options


def main():
	unsen_towels = get_input(FILE_PATH_MAIN)
	print(unsen_towels)
	trie = Trie()
	for towel in unsen_towels.towels:
		trie.add(towel)
	
	print(trie.nodes.keys())

	possible_designs = []
	possible_count = 0
	for _, design in enumerate(unsen_towels.designs):
		result = get_possible_variations(design, trie)
		possible_designs.append(result)
		if result > 0:
			possible_count += 1
		# print(f"{i} {design} {result}")

	print(f"Result1: {possible_count}")
	print(f"Result2: {sum(possible_designs)}")


if __name__ == "__main__":
	main()
