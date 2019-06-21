import os
from aip import AipSpeech

APP_ID = '16574945'
API_KEY = 'vOCGnszOkAzSrPa9iMkxlyIS'
SECRET_KEY = 'LFGP5AmRQyCDDO1A8pMoZUwlqtHb8r0a'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 角色参数
role_param = {
        'vol': 5,
        'per': '4',
        'pit': '5'
    }


def text2audio(worlds, role_param, out_putfile, lang='zh'):
    """
    :param worlds: 待合成文本信息
    :param role_param: 角色参数
    :param out_putfile: 输出文件路径
    :return: ok，失败返回None
    """
    result = client.synthesis(worlds, lang, 1, role_param)
    if not isinstance(result, dict):
        with open(out_putfile, 'wb') as f:
            f.write(result)
        return 'ok'


def audio2text(file_name):
    """
    :param file_name: 待识别音频文件
    :return: 返回识别结果，识别失败返回None
    """
    output_file = anything2pcm(file_name)
    result = client.asr(get_file_content(output_file), 'pcm', 16000, {
        'dev_pid': 1536,
    })

    if result['err_no'] == 0:
        print(result['result'][0])
        return result['result'][0]
    else:
        print('识别失败！')


def anything2pcm(input_file):
    """将一切格式的音频转为 pcm 格式，需将ffmpeg 添加到环境变量"""
    # input_file = os.path.join(os.getcwd(), input_file)
    output_file = input_file.rsplit('.', 1)[0] + '.pcm'
    cmd = 'ffmpeg -y  -i {}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {}'.format(input_file, output_file)
    print(os.popen(cmd).read())
    # 返回pcm文件路径
    return output_file


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    # 测试语音合成
    file_name = 'hello.mp3'
    # if text2audio('你好百度', role_param, file_name, lang='zh'):
    #     print('合成成功')
    # else:
    #     exit('合成失败')

    # # 测试语音识别
    print(audio2text(file_name))

