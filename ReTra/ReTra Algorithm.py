import subprocess
def start_RETRA():
    language1 = 'en'
    language2 = 'de'
    input1 = '1'     #Hyper Virtual Mic
    input2 = '3'     #Freedoom
    output1 = '12'   #Hyper Virtual Headphone
    output2 = '14'   #Freedom Headphone
    
    subprocess.Popen(['python', 'Retra1.py', language1, language2, output2, input1 ])
    subprocess.Popen(['python', 'Retra1.py', language2, language1, output1, input2 ])

if __name__ == '__main__':
    start_RETRA()