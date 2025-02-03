import time

from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException, NoSuchElementException


class BasicPage(object):
    """Основной класс для страниц"""

    timeout = 12

    def __init__(self, browser):
        self.browser = browser

    def find_elem(self, locator:tuple[str, str]):
        element = None

        try:
            element = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(locator))
        except NoSuchElementException:
            print(f'Элемент {locator[1]} не найден')
        try:
            element = WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            print(f'Элемент {locator[1]} не найден за {self.timeout} секунд')
        except:
            print(f'Не удалось кликнуть по элементу {locator[1]}')
        return False


    def click_on_element(self, locator:tuple[str, str]):
        element = self.find_elem(locator)
        if element:
            element.click()
            print(f'Клик по элементу: {locator[1]}')


    def page_has_loaded(self):
        page_state = self.browser.execute_script('return document.readyState;')
        return page_state == 'complete'

    def save_scr(self, file_name:str):
        time.sleep(3)
        if self.page_has_loaded():
            self.browser.save_screenshot(f'{file_name}.png')

    def send_text(self, locator, text):
        self.browser.find_element(*locator).send_keys(text)
