import databases
from pydantic.v1 import BaseSettings
from starlette.config import Config


class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6380
    redis_db: int = 0

    class Config:
        env_file = ".env"


class PostgresqlSettings(BaseSettings):
    database_url: str = 'postgresql+psycopg2://postgres:postgres@0.0.0.0:5434/mydb'

    class Config:
        env_file = ".env"


postgresql_settings = PostgresqlSettings()
redis_settings = RedisSettings()


config = Config(".env")

TESTING_DATAbASE = config('TESTING', cast=bool, default=True)

OTP_EX_TIME = config('OTP_EX_TIME', cast=int, default=300)
OTP_LEN = config('OTP_LEN', cast=int, default=4)
OTP_FAILED_TIMES = config('OTP_FAILED_TIMES', cast=int, default=5)

if TESTING_DATAbASE:
    DATABASE_URL = databases.DatabaseURL(url="sqlite:///test.db")
else:
    DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
db_config = {
    "pool_size": 20, "max_overflow": 0
}
