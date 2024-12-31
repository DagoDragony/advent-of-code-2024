import os
import os
from typing import Tuple, List, Dict
from collections import defaultdict, Counter
from itertools import combinations, groupby

DAY = 23
FILE_PATH_EXAMPLE = f"inputs/d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/d{DAY}.txt"


def get_input(file_path) -> List[str]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)

	with open(full_path, 'r') as file:
		return { normalize(*line.split('-'))  for line in file.read().splitlines() }


def normalize(a, b):
	return (min(a, b), max(a, b))

def get_size_3_lan_parties(all_connections):
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
	return len([ party for party in found_LAN_parties if party[0][0] == "t" or party[1][0] == "t" or party[2][0] == "t"])

 

def get_biggest_lan_party(all_connections):
	biggest_lan_party = []
	connected_nodes = defaultdict(set)
	for a, b in all_connections:
		connected_nodes[a].add(b)
	for pc, connections in connected_nodes.items():
		possible_connections = [ normalize(a, b) for a, b in combinations(connections, 2) ]
		actual_connections = [connection for connection in possible_connections if connection in all_connections]

		nodes = [a for connection in actual_connections for a in connection]
		if not nodes:
			continue
		
		print("nodes", nodes)
		counts = Counter(nodes)

		duplicates = {item: count for item, count in counts.items() if count > 1}
		if not duplicates:
			continue
		print(duplicates)

		count_nodes = defaultdict(set)
		for node, count in duplicates.items():
			count_nodes[count].add(node)

		print("groups", count_nodes.items())
		print("duplicates", duplicates.items())

		max_count = max([key for key, _ in count_nodes.items()])
		print(max_count)

		for count in range(max_count, 1, -1):
			print(">>", count)
			if count in count_nodes:
				nodes = count_nodes[count]
				print("nodes:", nodes)
			if len(nodes) == count + 1:
				if len(biggest_lan_party) < len(nodes) + 1:
					biggest_lan_party = nodes | {pc}
				break
	return biggest_lan_party


def main():
	all_connections = get_input(FILE_PATH_MAIN)
	# print(all_connections)

	print("Result1", get_size_3_lan_parties(all_connections))
	biggest_lan_party = get_biggest_lan_party(all_connections)
	print("Result2", ",".join(sorted(list(biggest_lan_party))))

		
if __name__ == "__main__":
	main()