#from cvc5.pythonic import *
#import sys, getopt
from itertools import chain
import shutil

def input(hashi_file):
    #moved to other file to enable data transfer
    # hashi_file = None

    # argv = sys.argv[1:]
    # try:
    #     opts, args = getopt.getopt(argv, "f:")
    # except:
    #     print("Error")

    # # get game file via terminal
    # for opt, arg in opts:
    #     if opt in ['-f']:
    #         #print("found file")
    #         hashi_file = arg

    # #print("name of file: " + hashi_file)

    # extract data from file
    with open(hashi_file, encoding = 'utf8') as f:
        data = [line.strip('\n') for line in f.readlines()]
    #print (data)

    # first line is the dimensions of the game board
    grid_wxh = data[0].split(' ')
    #print(grid_wxh)

    height = int(grid_wxh[0])
    width = int(grid_wxh[1])

    # extract information about the islands from the rest of the file: removing "." and subsequent empty entries
    islands = []
    for i in range(1, len(data)):
        islands.append(data[i].split('.'))
    # print(islands)
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

    #filling data with 0's where theres's a "." to work with it under specific circumstainces (skipping checking for 0's during island assignment): stored in new array
    islands_with_0 = []
    for i in range (1, len(data)):
        islands_with_0.append(data[i].replace(".", "0"))
    #print(islands_with_0)

    #storing coordinate information as well as island number in one structure
    #print(list(enumerate(data)))
    island_info = []
    #island_info.append((width, height, 0)) #coordinate information to give over to run_project
    data_help = data.copy()
    for x, ele in enumerate(data_help):
        #print("x:" + str(x))
        if(x>0):
            for y in data_help[x]:
                #print("y:" + str(y))
                #print(data_help[x])
                index = data_help[x].find(y)
                #print("index: " + str(index))
                if(data_help[x][index] != '.'):
                    island_info.append((x,index+1,int(data_help[x][index]))) #indices for the grid start at the top left corner with (1,1)
                data_help[x] = data_help[x][:index] + '_' + data_help[x][index+1:] #replace the character after I've passed it, so islands with the same value can be recorded independedly
    #print(island_info) #print needed to catch as output for further processing
    #island_info = island_info[1:] #take out dimension information for further processing afterwards
            
    bridge_list = hashi_constraints(width, height, island_info, hashi_file, islands_with_0)

    return width, height, island_info, bridge_list


