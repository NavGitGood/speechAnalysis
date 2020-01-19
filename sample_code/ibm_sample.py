import json
from os.path import join, dirname, isfile
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
import threading
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

if isfile(join(dirname(__file__), '../audio_clips/sample.wav')) :
    print ("File exist")
else:
    print ("File not exist")
your_api_key = os.getenv('your_api_key')
authenticator = IAMAuthenticator(your_api_key)
service = SpeechToTextV1(authenticator=authenticator)
service.set_service_url('https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/f684400b-f4f6-4489-9113-0099ce9c9dc5')

models = service.list_models().get_result()

model = service.get_model('en-GB_NarrowbandModel').get_result()

with open(join(dirname(__file__), '../audio_clips/sample.wav'),
          'rb') as audio_file:
    print(json.dumps(
        service.recognize(
            audio=audio_file,
            content_type='audio/wav',
            timestamps=True,
            word_confidence=True).get_result(),
        indent=2))