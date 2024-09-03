from pydantic.v1 import BaseSettings


class MongoSettings(BaseSettings):
    mongo_url: str = "mongodb://admin:admin@localhost:27018/admin?retryWrites=true&w=majority"

    class Config:
        env_file = ".env"


mongo_settings = MongoSettings()
