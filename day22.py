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
        return file.read().splitlines()

def mix(secret, number):
	return secret ^ number

def prune(secret):
	return secret % 16777216

def calculate_secret_number_after_X_iterations(secret_number, iter_count):
	for _ in range(iter_count):
		secret_number = prune(mix(secret_number, secret_number * 64))
		secret_number = prune(mix(secret_number, secret_number // 32))
		secret_number = prune(mix(secret_number, secret_number * 2048))
		print(secret_number)
	return secret_number



def main():
	print(calculate_secret_number_after_X_iterations(123, 1))

	# codes = get_input(FILE_PATH_MAIN)




if __name__ == "__main__":
	main()