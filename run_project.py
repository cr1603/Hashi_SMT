import subprocess
import numpy as np
from hashi_convert import *
from verifier import *
from output_solution import *
from generate_puzzle import *


def solve_puzzle(solve_or_generate, run_smt, island_info, bridge_list):
    connectivity = False
    err = 0 ## for catching empty puzzles ##

    if island_info == []:
        print("empty_puzzle!")
        err = 1
        return err, "", [], 0
    else:
        while(not connectivity):
            ## run cvc5 on .smt2 file ##
            result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
            output = result.stdout.strip()
            if solve_or_generate == "s":
                print(f"cvc5 output:\n{output}\n")

            ## format output and check connectivity with adjacency matrix -> verifier.py ##
            if(output[:5] != "unsat"):
                adjacency_matrix, bridge_list_smt, bridge_value = output_formatter(output, island_info, bridge_list)
                if solve_or_generate == "s":
                    print(f"adjacency matrix:\n{np.matrix(adjacency_matrix)}")
                #print(bridge_list)

                connectivity = verifier(adjacency_matrix)
                if solve_or_generate == "s":
                    print(f"connected: {connectivity}\n")

                ## if puzzle is solvable with isolated island clusters, assert that this solution is not to be included in possible solutions in subsequent passes -> verifier.py ##
                if(not connectivity):
                    add_to_smt_file(bridge_list_smt, test_file)
            else: break
        return err, output, bridge_list_smt, bridge_value

def generate(height, width):
    ## puzzle generation -> generate_puzzle.py ##
    puzzle_file = generate_puzzle(height, width)

    open_puzzle_file = f"python3 read_file.py -f \"{puzzle_file}\""

    result = subprocess.run(open_puzzle_file, capture_output=True, text=True, shell=True)
    puzzle_file = result.stdout.strip()

    ## generate .smt2 file -> hashi_convert.py ##
    _, _, island_info, bridge_list = hashi_input(puzzle_file)

    return puzzle_file, island_info, bridge_list


solve_or_generate = input("Solve (s) puzzle or Generate (g) puzzle?\n")

if solve_or_generate == "s":

    ## test_to_run needs to be changed to solve different puzzles ##
    test_to_run = "1"
    test_file = f"hashi_test{test_to_run}.smt2"
    #test_file = f"hashi_generated_puzzle.smt2"

    ## cmd commands to run ##
    open_test_file = f"python3 read_file.py -f \"input/test{test_to_run}.txt\""## cmd command to run ##
    #open_test_file = f"python3 read_file.py -f \"generated_puzzle.txt\""
    #convert_to_smt = f"python3 hashi_convert.py -f \"/mnt/e/Charlotte/Uni/Bachelorarbeit/input/test{test_to_run}.txt\""
    run_smt = f"./cvc5 {test_file}"

    ## open puzzle file ##
    result = subprocess.run(open_test_file, capture_output=True, text=True, shell=True)
    hashi_file = result.stdout.strip()
    # print(result)
    # print(hashi_file)    

    ## generate .smt2 file -> hashi_convert.py ##
    width, height, island_info, bridge_list = hashi_input(hashi_file)

    # result = subprocess.run(convert_to_smt, capture_output=True, text=True, shell=True)
    # helper = result.stdout.strip()
    # island_info = eval(helper) #parse representation of list (string) into actual array

    # print(f"island_info: {island_info}")
    # print(len(island_info))
    # print(island_info[0])

    ## solve puzzle -> line 9 ##
    err, output, bridge_list_smt, bridge_value = solve_puzzle(solve_or_generate, run_smt, island_info, bridge_list)
   
    ## output solution if one exists -> output_solution.py ##
    if err == 0:
        if(output[:5] != "unsat"):
            if len(bridge_list_smt) == 0:
                bridge_list_for_output = bridge_list.copy()
            else:
                bridge_list_for_output = bridge_list_smt.copy()

            output_solution(width, height, island_info, bridge_list_for_output, bridge_value)
        
elif solve_or_generate == "g":
    ## user inputs dimensions of puzzle grid ##
    height = int(input("height of puzzle: "))
    width = int(input("width of puzzle: "))
    #print(f"Generate Puzzle")     

    ## generate puzzle -> line 42 ##
    puzzle_file, island_info, bridge_list = generate(height, width)

    ## for testing purposes ##
    # open_puzzle_file = f"python3 read_file.py -f \"generated_puzzle.txt\""

    # result = subprocess.run(open_puzzle_file, capture_output=True, text=True, shell=True)
    # puzzle_file = result.stdout.strip()

    # _, _, island_info, bridge_list = hashi_input(puzzle_file)

    
    puzzle_file_name = puzzle_file.split(".")

    test_file = f"hashi_{puzzle_file_name[0]}.smt2"
    run_smt = f"./cvc5 {test_file}"

    ## run cvc5 on generated puzzle ##
    result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
    output = result.stdout.strip()


    ## if puzzle is unsolvable or empty, keep generating new puzzles ##
    while(output[:5] == "unsat"): ## this while loop catches puzzles that are only solvable with isolated island clusters ##
        while(output[:5] == "unsat" or island_info == []):
            puzzle_file, island_info, bridge_list = generate(height, width)
            result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
            output = result.stdout.strip()
        
        solve_puzzle(solve_or_generate, run_smt, island_info, bridge_list)

    #puzzle_file = "generated_puzzle.txt"

    ## output generated puzzle ##
    with open(puzzle_file, 'r') as file:
        file_lines = [line.strip('\n') for line in file.readlines()]
        for line in file_lines:
            print(line)