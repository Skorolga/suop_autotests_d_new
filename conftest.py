from datetime import datetime
import time
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_argument("--lang= ru")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disk-cache-size=0")
    options.set_capability('unhandledPromptBehavior', 'ignore')

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(20)  # неявное ожидание

    yield browser
    browser.quit()


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    dir_name = f'{session.items[0].name}_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}'
    cmd = f'allure generate -c ./allure-results --single-file -o ./allure-report/{dir_name}'
    proc = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, text=True)
    proc.wait()  # ждем завершение процесса subprocess
    cmd = f'.\\allure-report\\{dir_name}\\index.html'  # после теста открываем отчет
    subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, text=True)
