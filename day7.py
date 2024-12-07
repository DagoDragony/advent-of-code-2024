import os
from itertools import permutations
import sys

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d7_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d7.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
equations = []
with open(file_path, 'r') as file:
    for line in file.readlines():
        # print(line)
        answer_str, numbers_str = line.split(':')
        equations.append((int(answer_str), [int(number_str) for number_str in numbers_str.strip().split(' ')]))
        
for equation in equations:
    print(equation)

def calc_answer(operators, numbers, max_answer):
    agg_answer = numbers[0]
    for i in range(len(operators )):
        if agg_answer > max_answer:
            return sys.maxsize
        if agg_answer > answer:
            break
        if operators[i] == "+":
            agg_answer += numbers[i + 1]
        elif operators[i] == "*": 
            agg_answer *= numbers[i + 1]
    
    print(str(numbers[0]) + " " + "".join([f"{operators[i]} {numbers[i + 1]} " for i in range(len(operators))]) + f" = {agg_answer}")
    return agg_answer


def is_equation_possible(answer, numbers):
    # print(f"{answer}: {numbers}")
    operators = ["+" for _ in range(len(numbers) - 1)]
    if calc_answer(operators, numbers, answer) == answer:
        return True
    for i in range(len(operators)):
        operators[i] = "*"
        operators_sets = set(permutations(operators))
        print(operators_sets)
        for operators_set in operators_sets:
            if calc_answer(operators_set, numbers, answer) == answer:
                correct_equation = str(numbers[0]) + " " + "".join([f"{operators[i]} {numbers[i + 1]} " for i in range(len(operators))])
                return correct_equation
    return None
        
            
print("-"*100)    
possible_count = 0
for answer, numbers in equations:
    result = is_equation_possible(answer, numbers)
    if result != None:
        possible_count += 1
        print(result)

print("-"*100)    
print(f"Result: {possible_count}")
    

# # print(f"result1: {solve1(content)}")
