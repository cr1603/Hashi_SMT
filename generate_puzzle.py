import random

def generate_puzzle(height, width):
    puzzle = open("generated_puzzle.txt", "w")

    cell_options = [".", "1", "2", "3", "4", "5", "6", "7", "8"]

    puzzle.write(f"{height} {width}\n")

    for i in range(height):
        for j in range(width):
            puzzle.write(random.choice(cell_options))
        puzzle.write("\n")


generate_puzzle(5,5)