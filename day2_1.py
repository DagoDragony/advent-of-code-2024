import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/2_1_example.txt')
file_path = os.path.join(script_dir, 'inputs/d2.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
level_list = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        level_list.append(list(map(int, line.split(' '))))
print(level_list)

def check_levels(levels):
    print(f"checking {levels}")
    ascending = True if(levels[0] - levels[1] < 0) else False
    for i in range(len(levels) - 1):
        diff = levels[i] - levels[i+1]
        if abs(diff) < 1 or abs(diff) > 3:
            return False
        if ascending and diff > 0:
            return False
        if not ascending and diff < 0:
            return False
    return True


safe_count = 0
for levels in level_list:
    succeeded = check_levels(levels)
    # print(succeeded)
    safe_count += succeeded

print(sum([int(check_levels(levels)) for levels in level_list]))
print(f"result1: {safe_count}")