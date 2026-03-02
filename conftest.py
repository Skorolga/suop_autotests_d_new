from datetime import datetime
from sys import platform
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import allure
from config.config import SUOP
# webdriver-manager helps install the correct chromedriver
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def browser():
    options = Options()
    # Настройки Chrome для работы с Basic Auth
    prefs = {
        'profile.default_content_settings.popups': 0,
        'profile.managed_default_content_settings.notifications': 2,
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--disable-blink-features=BlockCredentialedSubresources')
    options.add_argument('--disable-web-resources-deprecation-warnings')
    
    if platform == 'linux':
        options.add_argument('--headless')

    # install and start chromedriver via webdriver-manager
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.execute_cdp_cmd('Network.enable', {})
    browser.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
        'headers': {
            'Authorization': SUOP.BASIC_AUTH_HEADER,
        }
    })
    # browser.implicitly_wait(20)  # неявное ожидание (вместе с явным использовать не рекомендуется)

    yield browser
    browser.quit()

@pytest.fixture
def pre_post_browser(browser):
    yield
    # Logout - use plain URL without credentials since we handle auth via headers now
    browser.get('https://www.tnop12.rt.ru/logout')

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для получения статуса теста и прикрепления скриншота при падении.
    """
    outcome = yield
    rep = outcome.get_result()

    # Проверяем, что тест упал на этапе выполнения (не setup/teardown)
    if rep.when == "call" and rep.failed:
        # Ищем драйвер среди фикстур теста
        browser = None
        for fixture_name in item.fixturenames:
            if "browser" in fixture_name:
                browser = item.funcargs[fixture_name]
                break

        if browser and hasattr(browser, "get_screenshot_as_png"):
            # Создаем скриншот и прикрепляем к Allure
            screenshot = browser.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f'Скриншот ошибки',
                attachment_type=allure.attachment_type.PNG,
            )

@pytest.hookimpl()
def pytest_sessionfinish(session):
    dir_name = f'{session.items[0].name}_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}'
    cmd = f'allure generate -c ./allure-results --single-file -o ./allure-report/{dir_name}'
    proc = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, text=True)
    proc.wait()  # ждем завершение процесса subprocess
    if platform == 'win32':
        cmd = f'.\\allure-report\\{dir_name}\\index.html'  # после теста открываем отчет
    subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, text=True)
