# 一键删除Merlin插件聊天历史记录
import requests
import json
import sys
def get_Idtoken(refreshToken):
    url = "https://securetoken.googleapis.com/v1/token?key=AIzaSyAvCgtQ4XbmlQGIynDT-v_M8eLaXrKmtiM"

    payload=f'grant_type=refresh_token&refresh_token={refreshToken}'
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
       'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    Idtoken = response_dict.get('access_token',None)
    if not Idtoken:
        print("获取Idtoken失败，refreshToken有误")
        sys.exit()
    return Idtoken
def get_chat_token(Idtoken):
    url = "https://merlin-uam-yak3s7dv3a-ue.a.run.app/session/get"

    payload = json.dumps({
       "token": Idtoken
    })
    headers = {
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

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    access_token = response_dict.get('data',{}).get('accessToken',None)
    if not access_token:
        print("获取AccessToken失败，IdToken有误")
        sys.exit()
    return access_token
def get_chat_ids(token):
    url = "https://merlin-uam-yak3s7dv3a-ue.a.run.app/user/getPaginatedUserChatHistory?customJWT=true"

    payload = json.dumps({
        "ENTRY_PER_PAGE": 30,
        "page": 1
    })
    headers = {
        'authority': 'merlin-uam-yak3s7dv3a-ue.a.run.app',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': 'Bearer ' + token,
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_dict = json.loads(response.text)

    id_list = [history.get('id',None) for history in response_dict.get('data',{}).get('history',{})]
    if not id_list:
        print("获取历史记录失败，AccessToken有误")
        sys.exit()
    return id_list


def delete_chat_history(token, chat_ids):
    headers = {
        'authority': 'us-central1-foyer-work.cloudfunctions.net',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json'
    }

    for chat_id in chat_ids:
        url_base = f"https://us-central1-foyer-work.cloudfunctions.net/deleteUserChatHistory?token={token}&chatId={chat_id}&customJWT=true"
        url = url_base.format(id=chat_id)
        response = requests.request("GET", url, headers=headers).text
        response = json.loads(response)

        print("Chat_id={}: {}".format(chat_id, response.get("data", {}).get("message",None)))



def main():
    tokenType = input('please use your tokenType(refreshToken:0,Idtoken:1,MerlinAccesToken:2)：')
    if tokenType=="0":
        refreshToken = input('please use your own refreshToken here:')
        Idtoken = get_Idtoken(refreshToken)
        chat_token = get_chat_token(Idtoken)
    elif tokenType=="1":
        Idtoken = input('please use your own Idtoken here:')
        chat_token = get_chat_token(Idtoken)
    elif tokenType=="2":
        chat_token = input('please use your own chat_token here:')
    else:
        return
    chat_ids = get_chat_ids(chat_token)
    delete_chat_history(chat_token, chat_ids)


if __name__ == "__main__":
    main()
