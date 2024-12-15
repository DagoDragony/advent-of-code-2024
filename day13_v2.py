import os
import itertools
from dataclasses import dataclass
from typing import Tuple
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d13_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d13.txt')

@dataclass
class Machine:
    button_a: Tuple[int, int]
    button_b: Tuple[int, int]
    prize: Tuple[int, int]

    def __iter__(self):
        return iter((self.button_a[0], self.button_a[1], self.button_b[0], self.button_b[1], self.prize[0], self.prize[1]))

def parse_machine_behavior(machine_settings_str) -> Machine:
    button_pattern = r"Button [A|B]: X\+(\d+), Y\+(\d+)"
    prize_pattern = r"Prize: X=(\d+), Y=(\d+)"
    a_match = re.match(button_pattern, machine_settings_str[0])
    b_match = re.match(button_pattern, machine_settings_str[1])
    prize_match = re.match(prize_pattern, machine_settings_str[2])

    return Machine(
        (int(a_match.group(1)), int(a_match.group(2))),
        (int(b_match.group(1)), int(b_match.group(2))),
        (int(prize_match.group(1)), int(prize_match.group(2)))
    )

def get_machine_behaviors(file_path) -> list:
    print(f"Reading file {file_path}")
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    
    machine_behaviors_strings = [lines[i:i+4] for i in range(0, len(lines), 4)]
    return [parse_machine_behavior(machine_behavior_string) for machine_behavior_string in machine_behaviors_strings]

def is_whole_number(n):
    return n % 1 == 0

def get_price_mathematically(machine_settings, price_addition=0) -> int | None:
    ax, ay, bx, by, px, py = machine_settings
    px = px + price_addition
    py = py + price_addition
    b_count = (ay*px-ax*py)/(ay*bx-ax*by)
    a_count = (py-b_count*by)/ay
    if is_whole_number(a_count) and is_whole_number(b_count):
        return int(a_count * 3 + b_count)
    return None

if __name__ == "__main__":
    machine_settings = get_machine_behaviors(file_path)
    print("Machine settings")
    for machine in machine_settings:
        print(machine)

    print("-" * 100)
    prices1 = sum(filter(lambda r: r is not None, [get_price_mathematically(machine) for machine in machine_settings]))
    print(f"Result1: {prices1}")
    prices1 = sum(filter(lambda r: r is not None, [get_price_mathematically(machine, 10000000000000) for machine in machine_settings]))
    print(f"Result2: {prices1}")