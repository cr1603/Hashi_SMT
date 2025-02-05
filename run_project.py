import subprocess
import numpy as np
from verifier import *
from output_solution import *

test_to_run = "1"
test_file = f"hashi_test{test_to_run}.smt2"

convert_to_smt = f"python3 hashi_convert.py -f \"/mnt/e/Charlotte/Uni/Bachelorarbeit/input/test{test_to_run}.txt\""
run_smt = f"./cvc5 {test_file}"

result = subprocess.run(convert_to_smt, capture_output=True, text=True, shell=True)
helper = result.stdout.strip()
island_info = eval(helper) #parse representation of list (string) into actual array

# print(f"island_info: {island_info}")
# print(len(island_info))
# print(island_info[0])

connectivity = False

while(not connectivity):
    result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
    output = result.stdout.strip()
    print(f"cvc5 output:\n{output}")

    if(output[:5] != "unsat"):
        adjacency_matrix, bridge_list = output_formatter(output, island_info)
        print(f"adjacency matrix:\n{np.matrix(adjacency_matrix)}")
        #print(bridge_list)

        connectivity = verifier(adjacency_matrix)
        print(f"connected: {connectivity}")

        if(not connectivity):
            add_to_smt_file(bridge_list, test_file)
    else: break

print(bridge_list)