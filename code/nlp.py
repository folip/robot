# coding=utf-8
import requests
import json
from aip import AipSpeech
import time 
import os

APP_ID = '17735049'
API_KEY = '9DSRkpblEAlf3LNoNV8arKAo'
SECRET_KEY = 'Gj65U9MZoQczYKoygcesv40ZLQpWO6qn'
# 初始化
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
 
def tuling(text="儿子"):
    # 与图灵机器人对话
    tuling_url = "http://www.tuling123.com/openapi/api"
    tuling_date = {
        'key': 'cff00af75c73487ca6efff0ed5569791',
        'info': text
    }  
    print(text)
    r = requests.post(tuling_url, data=tuling_date)
    print(json.loads(r.text)["text"])
    return json.loads(r.text)["text"]
	
def text2sound(words='你好'):
    # 语音合成函数，传入欲合成的内容，返回成功与否，若成功默认将文件保存为'test.wav'
    result = client.synthesis(words, 'zh', 1, {
        'vol': 5, 'aue': 6, 'per': 4
    })  # 具体的参数设置请参考官方文档
 
    if not isinstance(result, dict):
        with open('audio/reply.wav', 'wb') as f:
            f.write(result)
            #play('test.wav')
        return True
    else:
        return False
 
def sound2text(file_path='./test.wav'):
    # 语音识别函数，传入文件名（默认为'test.wav'），返回识别结果或错误代码
    with open(file_path, 'rb') as fp:
        recog = client.asr(fp.read(), 'wav', 16000, {'dev_pid': 1536})
        try:
            print(recog['result'][0])
        #if recog['err_no'] == 0:
         #   return recog['err_no']
            return recog['result'][0]
        except:
            print("sound2text failed")
            return None


		

