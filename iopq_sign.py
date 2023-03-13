# -- coding: utf-8 --

import re
import urllib.parse
import requests
from pyquery import PyQuery as pq
import notify
from datetime import datetime, timedelta

SESSION = requests.Session()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

BASE_URL = "https://www.iopq.net"


def parse_cookie(raw_cookie):
    pattern = r"(\S+)(_sid|_saltkey|_auth)=(\S+);"
    matches = re.findall(pattern, raw_cookie)
    cookies = {}
    for match in matches:
        cookies[match[0] + match[1]] = urllib.parse.quote(match[2], safe='')
    return cookies


def sign():
    response = SESSION.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()  # 判断请求状态是否正常
    response.encoding = 'gbk'
    doc = pq(response.text)
    message = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") + "\r\n" + doc('#extcreditmenu').text() + "\r\n" + doc('#g_upmine').text()
    print(message)
    notify.send("iopq签到", message)


if __name__ == '__main__':
    try:
        input_cookie = input("请输入iopq.net cookie的值：\r\n").strip()
        cookies = parse_cookie(input_cookie)
        SESSION.cookies.update(cookies)
        sign()
    except requests.exceptions.RequestException as e:
        print(e)
