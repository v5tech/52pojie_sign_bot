import requests
import os

headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}


def send(title, content):
    token = os.environ.get('PUSHPLUS_TOKEN')
    if not token:
        print('请设置 PUSHPLUS_TOKEN 环境变量')
        return
    json_data = {
        'token': f'{token}',
        'title': f'{title}',
        'content': f'{content}',
        'template': 'txt',
        'channel': 'wechat',
    }
    response = requests.post('http://www.pushplus.plus/send', headers=headers, json=json_data)
    response.raise_for_status()  # 判断请求状态是否正常
    print(response.text)


if __name__ == '__main__':
    try:
        send('标题', '内容')
    except requests.exceptions.RequestException as e:
        print(e)
