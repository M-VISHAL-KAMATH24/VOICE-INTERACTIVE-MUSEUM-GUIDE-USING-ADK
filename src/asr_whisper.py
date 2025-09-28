# src/asr_whisper.py

from faster_whisper import WhisperModel
import tempfile, wave, os

class WhisperASR:
    def __init__(self, model_name="tiny", device="cpu", vad=True, min_silence_ms=500):
        self.model = WhisperModel(model_name, device=device)
        self.vad = vad
        self.min_silence_ms = min_silence_ms

    def transcribe_pcm16(self, pcm16_bytes, samplerate=16000):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            path = f.name
        try:
            with wave.open(path, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(samplerate)
                w.writeframes(pcm16_bytes)
            segments, info = self.model.transcribe(
                path,
                beam_size=1,
                vad_filter=self.vad,
                vad_parameters=dict(min_silence_duration_ms=self.min_silence_ms),
                condition_on_previous_text=False
            )
            text = "".join(s.text for s in segments)
            return text.strip(), info.language
        finally:
            try: os.remove(path)
            except OSError: pass
