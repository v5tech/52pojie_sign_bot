# -- coding: utf-8 --

import re
from datetime import datetime, timedelta
import urllib.parse
import requests
from bs4 import BeautifulSoup
import notify

SESSION = requests.Session()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

BASE_URL = "https://www.52pojie.cn"


def sign():
    message = "签到成功"
    # url1 = f"{BASE_URL}/CSPDREL2hvbWUucGhwP21vZD10YXNrJmRvPWRyYXcmaWQ9Mg==?wzwscspd=MC4wLjAuMA=="
    url2 = f'{BASE_URL}/home.php?mod=task&do=apply&id=2&referer=%2F'
    # url3 = f'{BASE_URL}/home.php?mod=task&do=draw&id=2'

    # r = SESSION.get(url1, headers=HEADERS, allow_redirects=False)
    # r.raise_for_status()  # 判断请求状态是否正常

    r = SESSION.get(url2, headers=HEADERS, allow_redirects=False)
    r.raise_for_status()  # 判断请求状态是否正常

    # r = SESSION.get(url3, headers=HEADERS)
    # r.raise_for_status()  # 判断请求状态是否正常
    #
    # r_data = BeautifulSoup(r.text, "html.parser")
    # jx_data = r_data.find("div", id="messagetext").find("p").text
    #
    # if "您需要先登录才能继续本操作" in jx_data:
    #     message = "Cookie 失效"
    # elif "恭喜" in jx_data:
    #     message = "签到成功"
    # elif "不是进行中的任务" in jx_data:
    #     message = "今日已签到"
    # else:
    #     message = "签到失败"

    message = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S") + "\r\n" + message
    print(message)
    notify.send("52pojie签到", message)


def parse_cookie(raw_cookie):
    pattern = r"(\S+)(_saltkey|_auth)=(\S+);"
    matches = re.findall(pattern, raw_cookie)
    cookies = {}
    for match in matches:
        cookies[match[0] + match[1]] = urllib.parse.quote(match[2], safe='')
    return cookies


if __name__ == '__main__':
    try:
        input_cookie = input("请输入52pojie cookie的值：\r\n").strip()
        cookies = parse_cookie(input_cookie)
        SESSION.cookies.update(cookies)
        sign()
    except requests.exceptions.RequestException as e:
        print(e)
