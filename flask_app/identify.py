import pyaudio
import wave
import requests
import json
import os

def record_audio(filename, duration=10, sample_rate=44100, channels=1, chunk=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Recording...")
    frames = []
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def identify_song(filename):
    data = {
        'api_token': '8b94ea35c455d49209f97c4883520ec4',
        'return': 'apple_music,spotify',
    }   
    
    files = {
        'file': open(filename, 'rb')
    }
    
    response = requests.post('https://api.audd.io/', data=data, files=files)
    result = json.loads(response.text)
    
    return result

def detection():
    audio_file = 'recorded_audio.wav'

    # Record audio
    record_audio(audio_file)

    # Identify song
    result = identify_song(audio_file)
    
    # Clean up the audio file
    os.remove(audio_file)

    # Process and display results
    if result['status'] == 'success':
        if result['result'] is None:
            print("No song identified.")
            return [{'song': 'No song identified', 'artist': 'No artist identified'}]
        else:
            print(result)
            print(f"Song identified: {result['result']['title']} by {result['result']['artist']}")
            return [{'song': result['result']['title'], 'artist': result['result']['artist']}]
    else:
        print("Error identifying song:", result['error']['error_message'])
        return [{'song': 'Error identifying song', 'artist': 'Error identifying artist'}]



if __name__ == "__main__":
    detection()