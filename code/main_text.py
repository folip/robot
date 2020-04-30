from threading import Thread
import audio
import nlp
import time

g_audio_record_start = False
g_audio_available = False
g_listen_lock = False

def listen():
    global g_audio_record_start
    global g_audio_available
    while 1:
        if A.state == 'silent' and g_listen_lock == False:
            A.waiting()
            g_audio_record_start = True
        elif A.state == 'recording' and g_listen_lock == False:
            A.record()
            g_audio_record_start = False
            g_audio_available = True

if __name__ == "__main__":
    A = audio.Audio()
    A.streamStart()

    T_audio = Thread(target = listen)
    T_audio.start()

    state = 'waiting'
    while 1:
        if state == 'waiting':
            if g_audio_record_start == True:
                state = 'recording'
                print("state chanegd to recording")
        
        if state == 'recording':
            if g_audio_available == True:
                g_audio_available = False
                print("start stt...")
                g_listen_lock = True
                text = "你好"
                text = nlp.sound2text(A.in_path)
                time.sleep(0.4)
                print("stt done. state changed to processing")
                state = 'processing'
        
        if state == 'processing':
            text = text
            if text == None:
                state = 'waiting'
                print("state return to waiting")
                g_listen_lock = False 
            
            re_text = nlp.tuling(text)
            state = 'reply'
        
        if state == 'reply':
            nlp.text2sound(re_text)
            A.playWav()
            state = 'waiting'
            g_listen_lock = False
            print("back to waiting")    