import numpy as np

def output_solution(width, height, island_info, bridge_list, bridge_value):
    output = [["." for _ in range(width)] for _ in range(height)]

    x_coord = [x for x, y, v in island_info]
    y_coord = [y for x, y, v in island_info]
    value   = [v for x, y, v in island_info]

    if bridge_value == 0:
        island1 = [i1 for i1, i2, bv in bridge_list]
        island2 = [i2 for i1, i2, bv in bridge_list]
        bridge_values = [bv for i1, i2, bv in bridge_list]
    else:
        island1 = [i1 for i1, i2, bv in bridge_list]
        island2 = [i2 for i1, i2, bv in bridge_list]

    for i in range(len(x_coord)):
        output[x_coord[i]-1][y_coord[i]-1] = value[i]

    #for i in range(len(bridge_list)):
    
    print("solution:")
    print(np.matrix(output))