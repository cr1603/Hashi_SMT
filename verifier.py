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


def output_formatter(output, island_info):
    adjacency_matrix = [[0 for _ in range(len(island_info))] for _ in range(len(island_info))]

    # print(output)
    # print(len(island_info))
    # print(len(adjacency_matrix))
    # print(len(adjacency_matrix[0]))

    output_help = str(output)
    #print(output_help)
    output_help = skip_to(output_help, "Line")
    #print(output_help)
    while output_help[0] != "\n":
        output_help = skip_to(output_help, "ite")
        #print(output_help)
        output_help = skip_to(output_help, "_arg_1")
        #print(output_help)
        island1 = save_output_as_island(output_help)
        # print(output_help[7])
        # print(f"island1: {island1}")
        # print(type(island1))
        output_help = output_help[1:]
        output_help = skip_to(output_help, "_arg_2")
        #print(output_help)
        island2 = save_output_as_island(output_help)
        # print(output_help[7])
        # print(f"island2: {island2}")
        # print(type(island2))
        
        adjacency_matrix[island1-1][island2-1] = 1
        adjacency_matrix[island2-1][island1-1] = 1
        print(adjacency_matrix)

        while (output_help[:6] != "_arg_1") or (output_help[:6] != "_arg_2"):
            output_help = output_help[1:]
        

        output_help = output_help[1:]


    return adjacency_matrix


def verifier(adjacency_matrix):
    connectivity_satisfied = False


    return connectivity_satisfied