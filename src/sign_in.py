'''
@Author       : Scipline
@Since        : 2023-12-22 16:17:44
@LastEditor   : Scipline
@LastEditTime : 2023-12-22 17:25:52
@FileName     : sign_in.py
@Description  : 账号密码登录，获取access_token和refresh_token
@GitHub       : github.com/Scipline
'''
import requests
import json
import asyncio
from pathlib import Path
import aiohttp
url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyAvCgtQ4XbmlQGIynDT-v_M8eLaXrKmtiM"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'x-firebase-gmpid': '1:312050491589:web:a6323098a147f8bd98d0ac',
    'dnt': '1',
    'x-client-version': 'Chrome/JsCore/9.23.0/FirebaseCore-web',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-gpc': '1',
    'accept-language': 'zh-CN,zh;q=0.6',
    'origin': 'https://app.getmerlin.in',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'Content-Type': 'application/json'
}


async def sign_in(user):
    uemail, passwd = user.split(":")
    data = json.dumps({
        "returnSecureToken": True,
        "email": uemail.strip(),
        "password": passwd.strip(),
        "clientType": "CLIENT_TYPE_WEB"
    })
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=headers, data=data) as resp:
                response = await resp.json()
        if "refreshToken" in str(response) and "idToken" in str(response):
            return response["idToken"], response["refreshToken"]
        raise Exception("登录失败")
    except Exception as e:
        print(e)
        return None, None


async def write_access_tokens_to_file():
    data_file = Path("../Data/result.txt")
    access_token_file = Path("../Data/access.txt")
    refresh_token_file = Path("../Data/refresh.txt")
    """
    result sample：
    aaaa@gmail.com:123456789
    bbbb@gmail.com:123456789
    """
    with data_file.open("r", encoding='UTF-8') as af:
        # async with aiohttp.ClientSession() as session:
        tasks = [sign_in(user)
                 for user in af.readlines()]
        results = await asyncio.gather(*tasks)
    for result in results:
        if result is not None:
            access_token, refresh_token = result
            with access_token_file.open("a", encoding='UTF-8') as af:
                af.write(access_token + "\n")
            with refresh_token_file.open("a", encoding='UTF-8') as rf:
                rf.write(refresh_token + "\n")

if __name__ == "__main__":
    asyncio.run(write_access_tokens_to_file())
