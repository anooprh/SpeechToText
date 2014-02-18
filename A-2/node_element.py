import numpy as np;
import sys


class Node(np.object):

    def __init__(self):
        self.weight = -1
        self.backtrack = None;
        self.row = -1
        self.column = -1

    def __init__(self, distance):
        self.distance = distance
        self.in_path = False;

    def printDistance(self):
        sys.stdout.write(str(self.distance) + '  ')

class word_node:
    def __init__(self, distance):
        self.distance = distance
    def printDistance(self):
        sys.stdout.write(str(self.distance)+ ' ')
