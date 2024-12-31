import os
import os
from typing import Tuple, List, Dict

DAY = 22
FILE_PATH_EXAMPLE = f"inputs/d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/d{DAY}.txt"


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
	for i in range(iter_count):
		secret_number = prune(mix(secret_number, secret_number * 64))
		secret_number = prune(mix(secret_number, secret_number // 32))
		secret_number = prune(mix(secret_number, secret_number * 2048))

		current_price = secret_number % 10
		price_changes.append(current_price - last_price)

		prices.append(current_price)
		last_price = current_price

	price_changes_dict = {}
	seen_seq = set()
	for i in range(0, len(price_changes) - 3):
		key = tuple(price_changes[i:i+4])
		current_price = prices[i+3]
		# print(key, current_price)
		if not key in seen_seq:
			price_changes_dict[key] = current_price
			seen_seq.add(key)

	return (secret_number, price_changes_dict)


def main():
	secret_numbers = get_input(FILE_PATH_MAIN)

	all_price_changes = []
	all_secret_numbers = []
	for secret_number in secret_numbers:
		final_secret_number, price_changes = calculate_secret_number_after_X_iterations(secret_number, 2000)
		all_price_changes.append(price_changes)
		all_secret_numbers.append(final_secret_number)

	print("Result1:", sum(all_secret_numbers))

	general_combinations = set()
	for price_change in all_price_changes:
		general_combinations.update(price_change.keys())

	highest_sum = 0
	for general_combination in general_combinations:
		total_sold_for = 0
		for price_change_per_buyer in all_price_changes:
			sold_for = price_change_per_buyer.get(general_combination, 0)
			total_sold_for += sold_for
		
		if total_sold_for > highest_sum:
			highest_sum = total_sold_for

	print("highest_sum", highest_sum)


if __name__ == "__main__":
	main()