# from asyncio import create_task, get_event_loop, AbstractEventLoop,Task
# import websocket
# import json
from typing import List
# from os import environ


# class Asset:

#     __slots__:List[str] = [
#         "ticker",
#         "data"
#     ]

#     def __init__(self,ticker:str, ) -> None:
#         self.ticker: str = ticker
#         self.data: dict[str, None] = {
#             "lastPrice":None,
#             "Symbol":None,
#             "UNIX_timestemp":None,
#             "Volume":None,
#             "type": None

#             }

#     def extract(self, new_values: dict) -> dict:
#         if "p" in new_values:
#             self.data["lastPrice"] = new_values["p"]
#         if "s" in new_values:
#             self.data["Symbol"] = new_values["s"]
#         if "t" in new_values:
#             self.data["UNIX_timestemp"] = new_values["t"]
#         if "v" in new_values:
#             self.data["Volume"] = new_values["v"]
#         if "type" in new_values:
#             self.data["type"] = new_values["type"]

#     def get_data(self)-> dict:
#         return self.data

#     def __repr__(self) -> str:
#         return "Asset"

#     def __str__(self) -> str:
#         return "Asset"


# class PriceProducer:

#     __slots__: List[str] = [
#         "__key",
#         "symbols",
#         "start",
#         "assets_objects",
#         "ws",
#         "task"
#     ]

#     def __init__(self,symbols: List[str]=[]) -> None:
#         self.__key: str = environ.get("FINNHUB_KEY")
#         if not symbols:
#             raise Exception("assets list is empty")
#         self.symbols: List[str] = symbols
#         self.assets_objects: dict = {}
#         self.start: bool = False




#     def run(self) -> None:
#         self.start = True
#         websocket.enableTrace(True)
#         assets: list[str] = [x.upper() for x in self.symbols]
#         for asset in assets:
#             self.assets_objects[asset] = Asset(ticker=asset)
#         self.ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={self.__key}",
#                               on_message = self.on_message,
#                               on_error = self.on_error,
#                               on_close = self.on_close,
#                               )
#         self.ws.on_open = self.on_open
#         self.ws.run_forever()

#     def on_open(self,ws):
#         for asset in self.symbols:
#             self.ws.send(json.dumps({"type": "subscribe", "symbol": asset}))
#             print(f'Subscription for {asset} succeeded')

#     def on_message(self,ws , message) -> None:
#         message = json.loads(message)
#         if message['type'] == 'trade':
#             # self.task: Task[None] = create_task(self._process_data(message=message))
#             # self.assets_objects[message['data']]
#             print(message)

#     def on_error(self, ws, error) -> None:
#         print(error)

#     def on_close(self,ws) -> None:
#         print("### closed ###")

#     async def _process_data(self, message: dict) -> None:
#         asset: Asset = self.assets_objects[message['s']]
#         asset.extract(new_values=message)


# if __name__ =="__main__":
#    obj = PriceProducer(symbols=['MSFT', 'APPLE'])
#    obj.run()

# from asyncio import create_task, get_event_loop, AbstractEventLoop,Task,Queue,run
# import websockets
# import json
# from typing import List
# from os import environ
# import redis
# from os import environ
# from dotenv import load_dotenv
# load_dotenv()


class Asset:

    __slots__: List[str] = [
        "ticker",
        "data"
    ]

    def __init__(self, ticker: str) -> None:
        self.ticker: str = ticker
        self.data: dict[str, None] = {
            "lastPrice": None,
            "Symbol": None,
            "UNIX_timestemp": None,
            "Volume": None,
            "type": None
        }

    async def extract(self, messege: dict) -> dict:
        new_values = messege['data']
        if "p" in new_values:
            self.data["lastPrice"] = new_values["p"]
        if "s" in new_values:
            self.data["Symbol"] = new_values["s"]
        if "t" in new_values:
            self.data["UNIX_timestemp"] = new_values["t"]
        if "v" in new_values:
            self.data["Volume"] = new_values["v"]
        if "type" in new_values:
            self.data["type"] = new_values["type"]
        print(self.data['Symbol'],self.data['lastPrice'])
        await self.send_to_kafka(self.data)

    async def send_to_kafka(self, data: dict) -> None:
        # Use your async Kafka producer to send `data` to Kafka.
        pass


