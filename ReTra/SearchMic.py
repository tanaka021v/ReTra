import speech_recognition as sr

def select_microphone(device_index):
    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=device_index) as source:
        print("Sprechen Sie etwas...")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language="de-DE")
        print("Erkannter Text: ", recognized_text)
    except sr.UnknownValueError:
        print("Ich habe dich nicht verstanden.")
    except sr.RequestError as e:
        print("Fehler bei der Spracherkennung: {0}".format(e))

if __name__ == "__main__":
    # Liste aller verfügbaren Mikrofone abrufen
    mic_list = sr.Microphone.list_microphone_names()

    # Drucken Sie die Namen der verfügbaren Mikrofone und ihre zugehörigen Indizes
    for i, mic_name in enumerate(mic_list):
        print(f"Index {i}: {mic_name}")

    # Wählen Sie das gewünschte Mikrofon aus, indem Sie den entsprechenden Index verwenden
    selected_microphone_index = 0  # Ersetzen Sie 0 durch den gewünschten Index des Mikrofons
    select_microphone(selected_microphone_index)
