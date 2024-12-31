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

class WebSocketClient:
    def __init__(self, server_uri, message_handler):
        self.server_uri = server_uri
        self.message_handler = message_handler
        self.websocket = None

    async def connect(self):
        try:

            self.websocket = await websockets.connect(self.server_uri, ssl=ssl_context,ping_interval=None,user_agent_header="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
            print(f"Выполнено подключение к серверу:  {self.server_uri}")
            await self.send_message(":ru IDENT 352 -2 4030 1 2 :GALA")
        except websockets.exceptions.TimeoutError as ex:
            print(f"Соединение потеряно. Переподключаемся...{ex}")
            await self.connect()
       

    async def send_message(self, message):
        await self.websocket.send(str(message) + " \r\n")
        

    async def receive_messages(self):
        while True:
            
            try:
                message = await self.websocket.recv()
                
                req = self.message_handler.handle_message(message)
                if type(req) == str:
                    await self.send_message(req)
                elif type(req) == list:
                    for r in req:
                        await self.send_message(r)

            except  websockets.exceptions.ConnectionClosedError as ex:
                print(f"Соединение потеряно. Переподключаемся...через 180 сек. {ex}")
                time.sleep(180)
                await self.connect()
            

    async def run(self):
        await self.connect()
        await asyncio.gather(
            self.receive_messages(),
        )

