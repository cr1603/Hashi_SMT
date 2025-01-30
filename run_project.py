import subprocess
from verifier import *

test_to_run = "test1"

convert_to_smt = f"python3 hashi_convert.py -f \"/mnt/e/Charlotte/Uni/Bachelorarbeit/input/{test_to_run}.txt\""

run_smt = f"./cvc5 hashi_{test_to_run}.smt2"

result = subprocess.run(convert_to_smt, capture_output=True, text=True, shell=True)
helper = result.stdout.strip()
island_info = eval(helper) #parse representation of list (string) into actual array

print(f"island_info: {island_info}")
print(len(island_info))
#print(island_info[0])

result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
output = result.stdout.strip()

#print(output)

adjacency_matrix = output_formatter(output, island_info)

print(adjacency_matrix)