import os
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum
import time
import sys


sys.setrecursionlimit(10000)

# FILE_PATH = 'inputs/input_d17_example1.txt'
FILE_PATH = 'inputs/input_d17.txt'

@dataclass
class Program:
    a: int
    b: int
    c: int
    program: List[int]

    @staticmethod
    def parse(text) -> 'Program':
        lines = text.splitlines()
        register_A = lines[0].replace("Register A: ", "")
        register_B = lines[1].replace("Register B: ", "")
        register_C = lines[2].replace("Register C: ", "")
        program = lines[4].replace("Program: ", "")
        return Program(
            int(register_A),
            int(register_B),
            int(register_C),
            [int(op) for op in program.split(",")]
        )

@dataclass
class Register:
    a: int
    b: int
    c: int

# def get_output(operand, combo, register):

def get_combo_value(op_code, operand, register):
	match operand:
		case 0 | 1 | 2 | 3:
			return operand
		case 4:
			return register.a
		case 5:
			return register.b
		case 6:
			return register.c
		case 7:
			raise Exception(f"Found 7 in combo {op_code},{operand}")

def get_program_itself(program):
	program_without_jump = program[:-2]
	reversed_program = list(reversed(program))
	a_values = []
	print(reversed_program)
	a = 0 
	for i, code in enumerate(reversed_program):
		a = a * 8
		output = None
		print("searching for", code)
		done = 0
		while True:
			_, output = execute_iteration(program_without_jump, Register(a, 0, 0))
			if output == code:
				if i == 14 and done < 1:
					a = (a - (a // 8))
					print("previous a", a)
					done += 1
					# continue
				else:
					break
			a += 1
		_, output = execute_program(program, a, 0, 0)
		print("i", i, "found a", a)
		print("result:", output)
		a_values.append(a)

	return a
	
	# for i in reversed(program):
	# 	print(program[i])

def execute_iteration(program, register):
	counter = 0
	output = -1
	# print(program)
	while counter < len(program):
		if counter == len(program):
			# print("Program finished")
			break
		if counter + 1 >= len(program):
			raise Exception("counter is too far")

		op, operand = program[counter], program[counter + 1], 
		
		combo_ops = set([0, 2, 5, 6, 7])

		def truncate(number):
			return number % 8

		operand_value = get_combo_value(op, operand, register) if op in combo_ops else operand

		# print("operand")
		# print(f"   {counter}: {op},{operand} v={operand_value} A={register.a} B={register.b} C={register.c}")
		
		# recheck everything of which uses combo operands and which literal operands
		match op:
			case 0:
				# adv - A division 2 in power of combo_value, send to A
				register.a = register.a // (2**operand_value)
			case 1:
				# bxl - B bitwise XOR combo send to B
				register.b = register.b ^ operand_value
			case 2:
				# bst - combo modulo 8, truncate, send to B
				register.b = truncate(operand_value % 8)
			case 4:
				# bxc - B bitwise XOR C, send to B
				register.b = register.b ^ register.c
			case 5:
				# out - combo modulo 8, output
				# print(operand_value)
				output_number = operand_value % 8
				# print("ia", str(initial_a).rjust(3), "ib", str(initial_a % 8).rjust(3), "op", str(operand_value).rjust(3), "ic", str(register.c).rjust(3), "o", output_number)
				output = output_number
				# output.append(output_number)
			case 6:
				# bdv - like adv, but send to B
				register.b = register.a // (2**operand_value)
			case 7:
				# cdv - like adv, but send to C
				register.c = register.a // (2**operand_value)
		counter += 2
		# print(f">> {counter}: {op},{operand} v={operand_value} A={register.a} B={register.b} C={register.c}")
	return (register, output)

def execute_program(program, A, B, C):
	program_without_jump = program[:-2]

	output = []
	# print(program)
	register = Register(A, B, C)
	while register.a != 0:
		register, iteration_output = execute_iteration(program_without_jump, register)
		output.append(iteration_output)

	return (register, output)
     

def get_program(file_path) -> 'Program':
	script_dir = os.path.dirname(os.path.abspath(__file__))
	full_path = os.path.join(script_dir, file_path)
	with open(full_path, 'r') as file:
		return Program.parse(file.read())

def test(str_program, a=0, b=0, c=0, ea=None, eb=None, ec=None, eoutput=None):
	program = [int(l) for l in str_program.split(",")]
	register, output = execute_program(program, a, b, c)				
	# print(output, register)
	if ea != None:
		assert register.a == ea, f"{register.a} != {ea}"
	if eb != None:
		assert register.b == eb, f"{register.b} != {eb}"
	if ec != None:
		assert register.c == ec, f"{register.c} != {ec}"
	if eoutput != None:
		assert output == eoutput, f"outputs didn't match actual: {output} expected: {eoutput}"

def main():
	program = get_program(FILE_PATH)
	print(program)
	register, output = execute_program(program.program, program.a, program.b, program.c)				
	print(output, register)
	print(f"Result1: "+ ",".join([str(n) for n in output]))

	for i in range(1, 10):
		register, output = execute_program(program.program, i, program.b, program.c)				
		print(f"{i}: {output}")
	# 	# print(get_program_itself(program.program))
	# 	# print(i, output, register)
	# 	# print(f"Result1: "+ ",".join([str(n) for n in output]))


	a_for_program_copy = get_program_itself(program.program)
	# register, output = execute_program(program.program, a_for_program_copy, program.b, program.c)				
	# register, output = execute_program(program.program, 20534878121424, program.b, program.c)				
	register, output = execute_program(program.program, 164279024971426, program.b, program.c)				

	print(f"Result2: {a_for_program_copy}")
	print(f"Result   program: {output}")
	print(f"Original program: {program.program}")


	# test("2,6", c=9, eb=1)
	# test("5,0,5,1,5,4", a = 10, eoutput=[0, 1, 2])
	# test("1,7", b = 29, eb=26)
	# test("4,0", b= 2024, c=43690, eb=44354)

	# test("0,1,5,4,3,0", a = 2024, eoutput=[4,2,5,6,7,7,7,7,3,1,0], ea=0)

	# If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
	# pass



if __name__ == "__main__":
	main()
