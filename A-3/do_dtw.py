import sys

__author__ = 'anoop'
import numpy as np
import scipy.spatial.distance as dist

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

template_list = [np.array([np.array([1, 2, 3, 3, 5]),
                           np.array([5, 6, 7, 8, 9]),
                           np.array([11, 12, 13, 14, 15])]),
                 np.array([np.array([1, 2, 4, 3, 5]),
                           np.array([1, 2, 3, 4, 15])])]

input = np.array([[1, 2, 3, 3, 5],
                  [5, 6, 7, 8, 9],
                  [11, 12, 13, 14, 15]])

template_begin_indices = np.array([0])
for template_index in range(0, len(template_list)):
    template_begin_indices = np.append(template_begin_indices,template_begin_indices[-1] + template_list[template_index].shape[0])
template_begin_indices = template_begin_indices[:-1]
template_end_indices = template_begin_indices[1:] - 1
template_end_indices = np.append(template_end_indices, template_end_indices[-1] + template_list[-1].shape[0] )

trellis = np.full((input.shape[0], template_end_indices[-1]+1), float('inf'))
back_ptr_matrix = np.zeros_like(trellis)


def find_prev_nodes(input_index, template_index):
    # prev_node_0 = trellis[input_index - 1][template_index]
    # prev_node_1 = trellis[input_index - 1][template_index - 1]
    # prev_node_2 = trellis[input_index - 1][template_index - 2]
    # prev_array = [prev_node_0, prev_node_1, prev_node_2]
    prev_array = trellis[input_index - 1, max(template_index-2,0):template_index+1]
    # trellis[input_index - 1]
    # prev_array = np.append(np.full((1, 3 - prev_array.shape[0]), float('inf')), prev_array)
    minimum = min(prev_array)
    back_ptr = np.where(prev_array == minimum)[0][0]

    # back_ptr = prev_array.index(minimum)
    if (minimum == float('inf')):
        back_ptr = -1
        minimum = 0
    return minimum, back_ptr

for i in range(0, input.shape[0]):
    for j in range(0, len(template_list)):
        for k in range(0, template_list[j].shape[0]):
            node_cost = dist.euclidean(input[i], template_list[j][k])
            (path_cost, back_ptr) = find_prev_nodes(i, k);
            if (path_cost == float('inf')):
                path_cost = 0
            # back_ptr_matrix[i + 1][template_begin_indices[j] + k] = back_ptr
            trellis[i][template_begin_indices[j] + k] = path_cost + node_cost

# trellis = np.delete(trellis, 0, 0)
# trellis = np.delete(trellis, (0,1), 1)
# back_ptr_matrix = np.delete(back_ptr_matrix, 0, 0)
# back_ptr_matrix = np.delete(back_ptr_matrix, (0,1), 1)

print trellis

print back_ptr_matrix

print template_begin_indices
print template_end_indices

print 'Distance'

for i in range(len(template_end_indices)):
    print ' Template ' + str(i) + ' distance ' + str(trellis[-1, template_end_indices[i]])