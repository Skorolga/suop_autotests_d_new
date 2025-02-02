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