import asyncio
import websockets
import json
from typing import List
from os import environ

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
        async with websockets.connect(f"wss://ws.finnhub.io?token=cit981pr01qu27mnra5gcit981pr01qu27mnra60",timeout=15) as self.ws:
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
