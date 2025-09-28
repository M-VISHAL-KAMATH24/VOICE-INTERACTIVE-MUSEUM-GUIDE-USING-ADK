from RealtimeTTS import TextToAudioStream, SystemEngine
import threading

class TTSPlayer:
    def __init__(self, engine=None, **kwargs):
        self.engine = engine or SystemEngine()
        self.stream = TextToAudioStream(self.engine, **kwargs)
        self._lock = threading.Lock()

    def speak(self, text):
        with self._lock:
            self.stream.stop()
            self.stream.feed(text)
            self.stream.play_async()

    def pause(self):
        with self._lock:
            self.stream.pause()

    def resume(self):
        with self._lock:
            self.stream.resume()

    def stop(self):
        with self._lock:
            self.stream.stop()

    def is_playing(self):
        return self.stream.is_playing()
