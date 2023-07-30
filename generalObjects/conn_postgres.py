from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from os import environ
from dotenv import load_dotenv
load_dotenv()
from pandas import DataFrame,read_sql_query,to_datetime
from numpy import nan
from typing import Dict,List,Union


class Connect_Sql:

    __slots__: List[str] = [
        "dialect",
        "driver",
        "__host",
        "__db",
        "__user",
        "__pass",
        "__engine",
        "__session",
        "__server"
    ]

    def __init__(self, db: str, server: str) -> None:
        assert isinstance(db, str), "db must be a string"
        assert isinstance(server, str), "server must be a string"
        self.__server: str = server.upper()
        self.dialect: str = 'postgresql'
        self.driver: str = 'psycopg2'
        self.__host:str = str(environ.get(f'HOST_SQL_{self.__server}'))
        self.__user:str = str(environ.get(f'USER_SQL_{self.__server}'))
        self.__pass:str = str(environ.get(f'PASS_SQL_{self.__server}'))
        self.__db:str = db
        self.__session = None
        self.__engine: Union[Engine,None] = None


    def create_conn(self) -> None:
        try:
            connection_string: str = f"{self.dialect}://{self.__user}:{self.__pass}@{self.__host}/{self.__db}"
            self.__engine: Union[Engine,None] = create_engine(connection_string)
            self.__session = sessionmaker(bind=self.__engine)
            print(f'connection SQL {self.__server} open')
        except Exception as e:
            print(e,f'SQL connect to {self.__server} faild')


    def close_conn(self) -> None:
        if self.__engine:
            self.__engine.dispose()
            print(f'connection SQL {self.__server} close')

    def _ensure_sql_conn(self) -> bool:
        try:
            if not self.__engine:
                print('The connection was disconnected')
                self.create_conn()

            elif not self.__engine.connect().closed:
                print('The connection was disconnected')
                self.create_conn()
            return True
        except Exception as e:
            print("_ensure_sql_conn exceptation",e)
            return False

    def get_exsit_values_in_table(self,table:str, value: str, date: bool =False) -> list:
        assert isinstance(table,str),"table must be a string"
        assert isinstance(value,str),"value must be a string"
        assert isinstance(self.__engine,Engine)

        query: str = f'SELECT "{value}" FROM {table}'
        df: DataFrame = read_sql_query(query, con=self.__engine)
        if date and len(df)>0:
            df[value] = to_datetime(value).dt.date
        result_list:list= df[value].replace('', nan).drop_duplicates().dropna().to_list()
        return result_list

    def get_engine(self) -> Union[Engine,None]:
        return self.__engine

    def get_properties(self) -> Dict[str, str]:
        return  {
            "user": self.__user,
            "password": self.__pass,
        }

    def url_jdbc(self,db,port='5432') -> str:
        assert isinstance(db, str), "db must be string"
        url: str = f"jdbc:postgresql://{self.__host}:{port}/{db}"
        return url

    def set_db(self, db: str) -> None:
        assert isinstance(db, str), "server must be a string"
        self.db = db
        if self.__engine:
            self.create_conn()

    def _get_user(self) -> str:
        return self.__user

    def _get_pass(self) -> str:
        return self.__pass

    @property
    def db(self) -> str:
        return self.__db

    @db.setter
    def db(self, value: str = '') -> None:
        db: str = value.lower()  # Database names are typically lower case
        if db in ['funds', 'database']:  # I'm assuming 'database' is the correct value here, please replace it if not
            self.set_db(db)

    def __str__(self) -> str:
        return "sql-conector"

    def __repr__(self) -> str:
        return "sql-conector"