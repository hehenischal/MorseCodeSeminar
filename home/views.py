from django.shortcuts import render
import serial
import time
from django.contrib import messages
from threading import Lock

# Define a lock for thread-safe flag management
lock = Lock()
processing_request = False

def text_to_custom_morse(sentence):
    morse_code_dict = {
        'A': '12', 'B': '2111', 'C': '2121', 'D': '211', 'E': '1', 'F': '1121', 'G': '221',
        'H': '1111', 'I': '11', 'J': '1222', 'K': '212', 'L': '1211', 'M': '22', 'N': '21',
        'O': '222', 'P': '1221', 'Q': '2212', 'R': '121', 'S': '111', 'T': '2', 'U': '112',
        'V': '1112', 'W': '122', 'X': '2112', 'Y': '2122', 'Z': '2211',
        '0': '22222', '1': '12222', '2': '11222', '3': '11122', '4': '11112', '5': '11111',
        '6': '21111', '7': '22111', '8': '22211', '9': '22221',
        ',': '221122', '.': '121212', '?': '112211', "'": '122221', '!': '212122', '/': '21121',
        '(': '21212', ')': '212122', '&': '12111', ':': '222111', ';': '212121', '=': '21112',
        '+': '12121', '-': '211112', '_': '112121', '"': '121211', '$': '1112112', '@': '122121',
        ' ': '0'  
    }
    sentence = sentence.upper()
    custom_morse_sentence = ' '.join(morse_code_dict.get(char, '') for char in sentence)
    return custom_morse_sentence

def send_to_arduino(data, port='com6', baudrate=9600):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        time.sleep(2)
        ser.write(data.encode(encoding='utf-8'))
        ser.close()

def index(request):
    global processing_request
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text != '':
            custom_morse_text = text_to_custom_morse(text)
            with lock:
                if processing_request:
                    messages.error(request, f'Arduino is processing another request, please try again later! The Morse version of {text} is {custom_morse_text}')
                    return render(request, 'home/index.html')

                processing_request = True

            try:
                send_to_arduino(custom_morse_text)
                messages.success(request, f'{text} has been sent successfully! The Morse version of {text} is {custom_morse_text}')
            except Exception as e:
                messages.error(request, f'Error sending to Arduino: {str(e)}. The Morse version of {text} is {custom_morse_text}')
            finally:
                with lock:
                    processing_request = False

            print("Printing", text)
        return render(request, 'home/index.html')
    return render(request, 'home/index.html')
