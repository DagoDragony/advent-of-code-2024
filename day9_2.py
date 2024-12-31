import os

script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/d9.txt')
file_path = os.path.join(script_dir, 'inputs/d9_example1.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
        disk_map = file.read() + "0"

print(disk_map)

def expand_disk_map(original_map):
    map = []
    for i, symbol in enumerate(original_map):
        nmb = int(symbol)
        if i % 2 == 0:
            map.append([str(i // 2) for n in range(nmb)])
        else:
            map.append(["." for n in range(nmb)])
    return map

def compact_disk_map(map):
    empty_blocks = [(i, block, len(block)) for i, block in enumerate(map) if i % 2 == 1]
    number_blocks = list(reversed([(i, block) for i, block in enumerate(map) if i % 2 == 0]))

    number_index = 0 
    while True:
        number_i, number_block = number_blocks[number_index]
        empty_index = 0
        while True:
            empty_i, empty_block, leftover = empty_blocks[empty_index]
            if number_i <= empty_i:
                break

            if leftover >= len(number_block):
                empty_start_index = len(empty_block) - leftover
                for i, number in enumerate(number_block):
                    empty_block[empty_start_index + i] = number
                    number_block[i] = "."
                leftover = leftover - len(number_block)
                empty_blocks[empty_index] = (empty_i, empty_block, leftover)
                break
            empty_index += 1
        number_index += 1
        if number_index == len(number_blocks) - 1:
            break
        # print("".join(["".join(ls) for i, ls in enumerate(expanded_disk_map)]))

def print_expanded_disk_map(map):
    print("".join([str(v) for l in map for v in l]))

# 00 998 111 888 2 777 333 6 44 6 555 566
expanded_disk_map = expand_disk_map(disk_map)
print_expanded_disk_map(expanded_disk_map)

compact_disk_map(expanded_disk_map)
print_expanded_disk_map(expanded_disk_map)

file_list = []
for i in range(0, len(expanded_disk_map), 2):
    file_list.append(expanded_disk_map[i] + expanded_disk_map[i+1])
print(file_list)

print("-"*100)    

checksum_values = [0 if n == "." else int(n) for file in file_list for n in file]
checksum_products = [i * file for i, file in enumerate(checksum_values)]

def print_with_comment(comment, printable):
    print(comment)
    print(printable)

# print_with_comment("check_sum", checksum_values)
# print_with_comment("checksum_products", checksum_products)

print(f"result1: {sum(checksum_products)}")