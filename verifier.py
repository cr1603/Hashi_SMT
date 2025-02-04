import numpy as np

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

def island2func(output_help, island1, adjacency_matrix):
    output_help = skip_to(output_help, "_arg_2")
    island2 = save_output_as_island(output_help)
    #print(f"island2: {island2}")
    adjacency_matrix[island1-1][island2-1] = 1
    adjacency_matrix[island2-1][island1-1] = 1
    output_help = output_help[1:]
    return adjacency_matrix, output_help

def island1func(output_help):
    output_help = skip_to(output_help, "_arg_1")
    island1 = save_output_as_island(output_help)
    output_help = output_help[1:]
    return island1, output_help

def check_for_ite(output_help):
    ite_found = False
    if "ite" in output_help:
        ite_found = True
    return ite_found

def output_formatter(output, island_info):
    adjacency_matrix = [[0 for _ in range(len(island_info))] for _ in range(len(island_info))]

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
    if output_help[:3] == "sat":
        output_help = skip_to(output_help, "Line")
        #print(output_help)
        while output_help[:11] != "(define-fun":
            if check_for_ite(output_help):
                output_help = skip_to(output_help, "ite")
                if output_help[:13] == "ite (= _arg_1":
                    island1, output_help = island1func(output_help)
                if output_help[:13] == "ite (= _arg_2":
                    adjacency_matrix, output_help = island2func(output_help, island1, adjacency_matrix)
            #print(len(output_help))
            #print(adjacency_matrix)

            else:
                break      

        #output_help = output_help[1:]
        # print(output_help)


    return adjacency_matrix


def verifier(adjacency_matrix):
    connectivity_satisfied = False

    changed = True

    while(changed):
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