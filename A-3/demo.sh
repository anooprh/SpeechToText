#!/usr/bin/bash

python record_speech.py test_speak.wav
play test_speak.wav
python save_features.py test_speak
python do_dtw_single_template.py test_speak