# -- coding: utf-8 --

import requests
import json
import sys
import notify


def aliyundrive_sign(refresh_token):
    message = ""
    update_token_url = "https://auth.aliyundrive.com/v2/account/token"
    signin_url = "https://member.aliyundrive.com/v1/activity/sign_in_list"

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36',
    }
    data = json.dumps({
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    })
    req = requests.Session()
    resp = req.post(update_token_url, data=data, headers=headers)
    if resp.status_code == 200:
        rdata = resp.text
        access_token = json.loads(rdata)['access_token']
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/109.0.0.0 Safari/537.36',
            'Authorization': 'Bearer ' + access_token
        }
        resp = req.post(signin_url, data=data, headers=headers)
        result = json.loads(resp.text)['success']
        if result:
            message += f"阿里云盘签到成功！\n"
        else:
            message += f"阿里云盘签到失败！\n"
    else:
        message += f"阿里云盘签到失败：{json.loads(resp.text)['message']}\n"
    print(message)
    notify.send("阿里云盘签到", message)


if __name__ == '__main__':
    # 多个 refresh_token 使用逗号分隔
    refresh_token = input("请输入refresh_token：\n")
    if not refresh_token:
        print("refresh_token为空。")
        sys.exit()
    for token in refresh_token.split(","):
        aliyundrive_sign(token)
