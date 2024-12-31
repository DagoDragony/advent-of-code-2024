import os

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/d2.txt')
# file_path = os.path.join(script_dir, 'inputs/2_1_example.txt')

print(f"Reading file {file_path}")
print(f"PROCESSING PART 2...")
level_list = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        level_list.append(list(map(int, line.split(' '))))

def check_levels(levels):
    print(f"checking {levels}")
    ascending = True if(levels[0] - levels[1] < 0) else False
    for i in range(len(levels) - 1):
        diff = levels[i] - levels[i+1]
        # print(diff)
        if abs(diff) < 1 or abs(diff) > 3:
            return False
        if ascending and diff > 0:
            return False
        if not ascending and diff < 0:
            return False
    return True


print(level_list)
safe_count = 0
for levels in level_list:
    if(len(levels) > 1):
        ascending = True if(levels[0] - levels[1] < 0) else False
    second_chance = False
    succeeded = True
    succeeded = check_levels(levels)
    if not succeeded:
        for i in range(len(levels)):
            print(f"i={i}")
            new_levels = list(levels)
            print(f"removing {new_levels[i]}")
            del new_levels[i]
            good = check_levels(new_levels)
            if good:
                print("succeeded")
                succeeded = True
                break
    print(succeeded)
    if succeeded:
        safe_count += 1

print(f"result2: {safe_count}")