import sys
import node_element

THRESHOLD = 8
BEAM_WIDTH = 4



addition = 0
deletion = 0
substitution = 0



def printPath(nodes, input_string_list, template_string_list):
    global addition
    global deletion
    global substitution
    numrows = len(nodes)
    numcols = len(nodes[0])
    if (numrows == 1 and numcols == 1):
        print [0, 0]
        return

    [prev_row, prev_col] = nodes[numrows - 1][numcols - 1].previous_node
    print [numrows - 1, numcols - 1]
    if (prev_row == numrows - 2 and prev_col != numcols - 2):
        addition = addition + 1
    if (prev_col == numcols - 2 and prev_row != numrows - 2 ):
        deletion = deletion + 1
    if (prev_row == numrows - 2 and prev_col == numcols - 2 and input_string_list[numcols-2] != template_string_list[numrows - 2]):
        substitution = substitution + 1
    printPath(zip(*(zip(*(nodes[0:prev_row + 1]))[0:prev_col + 1])), input_string_list, template_string_list)

def displayNodes(nodes, input_string_list, template_string_list):
    numrows = len(nodes)
    numcols = len(nodes[0])
    for i in range(0, numrows):
        for j in range(0, numcols):
            if nodes[i][j] == None:
                sys.stdout.write('   ')
            else:
                nodes[i][j].printDistance()
        print '\n'

    printPath(nodes, input_string_list, template_string_list)
    print 'Additions   --> ' + str(addition)
    print 'Deletions   --> ' + str(deletion)
    print 'Substitions --> ' + str(substitution)

def compute_levenshtein_distance_editdistance(template_string_list, input_string_list):

    template_length = len(template_string_list) + 1
    input_length = len(input_string_list) + 1

    nodes = []

    for i in range(0, input_length):
        nodes.append([])
        for j in range(0, template_length):
            ################################################################################
            ## If in first row or column, do not use recursive strategy. Use common sense ##
            if (i == 0 and j == 0):
                nodes[i].append(node_element.word_node(0))
                continue
            if (i == 0):
                nodes[i].append(node_element.word_node(j))
                continue
            if (j == 0):
                nodes[i].append(node_element.word_node(i))
                continue
                ################################################################################

            ################################################################################
            #### Computing the distance at the current node by using recursive strategy ####
            diagonal_factor = 1
            if input_string_list[i - 1] == template_string_list[j - 1]:
                diagonal_factor = 0
            evaluation_vector = []

            if nodes[i - 1][j] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i - 1][j].distance + 1)
            if nodes[i][j - 1] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i][j - 1].distance + 1)
            if nodes[i - 1][j - 1] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i - 1][j - 1].distance + diagonal_factor)

            distance = min(evaluation_vector)
            ################################################################################

            ######### EDIT DISTANCE THRESHOLD PRUNING STRATEGY #############################
            if distance <= THRESHOLD:
                nodes[i].append(node_element.word_node(distance))
            else:
                nodes[i].append(None)
                continue
                ################################################################################

            ################################################################################
            ####### Adding backtrack information ###########################################
            came_from = evaluation_vector.index(min(evaluation_vector))
            if (came_from == 0):
                nodes[i][j].previous_node = [i - 1, j]
            if (came_from == 1):
                nodes[i][j].previous_node = [i, j - 1]
            if (came_from == 2):
                nodes[i][j].previous_node = [i - 1, j - 1]
                ################################################################################

    return nodes[input_length - 1][template_length - 1].distance, nodes

