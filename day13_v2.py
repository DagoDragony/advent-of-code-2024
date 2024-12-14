import os
import itertools
from dataclasses import dataclass
from typing import Tuple
import re
import time

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

@dataclass
class Machine:
    button_a: Tuple[int, int]
    button_b: Tuple[int, int]
    prize: Tuple[int, int]

    # Enable unpacking by defining __iter__
    def __iter__(self):
        return iter((self.button_a[0], self.button_a[1], self.button_b[0], self.button_b[1], self.prize[0], self.prize[1]))

def parse_machine_behavior(machine_settings_str) -> Machine:
    # print("machine_settings_str")
    # print(machine_settings_str)
    button_pattern = r"Button [A|B]: X\+(\d+), Y\+(\d+)"
    prize_pattern = r"Prize: X=(\d+), Y=(\d+)"
    # print(machine_settings_str[0])
    a_match = re.match(button_pattern, machine_settings_str[0])
    b_match = re.match(button_pattern, machine_settings_str[1])
    prize_match = re.match(prize_pattern, machine_settings_str[2])

    # print(a_match)


    return Machine(
        (int(a_match.group(1)), int(a_match.group(2))),
        (int(b_match.group(1)), int(b_match.group(2))),
        # (int(prize_match.group(1)), int(prize_match.group(2)))
        (int(prize_match.group(1)) + 10000000000000, int(prize_match.group(2)) + 10000000000000)
    )

def get_machine_behaviors(file_path) -> list:
    print(f"Reading file {file_path}")
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    
    machine_behaviors_strings = [lines[i:i+4] for i in range(0, len(lines), 4)]
    return [parse_machine_behavior(machine_behavior_string) for machine_behavior_string in machine_behaviors_strings]

# file_path = os.path.join(script_dir, 'inputs/input_d13_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d13.txt')
print("PROCESSING PART 1...")
machine_settings = get_machine_behaviors(file_path)

def is_whole_number(n):
    return n % 1 == 0

def get_price_mathematically(machine_settings) -> int | None:
    ax, ay, bx, by, px, py = machine_settings
    b_count = (ay*px-ax*py)/(ay*bx-ax*by)
    a_count = (py-b_count*by)/ay
    if is_whole_number(a_count) and is_whole_number(b_count):
        return int(a_count * 3 + b_count)
    return None


print("Machine settings")
print("-" * 100)
prices = []
for machine in machine_settings:
    price = get_price_mathematically(machine)
    if price:
        prices.append(price)
        print(price)

print(f"Result1: {sum(prices)}")
