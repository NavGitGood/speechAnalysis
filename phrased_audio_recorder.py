import pyaudio
import wave
import audioop
from collections import deque
import os
import time
import math
import threading
import sys
from sample_code.ms_sample import speech_recognize_continuous_from_file
from mongo_operations import augment_and_insert
from audio_device_selector import device_selection
# import threading

# Microphone stream config.
# CHUNK = 512  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
THRESHOLD = 2500  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).

SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.

PREV_AUDIO = 1  # Previous audio (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded audio is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.


def audio_int(num_samples=50):
    """ Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """

    print ("Getting intensity values from mic.")
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
              for x in range(num_samples)] 
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    stream.close()
    p.terminate()
    return r

def listen_for_speech(threshold=THRESHOLD, num_phrases=15):
    """
    Listens to Microphone, extracts phrases from it and sends it to 
    Azure Speech To Text service and returns response. a "phrase" is sound 
    surrounded by silence (according to threshold). num_phrases controls
    how many phrases to process before finishing the listening process 
    (-1 for infinite). 
    """
    #Open stream
    p = pyaudio.PyAudio()
    stream, CHANNELS, device_info, CHUNK, RATE = device_selection(p)

    # stream = p.open(format=FORMAT,
    #                 channels=0,  #CHANNELS
    #                 rate=RATE,
    #                 input=True,
    #                 frames_per_buffer=CHUNK,
    #                 input_device_index=6,
    #                 as_loopback = True)   #1

    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    print(rel)
    print(SILENCE_LIMIT * rel)
    slid_win = deque(maxlen=int(SILENCE_LIMIT * rel))
    # Prepend audio from 0.5 seconds before noise was detected
    prev_audio = deque(maxlen=int(PREV_AUDIO * rel))
    started = False
    n = num_phrases
    response = []
    index=0
    while (num_phrases == -1 or n > 0):
        
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        if(sum([x > THRESHOLD for x in slid_win]) > 0):
            if(not started):
                # Starting record of phrase
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            # The limit was reached, finish capture and deliver.
            filename = save_speech(list(prev_audio) + audio2send, p, device_info, CHANNELS)
            # transcript = speech_recognize_continuous_from_file(filename, index)
            # print(transcript[index])
            # augment_and_insert(transcript[index])
            x=threading.Thread(target=speech_recognize_continuous_from_file, args=(filename, index))
            x.start()
            # x.join()
            index = index+1
            started = False
            slid_win = deque(maxlen=int(SILENCE_LIMIT * rel))
            prev_audio = deque(maxlen=int(1 * rel))
            audio2send = []
            n -= 1
            # Listening ...
        else:
            prev_audio.append(cur_data)

    # Done recording
    stream.close()
    p.terminate()
    # sys.exit()
    return response


def save_speech(data, p, device_info, channelcount):
    filename = 'microphone_audio/output_'+str(int(time.time()))
    waveFile = wave.open(filename + '.wav', 'wb')
    waveFile.setnchannels(channelcount)
    waveFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(int(device_info["defaultSampleRate"]))
    waveFile.writeframes(b''.join(data))
    waveFile.close()
    return filename + '.wav'

if(__name__ == '__main__'):
    listen_for_speech()  # listen to mic.