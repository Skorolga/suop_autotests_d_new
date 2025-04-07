from datetime import datetime
from sys import platform
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import allure

@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=ru-RU")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'ru,ru_RU'})
    # options.add_argument("--disable-application-cache")
    options.add_argument("--incognito")

    # options.add_argument("--disk-cache-size=0")
    options.set_capability('unhandledPromptBehavior', 'ignore')
    if platform == 'linux':
        options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)
    # browser.implicitly_wait(20)  # неявное ожидание (вместе с явным использовать не рекомендуется)

    yield browser
    browser.quit()


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
                name=f"Скриншот ошибки",
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
