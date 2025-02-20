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

    def find_elem(self, locator:tuple[str, str], timeout=timeout) -> WebElement | bool:
        """Поиск элемента по локатору, возвращает элемент или bool"""
        element = None
        # Проверяем наличие элемента на странице
        try:
            element = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
            logger.info(f'Элемент {locator[1]} найден')
        except NoSuchElementException:
            logger.warning(f'Элемент {locator[1]} не найден')
            return False
        except TimeoutException:
            logger.warning(f'Элемент {locator[1]} не найден за {timeout} секунд')
            return False

        # Проверка кликабельности элемента
        try:
            WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            logger.warning(f'Элемент {locator[1]} не найден за {timeout} секунд')
        except Exception as error:
            logger.warning(f'Не удалось кликнуть по элементу {locator[1]}. Ошибка: {error}')
            return False

    def find_all_elem(self, locator, timeout=timeout) -> list[WebElement] | bool:
        """Находит и возвращает список элементов"""
        try:
            elems = WebDriverWait(self.browser, timeout).until(EC.presence_of_all_elements_located(locator))
            return elems
        except Exception as error:
            logger.warning(f'Не удалось элементы по локатору {locator[1]}. Ошибка: {error}')
            return False

    def scroll_to_element(self, element):
        logger.info(f'Скроллим до элемента: {element}')
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    def click(self, locator:tuple[str, str], timeout=timeout):
        """Находит и кликает по элементу"""
        element = self.find_elem(locator, timeout)
        if element:
            try:
                element.click()
                logger.info(f'Клик по элементу: {locator[1]}')
            except Exception as error:
                logger.warning(f'Не удалось кликнуть по элементу {locator[1]}. Ошибка в методе click_on_element')
                logger.info(f'Видимость элемента: {element.is_displayed()}')
                try:
                    self.scroll_to_element(element)
                except Exception as error:
                    logger.info(f'Не удалось проскролить до элемента {locator[1]}')
                self.browser.execute_script('arguments[0].click();', element)  # кликаем если элемент есть но кликнуть штатно не получилось

    def page_has_loaded(self):
        page_state = self.browser.execute_script('return document.readyState;')
        return page_state == 'complete'

    def wait_for_page_loaded(self, locator=None, timeout=timeout) -> bool:
        """Ожидает загрузку страницы по переданному локатору"""
        WebDriverWait(self.browser, self.timeout).until(
            lambda b: b.execute_script("return document.readyState") == "complete")
        if locator:
            try:
                WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
                return True
            except TimeoutException:
                logger.warning(f'Вышло время ожидания загрузки страницы по элементу: {locator} в функции basic_page.wait_for_page_loaded()')
                return False

    def save_scr(self, file_name:str):
        """Сохраняет скриншот в текущий каталог"""
        self.wait_for_page_loaded()
        if self.page_has_loaded():
            self.browser.save_screenshot(f'{file_name}.png')

    def type(self, locator, text):
        """Набирает тест"""
        self.browser.find_element(*locator).send_keys(text)

    def get_text(self, locator):
        elem = self.find_elem(locator)
        if elem:
            return elem.text
