import time

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException, NoSuchElementException
from src.logger.formatted_logger import logger


class BasicPage(object):
    """Основной класс для страниц"""

    timeout = 30

    def __init__(self, browser):
        self.browser = browser

    def find_elem(self, locator:tuple[str, str]) -> WebElement | bool:
        """Поиск элемента по локатору, возвращает элемент или bool"""
        element = None

        # Проверяем наличие элемента на странице
        try:
            element = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(locator))
        except NoSuchElementException:
            logger.warning(f'Элемент {locator[1]} не найден')
            return False

        # Проверка кликабельности элемента
        try:
            element = WebDriverWait(self.browser, self.timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            logger.warning(f'Элемент {locator[1]} не найден за {self.timeout} секунд')
        except Exception as error:
            logger.warning(f'Не удалось кликнуть по элементу {locator[1]}. Ошибка: {error}')
            return False

        logger.info(f'Скроллим до элемента: {locator[1]}')
        action = ActionChains(self.browser)
        action.move_to_element_with_offset(element, 0, 0).pause(0).perform()
        if element:
            return element
        else:
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
                logger.warning(f'Время ожидания элемента: {locator} в функции basic_page.wait_for_page_loaded()')

    def save_scr(self, file_name:str):
        self.wait_for_page_loaded()
        if self.page_has_loaded():
            self.browser.save_screenshot(f'{file_name}.png')

    def send_text(self, locator, text):
        self.browser.find_element(*locator).send_keys(text)

    def get_text(self, locator):
        elem = self.find_elem(locator)
        if elem:
            return elem.text
