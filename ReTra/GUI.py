import customtkinter as ctk
import socket
import time
import threading

import speech_recognition as sr
from datetime import datetime, timedelta
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from langid import classify
import subprocess
from gtts.lang import tts_langs
from queue import Queue
# pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez
#GUI for windows

import sounddevice as sd
import soundfile as sf

    
class Retra_GUI(ctk.CTk):
    
   
    def __init__(self):
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('green')
        self.headphone_input = None
        self.headphone_input2 = None
        self.headphone_output = None
        self.headphone_output2 = None
        self.first_language = None
        self.second_language = None


        self.window = ctk.CTk()
        self.window.geometry('1000x800')
        self.window.title('ReTra')
        self.window.resizable(False,False)
        title_label = ctk.CTkLabel(master = self.window, text = 'ReTra', font  = ('Arial', 36, 'bold'))
        title_label.pack(padx = 10, pady  = 10 )

        self.headset_frame = ctk.CTkFrame(master = self.window)
        self.headset_frame.pack(padx = 30, pady = 30, anchor = 'nw', fill = 'x')

        
        self.headseti_one = ctk.CTkButton(master = self.headset_frame, text = 'Select input1', font = ('Arial', 32, 'bold'), command = lambda:  self.select_input(0) )
        self.headseti_one.pack(padx = 10, pady = 5, side = 'left')
        self.headseti_two = ctk.CTkButton(master = self.headset_frame, text = 'Select Output1', font = ('Arial', 32, 'bold'), command = lambda: self.select_output(1) )
        self.headseti_two.pack(padx = 10, pady = 5, side = 'right')
        
        self.headseto_one = ctk.CTkButton(master = self.headset_frame, text = 'Select Output2', font = ('Arial', 32, 'bold'), command = lambda: self.select_output(0) )
        self.headseto_one.pack(padx = 10, pady = 5, side = 'left')
        self.headseto_two = ctk.CTkButton(master = self.headset_frame, text = 'Select input2', font = ('Arial', 32, 'bold'), command = lambda: self.select_input(1) )
        self.headseto_two.pack(padx = 10, pady = 5, side = 'right')

        self.language_frame = ctk.CTkFrame(master = self.window)
        self.language_frame.pack(anchor = 'nw', fill = 'x')

        self.language_one = ctk.CTkButton(master = self.language_frame, text = 'Select Language', font = ('Arial', 32, 'bold'), command = lambda: self.select_language('left') )
        self.language_one.pack(padx = 50, pady = 10, side = 'left')
        self.language_two = ctk.CTkButton(master = self.language_frame, text = 'Select Language', font = ('Arial', 32, 'bold'), command = lambda: self.select_language('right') )
        self.language_two.pack(padx = 50, pady = 10, side = 'right')

        self.translation_box = ctk.CTkTextbox(master = self.window, font = ('Arial', 18))
        self.translation_box.pack(padx = 10, pady  = 10, anchor = 'nw', side = 'left', fill = 'both' , expand = True)
        self.translation_box.insert('1.0','how are u ')
        self.translation_box.configure(state = 'disabled')
        thread = threading.Thread(target = self.start_retra)
        thread.start()

        self.window.mainloop()
        
    def start_retra(self):
        while True:
            if self.headphone_input is not None and self.headphone_input2 is not None and self.headphone_output is not None and self.headphone_output2 is not None and self.first_language is not None and self.second_language is not None:
                subprocess.Popen(['python', 'RetraAlgorithm.py', self.first_language, self.second_language, str(self.headphone_output), str(self.headphone_input2)])
                subprocess.Popen(['python', 'RetraAlgorithm.py', self.second_language, self.first_language, str(self.headphone_output2), str(self.headphone_input)])
                
                break
            time.sleep(3) 
        
            
    def list_output_devices(self):
        devices = sd.query_devices()
        output_devices = [device["name"] for device in devices if device["max_output_channels"] > 0]

        return output_devices
    
    def select_output(self, side):
        self.new_window_output = ctk.CTkToplevel(self.window)

        self.new_window_output.geometry('800x600')
        
        self.headset_frame2 = ctk.CTkFrame(self.new_window_output)
        self.headset_frame2.pack(fill = 'both', expand = True)

        self.canvas2 = ctk.CTkCanvas(self.headset_frame2)
        self.canvas2.pack(side='left', fill='both', expand=True)

        scrollbar = ctk.CTkScrollbar(self.headset_frame2, command=self.canvas2.yview)
        scrollbar.pack(side='right', fill='y')

        self.canvas2.configure(yscrollcommand= scrollbar.set)
        self.canvas2.bind('<Configure>', lambda event: self.canvas2.configure(scrollregion=self.canvas2.bbox('all')))
        
        self.scroll_frame2 = ctk.CTkFrame(self.canvas2)
        output_devices = self.list_output_devices()
    # Drucken Sie die Namen der verfügbaren Mikrofone und ihre zugehörigen Indizes
        for i, name in enumerate(output_devices):
            button = ctk.CTkButton(self.scroll_frame2, text=f'{i}: {name}', font=('Arial', 18, 'bold'), width=30, height=5, command = lambda i = i, mic_name = name,  side = side: self.enter_output(i,side, mic_name))
            button.grid(row=i, column=0)
        self.canvas2.create_window((0, 0), window=self.scroll_frame2, anchor='nw')
        self.canvas2.bind('<MouseWheel>', lambda event: self.canvas2.yview_scroll(int(-1 * (event.delta/120)), 'units'))
        
    def enter_output(self,index, side, output_name):
        if side == 0:
            self.headphone_output = index
        else:
            self.headphone_output2 = index
        self.new_window_output.destroy()

    
    def select_input(self, side):
        self.new_window_mic = ctk.CTkToplevel(self.window)

        self.new_window_mic.geometry('800x600')
        
        self.headset_frame1 = ctk.CTkFrame(self.new_window_mic)
        self.headset_frame1.pack(fill = 'both', expand = True)

        self.canvas1 = ctk.CTkCanvas(self.headset_frame1)
        self.canvas1.pack(side='left', fill='both', expand=True)

        scrollbar = ctk.CTkScrollbar(self.headset_frame1, command=self.canvas1.yview)
        scrollbar.pack(side='right', fill='y')

        self.canvas1.configure(yscrollcommand= scrollbar.set)
        self.canvas1.bind('<Configure>', lambda event: self.canvas1.configure(scrollregion=self.canvas1.bbox('all')))
        
        self.scroll_frame1 = ctk.CTkFrame(self.canvas1)
        mic_list = sr.Microphone.list_microphone_names()
    # Drucken Sie die Namen der verfügbaren Mikrofone und ihre zugehörigen Indizes
        for i, mic_name in enumerate(mic_list):
            button = ctk.CTkButton(self.scroll_frame1, text=f'{i}: {mic_name}', font=('Arial', 18, 'bold'), width=30, height=5, command = lambda i = i, side = side: self.enter_input(i, side))
            button.grid(row=i, column=0)
        self.canvas1.create_window((0, 0), window=self.scroll_frame1, anchor='nw')
        self.canvas1.bind('<MouseWheel>', lambda event: self.canvas1.yview_scroll(int(-1 * (event.delta/120)), 'units'))

    def enter_input(self, i, side1):
        if side1 == 0:
            self.headphone_input = i
            
        else:
            self.headphone_input2 = i
        self.new_window_mic.destroy()
        
        
    def select_language(self, side):
        self.new_window_lang = ctk.CTkToplevel(self.window)

        self.new_window_lang.geometry('300x600')
        
        self.network_frame = ctk.CTkFrame(self.new_window_lang)
        self.network_frame.pack(fill = 'both', expand = True)

        self.canvas = ctk.CTkCanvas(self.network_frame)
        self.canvas.pack(side='left', fill='both', expand=True)

        scrollbar = ctk.CTkScrollbar(self.network_frame, command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        
        self.scroll_frame = ctk.CTkFrame(self.canvas)
        i = 0
        for key, value in tts_langs().items():
            button = ctk.CTkButton(self.scroll_frame, text=f'{value}', font=('Arial', 18, 'bold'), width=30, height=5, command=lambda key=key, value = value, side = side: self.enter_language(key, value, side))
            button.grid(row=i, column=0)
            i += 1

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')
        self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(-1 * (event.delta/120)), 'units'))

    def enter_language(self, key,value, side1):
        if side1 == 'left':
            self.first_language = key
            self.language_one.destroy()
            self.language_one = ctk.CTkButton(master = self.language_frame, text = f'{value}', font = ('Arial', 32, 'bold'), command = lambda: self.select_language('left') )
            self.language_one.pack(padx = 50, pady = 10, side = 'left')

        else:
            self.second_language = key
            self.language_two.destroy()
            self.language_two = ctk.CTkButton(master = self.language_frame, text = f'{value}', font = ('Arial', 32, 'bold'), command = lambda: self.select_language('right'))
            self.language_two.pack(padx = 50, pady = 10, side = 'right')
        self.new_window_lang.destroy() 
            
        
            
                
            
if __name__ == '__main__':
    retra = Retra_GUI()
