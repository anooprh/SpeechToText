import numpy as np
from scipy.signal import lfilter
import math


class SignalHelpers:

    def pre_emphasize(self, speech_signal, pre_emphasizing_factor):
        numerator_co_effecients = np.array([1, -pre_emphasizing_factor])
        denominator_co_effecients = 1
        return lfilter(numerator_co_effecients, denominator_co_effecients, speech_signal)

    def fetch_hamming_window(self, window_length):
        M = window_length - 1
        n = np.arange(0, window_length)
        hamming_window = 0.54 - 0.46 * np.cos(math.pi * 2 * n / M)
        return hamming_window

    def dct(self, signal, no_of_coeffecients):
        S = signal.shape
        cos_arg = np.arange(1, 2 * S[0], 2)
        dct_mat = np.zeros((S[0], S[0]))
        for k in np.arange(0, S[0]):
            dct_mat[k, :] = math.sqrt(2.0 / S[0]) * np.cos(math.pi * 0.5 * k * cos_arg / S[0])

        dct_mat[0, :] = dct_mat[0, :] / math.sqrt(2.0)
        C = np.dot(dct_mat, signal)
        C = C[0:no_of_coeffecients, :]
        return C

    def idct(self,Q,numlen):
        S = Q.shape
        if numlen > S[0]:
          newQ = np.zeros((numlen,S[1]))
          newQ[0:S[0],:] = Q
          Q = newQ
        S = Q.shape
        cos_arg = np.arange(0,S[0])
        dct_mat = np.zeros((S[0],S[0]))
        for n in np.arange(0,S[0]):
          dct_mat[n,:] = math.sqrt(2.0/S[0])*np.cos(math.pi*0.5*cos_arg*(2*n+1)/S[0])

        dct_mat[:,0] = dct_mat[:,0]/math.sqrt(2.0)
        R = np.dot(dct_mat,Q)
        return R
