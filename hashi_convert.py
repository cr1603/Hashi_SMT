#from cvc5.pythonic import *
import sys, getopt
from itertools import chain
import shutil

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
    #print(int_islands)
    #print(data)

    #storing coordinate information as well as island number in one structure
    #print(list(enumerate(data)))
    island_info = []
    data_help = data.copy()
    for x, ele in enumerate(data_help):
        #print("x:" + str(x))
        if(x>0):
            for y in data_help[x]:
                print("y:" + str(y))
                print(data_help[x])
                index = data_help[x].find(y)
                print("index: " + str(index))
                if(data_help[x][index] != '.'):
                    island_info.append((x,index+1,int(data_help[x][index]))) #indices for the grid start at the top left corner with (1,1)
                data_help[x] = data_help[x][:index] + '_' + data_help[x][index+1:] #replace the character after I've passed it, so islands with the same value can be recorded independedly
    print(island_info)
            
    hashi_constraints(width, height, island_info, hashi_file)

# def piece(i, j, d, w, h):
#     res = (w*h) * (i-1) + w * (j-1) + d #assumption: w = h
#     return res

def hashi_constraints(w, h, island_info, hashi_file):
     
    #d: 0 = empty; 1 = 1 horizontal bridge; 2 = 2 horizontal bridges; 3 = 1 vertical bridge: 4: 2 vertical bridges; 5: island
    res = []
    help = hashi_file.split(".")
    #print("file_name_parts: " + str(help))
    file_name_parts = help[0].split("/")
    #print("file_name_parts: " + str(file_name_parts))
    file = open(shutil.copyfile('hashi.smt2', 'hashi_' + file_name_parts[7] + '.smt2'), 'a')
    x_coord = [x for x, y, v in island_info]
    y_coord = [y for x, y, v in island_info]
    value   = [v for x, y, v in island_info]

    # print("x_coord: " + str(x_coord))
    # print("y_coord: " + str(y_coord))

    #each cell can be one of the above defined game pieces, but only one (not islands, as these can be explicitly set)
    # for i in range(1, w+1):
    #     for j in range(1, w+1):
    #         res.append([piece(i, j, d, w, h) for d in range(0, 5)]) 
    #         for d in range(1, 10):
    #             for dp in range(d + 1, 10):
    #                 res.append([-piece(i, j, d, w, h), -piece(i, j, dp, w, h)])

    #set each island piece and all possible pieces for the rest of the cells per definition of d
    for i in range(1, h+1):    
        #print("i outside: " + str(i))
        for j in range(1,w+1):
            # print("i out: " + str(i))
            # print("j out: " + str(j))
            if i == x_coord[0] and j == y_coord[0]:
                # print("i if: " + str(i))
                # print("j if: " + str(j))
                # print("x: " + str(x_coord[0]))
                # print("y: "+ str(y_coord[0]))
                res.append((5))
                file.write("(assert = (Island " + str(x_coord[0]) + " " + str(y_coord[0]) + ") " + str(value[0]) + ")\n") #generating islands
                x_coord.pop(0)
                y_coord.pop(0) #remove coordinates after use
                value.pop(0)
                #print("res: " + str(res))
            elif i == 1 or i == h+1: #upper and lower edge can only be horizontal bridges
                # print("i else: " + str(i))
                # print("j else: " + str(j))
                # print("x: " + str(x_coord[0]))
                # print("y: "+ str(y_coord[0]))
                res.append((0,1,2))
                #print("res: " + str(res))
            elif j == 1 or j == w+1: # right and left edge can only be vertical bridges
                res.append((0,3,4))
            else:
                res.append((0,1,2,3,4))
    
    #print(res)
    file.close()


    # def valid(cells):
    #     if(i == 1 or i == h):
    #         for d in range(3, 5):
    #             res.append([-v(i, j, d, w, h)])



    return res
     
        
input()