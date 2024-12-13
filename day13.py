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
        return iter((self.button_a, self.button_b, self.prize))

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
        (int(prize_match.group(1)), int(prize_match.group(2)))
    )

print("PROCESSING PART 1...")
def get_machine_behaviors(file_path) -> list:
    print(f"Reading file {file_path}")
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file]
    
    machine_behaviors_strings = [lines[i:i+4] for i in range(0, len(lines), 4)]
    return [parse_machine_behavior(machine_behavior_string) for machine_behavior_string in machine_behaviors_strings]

file_path = os.path.join(script_dir, 'inputs/input_d13_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d13.txt')
machine_settings = get_machine_behaviors(file_path)

def get_price(a_count, b_count, coord, machine_settings):




def get_price(machine_settings):
    best_price = None 

    def get_options(machine_settings, coord, price, depth):
        nonlocal best_price

        if depth < 0:
            return None

        # print(depth)
        # time.sleep(0.01)

        bt_a, bt_b, prize = machine_settings

        if coord == prize:
            best_price = min(best_price, price)

        if best_price != None and best_price < price:
            print("best_price", best_price)
            return

        if coord[0] > prize[0] or coord[1] > prize[1]:
            # print("overeached_prize_coord")
            return

        get_options(machine_settings, (coord[0] + bt_a[0], coord[1] + bt_a[1]), price + 3, depth - 1)
        get_options(machine_settings, (coord[0] + bt_b[0], coord[1] + bt_b[1]), price + 1, depth - 1)
    
    get_options(machine_settings, (0, 0), 0, 100)
    
    return best_price

print("Machine settings")
print("-" * 100)
for machine in machine_settings:
    print(machine)
    print(get_price(machine))