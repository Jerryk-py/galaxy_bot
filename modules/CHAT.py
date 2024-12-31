import json
import re
import requests
import random



class ChatModule:
    
    ALLOW = ['PRIVMSG', 'NOTE']

    def process_message(self, key, text, storage, services):

        if key =='NOTE':
            
            print("Написали в приват")




class RequestsSession(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def request(self, method, url, **kwargs):
       
        if 'headers' not in kwargs:
            kwargs['headers'] = {}  
        kwargs['headers'].update({
            "accept": "*/*",
            "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-galaxy-client-ver": "9.5",
            "x-galaxy-kbv": "352",
            "x-galaxy-lng": "ru",
            "x-galaxy-model": "chrome 120.0.0.0",
            "x-galaxy-orientation": "portrait",
            "x-galaxy-os-ver": "1",
            "x-galaxy-platform": "web",
            "x-galaxy-scr-dpi": "1.25",
            "x-galaxy-scr-h": "726",
            "x-galaxy-scr-w": "700",
            "x-galaxy-user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        })

        response = super().request(method, url, **kwargs)
        print(response.text)
        if response.status_code == 200:
            return True
        else:
            return False


class Services:


    def send_mail(user_id,text, storage):
        random_float = random.uniform(0.0, 1.0)

        data= {
            "new_message":text,
            "jad_PartID":"25",
            "jad_userID":"null",
            "jad_DeviceId": "",
            "jad_locale":"ru"
        }
        MAIL_URL = f"https://galaxy.mobstudio.ru/services/?userID={storage.get('UserId')}&password={storage.get('UserPass')}&a=new_mail_main&usercur={user_id}&act=show_dialog&send=1&lngg=ru&from=&random={random_float}"
        session = RequestsSession()
        return session.post(url=MAIL_URL,data=data)
        
      

    