def hashi_constraints(w, h, island_info, hashi_file, islands_with_0):

    #d: 0 = empty; 1 = 1 horizontal bridge; 2 = 2 horizontal bridges; 3 = 1 vertical bridge: 4: 2 vertical bridges; 5: island
    #res = []
    help = hashi_file.split(".")
    #print("file_name_parts: " + str(help))
    file_name_parts = help[0].split("/")
    #print("file_name_parts: " + str(file_name_parts))
    file = open(shutil.copyfile('hashi.smt2', 'hashi_' + file_name_parts[1] + '.smt2'), 'a')
    x_coord = [x for x, y, v in island_info]
    y_coord = [y for x, y, v in island_info]
    value   = [v for x, y, v in island_info]

    # print("x_coord: " + str(x_coord))
    # print("y_coord: " + str(y_coord))

    #each cell can be one of the above defined game pieces, but only one (not islands, as these can be explicitly set)

    #start island constraints
    file.write("(assert\n")
    file.write("    (and\n")

    # print("width: " + str(w))
    # print("height: " + str(h))

    #set each island piece and all possible pieces for the rest of the cells per definition of d
    for i in range(1, h+1):    
        #print("i outside: " + str(i))
        for j in range(1,w+1):
            # print("i out: " + str(i))
            # print("j out: " + str(j))
            if islands_with_0[i-1][j-1] == "0":
                # print("islands with 0 value: " + str(islands_with_0[i-1][j-1]))
                continue
            if i == x_coord[0] and j == y_coord[0]:
                # print("i if: " + str(i))
                # print("j if: " + str(j))
                # print("x: " + str(x_coord[0]))
                # print("y: "+ str(y_coord[0]))
                #res.append((5))
                file.write(f"        (= (Island {x_coord[0]} {y_coord[0]}) {value[0]})\n") #generating islands
                x_coord.pop(0)
                y_coord.pop(0) #remove coordinates after use
                value.pop(0)
                #print("res: " + str(res))
            # elif i == 1 or i == h+1: #upper and lower edge can only be horizontal bridges
            #     # print("i else: " + str(i))
            #     # print("j else: " + str(j))
            #     # print("x: " + str(x_coord[0]))
            #     # print("y: "+ str(y_coord[0]))
            #     res.append((0,1,2))
            #     #print("res: " + str(res))
            # elif j == 1 or j == w+1: # right and left edge can only be vertical bridges
            #     res.append((0,3,4))
            # else:
            #     res.append((0,1,2,3,4))

    file.write("    )\n)\n\n") #island constraints are finished here


    #start bridge constraints
    file.write("(assert\n")
    file.write("    (and\n")

    x_coord = [x for x, y, v in island_info]
    y_coord = [y for x, y, v in island_info]
    value   = [v for x, y, v in island_info]

    in_between_x = []
    in_between_y = []

    bridge_list = []


    #single or double bridges between islands
    for i in range(len(island_info)):
        for j in range(i+1, len(island_info)):
            if x_coord[i] == x_coord[j]:
                in_between_x.append(j)
                if j == min(in_between_x):
                    file.write("        (or\n")
                    file.write(f"            (= (Line {i+1} {j+1}) {0})\n")
                    file.write(f"            (= (Line {i+1} {j+1}) {1})\n")
                    file.write(f"            (= (Line {i+1} {j+1}) {2})\n")
                    file.write("        )\n")
                    bridge_list.append((i+1, j+1))
            if y_coord[i] == y_coord[j]:
                in_between_y.append(j)
                if j == min(in_between_y):
                    file.write("        (or\n")
                    file.write(f"            (= (Line {i+1} {j+1}) {0})\n")
                    file.write(f"            (= (Line {i+1} {j+1}) {1})\n")
                    file.write(f"            (= (Line {i+1} {j+1}) {2})\n")
                    file.write("        )\n")
                    bridge_list.append((i+1, j+1))
        
        in_between_x = []
        in_between_y = []

    #number of bridges connected to an island equals value of island
    #print(bridge_list)
    for i in range(len(island_info)):
        file.write(f"        (= (Island {x_coord[i]} {y_coord[i]}) (+ 0")
        for island1, island2 in bridge_list:
            if i+1 == island1 or i+1 == island2:
                file.write(f" (Line {island1} {island2})")
            #print(island1, island2)
        file.write("))\n")

    #bridges cannot cross each other
    #check horizontal connections for crossing vertical connections
    #only check tow pairs of islands at a time
    for islandx1, islandx2 in bridge_list:
        for islandy1, islandy2 in bridge_list:
            if x_coord[islandx1-1] == x_coord[islandx2-1]:
                if ((x_coord[islandx1-1] > x_coord[islandy1-1]) and (x_coord[islandx1-1] < x_coord[islandy2-1])) or ((x_coord[islandx1-1] < x_coord[islandy1-1]) and (x_coord[islandx1-1] > x_coord[islandy2-1])):
                    if ((y_coord[islandy1-1] > y_coord[islandx1-1]) and (y_coord[islandy1-1] < y_coord[islandx2-1])) or ((y_coord[islandy1-1] < y_coord[islandx1-1]) and (y_coord[islandy1-1] > y_coord[islandx2-1])):
                        file.write("        (or\n")
                        file.write(f"           (= 0 (Line {islandx1} {islandx2}))\n")
                        file.write(f"           (= 0 (Line {islandy1} {islandy2}))\n")
                        file.write("         )\n")


    
    file.write("    )\n)\n\n") #bridge constraints are finished here 

    #print(res)
    file.write("(check-sat)\n")
    file.write("(get-model)")
    file.close()

    return bridge_list
   
        
#input(hashi_file)