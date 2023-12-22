# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/22 17:04
# @Author   : Scipline
# @File     : merlin-unlimited.py
# Description: This script is ...
import json
import asyncio
import aiohttp
import time
import random
import string
from pathlib import Path

get_access_token_URL = "https://securetoken.googleapis.com/v1/token?key=AIzaSyAvCgtQ4XbmlQGIynDT-v_M8eLaXrKmtiM"
get_chat_token_URL = "https://merlin-uam-yak3s7dv3a-ue.a.run.app/session/get"
get_account_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyAvCgtQ4XbmlQGIynDT-v_M8eLaXrKmtiM"

access_token_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}
chat_token_HEADERS = {
    'authority': 'merlin-uam-yak3s7dv3a-ue.a.run.app',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://app.getmerlin.in',
    'pragma': 'no-cache',
    'referer': 'https://app.getmerlin.in/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'content-type': 'application/json'
}
get_account_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}
account_to_delete = []


def get_local_data():
    path = r"E:\DevProject\JsProject\ChromeExtension\MerlinFree"
    folder_path = Path(path)
    refresh_token_list = []

    # 创建Data目录和refresh_token.txt文件
    data_dir = Path("../Data")
    data_dir.mkdir(exist_ok=True)
    refresh_token_file = data_dir / "refresh_token.txt"

    for json_file in folder_path.rglob('indexeddb*.json'):
        with open(json_file, 'r', encoding='UTF-8') as f:
            json_content = json.load(f)
            if "value" in json_content and "stsTokenManager" in json_content["value"] and "refreshToken" in \
                    json_content["value"]["stsTokenManager"]:
                refresh_token = json_content["value"]["stsTokenManager"]["refreshToken"]
                refresh_token_list.append(refresh_token)

                # 将refresh_token写入文件
                with refresh_token_file.open("a", encoding='UTF-8') as rf:
                    rf.write(refresh_token + "\n")

    print(f"读取到 {len(refresh_token_list)} 个账号。")
    return refresh_token_list


async def get_access_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(get_access_token_URL, headers=access_token_HEADERS, data=data) as resp:
                response = await resp.json()
        if "USER_NOT_FOUND" in str(response) or "USER_DISABLED" in str(response):
            account_to_delete.append(refresh_token)
            raise Exception("已封号")
        return response.get("access_token", None)
    except Exception as e:
        print(e)
        return None


async def write_access_tokens_to_file(refresh_tokens):
    access_token_file = Path("../Data/access_token.txt")
    with access_token_file.open("w", encoding='UTF-8') as af:
        af.write("")
    # async with aiohttp.ClientSession() as session:
    tasks = [get_access_token(token) for token in refresh_tokens]
    results = await asyncio.gather(*tasks)
    with access_token_file.open("a", encoding='UTF-8') as af:
        for access_token in results:
            if access_token:
                af.write(access_token + "\n")
    with refresh_token_file.open("a", encoding='UTF-8') as rf:
        for refresh_token in refresh_tokens:
            if refresh_token not in account_to_delete:
                rf.write(refresh_token + "\n")


async def get_chat_token(Idtoken):
    payload = json.dumps({
        "token": Idtoken
    })

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(get_chat_token_URL, headers=chat_token_HEADERS, data=payload) as resp:
                response_dict = await resp.json()
        access_token = response_dict.get('data', {}).get('accessToken', None)
        if not access_token:
            raise Exception(f"没有找到access_token:{response_dict}")

        return access_token
    except Exception as e:
        print(e)
        return None


async def write_chat_tokens_to_file(access_tokens):
    chat_token_file = Path("../Data/chat_token.txt")

    # async with aiohttp.ClientSession() as session:
    tasks = [get_chat_token(token) for token in access_tokens]
    results = await asyncio.gather(*tasks)
    with chat_token_file.open("a", encoding='UTF-8') as af:
        for chat_token in results:
            if chat_token:  # Skip if chat_token is False or None
                af.write(chat_token + "\n")


async def get_account(email, passwd):
    payload = json.dumps({
        "returnSecureToken": True,
        "email": email,
        "password": passwd,
        "clientType": "CLIENT_TYPE_WEB"
    })
    try:
        async with (aiohttp.ClientSession() as session):
            async with session.post(get_account_URL, headers=get_account_HEADERS, data=payload,
                                    verify_ssl=False) as resp:
                response_dict = await resp.json()
                access_token = response_dict.get('idToken', None)
                refresh_token = response_dict.get('refreshToken', None)
        if not access_token or not refresh_token:
            raise Exception(f"注册失败:{response_dict}")
        return access_token, refresh_token
    except Exception as e:
        print(e)
        return None, None


def generate_random_emails(email_count):
    emails = []
    while len(emails) < email_count:
        letters = string.ascii_lowercase
        name_length = random.randint(5, 10)
        name = ''.join(random.choice(letters) for _ in range(name_length))
        domain = "gmail.com"
        email = name + "@" + domain
        if email not in emails:
            emails.append(email)
    return emails


async def write_tokens_to_file(email_count, passwd):
    access_token_file = Path("../Data/access_token.txt")
    refresh_token_file = Path("../Data/refresh_token.txt")
    # access_token有时效性，不需要保留旧值
    with access_token_file.open("w", encoding='UTF-8') as af:
        af.write("")
    emails = generate_random_emails(email_count)

    # async with aiohttp.ClientSession() as session:
    tasks = [get_account(email, passwd) for email in emails]
    results = await asyncio.gather(*tasks)
    for result in results:
        access_token, refresh_token = result
        if access_token:
            with access_token_file.open("a", encoding='UTF-8') as af:
                af.write(access_token + "\n")
        if refresh_token:
            with refresh_token_file.open("a", encoding='UTF-8') as af:
                af.write(refresh_token + "\n")


if __name__ == '__main__':
    opcode = int(input("请输入操作码："))
    start_time = time.time()
    if opcode == 1:
        refresh_token_list = get_local_data()
    elif opcode == 2:
        print("refresh_token --> access_token")
        refresh_token_file = Path("../Data/refresh_token.txt")
        with refresh_token_file.open("r", encoding='UTF-8') as rf:
            refresh_tokens = rf.read().splitlines()
        # Run the async tasks
        asyncio.run(write_access_tokens_to_file(refresh_tokens))
    elif opcode == 3:
        print("access_token --> chat_token")
        access_token_file = Path("../Data/access_token.txt")
        with access_token_file.open("r", encoding='UTF-8') as af:
            access_tokens = af.read().splitlines()
        # Run the async tasks
        asyncio.run(write_chat_tokens_to_file(access_tokens))
    elif opcode == 4:
        email_count = int(input("请输入邮箱数量："))
        passwd = "123456789"
        asyncio.run(write_tokens_to_file(email_count, passwd))
    end_time = time.time()
    print(f"运行时间：{round(end_time - start_time, 3)}s")
