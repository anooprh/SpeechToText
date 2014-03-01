__author__ = 'anoop'
import matplotlib.pyplot as plt
import scipy as sp
import scipy
import numpy as np
from record_speech import record_to_file
from mfcc_features import MelFeatures
from dtw_Node import DTW_Node
THRESHOLD = 10000
wavfiles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

template_features = []
# FILE_NAME = 'test_speak.wav'
# print("please speak a word into the microphone")
# record_to_file(FILE_NAME)
# print("done - result written to " + FILE_NAME)

print "Calculating MEL features..."
MelFeat = MelFeatures()
raw_data = MelFeat.loadWAVfile("anoop_speak.wav")
mfcc_features = MelFeat.calcMelFeatures(raw_data)
mfcc_features = np.hstack((np.zeros((39, 1)), mfcc_features))

template_length = 0

active_list = [0,0]

for file in wavfiles:
    template_feature = scipy.io.loadmat(file + '.mat').get('data')
    template_features.append(template_feature)
    template_length = template_length + template_feature.shape[1]
    temp_active_list = np.append(1,np.zeros((template_feature.shape[1]-1)))
    active_list = np.append(active_list, temp_active_list)

dtw_nodes = np.zeros((mfcc_features.shape[1]+1, len(template_features) * template_length + 2))
dtw_nodes[:] = float('inf')

direction_matrix = np.zeros_like(dtw_nodes)
direction_matrix[2][1] = -1


def getPredecessorNodes(row, col):
    col_offset = col - 1
    row_offset = row + 2
    return [dtw_nodes[row_offset][col_offset-1],dtw_nodes[row_offset-1][col_offset-1], dtw_nodes[row_offset-2][col_offset-1]]

template_features[0].shape[1]
for i in range(mfcc_features.shape[1]):
    for j in range(len(template_features)):
        for k in range(template_features[j].shape[1]):
            if(active_list[j+k] != 1 ):
                continue
            distance = sp.spatial.distance.euclidean(mfcc_features[:, i], template_feature[:, k])

            predecessors = getPredecessorNodes(i, j+k)
            predecessor_cost = min(predecessors)
            direction = predecessors.index(predecessor_cost)

            direction_matrix[i+1][j+k+2] = direction
            dtw_nodes[i+1][j+k+2] = predecessor_cost + distance

    new_active_list = active_list

    for index in range(len(active_list)):
        if active_list[index] == 1:
            new_active_list[index] = new_active_list[index + 1] = new_active_list[index + 2] = 1

    for index in range(len(new_active_list)):
        if new_active_list[index] == 1:
            if dtw_nodes[i][index] > THRESHOLD:
                new_active_list[index] = 0
    active_list = new_active_list




pass