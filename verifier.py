import os

def skip_to(output_help, str):
    while output_help[:(len(str))] != str:
        output_help = output_help[1:]
    return output_help

def save_output_as_island(output_help):
    i = 7
    while output_help[i].isnumeric():
        i += 1
    island = int(output_help[7:i])
    return island

def save_bridge_value(output_help):
    output_help = skip_to(output_help, ")")
    #print(output_help)
    i = 2
    while output_help[i].isnumeric():
        i += 1
    value = int(output_help[2:i])
    return value

def island2func(output_help, island1, adjacency_matrix, bridge_list):
    output_help = skip_to(output_help, "_arg_2")
    island2 = save_output_as_island(output_help)
    #print(f"island2: {island2}")
    adjacency_matrix[island1-1][island2-1] = 1
    adjacency_matrix[island2-1][island1-1] = 1
    output_help = output_help[1:]
    value = save_bridge_value(output_help)
    bridge_list.append((island1, island2, value))
    return island1, island2, adjacency_matrix, output_help, bridge_list

def island1func(output_help):
    output_help = skip_to(output_help, "_arg_1")
    island1 = save_output_as_island(output_help)
    #print(f"island1: {island1}")
    output_help = output_help[1:]
    return island1, output_help

def check_for_ite(output_help):
    ite_found = False
    if "ite" in output_help:
        ite_found = True
    return ite_found

def output_formatter(output, island_info, bridge_list_input):
    #island_info = island_info[1:] #-1 because of dimension information
    adjacency_matrix = [[0 for _ in range(len(island_info))] for _ in range(len(island_info))]
    #print(len(adjacency_matrix))

    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix)):
            if i == j:
                adjacency_matrix[i][j] = 1

    # print(output)
    # print(len(island_info))
    # print(len(adjacency_matrix))
    # print(len(adjacency_matrix[0]))

    output_help = str(output)
    #print(output_help)
    bridge_list = []
    bridge_value = 0
    #if output_help[:3] == "sat":
    output_help = skip_to(output_help, "Line")
    #print(output_help)
    while output_help[:11] != "(define-fun":
        if check_for_ite(output_help):
            output_help = skip_to(output_help, "ite")
            if output_help[:13] == "ite (= _arg_1":
                island1, output_help = island1func(output_help)
            if output_help[:13] == "ite (= _arg_2":
                island1, island2, adjacency_matrix, output_help, bridge_list = island2func(output_help, island1, adjacency_matrix, bridge_list)
                output_help = skip_to(output_help, ")")
                #print(output_help)
                if output_help[4] != "0":
                    # print(output_help)
                    # print(bridge_list_input)
                    # print(island1, island2)
                    for i1, i2 in bridge_list_input:
                        if (i1 == island1 and i2 != island2) or (i1 == island2 and i2 != island1):
                            print(i1, i2)
                            adjacency_matrix[i1-1][i2-1] = 1
                            adjacency_matrix[i2-1][i1-1] = 1
                            value = int(output_help[4])
                            bridge_list.append((i1, i2, value))
                            #print(value)
                    
        #print(len(output_help))
        #print(adjacency_matrix)

        elif output_help.startswith("Line"):
            output_help = skip_to(output_help, ") Int")
            i = 6
            #print(output_help[i])
            while output_help[i].isnumeric():
                i += 1
            bridge_value = int(output_help[6:i])

            if bridge_value == 2:
                bridge_value -= 1
            adjacency_matrix = [[bridge_value for _ in range(len(island_info))] for _ in range(len(island_info))]
            break                    

        else:
            break

        #output_help = output_help[1:]
        # print(output_help)
        


    return adjacency_matrix, bridge_list, bridge_value


def verifier(adjacency_matrix):
    connectivity_satisfied = False

    changed = True

    while(changed): #Breadth-First-Search BFS
        changed = False
        for start in range (len(adjacency_matrix)):
            for end in range (len(adjacency_matrix)):
                if adjacency_matrix[start][end] == 0:
                    for middle in range (len(adjacency_matrix)):
                        if adjacency_matrix[start][middle] == 1 and adjacency_matrix[middle][end] == 1:
                            adjacency_matrix[start][end] = 1
                            changed = True
                            #print(np.matrix(adjacency_matrix))
                            break
    
    
    # print(np.matrix(adjacency_matrix))
    # print(len(adjacency_matrix))

    checkerlist = [1 for i in range (len(adjacency_matrix))]
    #print(checkerlist)
    
    connectivity_satisfied = (all(x == checkerlist for x in adjacency_matrix))
    #print(all(x == checkerlist for x in adjacency_matrix))

    return connectivity_satisfied

def add_to_smt_file(bridge_list, test_file):
    file = open(test_file, 'r+')

    file.seek(0, os.SEEK_END)
    pos = file.tell() - 1
    while pos > 0 and file.read(1) != "\n":
        pos -= 1
        file.seek(pos, os.SEEK_SET)
    if pos > 0:
        pos -= 1
        file.seek(pos, os.SEEK_SET)
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)
    if pos > 0:
        file.seek(pos + 1, os.SEEK_SET)
        file.truncate()

    file.write("(assert\n")
    file.write("    (not\n")
    file.write("        (and\n")

    for island1, island2, value in bridge_list:
        file.write(f"           (= (Line {island1} {island2}) {value})\n")
    
    file.write("        )\n    )\n)\n\n")

    file.write("(check-sat)\n")
    file.write("(get-model)")
    file.close()


