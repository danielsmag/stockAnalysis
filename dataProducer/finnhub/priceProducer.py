import asyncio
import websockets
import json
from typing import List, Dict
from os import environ
import redis
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka.admin import AdminClient, NewTopic

class Asset:

    __slots__: List[str] = [
        "ticker",
        "data",
        "avro_producer",
        "schema",
        "value_schema"
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
        with open('finnhub/schemas/asset_schema.avsc', 'r') as schema_file:
            value_schema_str: str = schema_file.read()
        self.schema = avro.loads(value_schema_str)
        self.avro_producer = AvroProducer(
        {
            'bootstrap.servers': "kafka:9092",
            'schema.registry.url': "http://schema-registry:8081"
        }
            )
        self.value_schema = avro.loads(value_schema_str)

    async def extract(self, messege: dict) -> None:
        # new_values = messege['data']
        if "p" in messege:
            self.data["lastPrice"] = messege["p"]
        if "s" in messege:
            self.data["Symbol"] = messege["s"]
        if "t" in messege:
            self.data["UNIX_timestemp"] = messege["t"]
        if "v" in messege:
            self.data["Volume"] = messege["v"]
        if "type" in messege:
            self.data["type"] = messege["type"]
        print(self.data['Symbol'],self.data['lastPrice'])
        await self.send_to_kafka(self.data)

    async def send_to_kafka(self, data: dict) -> None:
        # Use your async Kafka producer to send `data` to Kafka.
        self.avro_producer.produce(topic='assets-price', value=data, value_schema=self.value_schema)
        self.avro_producer.flush()

class PriceProducer:

    __slots__: List[str] = [
        "__key",
        "symbols",
        "start",
        "assets_objects",
        "ws",
        "task",
        "r"
    ]

    def __init__(self,symbols: List[str]=[]) -> None:
        self.__key: str = environ.get("FINNHUB_KEY")
        if not symbols:
            raise Exception("assets list is empty")
        self.symbols: List[str] = symbols
        self.assets_objects: dict = {}
        self.start: bool = False


    async def run(self) -> None:
        self.r = redis.Redis(host='redis', port=6379, decode_responses=True)
        self.r.lpush('ticker_to_add','')
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
        if message['type'] == 'trade':
            await self._process_data(message=message)
        # print(message)

    async def _process_data(self, message: dict) -> None:
        # print(message.keys())
        message: dict = message['data'][0]
        asset: Asset = self.assets_objects[message['s']]
        await asset.extract(messege=message)




if __name__ =="__main__":
    conf: Dict[str, str] = {'bootstrap.servers': 'kafka:9092'}
    topic_name = 'assets-price'

    admin_client = AdminClient(conf)

    # Get the list of topics
    topics = admin_client.list_topics().topics

    # Check if topic exists
    if topic_name in topics:
        print(f'Topic "{topic_name}" already exists.')
    else:
        print(f'Topic "{topic_name}" does not exist. Creating...')
        topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        admin_client.create_topics([topic])
    obj = PriceProducer(symbols=['AAPL','MSFT'])
    asyncio.run(obj.run())
