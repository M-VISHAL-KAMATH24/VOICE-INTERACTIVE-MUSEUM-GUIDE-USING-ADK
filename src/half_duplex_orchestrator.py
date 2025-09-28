import time
import numpy as np
from src.audio_io import MicStream
from src.asr_whisper import WhisperASR
from src.tts_player import TTSPlayer

class HalfDuplexLoop:
    def __init__(self, samplerate=16000, frame_ms=30, chunk_sec=2.0, silence_ms=500, energy_thresh=0.01):
        self.mic = MicStream(samplerate=samplerate, frame_ms=frame_ms, energy_thresh=energy_thresh)
        self.asr = WhisperASR(model_name="tiny", device="cpu", vad=True, min_silence_ms=int(silence_ms))
        self.tts = TTSPlayer()
        self.samplerate = samplerate
        self.chunk_samples = int(samplerate * chunk_sec)
        self.energy_thresh = energy_thresh

    @staticmethod
    def float_to_pcm16(x):
        x = np.clip(x, -1.0, 1.0)
        return (x * 32767.0).astype(np.int16).tobytes()

    def run(self):
        self.mic.start()
        try:
            buf = np.empty((0, 1), dtype=np.float32)
            print("Speak; I'll respond briefly. Ctrl+C to stop.")
            for frame in self.mic.frames():
                # Barge-in: if playback and incoming speech, pause TTS immediately
                if self.tts.is_playing() and MicStream.is_speech(frame, self.energy_thresh):
                    self.tts.pause()

                buf = np.concatenate([buf, frame])

                # If enough audio collected, and trailing region looks quiet, run ASR
                if buf.shape[0] >= self.chunk_samples:
                    tail_len = int(self.samplerate * 0.4)
                    tail = buf[-tail_len:] if buf.shape[0] >= tail_len else buf

                    if not MicStream.is_speech(tail, self.energy_thresh):
                        pcm16 = self.float_to_pcm16(buf.flatten())
                        t0 = time.time()
                        text, lang = self.asr.transcribe_pcm16(pcm16, samplerate=self.samplerate)
                        t1 = time.time()

                        if text:
                            print(f"[ASR {t1 - t0:.2f}s] {text}")
                            # Short, fast reply to keep loop snappy
                            from src.intent_router import route_to_persona
                            intent, reply = route_to_persona(text)
                            print(f"Intent: {intent} | Reply: {reply}")

                            self.tts.speak(reply)

                        # Reset buffer after each turn
                        buf = np.empty((0, 1), dtype=np.float32)
        finally:
            self.mic.stop()
            self.tts.stop()
