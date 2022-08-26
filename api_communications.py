import requests
import time


# put your API key here
API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"

# upload
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_KEY}


# uploading file to assembly.ai
def upload(file_name):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers, data=read_file(file_name))
    audio_url = upload_response.json()['upload_url']
    return audio_url


# transcription
def transcribe(audio_url):
    json = {"audio_url": audio_url}
    response = requests.post(transcription_endpoint, json=json, headers=headers)
    job_id = response.json()['id']
    return job_id


# poll
def poll(transcript_id):
    polling_endpoint = transcription_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


# getting transcription result
def get_transcription_result(audio_url):
    transcript_id = transcribe(audio_url)
    print("Transcription started ..")
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        if data['status'] == 'error':
            return data, data['Error']
        print('Audio processing ..\nwaiting 15 seconds ..')
        time.sleep(15)


# save transcript
def save_transcript(audio_url, file_name):
    data, error = get_transcription_result(audio_url)
    if data:
        text_filename = file_name + '.txt'
        with open(text_filename, 'w') as f:
            f.write(data['text'])
        print('Transcription done ')
    elif error:
        print('Error ', error)


# printing transcript
def print_transcript(file_name):
    fp = open(file_name + '.txt', "rb")
    data = fp.read()
    print("txt file saved")
    print(data)
