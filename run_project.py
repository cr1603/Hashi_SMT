import subprocess

test_to_run = "test6"

convert_to_smt = f"python3 hashi_convert.py -f \"/mnt/e/Charlotte/Uni/Bachelorarbeit/input/{test_to_run}.txt\""

run_smt = f"./cvc5 hashi_{test_to_run}.smt2"

subprocess.run(convert_to_smt, shell=True)

result = subprocess.run(run_smt, capture_output=True, text=True, shell=True)
output = result.stdout.strip()

#print(output)