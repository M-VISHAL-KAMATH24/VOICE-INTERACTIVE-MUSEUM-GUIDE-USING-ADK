import sounddevice as sd
import numpy as np
import queue
import sys
import time

class MicStream:
    def __init__(self, samplerate=16000, channels=1, dtype="float32", frame_ms=30, energy_thresh=0.01):
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.blocksize = int(samplerate * frame_ms / 1000)
        self.q = queue.Queue()
        self.energy_thresh = energy_thresh
        self._stream = None

    def _cb(self, indata, frames, time_info, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def start(self):
        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            blocksize=self.blocksize,
            callback=self._cb
        )
        self._stream.start()

    def stop(self):
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def frames(self):
        while True:
            buf = self.q.get()
            yield buf

    @staticmethod
    def rms(x):
        return float(np.sqrt(np.mean(x.astype(np.float32) ** 2)))

    @staticmethod
    def is_speech(x, thresh=0.01):
        return MicStream.rms(x) > thresh
