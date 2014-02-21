from math import log10
import pyaudio
import wave
import numpy as np


class RecordSpeech:
    CHUNK = 320
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    MAX_RECORD_SECONDS = 20
    THRESHOLD_DB  = 30
    WAVE_OUTPUT_FILENAME = "output.wav"
    INITIAL_IGNORE_PERIOD_SECONDS = 1

    silence_frame_count = 0
    started_speaking = False
    def energy(self, samples):
        sum_of_squares = np.sum([sample ** 2 for sample in samples])
        return  0 if sum_of_squares == 0 else 10*log10(sum_of_squares)

    def record(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        print("Recording Started")

        frames = []
        started_speaking = False;

        for i in range(0, int(self.RATE / self.CHUNK * self.MAX_RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            signal_chunk = np.fromstring(data, 'Int16')
            energy_in_chunk = self.energy(signal_chunk)
            print i , energy_in_chunk
            frames.append(data)

            if i < int(self.RATE / self.CHUNK * self.INITIAL_IGNORE_PERIOD_SECONDS):
                continue
            if self.started_speaking==True and energy_in_chunk < self.THRESHOLD_DB:
                self.silence_frame_count = self.silence_frame_count + 1
            if self.silence_frame_count >= 10:
                break;
            if energy_in_chunk > self.THRESHOLD_DB:
                self.started_speaking = True
                self.silence_frame_count = 0


        print("* done recording")

        stream.stop_stream()
        p.close(stream)
        stream.close()
        p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


if __name__=='__main__':
    recorder = RecordSpeech()
    recorder.record()