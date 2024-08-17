import databases
from pydantic.v1 import BaseSettings
from starlette.config import Config

config = Config(".env")

TESTING_DATAbASE = config('TESTING', cast=bool, default=True)


class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6380
    redis_db: int = 0

    class Config:
        env_file = ".env"


redis_settings = RedisSettings()


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
