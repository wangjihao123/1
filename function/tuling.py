import requests
import json
import time

url = 'http://openapi.tuling123.com/openapi/api/v2'


def get_roboot_answer(info):
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": info
            },
            "selfInfo": {
                "location": {
                    "city": "泰安",
                    "province": "山东省",
                    "street": "泰山大街"
                }
            }
        },
        "userInfo": {
            "apiKey": "66e905e681374337bbbf02bbbeed3749",
            "userId": "111888"
        }
    }
    try:
        response = requests.post(url, data=json.dumps(data))
        answer = response.json()['result'][0]['values']['text']
    except Exception as e:
        print(e)
        answer = '网络异常！'
    return answer
