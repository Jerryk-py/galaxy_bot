
import asyncio
from core.WebSocketClient import WebSocketClient
from core.MessageHandler import MessageHandler
import json
import re
import time
import requests
import random
from bs4 import BeautifulSoup
import importlib, pathlib
from core.Storage import Storage
import configparser
import ssl
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.verify_mode = ssl.CERT_NONE


import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
#logger.addHandler(logging.StreamHandler())

import asyncio
import websockets
import time
import hashlib
import json
import re
import requests
import random
import sys,os

if __name__ == "__main__":

    #44880935 
    data= {
        'kod': 'code' ,
        'start_planet':'Жемчужина',
        'only_transfer':1, 
        'to_user':"77209528",
        'count_to_send':2030,
        'find_item':'()',
        "URI":"wss://cs.mobstudio.ru:6672"
    }

    PLANETS =[ 
'list of planet'

    ]


    handler = MessageHandler()

    handler.load_config(data)
    handler.load_modules()  
    handler.load_services( PLANETS)

   




    client = WebSocketClient(data['URI'], handler)

    asyncio.get_event_loop().run_until_complete(client.run())
    