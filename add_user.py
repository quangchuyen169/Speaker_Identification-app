import sounddevice as sd
import os
import pickle
import time
import shutil
import wave
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GM
import numpy as np
from speakerfeatures import extract_features

# Biến toàn cục để lưu tên của chủ nhà
host_name = None
def record_audio(duration, sample_rate=44100):
    print("Đang ghi âm...")

    # Ghi âm với thời gian và tốc độ lấy mẫu được chỉ định
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    print("Ghi âm hoàn thành.")

    return audio_data.flatten()

def add_user():

    name = input("Nhập tên của bạn: ")
    name_lower = name.lower()

    # Kiểm tra xem có lưu trạng thái chủ nhà hay không từ trước
    is_host_saved = False
    if os.path.isfile("is_host.txt"):
        with open("is_host.txt", "r") as file:
            is_host_saved = file.read().upper() == "Y"
    # Nếu chưa có trạng thái lưu trước đó, hỏi người nói có phải chủ nhà không
    if not is_host_saved:
        is_host_input = input("Bạn có phải chủ nhà không? (Y/N): ").upper()
        is_host = is_host_input == "Y"
        host_name = name  # Lưu tên chủ nhà vào biến toàn cục

            # Lưu tên chủ nhà vào file host_name.txt
        with open("host_name.txt", "w") as file:
            file.write(host_name)
        # Lưu trạng thái vào file
        with open("is_host.txt", "w") as file:
            file.write("Y" if is_host else "N")
    else:
        # Nếu đã có trạng thái lưu trước đó, đặt giá trị mặc định
        is_host = False
            
    FORMAT = np.int16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 6

    source = f"./dataset/train/{name}"

    if os.path.exists(source):
        override = input("Thư mục đã tồn tại. Bạn có muốn ghi đè không? (y/n): ").lower()
        if override != 'y':
            print("Thao tác đã hủy bỏ.")
            return
        else:
            # Xóa thư mục và tạo lại
            shutil.rmtree(source)
            os.mkdir(source)
    else:
        os.makedirs(source)

    for i in range(5):
        if i == 0:
            j = 3
        while j > 0:
            time.sleep(1.0)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Hãy nói trong vòng {} giây".format(j))
            j -= 1
        else:
            time.sleep(2.0)
            print("Tiếp tục nói lần {}".format(i+1))
            time.sleep(0.8)

        # Ghi âm
        audio_data = record_audio(RECORD_SECONDS, RATE)
        # Lưu trữ file âm thanh
        audio_path = os.path.join(source, f"{i + 1}.wav")
        with wave.open(audio_path, 'wb') as wavefile:
            wavefile.setnchannels(CHANNELS)
            wavefile.setsampwidth(audio_data.dtype.itemsize)
            wavefile.setframerate(RATE)
            wavefile.writeframes(audio_data.tobytes())
        print("Hoàn tất")

        with open('train_path.txt', 'w') as file:
            for k in range(1, 6):
                file.write(f'{name_lower}\\{k}.wav\n')
        
if __name__ == '__main__':
    add_user()
        