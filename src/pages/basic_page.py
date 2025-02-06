import time

from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException, NoSuchElementException
from src.logger.formatted_logger import logger


class BasicPage(object):
    """Основной класс для страниц"""

    timeout = 30

    def __init__(self, browser):
        self.browser = browser

    def find_elem(self, locator:tuple[str, str]):
        element = None

        try:
            element = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(locator))
        except NoSuchElementException:
            logger.warning(f'Элемент {locator[1]} не найден')
        try:
            element = WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            logger.warning(f'Элемент {locator[1]} не найден за {self.timeout} секунд')
        except Exception as error:
            logger.warning(f'Не удалось кликнуть по элементу {locator[1]}. Ошибка: {error}')
        return False


    def click_on_element(self, locator:tuple[str, str]):
        element = self.find_elem(locator)
        if element:
            element.click()
            logger.info(f'Клик по элементу: {locator[1]}')


    def page_has_loaded(self):
        page_state = self.browser.execute_script('return document.readyState;')
        return page_state == 'complete'

    def wait_for_page_loaded(self, locator=None):
        WebDriverWait(self.browser, self.timeout).until(
            lambda b: b.execute_script("return document.readyState") == "complete")
        if locator:
            try:
                WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(locator))
            except TimeoutException:
                logger.warning(f'Время ожидания элемента: {locator} в функции {self.wait_for_page_loaded().__name__}')

    def save_scr(self, file_name:str):
        self.wait_for_page_loaded()
        if self.page_has_loaded():
            self.browser.save_screenshot(f'{file_name}.png')

    def send_text(self, locator, text):
        self.browser.find_element(*locator).send_keys(text)
