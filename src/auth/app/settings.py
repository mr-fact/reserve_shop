from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=True)
SECRET_KEY = config('SECRET_KEY', cast=Secret, default='fj@^&!(ui73n82b=25rtu7ahs!ed)4ieq0lcen-!%d#pj9m&j#')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings, default=['0.0.0.0'])
PROJECT_NAME = 'reserve_shop_auth'
PREFIX = '/auth'
VERSION = '0.1.0'

with open("../private.key", "r") as private_file:
    JWT_PRIVATE_KEY = private_file.read()

with open("../public.key", "r") as public_file:
    JWT_PUBLIC_KEY = public_file.read()

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = config('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=1440)
JWT_ALGORITHM = config('JWT_ALGORITHM', cast=str, default='RS256')
