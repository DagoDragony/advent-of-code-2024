import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_1_1.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
left = []
right = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        a, b = line.split('   ')

        left.append(int(a))
        right.append(int(b))

left.sort()
right.sort()

result1 = []

# result1 = sum(abs(a - b) for a, b in zip(sorted(left_list), sorted(right_list)))
for a, b in zip(left, right):
    result1.append(abs(a - b))

print(f"result1: {sum(result1)}")

print(f"PROCESSING PART 2...")
uniqueMembers = set(left)

occ_map = {}
for r in right:
    if r in uniqueMembers:
        occ_map[r] = occ_map.get(r, 0) + 1

result2_scores = []
for l in left:
    result2_scores.append(l * occ_map.get(l, 0))

print(f"rezult2 {sum(result2_scores)}")