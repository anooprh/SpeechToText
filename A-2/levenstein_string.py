import sys


class word_node:
    def __init__(self, distance):
        self.distance = distance

def strcmp(string1, string2):
    if string1 == string2:
        return 0
    return 1

def string_levenstein(template_string, input_string):

    template_string_list = template_string.split(' ')
    input_string_list = input_string.split(' ')
    template_length = len(template_string_list) + 1
    input_length = len(input_string_list) + 1

    nodes = []

    for i in range(0, input_length):
        nodes.append([])
        for j in range(0, template_length):
            if(i == 0 and j == 0):
                nodes[i].append(word_node(0))
                continue
            if(i == 0):
                nodes[i].append(word_node(j))
                continue
            if(j == 0):
                nodes[i].append(word_node(i))
                continue

            diagonal_factor = 1
            if input_string_list[i - 1] == template_string_list[j - 1]:
                diagonal_factor = 0
            evaluation_vector = []

            evaluation_vector.append(nodes[i - 1][j].distance + 1)
            evaluation_vector.append(nodes[i][j - 1].distance + 1)
            evaluation_vector.append(nodes[i - 1][j - 1].distance + diagonal_factor)

            distance = min(evaluation_vector)
            nodes[i].append(word_node(distance))

    return nodes[input_length - 1][template_length - 1], nodes


def printNodes(word_matrix):
    row_num = len(word_matrix)
    col_num = len(word_matrix[0])
    for i in range(0, row_num):
        for j in range(0, col_num):
            sys.stdout.write(str(word_matrix[i][j].distance) + '  ')
        print('\n')


if __name__ == "__main__":
    [min_distance, word_matrix] = string_levenstein("I am not ok", "I am ok")

    printNodes(word_matrix)
    pass