def compute_levenshtein_distance_beam(template_string_list, input_string_list):
    template_length = len(template_string_list) + 1
    input_length = len(input_string_list) + 1

    nodes = []

    beam_entry_point = 0
    for i in range(0, input_length):
        nodes.append([])
        beam_range = range(max(beam_entry_point - BEAM_WIDTH + 1, 0),
                           min(beam_entry_point + BEAM_WIDTH, template_length))
        for j in range(0, template_length):
            if j not in beam_range: #and i != input_length - 1
                nodes[i].append(None)
                continue

            ################################################################################
            ## If in first row or column, do not use recursive strategy. Use common sense ##
            if (i == 0 and j == 0):
                distance = 0
                nodes[i].append(node_element.word_node(distance))
                continue
            if (i == 0):
                distance = j
                nodes[i].append(node_element.word_node(distance))
                continue
            if (j == 0):
                distance = i
                nodes[i].append(node_element.word_node(distance))
                continue
                ################################################################################

            ################################################################################
            #### Computing the distance at the current node by using recursive strategy ####
            diagonal_factor = 1
            if input_string_list[i - 1] == template_string_list[j - 1]:
                diagonal_factor = 0
            evaluation_vector = []

            if nodes[i - 1][j] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i - 1][j].distance + 1)
            if nodes[i][j - 1] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i][j - 1].distance + 1)
            if nodes[i - 1][j - 1] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i - 1][j - 1].distance + diagonal_factor)

            distance = min(evaluation_vector)
            ################################################################################

            nodes[i].append(node_element.Node(distance))


            ################################################################################
            ####### Adding backtrack information ###########################################
            came_from = evaluation_vector.index(min(evaluation_vector))
            if (came_from == 0):
                nodes[i][j].previous_node = [i - 1, j]
            if (came_from == 1):
                nodes[i][j].previous_node = [i, j - 1]
            if (came_from == 2):
                nodes[i][j].previous_node = [i - 1, j - 1]
                ################################################################################

        #update beam start point
        temp = []
        for j in range(0, len(nodes[i])):
            if nodes[i][j] == None:
                temp.append(None)
            else:
                temp.append(nodes[i][j].distance)
        beam_entry_point = temp.index(min(filter(lambda x: x is not None, temp)))
    return nodes[input_length - 1][template_length - 1].distance, nodes

def compute_levenshtein_distance_nopruning(template_string_list, input_string_list):
    template_length = len(template_string_list) + 1
    input_length = len(input_string_list) + 1
    nodes = []

    for i in range(0, input_length):
        nodes.append([])
        for j in range(0, template_length):
            ################################################################################
            ## If in first row or column, do not use recursive strategy. Use common sense ##
            if (i == 0 and j == 0):
                nodes[i].append(node_element.word_node(0))
                continue
            if (i == 0):
                nodes[i].append(node_element.word_node(j))
                continue
            if (j == 0):
                nodes[i].append(node_element.word_node(i))
                continue
                ################################################################################

            ################################################################################
            #### Computing the distance at the current node by using recursive strategy ####
            diagonal_factor = 1
            if input_string_list[i - 1] == template_string_list[j - 1]:
                diagonal_factor = 0
            evaluation_vector = []

            if nodes[i - 1][j] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i - 1][j].distance + 1)
            if nodes[i][j - 1] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i][j - 1].distance + 1)
            if nodes[i - 1][j - 1] == None:
                evaluation_vector.append(1000)
            else:
                evaluation_vector.append(nodes[i - 1][j - 1].distance + diagonal_factor)

            distance = min(evaluation_vector)
            ################################################################################

            nodes[i].append(node_element.word_node(distance))
            ################################################################################

            ################################################################################
            ####### Adding backtrack information ###########################################
            came_from = evaluation_vector.index(min(evaluation_vector))
            if (came_from == 0):
                nodes[i][j].previous_node = [i - 1, j]
            if (came_from == 1):
                nodes[i][j].previous_node = [i, j - 1]
            if (came_from == 2):
                nodes[i][j].previous_node = [i - 1, j - 1]
                ################################################################################


    return nodes[input_length - 1][template_length - 1].distance, nodes

def levenshtein_distance(template_string, input_string, pruning_strategy=None):
    global addition
    global deletion
    global substitution

    addition = 0
    deletion = 0
    substitution = 0

    distance = 10000;
    template_string_list = template_string.split(' ')
    input_string_list = input_string.split(' ')
    if pruning_strategy == 'beam':
        [min_distance, nodes] = compute_levenshtein_distance_beam(template_string_list, input_string_list)
    elif pruning_strategy == 'edit':
        [min_distance, nodes] = compute_levenshtein_distance_editdistance(template_string_list, input_string_list)
    else:
        [min_distance, nodes] = compute_levenshtein_distance_nopruning(template_string_list, input_string_list)
    if min_distance < distance:
        distance = min_distance
    displayNodes(nodes, template_string_list, input_string_list)

    return distance

if __name__ == "__main__":
    input_string = "I am good"
    template_string = "I am not so good"

    distance= levenshtein_distance(template_string, input_string, pruning_strategy=None)
    print(distance, input_string, template_string)
    pass

