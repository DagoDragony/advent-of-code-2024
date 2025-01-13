import os

DAY = 2

script_dir = os.path.dirname(os.path.abspath(__file__))

def get_input(file_path):
    with open(file_path, 'r') as file:
        level_list = [list(map(int, line.split(' '))) for line in file.readlines()]
    return level_list


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


level_list = get_input(f"inputs/d{DAY}.txt")
safe_count = 0
for levels in level_list:
    succeeded = check_levels(levels)
    safe_count += succeeded


print(sum([int(check_levels(levels)) for levels in level_list]))
print(f"result1: {safe_count}")