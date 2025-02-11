import numpy as np

def output_solution(width, height, island_info, bridge_list_unsorted, bridge_value):
    output = [["." for _ in range(width)] for _ in range(height)]

    x_coord = [x for x, y, v in island_info]
    y_coord = [y for x, y, v in island_info]
    value   = [v for x, y, v in island_info]
    print(x_coord)
    print(y_coord)

    bridge_list = sorted(bridge_list_unsorted, key = lambda x: (x[0], x[1]))
    print(bridge_list)

    if bridge_value == 0:
        island1 = [i1 for i1, i2, bv in bridge_list]
        island2 = [i2 for i1, i2, bv in bridge_list]
        bridge_values = [bv for i1, i2, bv in bridge_list]
    else:
        island1 = [i1 for i1, i2 in bridge_list]
        island2 = [i2 for i1, i2 in bridge_list]


    for i in range(len(x_coord)):
        output[x_coord[i]-1][y_coord[i]-1] = value[i]

    count = 0

    #horizontal bridges
    for i in range(height):
        for j in range(width):
            if output[i][j] == ".":
                for a in range(len(island1)):
                    if (x_coord[island1[a]-1]-1 == i) and (x_coord[island1[a]-1] == x_coord[island2[a]-1]):
                        while j>y_coord[island1[a]-1]-1 and j<y_coord[island2[a]-1]-1:
                            # print(a)
                            # print(j)
                            # print(y_coord[island2[a]-1]-1)
                            if bridge_value == 0:
                                if bridge_values[a] == 1:
                                    output[i][j] = "-"
                                    #print(np.matrix(output))
                                elif bridge_values[a] == 2:
                                    output[i][j] = "="
                                    #print(np.matrix(output))
                            else:
                                if bridge_value == 1:
                                    output[i][j] = "-"
                                    #print(np.matrix(output))
                                elif bridge_value == 2:
                                    output[i][j] = "="
                                    #print(np.matrix(output))
                            j += 1

    #vertical bridges                
    for i in range(height):
        for j in range(width):
            if output[i][j] == ".":
                for a in range(len(island1)):
                    #print(f"j before if: {j}")
                    if (y_coord[island1[a]-1]-1 == j) and (y_coord[island1[a]-1] == y_coord[island2[a]-1]): 
                        for ihelp in range(x_coord[island1[a]-1], x_coord[island2[a]-1]-1):
                            if bridge_value == 0:
                                if bridge_values[a] == 1:
                                    output[ihelp][j] = "|"
                                    #print(np.matrix(output))
                                elif bridge_values[a] == 2:
                                    output[ihelp][j] = "$"
                                    #print(np.matrix(output))
                            else:
                                if bridge_value == 1:
                                    output[ihelp][j] = "|"
                                    #print(np.matrix(output))
                                elif bridge_value == 2:
                                    output[ihelp][j] = "$"
                                    #print(np.matrix(output))
    
    print("solution:")
    print(np.matrix(output))
    #print(*output, sep= "\n")