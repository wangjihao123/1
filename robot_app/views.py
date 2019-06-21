import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from function.baidu_ai import audio2text, text2audio

# Create your views here.


def home(request):
    return render(request, 'robot_app/index.html')


def upload(request):
    # print(request.POST)
    file_name = os.path.join('robot_app', 'static', 'audio_file', request.POST['name'])
    file = request.FILES['file']

    with open(file_name, 'wb') as f:
        f.write(file.read())

    text = audio2text(file_name)
    hecheng_name = os.path.join('robot_app', 'static', 'audio_file', 'hecheng' + request.POST['name'])

    if text2audio(text, hecheng_name):
        print('合成成功！')
        res_name = hecheng_name.strip('robot_app//')
    else:
        print('合成失败！')
        res_name = ''

    res_str = {
        'play_tpe': 'talk',
        'res_name': res_name,
        'content': text
    }

    return HttpResponse(json.dumps(res_str), content_type='application/json')
