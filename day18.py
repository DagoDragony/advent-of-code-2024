import os
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum
import time

FILE_PATH = 'inputs/input_d18_example1.txt'
# FILE_PATH = 'inputs/input_d18.txt'

def get_input(file_path) -> List[Tuple[int, int]]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)
	with open(full_path, 'r') as file:
		coord_lists = [line.split(",") for line in file.read().splitlines()]
		return [(coord[0], coord[1]) for coord in coord_lists]

def test(str_program, a=0, b=0, c=0, ea=None, eb=None, ec=None, eoutput=None):
	program = [int(l) for l in str_program.split(",")]
	register, output = execute_program(program, a, b, c)				
	# print(output, register)
	if ea != None:
		assert register.a == ea, f"{register.a} != ea"
	if eb != None:
		assert register.b == eb, f"{register.b} != {eb}"
	if ec != None:
		assert register.c == ec, f"{register.c} != {ec}"
	if eoutput != None:
		assert output == eoutput, f"outputs didn't match actual: {output} expected: {eoutput}"

def fall(count, byte_coords):
	return byte_coords[:count]
	


def main():
	boundaries = (0, 6)
	byte_coords = get_input(FILE_PATH)

	print(byte_coords)


if __name__ == "__main__":
	main()
