import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_d7_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/input_d7.txt')

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

print("-"*100)    
# # print(f"result1: {solve1(content)}")
