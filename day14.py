import os
import itertools
from collections import Counter
from dataclasses import dataclass
from typing import Tuple
import re

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

def in_any_quadrant(quadrants, item):
    for quadrant in quadrants:
        x_range, y_range = quadrant
        x, y = item
        if x in x_range and y in y_range:
            return True
    return False 

def count_robots_in_quadrants(robots, time):
    final_locations = count_final_locations(robots, time)
    print("final locations")
    print(sorted(final_locations))
    

    locations = Counter(final_locations)
    print("locations")
    print(locations)
    quadrant1 = (range(0, 50), range(0, 50))
    quadrant2 = (range(51,102),range(0, 50))
    quadrant3 = (range(0, 50), range(51, 104))
    quadrant4 = (range(51,102),range(51, 104))
    quadrants = [quadrant1, quadrant2, quadrant3, quadrant4]

    print_map(locations)
    print("quadrants")
    print(quadrants)


    robots_in_quadrants = [count for loc, count in locations.items() if in_any_quadrant(quadrants, loc)]
    return sum(robots_in_quadrants)

def print_map(locations):
    print('-' * 100)
    for y in range(0, boundaries_y):
        line = []
        for x in range(0, boundaries_x):
            if (x, y) in locations:
                line.append(str(locations[(x, y)]))
            else:
                line.append(".")
        print("".join(line))
    print('-' * 100)

# todo: remove
# boundaries_x, boundaries_y = (11, 7)

robots_data = get_robots_data(file_path)
for robot_data in robots_data:
    print(robot_data)


# print([(robot.initial_location[0], robot.initial_location[1]) for robot in robots_data])
# initial_counter = Counter([(robot.initial_location[0], robot.initial_location[1]) for robot in robots_data])
# print(initial_counter)
# print("Initial map")
# print_map(initial_counter)


print(f"Result1 {count_robots_in_quadrants(robots_data, 100)}")
# 500 - too low

    

