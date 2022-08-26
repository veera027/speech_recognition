from api_communication import *
from live_audio_recording import *


if __name__ == '__main__':
    audio_file_name = input("Enter the person name: ")
    file_name = create_audio_file(audio_file_name)
    audio_url = upload(file_name)
    save_transcript(audio_url, file_name)
    print_transcript(file_name)
