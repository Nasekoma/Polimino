import sys

class Figure:
    def __init__(self, data, type, largest_side, matrix):
        #data: ((size1, size2), num)
        self.size = data[0]
        self.num = data[1]
        self.type = type
        self.largest_side = largest_side
        self.matrix = matrix

def create_matrix(size, type):
    #type = 0 = rectangle, type = 1 = type2
    #size = (size1, size2)
    matrix = [[1 for i in range(0, size[0])] for j in range(0, size[1])]
    if type == 0:
        return matrix
    for i in range(1, size[1] - 1):
        for j in range(1, size[0]):
            matrix[i][j] = 0
    return matrix

def rotate_matrix(matrix):
    # 1 1 1    1 1 1
    # 1 0 0 -> 1 0 1
    # 1 1 1    1 0 1 
    res_matrix = [[0 for i in range(0, len(matrix))] for j in range(0, len(matrix[0]))]
    for i in range(0, len(matrix[0])):
        for j in range(0, len(matrix)):
            res_matrix[i][j] = matrix[j][i]
    matrix = res_matrix
    return matrix

def flip_matrix(matrix):
    # 1 1 1    1 1 1
    # 1 0 0 -> 0 0 1
    # 1 1 1    1 1 1
    res_matrix = [[matrix[i][j] for j in range(0, len(matrix[0]))] for i in range(0, len(matrix))]
    res_matrix[0] = matrix[-1][:]
    res_matrix[-1] = matrix[0][:]
    for i in range(0, len(matrix)):
        res_matrix[i][0] = matrix[i][-1]
        res_matrix[i][-1] = matrix[i][0]
    matrix = res_matrix
    return matrix


def matrix_number(matrix):
    #converts matrix[[]] made of 0 and 1 to decimal number as if it was binary number
    #example: matrix = [[1, 0], [0, 1]] converts to 9
    str_matrix = [''.join(map(str, matrix[i])) for i in range(0, len(matrix))]
    res = int(''.join(str_matrix), 2)
    return res

def place_figure(table, figure, coords):
    #coords shows the position of upper-left coordinate of figure
    #coords = [height, wigth]; [0,0] - upper-left corner of table
    #returns True if OK, returns False if figure can't be placed
    res_table = [[0 for i in range(0, len(table[0]))] for j in range(0, len(table))]
    for i in range(0, len(figure)):
        for j in range(0, len(figure[0])):
            res_table[coords[0] + i][coords[1] + j] = figure[i][j]
    if (matrix_number(res_table) & matrix_number(table)) != 0:
        return False, table
    for i in range(0, len(table)):
        for j in range(0, len(table[0])):
            if table[i][j] == 1:
                res_table[i][j] = 1
    return True, res_table

def search_for_place(table, figure, coords):
    # searches for place for figure on table
    # returns True if figure is placed, returns False if not
    #coords = [height, width, flag], flag = are coords correct
    flag = False # is figure placed
    if (coords[1] + len(figure[0])) > len(table[0]):
        coords[1] = 0
        coords[0] += 1
    if (coords[0] + len(figure)) > len(table):
        coords[2] = False
        return flag, table
    while not flag:
        flag, table = place_figure(table, figure, coords[:2])
        if flag:
            return flag, table
        coords[1] += 1
        if (coords[1] + len(figure[0])) > len(table[0]):
            coords[1] = 0
            coords[0] += 1
            if (coords[0] + len(figure)) > len(table):
                coords[2] = False
                break
    return flag, table

def filling(start_table, all_tuples, index, num):
    # returns the result of placement for current figure and all next ones
    # num = how many figures of current type you need to place
    # all_tuples[index] = current type of figure
    # True if all placed, False if not
    if index >= len(all_tuples):
        return True
    if num == 0:
        if (index + 1) >= len(all_tuples):
            return True
        return filling(start_table, all_tuples, index + 1, all_tuples[index + 1].num)
    coords1 = [0, 0, True]
    coords2 = [0, 0, True]
    coords3 = [0, 0, True]
    coords4 = [0, 0, True]
    table = [[start_table[i][j] for j in range(0, len(start_table[0]))] for i in range(0, len(start_table))]
    flag = False
    flag_next = False
    figure1 = [[all_tuples[index].matrix[i][j] for j in range(0, len(all_tuples[index].matrix[0]))] for i in range(0, len(all_tuples[index].matrix))]
    figure2 = rotate_matrix(figure1)
    figure3 = flip_matrix(figure2)
    figure4 = flip_matrix(figure1)
    while (not flag_next) and (coords1[2] or coords2[2] or coords3[2] or coords4[2]):
        if(coords1[2]):
            # first position of figure
            table = [[start_table[i][j] for j in range(0, len(start_table[0]))] for i in range(0, len(start_table))]
            flag, table = search_for_place(table, figure1, coords1)
            coords1[1] += 1
            if flag:
                # checking for next figures
                flag_next = filling(table, all_tuples, index, num - 1)
                continue
        if ((all_tuples[index].type == 1) or (all_tuples[index].size[0] != all_tuples[index].size[1])) and coords2[2]:
            # second position of figure, no need to check for squares (equal sides)
            table = [[start_table[i][j] for j in range(0, len(start_table[0]))] for i in range(0, len(start_table))]
            flag, table = search_for_place(table, figure2, coords2)
            coords2[1] += 1
            if flag:
                # checking for next figures
                flag_next = filling(table, all_tuples, index, num - 1)
                continue
        else:
            # changing coords2 to be able to end cycle for squares (equal sides)
            coords2[2] = False
        if all_tuples[index].type == 1:
            # checking positions that are new only for type2
            if coords3[2]:
                # third position of figure
                table = [[start_table[i][j] for j in range(0, len(start_table[0]))] for i in range(0, len(start_table))]
                flag, table = search_for_place(table, figure3, coords3)
                coords3[1] += 1
                if flag:
                    # checking for next figures
                    flag_next = filling(table, all_tuples, index, num - 1)
                    continue
            if coords4[2]:
                # fourth position of figure
                table = [[start_table[i][j] for j in range(0, len(start_table[0]))] for i in range(0, len(start_table))]
                flag, table = search_for_place(table, figure4, coords4)
                coords4[1] += 1
                if flag:
                    # checking for next figures
                    flag_next = filling(table, all_tuples, index, num - 1)
                    continue
        else:
            # changing coords3 and coords4 to be able to end cycle for rectangles
            coords3[2] = False
            coords4[2] = False
    if not (coords1[2] or coords2[2] or coords3[2] or coords4[2]):
        return False
    return (flag and flag_next)

