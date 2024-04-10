# ReTra: Real-Time Speech Translation for Instant Multilingual Conversations (Windows Only)
## How It Works:
The concept behind ReTra is to enable real-time multilingual conversations by connecting two headphones to a Windows laptop via Bluetooth or USB. Each headphone is assigned the language known by the respective speaker. For instance, if Speaker A speaks German and Speaker B speaks English, ReTra translates the spoken language from one speaker to the other. Here's how it operates:

-When Speaker A speaks, the microphone captures the speech at intervals, typically five seconds.
-The captured speech is converted to text using the Speech Recognition Google API.
-The text is then translated into the language understood by Speaker B.
-The translated speech is played through Speaker B's headphones, and vice versa for Speaker B.
## ReTraAlgorithm Code Explanation:
In this section, I'll discuss the logic behind the ReTraAlgorithm code, inspired by a GitHub repository (https://github.com/davabase/whisper_real_time/blob/master/transcribe_demo.py).

-Raw audio data is continuously recorded in the background by the microphone and stored in a queue.
-At set intervals (e.g., every five seconds), the previous audio snippets in the queue are processed.
-The audio data is converted to text using the Speech Recognition module.
-The recognized speech is appended to the previous text or added to the list, depending on whether it occurred at the interval.
-To prevent repeated translation of unchanged text, a filtering mechanism is implemented. Only the new part of the recognized text is considered for translation and playback.
-For instance, if the previous text was "I'm Tanaka021v and I love Python," and the new text is "I'm Tanaka021v and I love Python, but I'm bored," only the new part ", but I'm bored" is translated and played.
-Special consideration is given to the first text spoken, which has no previous text for comparison. In this case, the entire text is translated and played without filtering.
Overall, the ReTraAlgorithm ensures real-time translation and playback of speech for seamless multilingual communication.
