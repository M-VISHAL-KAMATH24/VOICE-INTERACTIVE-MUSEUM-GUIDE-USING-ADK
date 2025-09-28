from TTS.api import TTS
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
tts.tts_to_file(text="Hello from Coqui", file_path="hello.wav")
print("Wrote hello.wav")