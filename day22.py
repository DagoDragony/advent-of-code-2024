import os
import os
from dataclasses import dataclass, field
from typing import Tuple, List, Iterable, TypeAlias, Dict
from enum import Enum
from collections import defaultdict
import time
from heapq import heappush, heappop
from itertools import groupby, permutations

DAY = 22
FILE_PATH_EXAMPLE = f"inputs/input_d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/input_d{DAY}.txt"


def get_input(file_path) -> List[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)
    with open(full_path, 'r') as file:
        return [int(line) for line in file.read().splitlines()]


def mix(secret, number):
	return secret ^ number

def prune(secret):
	return secret % 16777216

def calculate_secret_number_after_X_iterations(secret_number, iter_count) -> Tuple[int, Dict[Tuple[int, int, int], int]]:
	last_price = secret_number % 10
	price_changes = []
	prices = []
	for _ in range(iter_count):
		secret_number = prune(mix(secret_number, secret_number * 64))
		secret_number = prune(mix(secret_number, secret_number // 32))
		secret_number = prune(mix(secret_number, secret_number * 2048))

		current_price = secret_number % 10
		price_changes.append(current_price - last_price)
		prices.append(current_price)

	price_changes_dict = { 
                       tuple(price_changes[i:i+4]): prices[i+4+1] 
                       for i in range(0, len(price_changes) - 5) 
    }

	return (secret_number, price_changes_dict)


def main():
	secret_numbers = get_input(FILE_PATH_MAIN)
	# final_secret_numbers = [calculate_secret_number_after_X_iterations(secret_number, 2000) for secret_number in secret_numbers]

	all_price_changes = []
	for secret_number in  [1, 2, 3, 2024]:
		final_secret_number, price_changes = calculate_secret_number_after_X_iterations(secret_number, 2000)
		all_price_changes.append(price_changes)

	pool_of_price_changes = set()
	for price_change in all_price_changes:
		pool_of_price_changes.update(price_change.keys())

	highest_sum = 0
	for price_change in pool_of_price_changes:

	

	# print("Result1:", sum(final_secret_numbers))


if __name__ == "__main__":
	main()