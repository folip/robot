import pyaudio
import wave
from sys import byteorder
from array import array
from struct import pack

class Audio:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.MAXIMUM = 16384
        self.audioCreate()
        self.state = 'silent'
        self.r = None

    def audioCreate(self):
        self.p = pyaudio.PyAudio()

    def audioRelease(self):
        self.p.terminate()
    
    def streamStart(self):
        self.stream = self.p.open(
            format = self.FORMAT,
            channels = self.CHANNELS,
            rate = self.RATE,
            input = True,
            frames_per_buffer = self.CHUNK
        )
        self.state = 'silent'
        return self.stream

    def streamClose(self):
        self.stream.stop_stream()
        self.stream.close()
    
    def audioReadChunks(self):
        data = self.stream.read(self.CHUNK)
        snd_data = array('h',data)
        if byteorder == 'big':
            snd_data.byteswap()
        return snd_data

    def playData(self,data):
        while len(data) > 0:
            chunk = data[:self.CHUNK]
            data = data[self.CHUNK:]
            self.stream.write(chunk)

class streamTransfer:
    def __init__(self,file_path,stream):
        self.state = 'init'
        self.closed = False
        self.D = None
       
    def bind(self,D):
        self.D = D
        self.logger = D.logger 

    def info(self,mes):
        mes = '[[file sender]]' + str(mes) 
        info(mes)
        if self.logger != None:
            self.logger['log'] += mes + '\n'
            self.logger['signal'].emit()

    def _write(self,data):
        self.sock.sendall(data)

    def _read(self):
        return self.sock.recv(4096)

    def bind_sock(self,sock):
        self.sock = sock 

    def hello(self):
        dic = {
            'type': 'File Transfer',
            'file_name': self.file_name,
            'file_size': self.file_size
        }
        mes = encode(dic)
        self._write(mes)
        

    def wait_for_ack(self):
        self.info('waiting for hello reply')        
        
        self.sock.setblocking(True)
        ack = self._read()
        self.info('ack: ' + str(ack))
        self.sock.setblocking(False)

        self.wait_for_ack()
        
        if ack == b'ready':
            self.info('Receiver ready.')
            self.state = 'sending'

    def send_chunk(self):
        #read chunk from file
        chunk = self.f.read(self.chunk_size)
        chunk_size = len(chunk)
        self.sent_byte += chunk_size

        if chunk_size == 0 or self.sent_byte == self.file_size:
            self.display_progress()
            self.info('state changed to sent.')
            self.state = 'sent'
        #send the chunk
        self._write(chunk)
        self.display_progress()
    
    def display_progress(self):
        if self.sent_byte > self.next_logging:
            self.next_logging += self.logging_size
            self.info(str(self.sent_byte) + ' sent')

        if self.sent_byte == self.file_size:
            self.info(str(self.sent_byte) + ' sent')
            self.info('(All bytes sent).')
    
    def close(self):
        self.sock.close()
        self.f.close()
        self.info('File and sock closed. Mission compelate.')
        self.closed = True

    def write(self):
        # self.info('write chance')
        if self.state == 'init':
            try:
                self.hello()
                self.info('hello. waiting for ack.')
                self.state = 'waiting'
            except:
                self.info('hello not sent.')

        if self.state == 'sending':
            self.send_chunk()
    
    def read(self):
        # self.info('read chance.')
        res = self._read()
        self.info('reply received: ' + str(res))
        
        if self.state == 'waiting':
            if res == b'ready':
                self.info('Receiver ready')
                self.state = 'sending'

        elif self.state == 'sent':
            if res == b'all received':
                self.close()
