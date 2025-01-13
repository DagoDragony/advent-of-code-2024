import os

DAY = 2

def get_input(file_path):
    with open(file_path, 'r') as file:
        level_list = [list(map(int, line.split(' '))) for line in file.readlines()]
    return level_list


def check_levels(levels):
    # print(f"checking {levels}")
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


def solve1(level_list):
    safe_count = 0
    for levels in level_list:
        succeeded = check_levels(levels)
        safe_count += succeeded
    return safe_count


def solve2(level_list):
    safe_count = 0
    for levels in level_list:
        succeeded = True
        succeeded = check_levels(levels)
        if not succeeded:
            for i in range(len(levels)):
                new_levels = list(levels)
                del new_levels[i]
                good = check_levels(new_levels)
                if good:
                    succeeded = True
                    break
        if succeeded:
            safe_count += 1
    return safe_count


level_list = get_input(f"inputs/d{DAY}.txt")
print(f"result1: {solve1(level_list)}")
print(f"result2: {solve2(level_list)}")