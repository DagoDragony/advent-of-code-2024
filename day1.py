import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_1_1.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
left_list = []
right_list = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        content = line.split('   ')

        left_list.append(int(content[0]))
        right_list.append(int(content[1]))


left_list.sort()
right_list.sort()

result1 = []
for a, b in zip(left_list, right_list):
    result1.append(abs(a - b))

print(f"PROCESSING PART 1...")
uniqueMembers = set(left_list)

occ_map = {}
for r in right_list:
    if r in uniqueMembers:
        occ_map[r] = occ_map.get(r, 0) + 1

result2_scores = []
for l in left_list:
    result2_scores.append(l * occ_map.get(l, 0))



print(f"result1: {sum(result1)}")
print(f"rezult2 {sum(result2_scores)}")