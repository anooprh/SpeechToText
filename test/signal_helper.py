import unittest
import numpy as np
from signal_helpers import SignalHelpers

class TestSignalHelperd(unittest.TestCase):

    def setUp(self):
        self.signal_helper = SignalHelpers()

    def test_pre_emphasize(self):
        sample_signal = [100, 90, 80]
        emphasized_signal = self.signal_helper.pre_emphasize(sample_signal, 0.5)
        self.assertEquals([1,2,2], emphasized_signal)
        np.tes


if __name__ == '__main__':
    unittest.main()