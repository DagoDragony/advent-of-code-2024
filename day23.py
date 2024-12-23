import os
import os
from typing import Tuple, List, Dict
from collections import defaultdict
from itertools import combinations

DAY = 23
FILE_PATH_EXAMPLE = f"inputs/input_d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/input_d{DAY}.txt"


def get_input(file_path) -> List[str]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)

	with open(full_path, 'r') as file:
		return { normalize(*line.split('-'))  for line in file.read().splitlines() }


def normalize(a, b):
	return (min(a, b), max(a, b))


def main():
	all_connections = get_input(FILE_PATH_MAIN)
	# print(all_connections)

	connected_nodes = defaultdict(set)
	for a, b in all_connections:
		connected_nodes[a].add(b)
		# ???
		# pairs[b].add(a)
	
	found_LAN_parties = []
	for pc, connections in connected_nodes.items():
		# print()
		# print("PC", pc)
		# print("-----------------------")
		# print(connections)
		possible_connections = [ normalize(a, b) for a, b in combinations(connections, 2) ]
		# print(possible_connections)
		for connection in possible_connections:
			# print(connection)
			if connection in all_connections:
				found_LAN_parties.append((pc, connection[0], connection[1]))
			
	# print("LAN parties", found_LAN_parties)
	# print("LAN count", len(found_LAN_parties))
	print("Result1", len([ party for party in found_LAN_parties if party[0][0] == "t" or party[1][0] == "t" or party[2][0] == "t"]))

	biggest_lan_party = []
	for pc, connections in connected_nodes.items():
		possible_connections = [ normalize(a, b) for a, b in combinations(connections, 2) ]
		actual_connections = [connection for connection in possible_connections if connection in all_connections]

		
		
if __name__ == "__main__":
	main()