from os import environ

from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv("local.env")


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DefaultSettings, cls).__new__(cls)
        return cls.instance

    ENV: str = environ.get("ENV", "local")
    # APP Settings
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/v1")
    APP_HOST: str = environ.get("APP_HOST", "http://0.0.0.0")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))

    # Postgresql Settings
    DB_NAME: str = environ.get("DB_NAME", "medvezhiy-ugol")
    DB_PATH: str = environ.get("DB_PATH", "localhost")
    DB_USER: str = environ.get("DB_USER", "postgres")
    DB_PORT: int = int(environ.get("DB_PORT", 6432))
    DB_PASSWORD: str = environ.get("DB_PASSWORD", "postgres")
    DB_POOL_SIZE: int = int(environ.get("DB_POOL_SIZE", 15))
    DB_CONNECT_RETRY: int = int(environ.get("DB_CONNECT_RETRY", 20))
    
    # TOKEN SETTINGS
    ALGORITHM: str = environ.get("ALGORITHM", "HS256")
    SECRET_KEY: str = environ.get(
        "SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 100000)
    )
    # Mongo Settings
    MG_PATH: str = environ.get("MG_PATH", "localhost")
    MG_PORT: str = environ.get("MG_PORT",27017)
    
    # IIKO Settings
    API_LOGIN: str = environ.get("API_LOGIN")
    URL_BASE: str =  environ.get("IIKO_BASE")
    URL_MENU: str = environ.get("IIKO_MENU")
    URL_TOKEN: str = environ.get("IIKO_TOKEN")
    URL_TERMINAL: str = environ.get("IIKO_TERMINAL")
    URL_ORGANIZATIONS: str = environ.get("IIKO_ORGANIZTION")
    URL_ORDER: str = environ.get("IIKO_ORDER")
    
    
    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.DB_NAME,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_PATH,
            "port": self.DB_PORT,
        }


    @property
    def mongo_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "host": self.MG_PATH,
            "port": self.MG_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )


    @property
    def database_uri_async(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )
    
    
    @property
    def database_mongo(self) -> str:
        
        return "mongodb://{host}:{port}/".format(**self.mongo_settings,)
