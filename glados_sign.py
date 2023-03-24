# -- coding: utf-8 --

import requests
import notify
from datetime import datetime, timedelta

if __name__ == '__main__':
    cookie = input("请输入glados.network cookie的值：\r\n").strip()
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Cookie": f"{cookie}",
    }
    checkinUrl = 'https://glados.network/api/user/checkin'
    resp = requests.post(checkinUrl, data={'token': 'glados.network'}, headers=HEADERS)
    message = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") + "\r\n" + resp.json().get('message')
    print(message)
    notify.send("GLaDOS签到", message)
