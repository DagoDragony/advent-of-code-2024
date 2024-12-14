import os
import itertools
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Tuple
import re
from math import prod

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d14_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d14.txt')

@dataclass
class RobotData:
	initial_location: Tuple[int, int]
	velocity: Tuple[int, int]

	def __str__(self):
		return f"p={self.initial_location} v={self.velocity}"

	def __iter__(self):
		return iter((self.initial_location[0], self.initial_location[1], self.velocity[0], self.velocity[1]))

def parse_robot_data(robot_data_row) -> RobotData:
	# print("machine_settings_str")
	# print(machine_settings_str)
	pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
	# print(machine_settings_str[0])
	match = re.match(pattern, robot_data_row)
	if match:
		return RobotData(
			(int(match.group(1)), int(match.group(2))),
			(int(match.group(3)), int(match.group(4)))
		)

print("PROCESSING PART 1...")
def get_robots_data(file_path) -> list:
	print(f"Reading file {file_path}")
	with open(file_path, 'r') as file:
		return [parse_robot_data(line.strip()) for line in file]


boundaries_x, boundaries_y = (101, 103)

def count_robot_location(robot, time):
	ix, iy, vx, vy = robot
	final_x, final_y = ((vx * time + ix)%boundaries_x, (time*vy + iy)%boundaries_y)
	return (final_x, final_y)

def count_final_locations(robots, time):
	return [count_robot_location(robot, time) for robot in robots]

def in_quadrant(quadrant, loc):
	x_range, y_range = quadrant
	x, y = loc
	if x in x_range and y in y_range:
		return True
	return False 

def get_quadrant_ranges():
	x_middle = boundaries_x // 2
	y_middle = boundaries_y // 2
	quadrant1 = (range(0, x_middle), range(0, y_middle))
	quadrant2 = (range(x_middle + 1, boundaries_x),range(0, y_middle))
	quadrant3 = (range(0, x_middle), range(y_middle + 1, boundaries_y))
	quadrant4 = (range(x_middle + 1,boundaries_x),range(y_middle +1, boundaries_y))
	return [quadrant1, quadrant2, quadrant3, quadrant4]

def count_robots_in_quadrants(robots, time):
	final_locations = count_final_locations(robots, time)
	print("final locations")
	print(sorted(final_locations))

	locations = Counter(final_locations)
	print("locations")
	print(locations)

	print_map(locations)

	q1, q2, q3, q4 = get_quadrant_ranges()
	q1_count = sum([count for loc, count in locations.items() if in_quadrant(q1, loc)])
	q2_count = sum([count for loc, count in locations.items() if in_quadrant(q2, loc)])
	q3_count = sum([count for loc, count in locations.items() if in_quadrant(q3, loc)])
	q4_count = sum([count for loc, count in locations.items() if in_quadrant(q4, loc)])

	print("Robots in quadrants")
	robots_in_quadrants = [q1_count, q2_count, q3_count, q4_count]
	print(robots_in_quadrants)
	return prod(robots_in_quadrants)

def print_robots_iterations_map(robots, max_time):
	for i in range(1, max_time):
		final_locations = set(count_final_locations(robots, i))
		y_locations = sorted([(y, x) for x, y in final_locations])
		# print(y_locations)

		# t = defaultdict(int)
		last_coord = (-1, -1)
		consecutive_count = 1
		for y, x in y_locations:
			if last_coord[0] + 1 == x and last_coord[1] == y:
				consecutive_count += 1
				if consecutive_count == 3:
					is_top = all([
						# about is .#.
						not (x-2, y-1) in final_locations,
						(x-1, y-1) in final_locations,
						not (x, y-1) in final_locations,
						# down is ###
						(x-2, y+1) in final_locations,
						(x-1, y+1) in final_locations,
						(x, y+1) in final_locations,
					])
					if is_top:
						print_map(Counter(final_locations))
						return i
			else:
				consecutive_count = 1
			
			last_coord = (x, y)
		
		# print_map(Counter(final_locations))
		
		# line_counts = t
		# seems_like_christmas_tree = final_

		# seems_like_christmas_tree = all([line_counts[y] <= line_counts[y+1] for y in range(boundaries_y-1, boundaries_y - 10, -1)])
		# # seems_like_christmas_tree = all([line_counts[y] == y + 2 for y in range(boundaries_y-4, 0, -1)])
		# # seems_like_christmas_tree = all([line_counts[y]  == y + 2 for y in range(boundaries_y-4, 0, -1)])

		# if seems_like_christmas_tree:
		# 	print("final_locations")
		# 	print(final_locations)
		# 	print("line_counts")
		# 	print(line_counts)
		# 	print(line_counts[3], line_counts[4])
		# 	print(line_counts[4], line_counts[5])
		# 	print(line_counts[5], line_counts[4])

		# 	locations = Counter(final_locations)
		# 	# print(locations)
		# 	print_map(locations)

		# 	break
		# if line_counts[3] > line_counts[4] and  line_counts[4] > line_counts[5] and line_counts[5] > line_counts[6]:
			# print(sorted([ for k, count in line_counts]))

			# break


def print_map(locations):
	print('-' * 100)
	# print(locations)
	for y in range(0, boundaries_y):
		line = [f"y: {y} |"]
		for x in range(0, boundaries_x):
			if (x, y) in locations:
				line.append(str(locations[(x, y)]))
			else:
				line.append(".")
		print("".join(line))
	print('-' * 100)

# # todo: remove for non example
# boundaries_x, boundaries_y = (11, 7)

robots_data = get_robots_data(file_path)
for robot_data in robots_data:
	print(robot_data)


# print([(robot.initial_location[0], robot.initial_location[1]) for robot in robots_data])
# initial_counter = Counter([(robot.initial_location[0], robot.initial_location[1]) for robot in robots_data])
# print(initial_counter)
# print("Initial map")
# print_map(initial_counter)


# print(f"Result1 {count_robots_in_quadrants(robots_data, 100)}")


print(print_robots_iterations_map(robots_data, 20000))