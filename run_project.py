import subprocess
import numpy as np
import sys
from hashi_convert import *
from verifier import *
from output_solution import *
from generate_puzzle import *

class DevNull(object):
    def write(self, arg):
        pass

def solve_puzzle(run_smt, island_info):
    connectivity = False

    while(not connectivity):
        result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
        output = result.stdout.strip()
        print(f"cvc5 output:\n{output}")

        if(output[:5] != "unsat"):
            adjacency_matrix, bridge_list_smt, bridge_value = output_formatter(output, island_info)
            print(f"adjacency matrix:\n{np.matrix(adjacency_matrix)}")
            #print(bridge_list)

            connectivity = verifier(adjacency_matrix)
            print(f"connected: {connectivity}")

            if(not connectivity):
                add_to_smt_file(bridge_list_smt, test_file)
        else: break
    return output, bridge_list_smt, bridge_value

def generate(height, width):
    puzzle_file = generate_puzzle(height, width)

    open_puzzle_file = f"python3 read_file.py -f \"{puzzle_file}\""

    result = subprocess.run(open_puzzle_file, capture_output=True, text=True, shell=True)
    puzzle_file = result.stdout.strip()

    _, _, island_info, bridge_list = hashi_input(puzzle_file)

    return puzzle_file, island_info, bridge_list


solve_or_generate = input("Solve (s) puzzle or Generate (g) puzzle?\n")

if solve_or_generate == "s":
    test_to_run = "1"
    test_file = f"hashi_test{test_to_run}.smt2"

    open_test_file = f"python3 read_file.py -f \"input/test{test_to_run}.txt\""
    #convert_to_smt = f"python3 hashi_convert.py -f \"/mnt/e/Charlotte/Uni/Bachelorarbeit/input/test{test_to_run}.txt\""
    run_smt = f"./cvc5 {test_file}"

    result = subprocess.run(open_test_file, capture_output=True, text=True, shell=True)
    hashi_file = result.stdout.strip()
    # print(result)
    # print(hashi_file)    

    width, height, island_info, bridge_list = hashi_input(hashi_file)

    # # result = subprocess.run(convert_to_smt, capture_output=True, text=True, shell=True)
    # # helper = result.stdout.strip()
    # # island_info = eval(helper) #parse representation of list (string) into actual array

    # # print(f"island_info: {island_info}")
    # # print(len(island_info))
    # # print(island_info[0])

    output, bridge_list_smt, bridge_value = solve_puzzle(run_smt, island_info)
    # connectivity = False

    # while(not connectivity):
    #     result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
    #     output = result.stdout.strip()
    #     print(f"cvc5 output:\n{output}")

    #     if(output[:5] != "unsat"):
    #         adjacency_matrix, bridge_list_smt, bridge_value = output_formatter(output, island_info)
    #         print(f"adjacency matrix:\n{np.matrix(adjacency_matrix)}")
    #         #print(bridge_list)

    #         connectivity = verifier(adjacency_matrix)
    #         print(f"connected: {connectivity}")

    #         if(not connectivity):
    #             add_to_smt_file(bridge_list_smt, test_file)
    #     else: break

    # # print(bridge_list)
    # # print(bridge_list_smt)
    # # print(bridge_value)

    if(output[:5] != "unsat"):
        if len(bridge_list_smt) == 0:
            bridge_list_for_output = bridge_list.copy()
        else:
            bridge_list_for_output = bridge_list_smt.copy()

        output_solution(width, height, island_info, bridge_list_for_output, bridge_value)
    
elif solve_or_generate == "g":
    height = int(input("height of puzzle: "))
    width = int(input("width of puzzle: "))
    #print(f"Generate Puzzle")     

    puzzle_file, island_info, bridge_list = generate(height, width)

    puzzle_file_name = puzzle_file.split(".")

    test_file = f"hashi_{puzzle_file_name[0]}.smt2"
    run_smt = f"./cvc5 {test_file}"

    result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
    output = result.stdout.strip()

    # _stdout = sys.stdout
    # sys.stdout = DevNull()
    
    while(output[:5] == "unsat"):
        puzzle_file, island_info, bridge_list = generate(height, width)
        result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
        output = result.stdout.strip()
    
    solve_puzzle(run_smt, island_info)

    #sys.stdout = _stdout

    #puzzle_file = "generated_puzzle.txt"

    with open(puzzle_file, 'r') as file:
        file_lines = [line.strip('\n') for line in file.readlines()]
        for line in file_lines:
            print(line)




