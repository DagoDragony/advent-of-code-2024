import os
from typing import Tuple, List, Dict
from collections import defaultdict, Counter
from itertools import combinations, groupby
from dataclasses import dataclass
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph

DAY = 24
FILE_PATH_EXAMPLE = f"inputs/input_d{DAY}_example1.txt"
FILE_PATH_EXAMPLE2 = f"inputs/input_d{DAY}_example2.txt"
FILE_PATH_EXAMPLE3 = f"inputs/input_d{DAY}_example3.txt"
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
			# print(f"{gate.result}: {gate.op1}({op_values[gate.op1]}) {gate.operator} {gate.op2}({op_values[gate.op2]}) = {result}")
			op_values[gate.result] = result
		else:
			unprocessed_gates.append(gate)
	return op_values


def binary_to_decimal(values):
	# print(values)
	number = 0
	for i, value in enumerate(values):
		number += (value * 2 ** i)
	return number

def decimal_to_binary(number) -> List[int]:
	# print(f"converting {number}")
	byte_list = []
	i = 0
	while number != 0:
		mod = number % 2
		byte_list.append(mod)
		number = number // 2
	
	# print(f"converted to {byte_list}")
	# print(f"converted back is  {binary_to_decimal(byte_list)}")
	return byte_list


def calculate_z_value(input):
	calculated_values = get_calculated_values(input)
	# for key, value in calculated_values.items():
		# print(key, value)

	z_values = sorted([ (key, int(value)) for key, value in calculated_values.items() if key.startswith("z") ])
	# for z_value in z_values:
		# print(z_value)

	return z_values

def solve1(input: Input):
	z_values = calculate_z_value(input)
	result = binary_to_decimal([value for _, value in z_values])
	return result

def solve2(input: Input):
	# print(input.initial_values)
	x_operands = sorted([(name, int(value)) for name, value in input.initial_values if name.startswith("x")])
	y_operands = sorted([(name, int(value)) for name, value in input.initial_values if name.startswith("y")]) 
	print("x o", x_operands)
	print("y o", y_operands)



	x_binary = [v for _, v in x_operands]
	y_binary = [v for _, v in y_operands]
	print("x b", x_binary)
	print("y b", y_binary)

	# x_decimal = binary_to_decimal(x_binary)
	# y_decimal = binary_to_decimal(y_binary)
	# print("x bin", bin(x_decimal))
	# print("y bin", bin(y_decimal))

	# expected_z_decimal = (x_decimal & y_decimal)
	expected_z_binary = [int(x_binary[i] and y_binary[i]) for i in range(len(x_binary))]

	actual_z_binary = [str(value) for _, value in calculate_z_value(input)]
	print("Expected:", expected_z_binary)
	print("Actual  :", [int(v) for v in actual_z_binary])

	mismatches = []
	for i in range(max(len(x_operands), len(y_operands)) + 1):
		expected = actual_z_binary[i] if len(actual_z_binary) > i else 0
		actual = expected_z_binary[i] if len(expected_z_binary) > i else 0

		if expected  != actual:
			mismatches.append(i)

	print("z mismatches", mismatches)
	
	mismatch_names = ["z{:02}".format(mismatch) for mismatch in mismatches]
	
	# all_mismatching_operands = set(mismatch_names)
	# members_to_check = list(mismatch_names)
	# while members_to_check:
	# 	member_to_check = members_to_check.pop()
	# 	for gate in input.gates:
	# 		if gate.result == member_to_check:
	# 			new_operands = [gate.op1, gate.op2]
	# 			def is_valid(operand):
	# 				return all([
	# 					operand not in all_mismatching_operands,
	# 					not operand.startswith("x"),
	# 					not operand.startswith("y")
	# 				])
	# 			valid_new_operands = [operand for operand in new_operands if is_valid(operand)]
	# 			for valid_new_operand in valid_new_operands:
	# 				all_mismatching_operands.add(valid_new_operand)
	# 				members_to_check.append(valid_new_operand)
	# print("all_mismatching_members", all_mismatching_operands)
	# print("all_mismatching_members_count:", len(all_mismatching_operands))


def main():
	input = get_input(FILE_PATH_MAIN)
	for value in input.initial_values:
		print(value)



	# Create a new directed graph
	dot = Digraph()

	for gate in input.gates:
		dot.node(gate.op1, gate.op1)
		dot.node(gate.op2, gate.op2)
		dot.node(gate.result, gate.result)

	for gate in input.gates:
		dot.edge(gate.op1, gate.result, label=gate.operator)
		dot.edge(gate.op2, gate.result, label=gate.operator)


	# Render and view the graph (in PNG format)
	dot.render('graph_operations', format='png', view=True)


	# # Create a graph
	# G = nx.Graph()
	# for gate in input.gates:
	# 	G.add_edge(gate.op1, gate.result, label=gate.operator)
	# 	G.add_edge(gate.op2, gate.result, label=gate.operator)

	# pos = nx.spring_layout(G)
	# labels = nx.get_edge_attributes(G, 'label')
	# nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue')
	# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

	# plt.show()

	# for gate in input.gates:
	# 	print(gate)

	# customizable_operands = set()
	# def is_new_customizable(operand: str):
	# 	return all([
	# 		not operand in customizable_operands,
	# 		not operand.startswith("x"),
	# 		not operand.startswith("y"),
	# 		# not operand.startswith("z"),
	# 	])
	# for gate in input.gates:
	# 	for op in [gate.op1, gate.op2, gate.result]:
	# 		if is_new_customizable(op):
	# 			customizable_operands.add(op)
	# print(customizable_operands)
	# print(len(customizable_operands))



	# print(f"Result1: {solve1(input)}")
	# print(f"Result2: {solve2(input)}")



		
if __name__ == "__main__":
	main()