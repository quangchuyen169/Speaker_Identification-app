import sounddevice as sd
import numpy as np
import wave

CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "record.wav"


def record():
    print("* Recording")

    # Ghi âm và lưu dữ liệu vào mảng numpy
    recording_data = sd.rec(int(RATE * RECORD_SECONDS), samplerate=RATE, channels=CHANNELS, dtype='int16')
    sd.wait()

    print("* Done recording")

    # Lưu mảng numpy vào tệp WAV
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 2 bytes cho kiểu dữ liệu 'int16'
    wf.setframerate(RATE)
    wf.writeframes(recording_data.tobytes())
    wf.close()

