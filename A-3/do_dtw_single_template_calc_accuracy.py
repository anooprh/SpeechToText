import scipy.io
import sys
from colorama import Fore, init, Back
from mfcc_features import MelFeatures
import matplotlib.pyplot as plt

__author__ = 'anoop'

import numpy as np
import scipy.spatial.distance as dist

init(autoreset=True)

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

correct = 0
wrong = 0
THRESHOLD = 10000
wavfiles_templates = ['zero_template', 'one_template', 'two_template', 'three_template', 'four_template',
                      'five_template', 'six_template', 'seven_template', 'eight_template', 'nine_template']
FILE_NAMES = [
    'zero_1', 'zero_2', 'zero_3', 'zero_4', 'zero_5',
    'one_1', 'one_2', 'one_3', 'one_4', 'one_5',
    'two_1', 'two_2', 'two_3', 'two_4', 'two_5',
    'three_1', 'three_2', 'three_3', 'three_4', 'three_5',
    'four_1', 'four_2', 'four_3', 'four_4', 'four_5',
    'five_1', 'five_2', 'five_3', 'five_4', 'five_5',
    'six_1', 'six_2', 'six_3', 'six_4', 'six_5',
    'seven_1', 'seven_2', 'seven_3', 'seven_4', 'seven_5',
    'eight_1', 'eight_2', 'eight_3', 'eight_4', 'eight_5',
    'nine_1', 'nine_2', 'nine_3', 'nine_4', 'nine_5'
]

template_list = []
for file in wavfiles_templates:
    template_list.append(scipy.io.loadmat(file + '.mat').get('data').transpose())

for f in range(len(FILE_NAMES)):
    FILE_NAME = FILE_NAMES[f] + '.wav'
    MelFeat = MelFeatures()
    raw_data = MelFeat.loadWAVfile(FILE_NAME)
    mfcc_features = MelFeat.calcMelFeatures(raw_data)
    input = mfcc_features.transpose()

    template_begin_indices = np.array([0])
    for template_index in range(0, len(template_list)):
        template_begin_indices = np.append(template_begin_indices,
                                           template_begin_indices[-1] + template_list[template_index].shape[0])
    template_begin_indices = template_begin_indices[:-1]
    template_end_indices = template_begin_indices[1:] - 1
    template_end_indices = np.append(template_end_indices, template_end_indices[-1] + template_list[-1].shape[0])

    trellis = np.full((input.shape[0], template_end_indices[-1] + 1), float('inf'))
    back_ptr_matrix = np.zeros_like(trellis)

    def find_prev_nodes(input_index, template_index):
        prev_array = trellis[input_index - 1, max(template_index - 2, 0):template_index + 1]
        minimum = min(prev_array)
        back_ptr = np.where(prev_array[::-1] == minimum)[0][0]
        if (minimum == float('inf')):
            back_ptr = -1
            minimum = 0
        return minimum, back_ptr

    active_list = np.array(range(template_end_indices[-1]))
    for i in range(0, input.shape[0]):
        for j in range(0, len(template_list)):
            for k in range(0, template_list[j].shape[0]):
                # if not np.any(active_list == template_begin_indices[j] + k):
                #     continue

                node_cost = dist.euclidean(input[i], template_list[j][k])
                (path_cost_prev, back_ptr) = find_prev_nodes(i, k);
                # if (path_cost == float('inf')):
                #     path_cost = 0
                back_ptr_matrix[i][template_begin_indices[j] + k] = back_ptr
                path_cost = path_cost_prev + node_cost
                trellis[i][template_begin_indices[j] + k] = path_cost

        active_list = filter(lambda _:_ <= template_end_indices[-1], np.unique(np.append(active_list, (active_list + 1, active_list + 2))))
        minimum_cost_in_col = min(trellis[i])
        active_list = np.array(filter(lambda _:trellis[i][_] < minimum_cost_in_col + THRESHOLD, active_list))

    split_trellis = np.split(trellis, template_begin_indices, axis=1)[1:]
    split_distance_matrix = np.split(back_ptr_matrix, template_begin_indices, axis=1)[1:]

    result_container = zip(split_trellis, split_distance_matrix)


    def custom_print_result(template_result):
        template_trellis = template_result[0].astype('float64')
        back_trace = template_result[1]

        # (next_i, next_j) = (template_trellis.shape[0]-1, template_trellis.shape[1]-1)
        (next_i, next_j) = (
            template_trellis.shape[0] - 1, np.where(min(template_trellis[-1][:]) == template_trellis[-1][:])[0][0])
        for i in range(template_trellis.shape[0])[::-1]:
            for j in range(template_trellis.shape[1])[::-1]:
                format_str = ''
                if (i == next_i and j == next_j):
                    format_str = Back.RED
                    (next_i, next_j) = (i - 1, j - int(back_trace[i][j]))
                data_str = '%4.0f' % (template_trellis[i][j]) + ' ' + Back.WHITE
                sys.stdout.write(format_str + data_str)
            print('\n')


    computed_distances = []
    for i in range(len(result_container)):
        computed_distances.append(min(result_container[i][0][-1]))
        # print 'Template ' + str(i) + ' Distance ---> ' + str(min(result_container[i][0][-1])) + '\n'
        # custom_print_result(result_container[i])


    index_recognized = np.where(computed_distances == min(computed_distances))[0][0]
    print 'Actual --> ' + wavfiles_templates[int(f/5)]
    print 'My Prediction --> ' + wavfiles_templates[index_recognized]
    if index_recognized == int(f/5):correct = correct + 1
    else:wrong = wrong + 1

print '\n\n\n'
print 'Accuracy -----> ' + str(float(correct)/(correct + wrong))