import azure.cognitiveservices.speech as speechsdk
import os.path
import time
import wave
from mongo_operations import augment_and_insert
from datetime import datetime

transcript_list = []

speech_key=os.getenv('speech_key')
print(speech_key)
service_region = "westus"

def getRecognized(evt):
    transcript_list.append(evt.result.text)
    # print(transcript)
    return transcript_list

def speech_recognize_continuous_from_file(audio_filename, index):
    # audio_filename = "microphone_audio/output_1579388897.wav"
    if os.path.isfile(audio_filename):
        print ("File exist")
    else:
        print ("File not exist")
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y|%H:%M:%S")

    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        # print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
        # print('stop_cb: ' + transcript_list)

    # Connect callbacks to the events fired by the speech recognizer
    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    # speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.recognized.connect(getRecognized)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    if done:
        # time.sleep(1)
        for i in range(10):
            if len(transcript_list) < index+1:
                time.sleep(.5)
            else:
                augment_and_insert(transcript_list[index], date_time)
                break
    # print(transcript_list)
    # return transcript_list

