import os
import json

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def buka_json(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {file} tidak ditemukan.")
        return None