from dotenv import load_dotenv
from pathlib import Path
import os


dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path, override=True)


class SUOP:
    BASE_URL = os.getenv('BASE_URL').split('//')
    BASIC_AUTH_LOGIN = os.getenv('BASIC_AUTH_LOGIN')
    BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD')
    MAIN_URL = f'{BASE_URL[0]}//{BASIC_AUTH_LOGIN}:{BASIC_AUTH_PASSWORD}@{BASE_URL[1]}'
    CLIENT_LOGIN = os.getenv('CLIENT_LOGIN')
    CLIENT_PASSWORD = os.getenv('CLIENT_PASSWORD')
    ORGANIZATION_CLIENT = os.getenv('ORGANIZATION_CLIENT')