import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/input_2_1_example.txt')
# file_path = os.path.join(script_dir, 'inputs/input_2_1.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 2...")
level_list = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        level_list.append(list(map(int, line.split(' '))))

def check_failure(a, b, ascending):
    diff = a - b
    print(diff)
    if abs(diff) < 1 or abs(diff) > 3:
        return False
    if ascending and diff > 0:
        return False
    if not ascending and diff < 0:
        return False
    return True

def is_last_index(i, arr):
    return i == len(arr) - 1

print(level_list)
safe_count = 0
for levels in level_list:
    if(len(levels) > 1):
        ascending = True if(levels[0] - levels[1] < 0) else False
    second_chance = False
    succeeded = True
    print(levels)
    i = 0
    while i < len(levels) - 1:
        good = check_failure(levels[i], levels[i+1], ascending)
        if not good:
            if second_chance:
                succeeded = False
                break;
            else:
                if not is_last_index(i + 1, levels):
                    print("2nd chance")
                    good = check_failure(levels[i], levels[i+2], ascending)
                    if good:
                        i += 1
                    else:
                        succeeded = False
                        break;
                else:
                    succeeded = False
                    break;
        i += 1
    print(succeeded)
    if succeeded:
        safe_count += 1

print(f"result1: {safe_count}")