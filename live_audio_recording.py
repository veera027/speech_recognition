import pyaudio
import wave
import time


# creating audio file, input is taken from microphone for 5 seconds
def create_audio_file(name):
    Frames_per_buffer = 3200
    Format = pyaudio.paInt16
    Channels = 1
    Rate = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=Format, frames_per_buffer=Frames_per_buffer, rate=Rate, channels=Channels, input=True)

    seconds = 5
    print("Recording for 5 secons \nstarts in 3 ", end=' ')
    time.sleep(1)
    print("2 ", end=' ')
    time.sleep(1)
    print("1 ")
    time.sleep(1)
    print('GO ..')
    time.sleep(0.5)

    Frames = []
    for i in range(0, int(Rate/Frames_per_buffer*seconds)):
        data = stream.read(Frames_per_buffer)
        Frames.append(data)

    stream.stop_stream()
    stream.close()

    file_name = 'rec_'+name+'.wav'
    obj = wave.open(file_name, 'wb')
    obj.setnchannels(Channels)
    obj.setframerate(Rate)
    obj.setsampwidth(p.get_sample_size(Format))
    obj.writeframes(b"".join(Frames))
    obj.close()
    print('Sounds good, audio saved')
    return file_name
