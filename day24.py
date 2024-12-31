import os
from typing import Tuple, List
from dataclasses import dataclass
from collections import deque

DAY = 24
FILE_PATH_EXAMPLE = f"inputs/d{DAY}_example1.txt"
FILE_PATH_EXAMPLE2 = f"inputs/d{DAY}_example2.txt"
FILE_PATH_EXAMPLE3 = f"inputs/d{DAY}_example3.txt"
FILE_PATH_MAIN = f"inputs/d{DAY}.txt"

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


def get_input(file_path) -> Input:
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)

	def parse_gate(line) -> Gate:
		action, result = line.split(" -> ")
		op1, operator, op2 = action.split(" ")
		return Gate(op1, operator, op2, result)

	def parse_value(line) -> Tuple[str, bool]:
		operand, value = line.split(": ")
		
		return (operand, True if value == "1" else False)


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
			op_values[gate.result] = result
		else:
			unprocessed_gates.append(gate)
	return op_values


def binary_to_decimal(values):
	number = 0
	for i, value in enumerate(values):
		number += (value * 2 ** i)
	return number

def decimal_to_binary(number) -> List[int]:
	byte_list = []
	i = 0
	while number != 0:
		mod = number % 2
		byte_list.append(mod)
		number = number // 2
	
	return byte_list


def calculate_z_value(input):
	calculated_values = get_calculated_values(input)

	z_values = sorted([ (key, int(value)) for key, value in calculated_values.items() if key.startswith("z") ])

	return z_values

def solve1(input: Input):
	z_values = calculate_z_value(input)
	result = binary_to_decimal([value for _, value in z_values])
	return result


def get_z_anomalies(gates: List[Gate]) -> List[str]:
	"""
	Getting z result should be done through XOR operation
	Exception - last z byte
 	"""
	z_to_swap = []
	last_z = "z" + str(max([int(gate.result[1:]) for gate in gates if gate.result.startswith("z")]))
	
	for gate in gates:
		if gate.result.startswith("z") and gate.result != last_z:
			if gate.operator != "XOR":
				z_to_swap.append(gate.result)
	return z_to_swap


def get_anomalies_2(gates: List[Gate]) -> List[str]:
	"""
	If inputs are not x, y and output is not z, then operations should be AND or OR
 	"""
	valid_operations = set(["AND", "OR"])

	def output_is_z(gate: Gate):
		return gate.result.startswith("z")

	invalid_operands = []
	for gate in gates:
		if not input_is_x_y(gate) and not output_is_z(gate):
			if not gate.operator in valid_operations:
				invalid_operands.append(gate.result)

	return invalid_operands

def input_is_x_y(gate: Gate):
	return gate.op1.startswith(("x", "y")) and gate.op2.startswith(("x", "y"))


def get_anomalies_3(gates: List[Gate]) -> List[str]:
	"""
	x, y XOR result must be input for another XOR operation
 	"""
	x_y_xor_gates = [gate for gate in gates if input_is_x_y(gate) and gate.operator == "XOR" and not is_x_y_00_operands(gate)]

	anomalies = []
	for x_y_xor_gate in x_y_xor_gates:
		found = False
		for gate in gates:
			fits = all([
				gate.operator == "XOR",
				gate.op1 == x_y_xor_gate.result or gate.op2 == x_y_xor_gate.result,
			])
			if fits:
				# print(gate)
				found = True
				break
		if not found:
			# print(x_y_xor_gate)
			anomalies.append(x_y_xor_gate.result)

	return anomalies

def is_x_y_00_operands(gate: Gate) -> bool:
	xy_00_operands = set(["x00", "y00"])
	return gate.op1 in xy_00_operands or gate.op2 in xy_00_operands


def get_anomalies_4(gates: List[Gate]) -> List[str]:
	"""
	if you have AND gate, result should be in OR gate or AND gate is faulty
 	"""
	and_gates = [gate for gate in gates if gate.operator == "AND" and not is_x_y_00_operands(gate) and not gate.result.startswith("z")]

	anomalies = []
	for and_gate in and_gates:
		found = False
		for gate in gates:
			fits = all([
				gate.operator == "OR",
				gate.op1 == and_gate.result or gate.op2 == and_gate.result,
				not input_is_x_y(gate)
			])
			if fits:
				found = True
				break
		if not found:
			anomalies.append(and_gate.result)

	return anomalies


def solve2(input: Input):
	return get_z_anomalies(input.gates) + get_anomalies_2(input.gates) + get_anomalies_3(input.gates) + get_anomalies_4(input.gates)


def main():
	input = get_input(FILE_PATH_MAIN)
	# for value in input.initial_values:
	# 	print(value)
	
	print("Result1:", solve1(input))
	print("Result2:",  ",".join(sorted(solve2(input))))

		
if __name__ == "__main__":
	main()