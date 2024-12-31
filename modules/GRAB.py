            
class GrabModule:

    

    ALLOW = ['OBJ_STATUS_SET','OBJ_ACT', 'OBJ_ADD',':srv','PRIVMSG','PING']
    
    def process_message(self, key, text, storage , services):
        IDS = [17,18,35]
        #if storage.get("InitCheck") == 1:
            #GalaCollector.inventory_main(storage.get("UserId"), storage.get("UserPass"), True, storage)
            #storage.set("InitCheck",0)
        
        if key == "OBJ_STATUS_SET":
            for service_name, service_instance in services.items():
                    if service_name == "Elka":
                        service_instance.set(text[0],text[1])


        if key == 'PING':
            if storage.get("COUNT") > 0:
                for service_name, service_instance in services.items():
                    if service_name == "Elka":
                        list  = service_instance.list()
                        print(list)
                        objs = []
                        for item in list:
                            if int(item['status']) == 6:
                                objs.append(f"OBJ_ACT {item['type']} {item['id']} 11 present_off")
                
                storage.set("COUNT",0)
                for service_name, service_instance in services.items():
                    if service_name == "PlanetsRotator":
                        pl = service_instance.next()
                for service_name, service_instance in services.items():
                    if service_name == "Elka":
                        service_instance.clear()
                objs.append("PONG")
                objs.append(f"JOIN {pl}")
                return objs 
            else:
                storage.set("COUNT", int(storage.get("COUNT")) + 1 )
                print(f" ПИНГОВ ПОЛУЧЕНО {storage.get("COUNT")}")
                return ["PONG"]
            
        

            
        
        if key == ":srv":
            
                        
            if text[2][1:] == storage.get("UserName"):
                print(f"Получили {text}")
                #if storage.get("COUNT") > storage.get("count_to_send"):
                    #storage.set("COUNT",0)
                    #GalaCollector.inventory_main(storage.get("UserId"), storage.get("UserPass"), False, storage)
                    
                #else:
                    #storage.set("COUNT",storage.get("COUNT")+1)
                   # print(f"Счетчик {storage.get('COUNT')}")

        


        if key == "PRIVMSG":
            if storage.get("count") >10:
                for service_name, service_instance in services.items():
                    if service_name == "PlanetsRotator":
                        pl = service_instance.next()
                return f"JOIN {pl}"
            pass
            
        if key == "OBJ_ADD":
            
            if int(text[1]) in IDS:
                for service_name, service_instance in services.items():
                    if service_name == "Elka":
                        service_instance.add(text[0], text[1],"")
                print(f"Найден Ел {text[0]}")
                pass


import json
import re
import time
import requests
import random
from bs4 import BeautifulSoup



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
        time.sleep(random.uniform(1.0, 2.0)) 
        response = super().request(method, url, **kwargs)
        return response

class GalaCollector:

    def send_present(user_id,password,to,ids):
        SEND = f"https://galaxy.mobstudio.ru/services/?userID={user_id}&password={password}&a=present_make&usercur={to}&confirm=1&random={random.uniform(0.0, 1.0)}&"
        
        url = '&'.join(f'checked_items[{id}]=1' for id in ids)
        body = f"{url}&search_field=&give_anonymous=1&jad_PartID=XX&jad_userID=null&jad_DeviceId=&jad_locale=ru"

        session = RequestsSession()
        req = session.post(SEND, data=body)
        if req.status_code == 200:
            return True
        else:
            return False

    def inventory_main(user_id, password, first, storage):


        URL = f"https://galaxy.mobstudio.ru/services/?userID={user_id}&password={password}&a=show_inventory&usercur={user_id}&random={random.uniform(0.0, 1.0)}" 
        session = RequestsSession()
        response = session.get(URL).content
        main = BeautifulSoup(response, "lxml")
        game_items = main.find_all("div", class_="s__game_item")
        good_list = main.find_all("div", class_="s__goodlist_wrap")
        goods_count_pages = main.find("div", class_="s__pages__counter").text
        
        if first == True:
            goods_count_pages = goods_count_pages.split("/")[1]
        else:
            goods_count_pages = 3
        find = []
                           
        GOOD_URL = f"https://galaxy.mobstudio.ru/services/?userID={user_id}&password={password}&a=show_inventory&usercur={user_id}&random={random.uniform(0.0, 1.0)}&page=1&sock=0&select_all=0&unselect_all=0"

        if goods_count_pages == "1":
            response = session.get(GOOD_URL).content
            main = BeautifulSoup(response, "lxml")
            game_items_1 = main.find_all("div", class_="s__item")
            for game_ite in game_items_1:

                goodID =  re.search(r'goodID=(\d+)', str(game_ite)).group(1)

                name = game_ite.find("div", class_="s__name").text
                if storage.get("find_item") in name:
                    find.append(goodID)
                    print(goodID + " " + name)


        else:
            for page_id in range(1, int(goods_count_pages)):

                        
                GOOD_URL = f"https://galaxy.mobstudio.ru/services/?userID={user_id}&password={password}&a=show_inventory&usercur={user_id}&random={random.uniform(0.0, 1.0)}&page={page_id}&sock=0&select_all=0&unselect_all=0"
                response = session.get(GOOD_URL).content
                main = BeautifulSoup(response, "lxml")
                game_items_1 = main.find_all("div", class_="s__item")
                for game_ite in game_items_1:
                    goodID =  re.search(r'goodID=(\d+)', str(game_ite)).group(1)

                    name = game_ite.find("div", class_="s__name").text
                    if storage.get("find_item") in name:
                        find.append(goodID)
                        
                        print(goodID + " " + name)
        if len(find) == 0:
            pass
        else:

            if GalaCollector.send_present(user_id,password,storage.get("to_user"),find):
                print("Отправлены подарки")

    def inventory_own(user_id,password):
        URL = f"https://galaxy.mobstudio.ru/services/?userID={user_id}&password={password}&a=show_inventory&usercur={id}&random={random.uniform(0.0, 1.0)}" 


    
