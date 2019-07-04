import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from function.baidu_ai import audio2text, text2audio
from function.tuling import get_roboot_answer
from function.gensim_lsi import get_high_sim
from function.database import read_answer
from selenium import webdriver
from function.come import *
import time
import os
import win32api
import win32con
from selenium.webdriver.common.keys import Keys
# Create your views here.

con={}
def home(request):
    return render(request, 'robot_app/index.html',{'历史记录':con})


def upload(request):
    # print(request.POST)
    file_name = os.path.join('robot_app', 'static', 'audio_file', request.POST['name'])
    file = request.FILES['file']

    with open(file_name, 'wb') as f:
        f.write(file.read())
    text = audio2text(file_name)
    if text[0:2] == '搜索' or text[0:2] == '发送' or text[0:2] == '播放':
        index = get_high_sim(text[0:2])
    else:
        index = get_high_sim(text)
    if index is not None:
        answer = read_answer(index)
        if index == 4:
            os.popen('notepad')
        if index == 3:
            os.popen('G:\QQ\Bin\QQScLauncher.exe')
            time.sleep(5)
            win32api.keybd_event(13, 0, 0, 0)  # enter键位码是86
            win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
        if index == 5:
            driver = webdriver.Chrome()  # 利用浏览器
            driver.get("http://www.baidu.com")  # 打开get到的网址
            time.sleep(3)  # t停顿3秒，即3秒内一直在这个界面
            # print("网站的名称：",driver.title)  # 获取网站名称并输出     #打开keyword.txt文件，并一行行读取数据：keyword.txt中可以存放任意关键字，比如：selenium python 赵丽颖(ps:一个关键字占一行）
            driver.find_element('id', 'kw').send_keys(text[2:])  # 通过输入框的id为kw,定位到输入框，输入”selenium”
            driver.find_element('id', 'su').click()  # 通过搜索按钮的id为su定位到搜索按钮，点击按钮
            # time.sleep(5)  # 停顿5秒
        if index == 6:
            picture_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            directory_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            print(picture_time)
            print(directory_time)
            # 打印文件目录
            print(os.getcwd())
            # 获取到当前文件的目录，并检查是否有 directory_time 文件夹，如果不存在则自动新建 directory_time 文件
            try:
                File_Path = os.getcwd() + '\\' + directory_time + '\\'
                if not os.path.exists(File_Path):
                    os.makedirs(File_Path)
                    print("目录新建成功：%s" % File_Path)
                else:
                    print("目录已存在！！！")
            except BaseException as msg:
                print("新建目录失败：%s" % msg)
            driver = webdriver.Chrome()
            driver.get("https://baidu.com/")
            try:
                url = driver.save_screenshot('.\\' + directory_time + '\\' + picture_time + '.png')
                print("%s ：截图成功！！！" % url)
            except BaseException as pic_msg:
                print("截图失败：%s" % pic_msg)
            time.sleep(2)
            driver.quit()
        if index == 7:
            os.popen('G:\CloudMusic\cloudmusic.exe')
            time.sleep(8)
            start()
        if index == 8:
            x=text.index('给')
            int(x)
            to_who=text[x+1:]
            msg=text[2:x]
            qq(to_who)
            send_qq(to_who,msg)
        if index == 9:
            stop()
        if index == 10:
            last()
        if index == 11:
            next()
        if index == 12:
            turn_up()
        if index == 13:
            turn_down()
        if index == 14:
            love()
        if index == 15:
            show_words()
        if index == 16:
            shoutsown_words()
        if index == 17:
            os.system(r'taskkill /f /t /im cloudmusic.exe')
        if index == 18:
            start()
        if index == 19:
            music=text[2:]
            find_music()
            time.sleep(1)
            play_music(music)
    else:
        answer = get_roboot_answer(text)
    con[text]=answer
    hecheng_name = os.path.join('robot_app', 'static', 'audio_file', 'hecheng' + request.POST['name'])

    if text2audio(answer, hecheng_name):
        print('合成成功！')
        res_name = hecheng_name.strip('robot_app//')
    else:
        print('合成失败！')
        res_name = ''

    res_str = {
        'play_tpe': 'talk',
        'res_name': res_name,
        'content': answer
    }

    return HttpResponse(json.dumps(res_str), content_type='application/json')
