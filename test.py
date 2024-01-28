import random

def readText(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()


    lines = [line.replace("\n", "") for line in lines]

    print(lines)

readText(file_path="./tik_configs/comments.txt")