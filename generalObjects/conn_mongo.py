from pymongo import MongoClient, errors
from pymongo.errors import ServerSelectionTimeoutError
from typing import Dict, List
from os import environ
import json
from bson import json_util

class MongoConnection:

    __slots__: List[str] = [
        "__server",
        "__host",
        "__db",
        "__user",
        "__pass",
        "__engine",
        "__session",
        "MongoCollection",
        "__collection"

    ]

    def __init__(self,server: str , db: str) -> None:
        assert isinstance(db, str), "db must be a string"
        assert isinstance(server, str), "server must be a string"
        self.__server: str = server.upper()
        self.__db:str = db
        self._initialize_identity()

    def _initialize_identity(self) -> None:
        self.__host:str = str(environ.get(f'HOST_MONGODB_{self.__server}'))
        self.__user:str = str(environ.get(f'USER_MONGODB_{self.__server}'))
        self.__pass:str = str(environ.get(f'PASS_MONGODB_{self.__server}'))


    def create_conn(self) -> None:
        try:
            self.__engine: MongoClient = MongoClient(f'mongodb://{self.__user}:{self.__pass}@{self.__host}:27017/')
            self.__engine[self.__db].command('ismaster')
            print(f"Connected to MongoDB DB:{self.__db}")
        except errors.OperationFailure as e:
            print(f"Could not connect to MongoDB: {e}")

    def ensure_connection(self) -> bool:
        if self.__engine is None:
            print("Failed to connect to MongoDB")
            return False
        try:
            self.__engine[self.__db].command('ismaster')
            return True
        except ServerSelectionTimeoutError as e:
            print("Failed to connect to MongoDB")
            print(e)
            return False

    def load_data_to_json(self,index_value: dict ,collection: str = '')-> dict:
        if collection != '':
            self.__collection = collection
        result_dict = {}
        if isinstance(self.__collection,str) and self.__collection != '':
            self.__collection: str = collection
            assert self.ensure_connection(), "no connection to mongo"
            # assert self.__session is not None, "Connection to database not established. Call create_conn() first."
            collection = self.__engine[self.__db][self.__collection]
            result = collection.find_one(index_value)
            result_json: str = json.dumps(result, default=json_util.default)
            result_dict: dict = json.loads(result_json)
        return result_dict


    def close_conn(self) -> None:
        if self.__engine is not None:
            self.__engine.close()
            self.__engine = None
            self.__session = None
            print('connection to MongoDB close ')

    @property
    def db(self) -> str:
        return self.__db

    @db.setter
    def db(self, new_db: str) -> None:
        assert isinstance(new_db, str), "new db must be a string"
        self.__db = new_db
        self.create_conn()

    @property
    def collection(self) -> str:
        return self.__collection  # changed MongoCollection to __collection

    @collection.setter
    def collection(self, new_collection: str) -> None:
        assert isinstance(new_collection, str), "new collection must be a string"
        self.__collection = new_collection  # changed MongoCollection to __collection


    def __repr__(self) -> str:
        return "MongoConnection"

    def __str__(self) -> str:
        return "MongoConnection"