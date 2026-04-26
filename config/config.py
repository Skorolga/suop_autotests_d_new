from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

class SUOP:
    BASE_URL = os.getenv('BASE_URL', 'https://tnop12.rt.ru')
    BASIC_AUTH_LOGIN = os.getenv('BASIC_AUTH_LOGIN', 'tnop')
    BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'TZjLZ~uOx1~0EG~')

    # Открываем страницу без встроенных в URL credentials.
    # Basic auth вводится вручную в нативном окне браузера.
    MAIN_URL = BASE_URL

    # Остальные переменные
    CLIENT_LOGIN = os.getenv('CLIENT_LOGIN')
    CLIENT_PASSWORD = os.getenv('CLIENT_PASSWORD')
    ORGANIZATION_CLIENT = os.getenv('ORGANIZATION_CLIENT')
    ORGANIZATION_MANAGER = os.getenv('ORGANIZATION_MANAGER')
    ORGANIZATION_ADMIN = os.getenv('ORGANIZATION_ADMIN')
