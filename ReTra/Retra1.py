
import os
import speech_recognition as sr
import threading
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
# from sys import platform
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import nltk
from langid import classify

import sounddevice as sd
import soundfile as sf

import sys

def firsttranscriber(language1, language2, device_index, microphone_index):
    
    phrase_time = None
  
    last_sample = bytes()
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
    
    recorder = sr.Recognizer()
    recorder.energy_threshold = 1000
    
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False
    
    source = sr.Microphone(sample_rate=16000, device_index=microphone_index)
    translator = Translator()
    record_timeout = 5
    phrase_timeout = 5

    transcription = ['']
    string1 = ''
    index1 = 0
    thread_queue = Queue()
    text = ''
    extra_text = ''
    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio:sr.AudioData) -> None:
        """
        Threaded callback function to recieve audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    def translate_and_play(text, index1, device_index):
    
        tokens = nltk.word_tokenize(text)
        langid_result = classify(' '.join(tokens))
        if (langid_result[0] == language1): 
            destination = language2
            if text:
                translation = translator.translate(text, dest=destination)
                audiofile = gTTS(translation.text, lang=destination)
                filename = (f'translation_text{index1}.mp3')
                audiofile.save(filename)
                # audio = AudioSegment.from_file(filename, format='mp3')
                wav = AudioSegment.from_mp3(filename)
                wav.export((f'translation_text{index1}.wav'), format = 'wav')
                data, fs = sf.read((f'translation_text{index1}.wav'), dtype='float32')
                sd.play(data, fs, device = device_index)
                sd.wait()
                # play(audio)
                os.remove(filename)
                os.remove((f'translation_text{index1}.wav'))
        
    def start_thread():
        while not thread_queue.empty():
            thread1 = thread_queue.get()
            thread1.start()
            thread1.join()
    print(f"Model loaded: Language chosen are: {sys.argv[1]} -> {sys.argv[2]}\n")
    while True: 
        try:
            now = datetime.utcnow()

            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True

                phrase_time = now

                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data     
     
                try:
                    audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                    text = recorder.recognize_google(audio_data, language = language1)
                    # second_text = recorder.recognize_google(audio_data, language='en')
                    
                except sr.UnknownValueError:
                    print('UnknownError')
                    continue
                except sr.RequestError as e:
                    print("Fehler bei der Anfrage an die Spracherkennungsdienste:", str(e))
                    break
                if phrase_complete:
                    transcription.append(text)  
                else:
                    transcription[-1] = text
                os.system('cls' if os.name=='nt' else 'clear')
                for line in transcription:
                    print(line)
                    # print(translator.translate(line, dest = 'en').text)
                
                print('...', end='', flush=True)
                
                common_prefix_len = 0
                for word1, word2 in zip(text.strip(), string1.strip()):
                    if word1 == word2:
                        common_prefix_len += 1
                    else:
                        break
                if common_prefix_len > 0:
                    extra_text = ''.join(text[common_prefix_len:])
                else:
                    extra_text = ''
                string1  = text 
                if extra_text: 
                    thread = threading.Thread(target = translate_and_play, args = (extra_text, index1, device_index))
                    index1 += 1
                    thread_queue.put(thread)
                else:
                    thread = threading.Thread(target = translate_and_play, args = (text, index1, device_index))
                    index1 += 1
                    thread_queue.put(thread)
                start_thread()   
                sleep(0.25)
        except KeyboardInterrupt:
            print('Keyboard Interruption')
            break

if __name__ == "__main__":
    firsttranscriber(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))        


