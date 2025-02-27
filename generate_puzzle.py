import random

def write_cell(puzzle, cell_options):
    threshold = random.randrange(1, 10)

    ## only ~30% of the cells will be islands ##
    if threshold>3:
        puzzle.write(".")
    else:
        puzzle.write(random.choice(cell_options))

def generate_puzzle(height, width):
    puzzle = open("generated_puzzle.txt", "w")

    middle_cells = ["1", "2", "3", "4", "5", "6", "7", "8"]
    ## islands on the edge of the board cannot have a value greater than 6 because they would need bridges in all four directions ##
    edge_cells = ["1", "2", "3", "4", "5", "6"]
    ## islands in the corners of the board cannot have a value greater than 4 because they would need bridges in at least three directions ##
    corner_cells = ["1", "2", "3", "4"]
    ## for small puzzles, island values are restricted to less than 4 to reduce generation time ##
    small_puzzles = ["1", "2", "3", "4"]

    puzzle.write(f"{height} {width}\n")

    ## puzzles are defined as small if one dimension of the boeard is at most 5 ##
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
    
    puzzle.close()
    return puzzle.name