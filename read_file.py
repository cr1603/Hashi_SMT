import sys, getopt

hashi_file = None

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "f:")
except:
    print("Error")

## get game file via terminal ##
for opt, arg in opts:
    if opt in ['-f']:
        #print("found file")
        hashi_file = arg

## print to catch the output with subprocess in run_project.py ##
print(hashi_file)