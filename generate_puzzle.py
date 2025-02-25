import random

def write_cell(puzzle, cell_options):
    threshold = random.randrange(1, 10)
    if threshold>3:
        puzzle.write(".")
    else:
        puzzle.write(random.choice(cell_options))

def generate_puzzle(height, width):
    puzzle = open("generated_puzzle.txt", "w")

    middle_cells = ["1", "2", "3", "4", "5", "6", "7", "8"]
    edge_cells = ["1", "2", "3", "4", "5", "6"]
    corner_cells = ["1", "2", "3", "4"]
    small_puzzles = ["1", "2", "3", "4"]

    puzzle.write(f"{height} {width}\n")

    if height <= 5 or width <= 5:
        for i in range(height):
            for j in range(width):
                write_cell(puzzle, small_puzzles)
            puzzle.write("\n")
    else:
        for i in range(height):
            for j in range(width):
                if (i == 0 and j == 0) or (i == 0 and j == width-1) or (i == height-1 and j == 0) or (i == height-1 and j == width -1):
                    write_cell(puzzle, corner_cells)
                elif i == 0 or j == 0:
                    write_cell(puzzle, edge_cells)
                elif i == height-1 or j == width-1:
                    write_cell(puzzle, edge_cells)
                else:
                    write_cell(puzzle, middle_cells)
                # threshold = random.randrange(1, 10)
                # if threshold>3:
                #     puzzle.write(".")
                # else:
                #     puzzle.write(random.choice(cell_options))
            puzzle.write("\n")
    
    return puzzle.name