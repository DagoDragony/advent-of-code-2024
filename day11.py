import os
import itertools
from collections import defaultdict, deque

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'inputs/d11_example1.txt')
# file_path = os.path.join(script_dir, 'inputs/d11.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
        initial_stones = [int(str_stone) for str_stone in file.read().strip().split(" ") ] 

def get_stones_after_n_blinks(i_stones, blinks):
    stones = deque(i_stones)
    for iteration in range(blinks):
        print(iteration)
        shift = 0
        for i in range(len(stones)):
            index = i + shift
            n = stones[index]
            if n == 0:
                stones[index] = 1
            elif (len(str(n)) % 2 == 0):
                str_stone = str(n)
                middle_index = int(len(str_stone) / 2)
                stones[index] = int(str_stone[:middle_index])
                stones[index] = int(str_stone[:middle_index])
                stones.insert(index, int(str_stone[middle_index:]))
                shift += 1
            else:
                stones[index] = stones[index] * 2024
    return stones

stone_count_cache = {}

def get_next_stones_2(stone):
    if stone == 0:
        return [1]
    elif (len(str(stone)) % 2 == 0):
        str_stone = str(stone)
        middle_index = int(len(str_stone) / 2)
        stones = [int(str_stone[:middle_index]), int(str_stone[middle_index:])]
        return stones
    else:
        stones = [stone * 2024]
        return stones

def get_stones_count(stone, left_iterations):
    key = (stone, left_iterations)
    if key in stone_count_cache:
        return stone_count_cache[key]
    if left_iterations == 1:
        result = len(get_next_stones_2(stone))
        stone_count_cache[key] = result
        return result
    else:
        result = sum([get_stones_count(new_stone, left_iterations - 1) for new_stone in get_next_stones_2(stone)])
        stone_count_cache[key] = result
        return result

    
# def get_stones

# def get_next_stones(stone, max_depth):
#     if stone in cache:
#         return cache[stone]


#     stones = get_next_stones()


#     if n == 0:
#         stones[index] = 1
#     elif (len(str(n)) % 2 == 0):
#         str_stone = str(n)
#         middle_index = int(len(str_stone) / 2)
#         stones[index] = int(str_stone[:middle_index])
#         stones[index] = int(str_stone[:middle_index])
#         stones.insert(index, int(str_stone[middle_index:]))
#         shift += 1
#     else:
#         stones[index] = stones[index] * 2024


# def get_stones_after_n_blinks_efficient(i_stones, blinks):
#     cache = defaultdict(list)
#     stones = deque(i_stones)
#     for iteration in range(blinks):
#         get_next_stones()
#         print(iteration)
#     return stones

print("Initial stones")
print(initial_stones)
print("Stones after 25 blinks")
result_25 = sum(get_stones_count(stone, 25) for stone in initial_stones)
print(result_25)
print("Stones after 75 blinks")
result_75 = sum(get_stones_count(stone, 75) for stone in initial_stones)
print(result_75)

# count = 0
# for stone in initial_stones:
#     print(stone)
#     count += get_stones_count(stone, 75)
# print(count)





# stones_after_25_blinks = get_stones_after_n_blinks(initial_stones, 25)
# # print(stones_after_25_blinks)
# print(len(stones_after_25_blinks))
# stones_after_75_blinks = get_stones_after_n_blinks(initial_stones, 75)
# # print(stones_after_25_blinks)
# print(len(stones_after_75_blinks))

# n - {
#      iter1: n1
#      iter2: n2
#      iter3: n3
#      iter4: n4
# }

# 0 -> 1
# 1 -> [2024]
# 2024 -> [20, 24]
# 20 -> [2, 0]
# 24 -> [2, 4]
# 2 -> [2*2024]
# 4 -> [4*2024]





