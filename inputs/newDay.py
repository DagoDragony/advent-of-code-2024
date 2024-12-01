#!/bin/env python3

import configparser
import os
import requests
import sys
from jinja2 import Environment, FileSystemLoader

home = os.path.expanduser('~')


def get_session_id(tokenName):
    config = configparser.ConfigParser()
    config.read(f"{home}/.config/addition")
    return config['Other'][tokenName]


def get_input_data(day, session_cookie, input_file_path):
    print("Before request")
    url = f"https://adventofcode.com/2024/day/{day}/input"
    headers = {"Cookie": f"session={session_cookie}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Save the input data to a file
        with open(input_file_path, 'w') as file:
            file.write(response.text.strip())

        print(f"Input data for day {day} saved to {input_file_path}")
    else:
        print(f"Failed to fetch input data for day {day}. Status code: {response.status_code}")


def create_directory_and_files(day, code_base_path, resources_base_path):
    resource_files = [f"d{day}e.txt", f"d{day}h.txt", f"d{day}w.txt"]

    for file_name in resource_files:
        full_path = os.path.join(f"{resources_base_path}", file_name)
        if not os.path.isfile(full_path) or os.path.getsize(full_path) == 0:
            file_path = os.path.join(f"{resources_base_path}", file_name)
            with open(file_path, 'w+'):
                pass

    print(f'Directory "{day}" and files created successfully.')


def getNextDirectoryName(base_path):
    # Get all directories in the base path
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    # Extract numeric indices from directory names
    indices = [int(d[3:]) for d in directories if d.startswith("day") and d[3:].isdigit()]

    if indices:
        # Find the maximum index
        max_index = max(indices)
    else:
        # If no indices are found, start from 0
        max_index = 0

    return max_index + 1


if __name__ == "__main__":
    code_base_path = '../scala'
    resources_base_path = '.'



    day_nmb = sys.argv[1] if len(sys.argv) > 1 else getNextDirectoryName(code_base_path)

    create_directory_and_files(day_nmb, code_base_path, resources_base_path)

    session_id = get_session_id('HomeSessionId')
    get_input_data(day_nmb, session_id, f"{resources_base_path}/input_{day_nmb}_1.txt")