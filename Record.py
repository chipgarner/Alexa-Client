
from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import wave


class Record:
    def __init__(self):
        self.threshold = 500  # audio levels not normalised.
        self.chunk_size = 1024
        self.max_silent_chunks = 3 * 16000 / 1024  # about 3 sec
        self.format = pyaudio.paInt16
        self.frame_max_value = 2 ** 15 - 1
        self.normalize_minus_one_dB = 10 ** (-1.0 / 20)
        self.rate = 16000
        self.channels = 1
        self.trim_append = self.rate / 4
        self.silent_chunks = 0
        
    def _is_silent(self, data_chunk):
        """Returns 'True' if below the 'silent' self.threshold"""
        return max(data_chunk) < self.threshold
    
    def _normalize(self, data_all):
        """Amplify the volume out to max -1dB"""
        # MAXIMUM = 16384
        normalize_factor = (float(self.normalize_minus_one_dB * self.frame_max_value)
                            / max(abs(i) for i in data_all))
    
        r = array('h')
        for i in data_all:
            r.append(int(i * normalize_factor))
        return r
    
    def _trim(self, data_all):
        _from = 0
        _to = len(data_all) - 1
        for i, b in enumerate(data_all):
            if abs(b) > self.threshold:
                _from = max(0, i - self.trim_append)
                break
    
        for i, b in enumerate(reversed(data_all)):
            if abs(b) > self.threshold:
                _to = min(len(data_all) - 1, len(data_all) - 1 - i + self.trim_append)
                break
    
        trimmed = data_all[int(_from):(int(_to) + 1)]
        return copy.deepcopy(trimmed)

    def continue_recording(self, silent, max_silent_chunks):
        continuing = True

        if silent:
            self.silent_chunks += 1
            if self.silent_chunks > max_silent_chunks:
                continuing = False
        else:
            self.silent_chunks = 0

        return continuing

    def _record(self):
        """Record a word or words from the microphone and 
        return the data as an array of signed shorts."""
    
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, output=True,
                        frames_per_buffer=self.chunk_size)
    
        data_all = array('h')
    
        while True:
            # little endian, signed short
            data_chunk = array('h', stream.read(self.chunk_size))
            if byteorder == 'big':
                data_chunk.byteswap()
            data_all.extend(data_chunk)
    
            silent = self._is_silent(data_chunk)
    
            if not self.continue_recording(silent, self.max_silent_chunks):
                break
    
        sample_width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()
    
        data_all = self._trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
        data_all = self._normalize(data_all)
        return sample_width, data_all
    
    def record_to_file(self, path):
        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = self._record()
        data = pack('<' + ('h' * len(data)), *data)
    
        wave_file = wave.open(path, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(self.rate)
        wave_file.writeframes(data)
        wave_file.close()

if __name__ == '__main__':
    rec = Record()
    print("Wait in silence to begin recording; wait in silence to terminate")
    rec.record_to_file('LiveRecordings/latest.wav')
    print("done - result written to demo.wav")