import sounddevice as sd
import numpy as np
import threading
def start(device_name):
    # device_index = output_devices.index(device_name)
    print(f"Sound wird auf '{device_name}' abgespielt...")
    duration = 3  # In Sekunden
    sample_rate = 48000  # Beispiel: 44,1 kHz
    frequency = 440  # Beispiel: A4-Note (440 Hz)
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    audio_data = 0.1 * np.sin(2 * np.pi * frequency * t)

    # Konvertiere das Mono-Audio in Stereo
    # audio_data_stereo = np.column_stack((audio_data, audio_data))
    play_sound(device_name, audio_data, sample_rate)
    
def play_sound(device_index, audio_data, sample_rate):
    sd.play(audio_data, sample_rate,  device=device_index)
    sd.wait()
    
def list_input_devices():
    devices = sd.query_devices()
    input_devices = [device["name"] for device in devices if device["max_input_channels"] > 0]

    return input_devices

def list_output_devices():
    devices = sd.query_devices()
    output_devices = [device["name"] for device in devices if device["max_output_channels"] > 0]

    return output_devices

def select_input_devices(device_names):
    try:
        input_devices_indices = [idx for idx, device in enumerate(sd.query_devices()) if device["name"] in device_names]
        sd.default.device[0] = input_devices_indices
        print(f"Eingabegeräte auf '{device_names}' gesetzt.")
    except ValueError as e:
        print(f"Fehler beim Setzen der Eingabegeräte: {e}")

def select_output_devices(device_names):
    try:
        output_devices_indices = [idx for idx, device in enumerate(sd.query_devices()) if device["name"] in device_names]
        sd.default.device[1] = output_devices_indices
        print(f"Ausgabegeräte auf '{device_names}' gesetzt.")
    except ValueError as e:
        print(f"Fehler beim Setzen der Ausgabegeräte: {e}")

if __name__ == "__main__":
    
    input_devices = list_input_devices()
    print("Verfügbare Eingabegeräte (Mikrofone):")
    for idx, device_name in enumerate(input_devices, start=1):
        print(f"{idx}. {device_name}")

    selected_input_indices = input("Gib die Nummern der gewünschten Eingabegeräte durch Leerzeichen getrennt ein: ")
    selected_input_indices = [int(idx) - 1 for idx in selected_input_indices.split()]
    selected_input_devices = [input_devices[idx] for idx in selected_input_indices]
    print(select_input_devices)
    select_input_devices(selected_input_devices)

    output_devices = list_output_devices()
    print("Verfügbare Ausgabegeräte (Lautsprecher):")
    for idx, device_name in enumerate(output_devices, start=1):
        print(f"{idx}. {device_name}")

    selected_output_indices = input("Gib die Nummern der gewünschten Ausgabegeräte durch Leerzeichen getrennt ein: ")
    selected_output_indices = [int(idx) - 1 for idx in selected_output_indices.split()]
    selected_output_devices = [output_devices[idx] for idx in selected_output_indices]
    select_output_devices(selected_output_devices)
    print(selected_output_indices[0], selected_output_indices[1] )
    thread = threading.Thread(target= start, args  =( selected_output_indices[0] ,))
    thread2 = threading.Thread(target = start, args = (selected_output_indices[1],))
    thread.start()
    thread2.start()
    
    
    
            
