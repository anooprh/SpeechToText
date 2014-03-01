import scipy.io
import sys
from colorama import Fore, init, Back
from mfcc_features import MelFeatures

__author__ = 'anoop'

import numpy as np
import scipy.spatial.distance as dist
init(autoreset=True)

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

wavfiles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
FILE_NAME = 'nine.wav'

template_list = []
for file in wavfiles:
    template_list.append(scipy.io.loadmat(file + '.mat').get('data').transpose())

MelFeat = MelFeatures()
raw_data = MelFeat.loadWAVfile(FILE_NAME)
mfcc_features = MelFeat.calcMelFeatures(raw_data)
input = mfcc_features.transpose()

# template_list = [np.array([np.array([1, 2, 3, 3, 5]),
#                            np.array([5, 6, 7, 8, 9]),
#                            np.array([11, 12, 13, 14, 15])]),
#                  np.array([np.array([1, 2, 4, 3, 5]),
#                            np.array([1, 2, 3, 4, 15])]),
#                  np.array([np.array([1, 2, 4, 3, 5]),
#                            np.array([5,11, 7, 2, 9]),
#                            np.array([5, 45, 7, 8, 9]),
#                            np.array([1, 2, 3, 34, 15])])]
#
# input = np.array([[1, 2, 3, 3, 5],
#                   [5, 1, 7, 8, 9],
#                   [5, 6, 7, 8, 9],
#                   [5, 6, 4, 8, 9],
#                   [5, 6, 7, 6, 9],
#                   [11, 12, 13, 14, 15]])

template_begin_indices = np.array([0])
for template_index in range(0, len(template_list)):
    template_begin_indices = np.append(template_begin_indices,template_begin_indices[-1] + template_list[template_index].shape[0])
template_begin_indices = template_begin_indices[:-1]
template_end_indices = template_begin_indices[1:] - 1
template_end_indices = np.append(template_end_indices, template_end_indices[-1] + template_list[-1].shape[0] )

trellis = np.full((input.shape[0], template_end_indices[-1]+1), float('inf'))
back_ptr_matrix = np.zeros_like(trellis)

def find_prev_nodes(input_index, template_index):
    prev_array = trellis[input_index - 1, max(template_index-2,0):template_index+1]
    minimum = min(prev_array)
    back_ptr = np.where(prev_array[::-1] == minimum)[0][0]

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
            back_ptr_matrix[i][template_begin_indices[j] + k] = back_ptr
            trellis[i][template_begin_indices[j] + k] = path_cost + node_cost


split_trellis = np.split(trellis,template_begin_indices,axis =1)[1:]
split_distance_matrix = np.split(back_ptr_matrix,template_begin_indices,axis =1)[1:]

result_container = zip(split_trellis, split_distance_matrix)
print 'Distance'


def custom_print_result(template_result):
    template_trellis = template_result[0].astype('float64')
    back_trace = template_result[1]

    (next_i, next_j) = (template_trellis.shape[0]-1, template_trellis.shape[1]-1)
    for i in range(template_trellis.shape[0])[::-1]:
        for j in range(template_trellis.shape[1])[::-1]:
            format_str = ''
            if(i == next_i and j == next_j):
                format_str = Fore.RED
                (next_i, next_j) = (i-1, j-int(back_trace[i][j]))
            data_str = '%5.2f' % (template_trellis[i][j]) + '   ' + Fore.RESET
            sys.stdout.write(format_str + data_str)
        print('\n')

for i in range(len(result_container)):
    print 'Template '  + str(i) + ' Distance ---> ' + str(result_container[0][0][-1,-1]) + '\n'
    # custom_print_result(result_container[i])