def is_fillable(table_size, all_tuples):
    table = [[0 for i in range(0, table_size[0])] for j in range(0, table_size[1])]
    return filling(table, all_tuples, 0, all_tuples[0].num)

#######################################################################################################################

# getting data (without checking it)
################################ skip this part if you have variables (more info in documentation)
table_size = tuple(map(int, input("Enter table size: ").split()))
rectangle = list(map(int, input("Enter fist set of polimino data: ").split()))
type2 = list(map(int, input("Enter second set of polimino data: ").split()))
rectangle_types = len(rectangle) // 3
type2_types = len(type2) // 3
rectangle_tuples = list()
type2_tuples = list()
# converting data to tuples
for i in range(0, rectangle_types):
    rectangle_tuples.append(((rectangle[i * 3], rectangle[i * 3 + 1]), rectangle[i * 3 + 2]))
for i in range(0, type2_types):
    type2_tuples.append(((type2[i * 3], type2[i * 3 + 1]), type2[i * 3 + 2]))
################################ stop skipping here
# checking area size
area = 0
for i in range(0, rectangle_types):
    area += rectangle_tuples[i][0][0] * rectangle_tuples[i][0][1] * rectangle_tuples[i][1]
for i in range(0, type2_types):
    area += (type2_tuples[i][0][0] * 2 + type2_tuples[i][0][1] - 2) * type2_tuples[i][1]
if area > (table_size[0] * table_size[1]):
    print("False")
    sys.exit(0)
# checking table size
for i in range(0, rectangle_types):
    if rectangle_tuples[i][1] != 0:
        if (rectangle_tuples[i][0][0] > table_size[0]) and (rectangle_tuples[i][0][0] > table_size[1]):
            print("False")
            sys.exit(0)
        elif (rectangle_tuples[i][0][1] > table_size[0]) and (rectangle_tuples[i][0][1] > table_size[1]):
            print("False")
            sys.exit(0)
for i in range(0, type2_types):
    if type2_tuples[i][1] != 0:
        if (type2_tuples[i][0][0] > table_size[0]) and (type2_tuples[i][0][0] > table_size[1]):
            print("False")
            sys.exit(0)
        elif (type2_tuples[i][0][1] > table_size[0]) and (type2_tuples[i][0][1] > table_size[1]):
            print("False")
            sys.exit(0)
####################################################### main algorythm
# making all-tuples list
all_tuples = []
for i in range(0, rectangle_types):
    largest_side = rectangle_tuples[i][0][1]
    all_tuples.append(Figure(rectangle_tuples[i], 0, largest_side, create_matrix(rectangle_tuples[i][0], 0)))
for i in range(0, type2_types):
    if type2_tuples[i][0][0] > type2_tuples[i][0][1]:
        largest_side = type2_tuples[i][0][0]
    else:
        largest_side = type2_tuples[i][0][1]
    all_tuples.append(Figure(type2_tuples[i], 1, largest_side, create_matrix(type2_tuples[i][0], 1)))
# Figure : (size1, size2), number, type, largest_side, matrix
# type = 0 = rectangle, type = 1 = type2
# matrix for 2x3 type = 1:                         matrix for 2x3 type = 0:
# [[1, 1],                                         [[1, 1],
#  [1, 0],                                          [1, 1],
#  [1, 1]]                                          [1, 1]]
all_tuples.sort(key=lambda cur_tuple: cur_tuple.largest_side)
all_tuples = all_tuples[::-1]
print(is_fillable(table_size, all_tuples))
