from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu")
segments, info = model.transcribe("testaudio.m4a", beam_size=1)
print(f"Language: {info.language}, prob: {info.language_probability:.2f}")
for s in segments:
    print(f"[{s.start:.2f} -> {s.end:.2f}] {s.text}")