# class PriceProducer:

#     __slots__: List[str] = [
#         "__key",
#         "symbols",
#         "assets_objects",
#         "queue",
#         "redis_client"
#     ]

#     def __init__(self, symbols: List[str]) -> None:
#         print('Initializing PriceProducer')
#         self.__key: str = environ.get("FINNHUB_KEY")
#         if not symbols:
#             raise Exception("assets list is empty")
#         self.symbols: List[str] = symbols
#         self.assets_objects: dict = {}
#         self.queue: Queue = Queue()
#         self.redis_client = redis.Redis(host='redis', port=6379, db=0,password=environ.get('REDIS_PASSWORD'))
#         if not self.redis_client.exists('add_tickers'):
#             self.redis_client.lpush('add_tickers','')
#             print('add tickers key created in redis')
#         print('PriceProducer initialized')

#     async def start(self) -> None:
#         print('Starting PriceProducer')
#         assets: list[str] = [x.upper() for x in self.symbols]
#         for asset in assets:
#             self.assets_objects[asset] = Asset(ticker=asset)
#         consumer_task: Task = create_task(self.consumer_handler())
#         await self.producer_handler()
#         await consumer_task
#         print('PriceProducer started')

#     async def producer_handler(self)-> None:
#         while True:  # Add a loop to retry the connection
#             try:
#                 async with websockets.connect(f"wss://ws.finnhub.io?token={self.__key}") as websocket:
#                     for asset in self.symbols:
#                         await websocket.send(json.dumps({"type": "subscribe", "symbol": asset}))
#                     while True:
#                         message = await websocket.recv()
#                         await self.queue.put(message)
#             except websockets.exceptions.ConnectionClosedError:
#                 print("Connection closed, retrying...")
#                 continue  # Retry the connection

#     async def consumer_handler(self):
#         while True:
#             message = await self.queue.get()
#             message = json.loads(message)
#             if message['type'] == 'trade':
#                 await self._process_data(message)

#     async def _process_data(self, message: dict) -> None:
#         asset: Asset = self.assets_objects[message['s']]
#         await asset.extract(new_values=message['data'])


# if __name__ == "__main__":
#     try:
#         print('run data producer')
#         runner = PriceProducer(symbols=['MSFT', 'APPLE'])
#         run(runner.start())
#     except Exception as e:
#         print(f"An error occurred: {e}")

import asyncio
import websockets
import json
from typing import List
from os import environ
# from task import create_task  # make sure this import is correct

class PriceProducer:

    __slots__: List[str] = [
        "__key",
        "symbols",
        "start",
        "assets_objects",
        "ws",
        "task"
    ]

    def __init__(self,symbols: List[str]=[]) -> None:
        self.__key: str = environ.get("FINNHUB_KEY")
        if not symbols:
            raise Exception("assets list is empty")
        self.symbols: List[str] = symbols
        self.assets_objects: dict = {}
        self.start: bool = False

    async def run(self) -> None:
        self.start = True
        assets: list[str] = [x.upper() for x in self.symbols]
        for asset in assets:
            self.assets_objects[asset] = Asset(ticker=asset)
        async with websockets.connect(f"wss://ws.finnhub.io?token={self.__key}") as self.ws:
            await self.on_open()
            async for message in self.ws:
                task = asyncio.create_task(self.on_message(message))
                # await self.on_message(message)
                await task
    async def on_open(self):
        for asset in self.symbols:
            await self.ws.send(json.dumps({"type": "subscribe", "symbol": asset}))
            print(f'Subscription for {asset} succeeded')

    async def on_message(self, message) -> None:
        message = json.loads(message)
        # if message['type'] == 'trade':
            # await self._process_data(message=message)
        print(message)

    async def _process_data(self, message: dict) -> None:
        asset: Asset = self.assets_objects[message['s']]
        asset.extract(new_values=message)


if __name__ =="__main__":
    obj = PriceProducer(symbols=['AAPL','MSFT'])
    asyncio.run(obj.run())
