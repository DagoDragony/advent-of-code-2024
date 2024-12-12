import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_2_1_example.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
level_list = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        level_list = line.split(' ')
safe_count = 0
for levels in level_list:
    for i in range(len(levels)-1):
        diff = levels[i]-levels[i+1]
        if abs(diff) == 0 or abs(diff) > 3:
            break

    safe_count += 1

    

print(f"result1: {}")
print(f"rezult2 {}")