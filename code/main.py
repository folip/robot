from threading import Thread
import audio
import video
import nlp
import time

g_audio_record_start = False
g_audio_available = False
g_emotion = None
g_emotion_captured = False
g_listen_lock = False

def capture():
    global g_emotion
    global g_emotion_captured 
    g_emotion_captured = False
    for i in range(5):
        print("trying to analyze emotions.. attempt " + str(i))
        frame = C.shoot_test('o.jpg')
        e = P.emotion_dect(frame)
        if e != None:
            g_emotion = e
            g_emotion_captured = True
            return 
    print("fail to dect emotions")

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
    C = video.Camera()
    P = video.PA()        
    A = audio.Audio(600)
    A.streamStart()

    T_audio = Thread(target = listen)
    T_audio.start()

    state = 'waiting'
    while 1:
        if state == 'waiting':
            if g_audio_record_start == True:
                T_video = Thread(target = capture)
                T_video.start()
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
            if g_emotion_captured == True:
                print(g_emotion)
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