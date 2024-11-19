#from cvc5.pythonic import *
import sys, getopt
from itertools import chain

def input():
    hashi_file = None

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "f:")
    except:
        print("Error")

    # get game file via terminal
    for opt, arg in opts:
        if opt in ['-f']:
            #print("found file")
            hashi_file = arg

    #print("name of file: " + hashi_file)

    #f = open(hashi_file, "r")
    # for x in f:
    #     print (x)
    #print(int(f.read(2)))
    #print(f.read())

    # extract data from file
    with open(hashi_file, encoding = 'utf8') as f:
        data = [line.strip('\n') for line in f.readlines()]
    print (data)

    # first line is the dimensions of the game board
    grid_wxh = data[0].split(' ')
    #print(grid_wxh)

    width = int(grid_wxh[0])
    height = int(grid_wxh[1])

    # extract information about the islands from the rest of the file: removing "." and subsequent empty entries
    islands = []
    for i in range(1, len(data)):
        islands.append(data[i].split('.'))
    for x in range(len(islands)):
        while("" in islands[x]):
            islands[x].remove("")
    islands = [ele for ele in islands if ele !=[]]
    #print(type(islands))
    #print(islands)

    #flattening islands array and turning it into an integer array
    int_islands = []
    flat_islands = list(chain.from_iterable(islands))
    #print(flat_islands)
    for i in range (len(flat_islands)):
        int_islands.append(int(flat_islands[i]))
    print(int_islands)
    #print(data)

    #storing coordinate information as well as island number in one structure
    #print(list(enumerate(data)))
    island_info = []
    for x, ele in enumerate(data):
        #print("x:" + str(x))
        if(x>0):
            for y in data[x]:
                #print("y:" + str(y))
                #print(data[x])
                index = data[x].find(y)
                if(data[x][index] != '.'):
                    island_info.append((x,index+1,int(data[x][index]))) #indices for the grid start at the top left corner with (1,1)
    print(island_info)
            



    hashi_constraints(int_islands)



def hashi_constraints(int_islands):
     res = []
     
     return res

input()