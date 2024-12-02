import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_2_1.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 1...")
level_list = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        level_list.append(list(map(int, line.split(' '))))

print(level_list)
safe_count = 0
for levels in level_list:
    if(len(levels) > 1):
        ascending = True if(levels[0] - levels[1] < 0) else False
    succeeded = True
    print(levels)
    for i in range(len(levels) -1):
        diff = levels[i]-levels[i+1]
        print(diff)
        if abs(diff) == 0 or abs(diff) > 3:
            succeeded = False
            break
        if ascending and diff > 0:
            succeeded = False
            break
    if succeeded:
        safe_count += 1

print(f"result1: {safe_count}")