import sys
import json
import requests
from pathlib import Path

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'


def get_local_data(path):
    folder_path = Path(path)
    refresh_token_list = []
    email_list = []

    for json_file in folder_path.rglob('indexeddb*.json'):
        with open(json_file, 'r', encoding='UTF-8') as f:
            json_content = json.load(f)
            if "value" in json_content and "stsTokenManager" in json_content["value"] and "refreshToken" in \
                    json_content["value"]["stsTokenManager"]:
                refresh_token_list.append(json_content["value"]["stsTokenManager"]["refreshToken"])
                email_list.append(json_content["value"]["email"])

    print(f"读取到 {len(refresh_token_list)} 个账号。")
    return refresh_token_list, email_list

def delete_files(path, files_to_delete):
    base_path = Path(path)
    for file_path in base_path.rglob('indexeddb*.json'):
        if file_path.is_file() and file_path.name in files_to_delete:
            file_path.unlink()
def get_access_token(refresh_token):
    url = "https://securetoken.googleapis.com/v1/token?key=AIzaSyAvCgtQ4XbmlQGIynDT-v_M8eLaXrKmtiM"

    headers = {
        'User-Agent': USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    try:
        response = requests.post(url, headers=headers, data=data).json()
        # {
        #     "error": {
        #         "code": 400,
        #         "message": "USER_NOT_FOUND",
        #         "status": "INVALID_ARGUMENT"
        #     }
        # }
                # {
          # "error": {
            # "code": 400,
            # "message": "USER_DISABLED",
            # "status": "INVALID_ARGUMENT"
          # }
        # }
        if "USER_NOT_FOUND" in str(response) or "USER_DISABLED" in str(response):
            print("已封号")
            return 4
        return response.get("access_token", None)
    except requests.exceptions.RequestException as e:
        print(e)
        return False

def gen_inviteCode(token):

    url = f"https://us-central1-foyer-work.cloudfunctions.net/generateReferralCode?print=3274186570&token={token}"

    headers = {
            'User-Agent': USER_AGENT,
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://app.getmerlin.in',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://app.getmerlin.in/'
        }
    response = requests.get(url, headers=headers).json()

    print(response.get("data",{}).get("inviteId",None))

def invite_handler(invite, token):
    url = f"https://us-central1-foyer-work.cloudfunctions.net/invitesHandler?print=1990685894&invite={invite}&token={token}"

    headers = {
        'User-Agent': USER_AGENT,
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://app.getmerlin.in',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://app.getmerlin.in/'
    }

    try:
        response = requests.get(url, headers=headers).json()
        if response.get("status") == "success":
            print("Invitation accepted!")
            return True
        else:
            error = response.get("error", {}).get("message")
            print(error)
            if "limit" in error:
                sys.exit()
            return False
    except requests.exceptions.RequestException as e:
        print("请求连接出错",e)
        return False


if __name__ == '__main__':
    # inviteId = "a1601d23"
    inviteId = input("邀请码如a1601d23：")
    local_data = "E:\DevProject\PythonProject\AiEra\ExtensionsCrack\MerlinDBMange\Data\Accounts"
    files_to_delete=[]
    invite_num = 0
    refresh_token_list, email_list = get_local_data(local_data)
    for i, refresh_token in enumerate(refresh_token_list):
        email = email_list[i]
        print(email,end=":")
        token = get_access_token(refresh_token)
        if token==4:
            files_to_delete.append("indexeddb_"+email+".json")
        elif token and token !=4 and invite_handler(inviteId, token):
            invite_num += 1
            if invite_num >1:
                break
    delete_files(local_data, files_to_delete)
