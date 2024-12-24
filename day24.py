import os
from typing import Tuple, List, Dict
from collections import defaultdict, Counter
from itertools import combinations, groupby
from dataclasses import dataclass
from collections import deque

DAY = 24
FILE_PATH_EXAMPLE = f"inputs/input_d{DAY}_example1.txt"
FILE_PATH_MAIN = f"inputs/input_d{DAY}.txt"

@dataclass
class Gate:
	op1: str
	operator: str
	op2: str
	result: str


@dataclass
class Input:
	initial_values: List[Tuple[str, bool]]
	gates: List[Gate]


def get_input(file_path) -> List[Gate]:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)

	def parse_gate(line) -> Gate:
		action, result = line.split(" -> ")
		op1, operator, op2 = action.split(" ")
		return Gate(op1, operator, op2, result)

	def parse_value(line) -> Tuple[str, bool]:
		operand, value = line.split(": ")
		return (operand, bool(value))


	with open(full_path, 'r') as file:
		all_content = file.read()
		starting_values_content, gates_content = all_content.split("\n\n")
		initial_values =[ parse_value(line) for line in starting_values_content.splitlines()]
		gates = [ parse_gate(line) for line in gates_content.splitlines()]

		return Input(initial_values, gates)

def execute_operation(op1, operator, op2):
	match operator:
		case "AND":
			return op1 and op2
		case "OR":
			return op1 or op2
		case "XOR":
			return op1 ^ op2
		case _:
			raise Exception(f"Uknown operator {operator}")


def get_calculated_values(input):
	op_values = { op: value for op, value in input.initial_values }
	unprocessed_gates = deque()
	for gate in input.gates:
		unprocessed_gates.append(gate)

	while unprocessed_gates:
		gate = unprocessed_gates.popleft()
		assert not gate.result in op_values

		if gate.op1 in op_values and gate.op2 in op_values:
			result = execute_operation(op_values[gate.op1], gate.operator, op_values[gate.op2])
			print(f"{gate.result}: {gate.op1}({op_values[gate.op1]}) {gate.operator} {gate.op2}({op_values[gate.op2]}) = {result}")
			op_values[gate.result] = result
		else:
			unprocessed_gates.append(gate)
	return op_values


def binary_to_decimal(values):
	print(values)
	number = 0
	for i, value in enumerate(values):
		number += (value * 2 ** i)
	return number


def main():
	input = get_input(FILE_PATH_EXAMPLE)
	for value in input.initial_values:
		print(value)

	for gate in input.gates:
		print(gate)

	calculated_values = get_calculated_values(input)
	for key, value in calculated_values.items():
		print(key, value)

	z_values = sorted([ (key, int(value)) for key, value in calculated_values.items() if key.startswith("z") ])
	for z_value in z_values:
		print(z_value)

	result = binary_to_decimal([value for _, value in z_values])
	print(result)

		
if __name__ == "__main__":
	main()