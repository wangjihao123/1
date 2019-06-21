import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from function.baidu_ai import audio2text, text2audio

# Create your views here.


def home(request):
    return render(request, 'robot_app/index.html')


def upload(request):
    # 拼接保存MP3文件名
    file_name = os.path.join('robot_app', 'static', 'audio_file', request.POST['name'])
    file = request.FILES['file']
    # 保存MP3
    with open(file_name, 'wb') as f:
        f.write(file.read())

    # 语音识别
    text = audio2text(file_name)

    # 拼接语音合成文件名（当前app下的static/audio_file目录下）
    hecheng_name = os.path.join('robot_app', 'static', 'audio_file', 'hecheng' + request.POST['name'])

    # 调用语音合成，并判断是否合成功
    if text2audio(text, hecheng_name):
        print('合成成功！')
        # 返回合成文件路径（去掉app名）
        res_name = hecheng_name.strip('robot_app//')
    else:
        print('合成失败！')
        res_name = ''

    res_str = {
        'play_tpe': 'talk',
        'res_name': res_name,    # 播放的合成文件路径
        'content': text          # 额外显示的信息
    }
    # 返回json 数据
    return HttpResponse(json.dumps(res_str), content_type='application/json')
