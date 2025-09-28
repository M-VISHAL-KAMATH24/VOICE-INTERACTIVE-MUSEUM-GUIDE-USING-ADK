import sounddevice as sd
import numpy as np
import queue
import sys
import wave
from faster_whisper import WhisperModel

# Sampling rate and audio queue
sr = 16000
sr3 = sr * 3  # 3 seconds worth of samples
q = queue.Queue()

# Callck to collect audio data
def cb(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

# Load Whisper model
model = WhisperModel("tiny", device="cpu")

# Start audio stream
with sd.InputStream(samplerate=sr, channels=1, dtype="float32", callback=cb):
    print("Speak... Ctrl+C to stop")
    buf = np.empty((0, 1), dtype=np.float32)

    try:
        while True:
            # Add audio data to buffer
            buf = np.concatenate([buf, q.get()])

            # Process when 3 seconds of audio is collected
            if buf.shape[0] >= sr3:
                # Convert to int16
                chunk = (buf[:sr3].flatten() * 32767).astype(np.int16)

                # Save audio to WAV file
                with wave.open("chunk.wav", "wb") as w:
                    w.setnchannels(1)
                    w.setsampwidth(2)  # 16-bit audio
                    w.setframerate(sr)
                    w.writeframes(chunk.tobytes())

                # Transcribe audio
                segs, _ = model.transcribe("chunk.wav", vad_filter=True, beam_size=1)
                print("You said:", "".join(s.text for s in segs))

                # Remove used audio from buffer
                buf = buf[sr3:]
    except KeyboardInterrupt:
        print("\nStopped.")
