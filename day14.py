import os
import itertools
from collections import Counter
from dataclasses import dataclass
from typing import Tuple
import re

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

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

file_path = os.path.join(script_dir, 'inputs/input_d14_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d14.txt')
robots_data = get_robots_data(file_path)
for robot_data in robots_data:
    print(robot_data)

boundaries_x, boundaries_y = (101, 103)

def count_robot_location(robot, time):
    ix, iy, vx, vy = robot
    final_x, final_y = ((vx * time + ix)/boundaries_x, (time*vy + iy)/boundaries_y)
    return (final_x, final_y)

def count_final_locations(robots, time):
    return [count_robot_location(robot, time) for robot in robots]

def count_robots_in_quadrants(final_locations):
    locations = Counter(final_locations)
    quadrant1 = (range(0, 50), )
    quadrant2 = (range(51-102),)
    quadrant1 = [from item, count in locations.items()]

    

