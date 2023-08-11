# ReTra
## Python Project2:  Real-Time Speech Translation for Instant Multilingual Conversations (Only works on Windows)

# How does it work:
My idea behind this is to link two headphones to my Windows laptop via Bluetooth or USB.
Each headphone is then assigned the language that the speaker also knows. Let's say _speaker A_ speaks German and _speaker B_ speaks English. When _speaker A_ speaks German, the microphone picks up what is spoken at certain intervals, converts it to text through the Speech Recognition Google API, and translates the text into English. The translated speech from German to English is then played through _speaker B's_ headphones and vice versa for _speaker B_ as well

## ReTraAlgorithm Code explained:

In this section I want to talk about the logic behind this code. I inspired the logic behind this code of the following github repository: _https://github.com/davabase/whisper_real_time/blob/master/transcribe_demo.py_ .
When speaker A talks, his talk is not recorded for the whole time until he has finished talking, i.e. an end is detected, but his speech is recorded for five seconds and converted into a text by the Speech Recognition (Google) module and this repeats in order to reach real time translation. (accuracity is not high compared to delayed recognition, because of reaching this) 

In the background (in a thread) raw audio data is recorded by the microphone. Since this audio data is one of several future audio snippets, these snippets are added to a queue. 
In the While loop, after phrase_timeout (5 seconds in my case), all previous raw audio data that are in the queue are stored in a byte sequence _last_sample_ variable. The audio data stored in _last_sample_ as binary data is stored in an object instance AudioData from the Speech Recognition module, as _audio_data_. This object now represents the audio data. This object is then converted to text, by _text = recorder.recognize_google(audio_data, language= language1)_ (line 112).
After the speech has been recognized, it is either appended to the end of the previous text or added to the list, depending on whether it occurred at phrase_timeout. (To document that spoken).

A big problem was that if nothing new is spoken, the last recognized text is always retranslated and played back repeatedly. To fix this, I had to filter the translated text so that the new recognized text differs from the last text. **Example :
text_1 = "I'm Tanaka021v and I love Python"
text_2 = "I'm Tanaka021v and I love Python, but I'm
bored" -> The aim is to filter only the new part, that would then be text_3 = ", but I'm bored".**
This _extra_text_ is then passed as a parameter into my thread, which calls the method to translate the text and then play it in the other headphone. Regarding this, one more case had to be considered, and that is the first text that is spoken and has no previous text (when the list _transcription_ has a length of zero at the beginning).
Because it has no previous "neighbor", the first text is compared to the string ''. Of course, these two have nothing in common, which is why the thread is not called, so I have to insert the else query to use the first text in the thread as a parameter in order to finally translate and play it.




