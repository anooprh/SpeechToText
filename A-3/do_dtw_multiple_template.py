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

NUMBER_OF_SEGMENTS = 1

wavfiles_templates = [
    ['zero_template', 'zero_template_1', 'zero_template_2', 'zero_template_3', 'zero_template_4'],
    ['one_template', 'one_template_1', 'one_template_2', 'one_template_3', 'one_template_4'],
    ['two_template', 'two_template_1', 'two_template_2', 'two_template_3', 'two_template_4'],
    ['three_template', 'three_template_1', 'three_template_2', 'three_template_3', 'three_template_4'],
    ['four_template', 'four_template_1', 'four_template_2', 'four_template_3', 'four_template_4'],
    ['five_template', 'five_template_1', 'five_template_2', 'five_template_3', 'five_template_4'],
    ['six_template', 'six_template_1', 'six_template_2', 'six_template_3', 'six_template_4'],
    ['seven_template', 'seven_template_1', 'seven_template_2', 'seven_template_3', 'seven_template_4'],
    ['eight_template', 'eight_template_1', 'eight_template_2', 'eight_template_3', 'eight_template_4'],
    ['nine_template', 'nine_template_1', 'nine_template_2', 'nine_template_3', 'nine_template_4'],
]

FILE_NAME = 'test_speak.wav'

template_list = []

template_holder = []
template_holder_raw = []
covariance_matric_holder = [[] for _ in range(NUMBER_OF_SEGMENTS)]
for idx, file_array in enumerate(wavfiles_templates):
    template_models = [[] for _ in range(NUMBER_OF_SEGMENTS)]
    template_holder_raw = [np.zeros((1,39)) for _ in range(NUMBER_OF_SEGMENTS)]
    for file in file_array:
        x = scipy.io.loadmat(file + '.mat').get('data').transpose()

        (num_samples, num_features) = x.shape
        num_vectors_in_segment = num_samples / NUMBER_OF_SEGMENTS
        to_remove = num_samples % NUMBER_OF_SEGMENTS
        if to_remove!= 0: x = x[0:-to_remove][:]
        signal_segments = np.split(x, NUMBER_OF_SEGMENTS)
        for chunk_idx, chunk in enumerate(signal_segments):
            template_models[chunk_idx].extend(chunk)
        pass
    # covariance = np.cov(template_models[idx])
    # covariance_matric_holder.append(covariance)
    for tm_idx, _ in enumerate(template_models):
        length = len(template_models[tm_idx])
        template_holder_raw[tm_idx] = np.vstack((template_holder_raw[tm_idx], template_models[tm_idx]))
        template_models[tm_idx] = reduce(lambda _1, _2 : _1 + _2, template_models[tm_idx]) / length
    template_holder.append(template_models)
    pass

for idx, template_raw in enumerate(template_holder_raw):
    covariance_matric_holder[idx] = np.diag(np.diag(np.cov(template_raw)))

# template_list.append(np.random.rand(20 + np.random.random_integers(20), 39))
template_list = np.array(template_holder)
MelFeat = MelFeatures()
raw_data = MelFeat.loadWAVfile(FILE_NAME)
mfcc_features = MelFeat.calcMelFeatures(raw_data)
input = mfcc_features.transpose()

# template_list = template_holder[0]
# template_list = [np.array([np.array([1, 2, 3, 3, 5]),
#                            np.array([5, 6, 7, 8, 9]),
#                            np.array([5, 6, 3, 1, 9]),
#                            np.array([11, 12, 13, 14, 15])]),
#                  np.array([np.array([1, 2, 4, 3, 5]),
#                            np.array([5, -6, 3, 1, 9]),
#                            np.array([5, 6, 3, 1, 19]),
#                            np.array([5, -6, 3, 1, -9]),
#                            np.array([-5, 6, 3, 1, 9]),
#                            np.array([-1, 2, 3, 4, 15])]),
#                  np.array([np.array([1, 2, 4, 3, 5]),
#                            np.array([5,11, 7, 2, 9]),
#                            np.array([5,11, 7, 2, 9]),
#                            np.array([5,11, 7, 2, 9]),
#                            np.array([5, 45, 7, 8, 9]),
#                            np.array([1, 2, 3, 34, 15])])]
#
# input = np.array(np.array([ np.array([ 1, 2, 3, 3, 5]),
#                             np.array([ 5, 6, 7, 8, 9]),
#                             np.array([ 5, 6, 7, 8, 9]),
#                             np.array([ 5, 6, 7, 8, 9]),
#                             np.array([11,12,13,14,15])]))

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


for i in range(0, input.shape[0]):
    for j in range(0, len(template_list)):
        for k in range(0, template_list[j].shape[0]):
            node_cost = dist.euclidean(input[i], template_list[j][k])
            # node_cost = dist.mahalanobis(input[i], template_list[j][k], [1/_ for _ in covariance_matric_holder[j]])
            (path_cost_prev, back_ptr) = find_prev_nodes(i, k);

            back_ptr_matrix[i][template_begin_indices[j] + k] = back_ptr
            path_cost = path_cost_prev + node_cost
            trellis[i][template_begin_indices[j] + k] = path_cost

split_trellis = np.split(trellis, template_begin_indices, axis=1)[1:]
split_distance_matrix = np.split(back_ptr_matrix, template_begin_indices, axis=1)[1:]

result_container = zip(split_trellis, split_distance_matrix)
print 'Distance'


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
    print 'Template ' + str(i) + ' Distance ---> ' + str(min(result_container[i][0][-1])) + '\n'
    custom_print_result(result_container[i])

print 'My Prediction --> ' + str(np.where(computed_distances == min(computed_distances))[0][0])