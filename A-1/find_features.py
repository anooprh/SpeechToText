from scipy.fftpack import fft
import scipy.io.wavfile as wav
import numpy as np
import math
import matplotlib.pyplot as plt

from signal_helpers import SignalHelpers


class MfccFeatures:
    PRE_EMPHASIZING_FACTOR = 0.95
    WINDOW_LENGTH = 0.025
    WINDOW_DISTANCE = 0.010
    NUMBER_OF_FILTERS = 40
    NUMBER_OF_FEATURES = 13
    DELTA_WIDTH = 2
    DOUBLE_DELTA_WIDTH = 4
    MINIMUM_FREQ = 133.0
    MAXIMUM_FREQ = 6855.0
    WIDTH = 1

    def hz2mel(self,frq):
        m   = 2595*math.log(1+frq/700,10)
        return m

    def mel2hz(self,m):
        frq = 700*(pow(10,m/2595)-1)
        return frq

    def __init__(self):
        self.signal_helpers = SignalHelpers()
        self.raw_signal = None
        self.fs = None

    def read_file(self, file_name):
        wav_file_properties = wav.read(file_name)
        self.raw_signal = wav_file_properties[1]
        self.fs = wav_file_properties[0]
        return wav_file_properties

    def apply_hamming_window(self, fft_length, hamming_window, num_windows, signal, signal_length, window_distance,
                             window_length):
        windowed_signal = np.zeros((1 + fft_length / 2, num_windows))
        k = 0
        for i in range(0, signal_length - 1, int(window_distance)):
            if i + window_length - 1 > len(signal):
                break
            x_seg = signal[i:i + window_length] * hamming_window
            X_seg = abs(fft(x_seg, fft_length))
            windowed_signal[:, k] = X_seg[0:1 + fft_length / 2]
            k += 1
        return windowed_signal

    def stft(self, signal, window_lenght_in_ms, window_distance_in_ms, fs):
        signal_length = len(signal)
        window_length = math.floor(window_lenght_in_ms * fs)
        window_distance = math.floor(window_distance_in_ms * fs)
        fft_length = math.pow(2, math.ceil(math.log(window_length, 2)))
        num_windows = int(1 + math.floor((signal_length - window_length) / window_distance))

        hamming_window = self.signal_helpers.fetch_hamming_window(window_length)
        windowed_signal = self.apply_hamming_window(fft_length, hamming_window, num_windows, signal, signal_length,
                                                    window_distance,
                                                    window_length)

        return (windowed_signal, fft_length, num_windows)

    def fetch_filter_bank(self, number_of_filters, minimum_frequency, maximum_frequency, width, fft_length):

        frequency_range_start = 0
        frequency_range_end = self.fs / 2 + self.fs / fft_length
        frequency_range_step = self.fs / fft_length
        frequencies = np.arange(frequency_range_start, frequency_range_end, frequency_range_step)

        filter_bank = np.zeros((len(frequencies), number_of_filters));

        mel_frequency_start = self.hz2mel(minimum_frequency)
        mel_frequency_end = self.hz2mel(maximum_frequency)
        mel_frequencies = np.linspace(mel_frequency_start, mel_frequency_end, number_of_filters + 2);
        central_fqs = np.zeros((number_of_filters + 2));

        for index in range(0, number_of_filters + 2):
            central_fqs[index] = self.mel2hz(mel_frequencies[index])

        for index in range(0, number_of_filters):
            filter_central_fqs = central_fqs[index:index + 3];
            filter_central_fqs = filter_central_fqs[1] + width * (filter_central_fqs - filter_central_fqs[1])

            loslope = (frequencies - filter_central_fqs[0]) / (filter_central_fqs[1] - filter_central_fqs[0])
            hislope = (filter_central_fqs[2] - frequencies) / (filter_central_fqs[2] - filter_central_fqs[1])

            filter_bank[:, index] = np.maximum(0, np.minimum(loslope, hislope))

        return filter_bank

    def cmn(self, C):
        m = np.mean(C, 1)
        for i in range(0, self.NUMBER_OF_FEATURES):
            C[i, :] = C[i, :] - m[i]

        return C

    def deltas(self, c, w):
        S = c.shape
        d = np.zeros((S[0], S[1]))
        for n in range(0, S[1]):
            d[:, n] = c[:, (n + w / 2) % S[1]] - c[:, n - w / 2] #negative indices wrap around
        d = d / w
        return d

    def features(self, speech_signal):
        pre_emphasized_signal = self.signal_helpers.pre_emphasize(speech_signal,
                                                                  pre_emphasizing_factor=self.PRE_EMPHASIZING_FACTOR)

        (processed_signal, fft_length, num_windows) = self.stft(pre_emphasized_signal, self.WINDOW_LENGTH,
                                                                self.WINDOW_DISTANCE, self.fs)

        filter_bank = self.fetch_filter_bank(self.NUMBER_OF_FILTERS, self.MINIMUM_FREQ, self.MAXIMUM_FREQ, self.WIDTH,
                                             fft_length)

        energy_signal = pow(processed_signal, 2)
        filter_bank_for_energy_signal = pow(filter_bank.transpose(), 2)

        filtered_signal = np.dot(filter_bank_for_energy_signal, energy_signal)
        filtered_signal_log_scale = np.log(filtered_signal)

        frequency_domain_signal = self.signal_helpers.dct(filtered_signal_log_scale, self.NUMBER_OF_FEATURES)

        zero_centered_signal = self.cmn(frequency_domain_signal)
        delta1 = self.deltas(zero_centered_signal, self.DELTA_WIDTH)
        delta2 = self.deltas(zero_centered_signal, self.DOUBLE_DELTA_WIDTH)

        calculated_from_idct = self.signal_helpers.idct(zero_centered_signal,128)

        features = np.zeros((3 * self.NUMBER_OF_FEATURES, num_windows))
        features[0:self.NUMBER_OF_FEATURES, :] = zero_centered_signal
        features[self.NUMBER_OF_FEATURES:2 * self.NUMBER_OF_FEATURES] = delta1
        features[2 * self.NUMBER_OF_FEATURES:3 * self.NUMBER_OF_FEATURES] = delta2

        return features;

    def plot_features(self, features):
        for i in np.arange(0,features.shape[0]):
            feature = features[i]
            plt.plot(feature)
            plt.savefig('feature_'+i.astype('str')+'.png')
            plt.clf()

    def show_signal(self, data):
        plt.plot(data)
        plt.show();


if __name__ == "__main__":
    mfcc_features = MfccFeatures()

    (fs, speech_signal) = mfcc_features.read_file(file_name="output.wav")
    features = mfcc_features.features(speech_signal)
    mfcc_features.plot_features(features);