from pydub import AudioSegment
t1 = 6 * 1000 #Works in milliseconds
t2 = 26 * 1000
newAudio = AudioSegment.from_wav("audio_clips/_audio.wav")
newAudio = newAudio[t1:t2]
newAudio.export('audio_clips/sample.wav', format="wav")