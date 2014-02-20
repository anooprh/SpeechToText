import pyaudio
import wave
import numpy as np
from find_features import MfccFeatures

CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

MAX_RECORD_SECONDS = 30
THRESHOLD_DB  = 2000
WAVE_OUTPUT_FILENAME = "output.wav"


def energy(samples):
    sum_sq = (np.sum([sample ** 2 for sample in samples]))
    return  np.sqrt(sum_sq)

p = pyaudio.PyAudio()
x = None;
while(x != ' '):
    x = raw_input('Press Space bar')
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []
energy_signal = []
energy_in_chunk = 0
started_speaking = False;

for i in range(0, int(RATE / CHUNK * MAX_RECORD_SECONDS)):

    # for first second, record without checking energy
    if i < 120 :
        data = stream.read(CHUNK)
        signal_chunk = np.fromstring(data, 'Int16')
        energy_in_chunk = energy(signal_chunk)
        frames.append(data)
       # continue

    if i >= 120 :
        data = stream.read(CHUNK)
        frames.append(data)
        signal_chunk = np.fromstring(data, 'Int16')
        energy_in_chunk = energy(signal_chunk)
        print i , energy_in_chunk
        if energy_in_chunk < THRESHOLD_DB:
            data = stream.read(CHUNK)
            frames.append(data)
            signal_chunk = np.fromstring(data, 'Int16')
            energy_in_chunk = energy(signal_chunk)
            if energy_in_chunk < THRESHOLD_DB:
                data = stream.read(CHUNK)
                frames.append(data)
                signal_chunk = np.fromstring(data, 'Int16')
                energy_in_chunk = energy(signal_chunk)

                if energy_in_chunk < THRESHOLD_DB:
                    data = stream.read(CHUNK)
                    frames.append(data)
                    signal_chunk = np.fromstring(data, 'Int16')
                    energy_in_chunk = energy(signal_chunk)
                    if energy_in_chunk < THRESHOLD_DB:
                         data = stream.read(CHUNK)
                         frames.append(data)
                         signal_chunk = np.fromstring(data, 'Int16')
                         energy_in_chunk = energy(signal_chunk)
                         break


print("* done recording")

stream.stop_stream()
p.close(stream)
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


mfcc_features = MfccFeatures()

(fs, speech_signal) = mfcc_features.read_file(file_name="output.wav")
features = mfcc_features.features(speech_signal)
mfcc_features.plot_features(features);