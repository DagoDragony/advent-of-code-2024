import os
import itertools
from collections import defaultdict

itertools.combinations

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d9_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d9.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
        disk_map = file.read() + "0"

print(disk_map)

def expand_disk_map(map):
    expanded_disk_map = []
    for i, symbol in enumerate(map):
        nmb = int(symbol)
        if i % 2 == 0:
            expanded_disk_map.append([str(i // 2) for n in range(nmb)])
        else:
            expanded_disk_map.append(["." for n in range(nmb)])
    return expanded_disk_map

def compact_disk_map(expaded_disk_map):
    empty_blocks = [(i, block) for i, block in enumerate(expanded_disk_map) if i % 2 == 1]
    number_blocks = list(reversed([(i, block) for i, block in enumerate(expanded_disk_map) if i % 2 == 0]))

    number_index = 0 
    empty_index = 0
    while True:
        empty_i, empty_block = empty_blocks[empty_index]
        number_i, number_block = number_blocks[number_index]

        if number_i <= empty_i:
            break

        if len(empty_block) >= len(number_block):
            for i, number in enumerate(number_block):
                empty_block[i] = number
            
            for i, 

            # copy one by one 
            expanded_disk_map[number_i] = 
            # empty one by one

            empty_index += 1
            number_index += 1
        elif len(empty_block) < len(number_block):
            number_index += 1



        if block
        

        # if last_emptied <= (ei, ej):
        #     break
        # #     lei, lej = last_emptied
        # #     expanded_disk_map[lei][lej] = expaded_disk_map[ni][nj]
        # else:
        # if (ei, ej) in filled:
        #     break

        expanded_disk_map[ei][ej] = expaded_disk_map[ni][nj]
        expanded_disk_map[ni][nj] = '.'

        # print("".join(["".join(ls) for i, ls in enumerate(expanded_disk_map)]))

# 00 998 111 888 2 777 333 6 44 6 555 566
expanded_disk_map = expand_disk_map(disk_map)
print(expanded_disk_map)
# print("".join(expanded_disk_map))
compact_disk_map(expanded_disk_map)
for l in expanded_disk_map:
    print(l)
print("checksum")
print(len(expanded_disk_map))
file_list = []

for i in range(0, len(expanded_disk_map), 2):
    file_list.append(expanded_disk_map[i] + expanded_disk_map[i+1])
print(file_list)


# final_sum = [i*int(file[i]) for file in file_list for i in range(len(file)) if file[i] != "."]
# final_sum = [i*int(file[i]) for file in file_list for i in range(len(file)) if file[i] != "." and file[i] != "X"]
print("-"*100)    

# print([int(n) for file in file_list for n in file if n != "." and n != "X"])
checksum_values = [0 if n == "." or n == "X" else int(n) for file in file_list for n in file]
checksum_products = [i * file for i, file in enumerate(checksum_values)]
print("checksum_values")
# print(checksum_values)
print("checksum_products")
# print(checksum_products)
print(f"result1: {sum(checksum_products)}")


# print(final_sum)
# print(sum(final_sum))
# print(expanded_disk_map)
            
# print("-"*100)    
# print(f"Result1: ")

# too low       6385338159123
# the right one 6385338159127
# too high      6385338185492