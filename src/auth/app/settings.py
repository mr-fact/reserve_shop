from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=True)
SECRET_KEY = config('SECRET_KEY', cast=Secret, default='fj@^&!(ui73n82b=25rtu7ahs!ed)4ieq0lcen-!%d#pj9m&j#')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings, default=['0.0.0.0'])
PROJECT_NAME = 'reserve_shop_auth'
PREFIX = '/auth'
VERSION = '0.1.0'
