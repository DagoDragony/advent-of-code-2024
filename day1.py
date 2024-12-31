from typing import List, Tuple
from collections import Counter

DAY = 1

def get_input(file_path) -> Tuple[List[int], List[int]]:
    print(f"Reading file {file_path}")
    left = []
    right = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            a, b = line.split('   ')

            left.append(int(a))
            right.append(int(b))

    return (sorted(left), sorted(right))


def solve1(left: List[int], right: List[int]) -> int:
    """
    Find distance between 2 sorted lists paired values
    and return sum
    """
    distances = []

    for a, b in zip(left, right):
        distances.append(abs(a - b))

    return sum(distances)


def solve2(left: List[int], right: List[int]) -> int:
    """
    Calculate similarity score
    Find how many times left list member appear in right one and multiply it by count
    """
    right_counter = Counter(right)
    # uniqueMembers = set(left)
    # occ_map = {}
    # for r in right:
    #     if r in uniqueMembers:
    #         occ_map[r] = occ_map.get(r, 0) + 1

    similarity_scores = [l * right_counter[l] for l in left]

    return sum(similarity_scores)


def main():
    left, right = get_input(f"inputs/input_d{DAY}.txt")
    print(f"Result1: {solve1(left, right)}")
    print(f"Result2: {solve2(left, right)}")

if __name__ == "__main__":
    main()