import matplotlib.pyplot as plt
import scipy as sp
import scipy
import numpy as np
from record_speech import record_to_file
from mfcc_features import MelFeatures
from dtw_Node import DTW_Node

wavfiles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

template_features = []
FILE_NAME = 'test_speak.wav'
print("please speak a word into the microphone")
record_to_file(FILE_NAME)
print("done - result written to " + FILE_NAME)

print "Calculating MEL features..."
MelFeat = MelFeatures()
raw_data = MelFeat.loadWAVfile(FILE_NAME)
mfcc_features = MelFeat.calcMelFeatures(raw_data)
mfcc_features = np.hstack((np.zeros((39, 1)), mfcc_features))

for file in wavfiles:
    template_features.append(scipy.io.loadmat(file + '.mat').get('data'))

dtw_nodes = []


def get_predecessor_nodes(i, k):
    predecessor_nodes = []
    if i == 0:
        return predecessor_nodes
    predecessor_nodes.append(dtw_nodes[i - 1][k])

    if k == 0:
        return predecessor_nodes

    predecessor_nodes.append(dtw_nodes[i - 1][k - 1])
    if k == 1:
        return predecessor_nodes
    predecessor_nodes.append(dtw_nodes[i - 1][k - 2])
    return predecessor_nodes

active_list = range(0, len(template_features)*template_features[0].shape[1])
new_active_list = None

for i in range(0, mfcc_features.shape[1]):
    dtw_nodes.append([])
    for j in range(0, len(template_features)):
        for k in range(0, template_features[j].shape[1] + 1):
            template_feature = np.hstack((np.zeros((39, 1)), template_features[0]))
            node = DTW_Node()
            node.time = i
            node.templateIndex = k

            if (i == 0):
                node.cost = k
                node.prev_node = [i,k-1]
                dtw_nodes[i].append(node)
                continue
            if (k == 0):
                node.cost = i
                node.prev_node = [i-1,k]
                dtw_nodes[i].append(node)
                continue

            distance = sp.spatial.distance.euclidean(mfcc_features[:, i], template_feature[:, k])

            predecessor_node_list = get_predecessor_nodes(i, k)

            prev_cost = 0
            prev_node = None
            if len(predecessor_node_list) == 0:
                prev_cost = -1
            if len(predecessor_node_list) == 1:
                prev_cost = predecessor_node_list[0].cost
                came_from = 0
            if len(predecessor_node_list) == 2:
                prev_cost = min(predecessor_node_list[0].cost, predecessor_node_list[1].cost)
                if prev_cost == predecessor_node_list[0].cost : came_from = [i-1,k]
                if prev_cost == predecessor_node_list[1].cost : came_from = [i-1,k-1]

            if len(predecessor_node_list) > 2:
                prev_cost = min(predecessor_node_list[0].cost, predecessor_node_list[1].cost, predecessor_node_list[2].cost)
                if prev_cost == predecessor_node_list[0].cost : came_from = [i-1,k]
                if prev_cost == predecessor_node_list[1].cost : came_from = [i-1,k-1]
                if prev_cost == predecessor_node_list[2].cost : came_from = [i-1,k-2]

            node.cost = prev_cost + distance
            node.prev_node = [-1,-1]
            if came_from == 0:
                node.prev_node = dtw_nodes[i-1][k]
            if came_from == 1:
                node.prev_node = dtw_nodes[i-1][k-1]
            if came_from == 2:
                node.prev_node = dtw_nodes[i-2][k-1]
            dtw_nodes[i].append(node)
        if i == mfcc_features.shape[1] -1 :
            print j,node.cost

toshow = []
for i in range(0,len(dtw_nodes)):
    toshow.append([])
    for j in range(0,len(dtw_nodes[i])):
        toshow[i].append(dtw_nodes[i][j].cost)

plt.imshow(toshow, aspect='auto', origin='lower')
# plt.show()
# plt.matshow(toshow, fignum=100)
plt.show()
pass