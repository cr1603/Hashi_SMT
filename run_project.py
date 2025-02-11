import subprocess
import numpy as np
from hashi_convert import *
from verifier import *
from output_solution import *

test_to_run = "6"
test_file = f"hashi_test{test_to_run}.smt2"

open_test_file = f"python3 read_file.py -f \"input/test{test_to_run}.txt\""
#convert_to_smt = f"python3 hashi_convert.py -f \"/mnt/e/Charlotte/Uni/Bachelorarbeit/input/test{test_to_run}.txt\""
run_smt = f"./cvc5 {test_file}"

result = subprocess.run(open_test_file, capture_output=True, text=True, shell=True)
hashi_file = result.stdout.strip()
# print(result)
# print(hashi_file)

width, height, island_info, bridge_list = input(hashi_file)

# result = subprocess.run(convert_to_smt, capture_output=True, text=True, shell=True)
# helper = result.stdout.strip()
# island_info = eval(helper) #parse representation of list (string) into actual array

# print(f"island_info: {island_info}")
# print(len(island_info))
# print(island_info[0])

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

print(bridge_list)
print(bridge_list_smt)
print(bridge_value)

if len(bridge_list_smt) == 0:
    bridge_list_for_output = bridge_list.copy()
else:
    bridge_list_for_output = bridge_list_smt.copy()

output_solution(width, height, island_info, bridge_list_for_output, bridge_value)