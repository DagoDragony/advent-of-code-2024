import os

import numpy as np

# Get the absolute path of the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(script_dir, 'inputs/input_d5_example1.txt')
file_path = os.path.join(script_dir, 'inputs/input_d5.txt')

print(f"Reading file {file_path}")
print("PROCESSING PART 1...")
with open(file_path, 'r') as file:
    content = file.read()
    rules, update = content.split("\n\n")
    rule_list, update_list = ([rule.split("|") for rule in rules.split("\n")], [line.split(",") for line in update.split("\n")])

print(rule_list)
print(update_list)

rule_dict = {}
for page_before, page_after in rule_list:
    print(page_before, page_after)
    if page_after in rule_dict:
        rule_dict[page_after].append(page_before)
    else:
        rule_dict[page_after] = []
        rule_dict[page_after].append(page_before)

print(rule_dict)

def check_abides(update_line, rule_dict):
    for i in range(len(update_line)):
        page = update_line[i] 
        if page in rule_dict:
            successors = rule_dict[page]
            other_pages = update_line[i + 1:]
            print(f"page {page} successors {successors} other pages {other_pages}")
            # print([other_page for other_page in other_pages if other_page in successors])
            error_exists  = any([True for other_page in other_pages if other_page in successors])
            print(error_exists)

            if error_exists:
                return False
    return True

def get_correct_and_incorrect():
    passed_lines = []
    failed_lines = []
    for update_line in update_list:
        if check_abides(update_line, rule_dict):
            passed_lines.append(update_line)
        else:
            failed_lines.append(update_line)
    return (passed_lines, failed_lines)

correct_updates, incorrect_updates = get_correct_and_incorrect()


result1 = sum([int(ls[len(ls)//2]) for ls in correct_updates])
print(f"result1: {result1}")
# # print(f"result2: {solve2(content)}")

def fix_updates():
    incorrect_updates
    correct

def correct_update(update):
    # failed_counts = 
    for l in update:
        bad = rule_dict[l]
    [ for l in update]
    

