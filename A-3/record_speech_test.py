import unittest
from record_speech import RecordSpeech

class RecordSpeechTest(unittest.TestCase):

    def setUp(self):
        self.recorder = RecordSpeech()
        pass

    def test_energy_calculation(self):
        self.assertEquals(20,self.recorder.energy([5,5,5,5]))

def main(self):
    unittest.main()

if __name__ == '__main__':
    main()