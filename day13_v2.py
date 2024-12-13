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
        return iter((self.button_a[0], self.button_a[1], self.button_b[0], self.button_b[1], self.prize))

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
        (int(prize_match.group(1)) + 10000000000000, int(prize_match.group(2)) + 10000000000000)
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


def min_or_none(values):
    filtered_values = filter(None, values)
    return min(filtered_values, default=None)

def get_price(machine_settings) -> int | None:
    cache = {}
    def get_inner_price(a_count, b_count, machine_settings) -> int | None:
        nonlocal cache
        # if a_count > 100 or b_count > 100:
        #     return None

        # print(machine)
        # print("iteration", a_count, b_count)
        key = (a_count, b_count)
        if key in cache:
            return cache[key]

        current_price = a_count * 3 + b_count * 1
        b_ax, b_ay, b_bx, b_by, prize = machine_settings
        current_coord = (b_ax * a_count  + b_bx * b_count, b_ay * a_count + b_by * b_count)
        
        # if a_count == 80 and b_count == 40:
        #     print("found")
        #     print(a_count, b_count)
        #     print("prize", prize)
        #     print("current price", current_price)
        #     print("current coord", current_coord)

        if current_coord == prize:
            # print("found one")
            return current_price

        if current_coord[0] > prize[0] or current_coord[1] > prize[1]:
            # print("overeached_prize_coord")
            return
        
        r1 = get_inner_price(a_count + 1, b_count, machine_settings)
        r2 = get_inner_price(a_count, b_count + 1, machine_settings)

        final_result = min_or_none([r1, r2])
        cache[key] = final_result

        return min_or_none([r1, r2])
    return get_inner_price(0, 0, machine_settings)


print("Machine settings")
print("-" * 100)
prices = []
for machine in machine_settings:
    print(machine)
    result = get_price(machine)
    if result:
        prices.append(result)
    print(result)

print(f"Result1: {sum(prices)}")
