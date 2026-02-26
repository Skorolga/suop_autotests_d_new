import time

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from src.logger.formatted_logger import logger
from config.config import SUOP
from pywinauto.keyboard import send_keys
from pywinauto import Application


class BasicPage(object):
    """Основной класс для страниц"""
    timeout = 60

    def __init__(self, browser):
        self.browser = browser

    def find_elem(self, locator:tuple[str, str], timeout=timeout) -> WebElement | bool:
        """Поиск элемента по локатору, возвращает элемент или bool"""
        element = None
        # Проверяем наличие элемента на странице
        try:
            element = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
            # logger.info(f'Элемент {locator[1]} найден')
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
        time.sleep(2)  # ждем завершение анимации скролла

    def click(self, locator:tuple[str, str], timeout=timeout):
        """Находит и кликает по элементу"""
        # element = self.find_elem(locator, timeout)
        element = WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator))
        if element:
            try:
                element.click()
                logger.info(f'Клик по элементу: {locator[1]}')
            except Exception as error:
                logger.warning(f'Элемент {locator[1]} не виден. Метод: click())')
                logger.info(f'Видимость элемента: {element.is_displayed()}')
                try:
                    self.scroll_to_element(element)
                    element.click()
                    logger.info(f'Клик по элементу после скролла: {locator[1]}')
                except Exception as error:
                    logger.info(f'Не удалось проскролить до элемента {locator[1]}')
                    self.browser.execute_script('arguments[0].click();', element)  # кликаем если элемент есть, но кликнуть штатно не получилось

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
                # при ошибке делаем скрин и сохраняем исходник для отладки
                try:
                    filename = "wait_for_page_loaded_failure"
                    self.browser.save_screenshot(f"{filename}.png")
                    logger.info(f"Скриншот страницы сохранен в {filename}.png")
                    page_source = self.browser.page_source
                    with open(f"{filename}.html", "w", encoding="utf-8") as f:
                        f.write(page_source)
                    logger.info(f"Исходник страницы сохранен в {filename}.html")
                except Exception as e:
                    logger.warning(f"Не удалось сохранить артефакты страницы: {e}")
                return False

    def save_scr(self, file_name:str):
        """Сохраняет скриншот в текущий каталог"""
        self.wait_for_page_loaded()
        if self.page_has_loaded():
            self.browser.save_screenshot(f'{file_name}.png')

    def get_screenshot_safe(self):
        """Get screenshot, dismissing any alerts that appear"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                return self.browser.get_screenshot_as_png()
            except Exception as alert_error:
                if 'UnexpectedAlertPresentException' in str(type(alert_error)) or 'Alert' in str(alert_error):
                    try:
                        alert = self.browser.switch_to.alert
                        alert.dismiss()
                        logger.info(f'Alert dismissed during screenshot (attempt {attempt + 1})')
                    except:
                        pass  # No alert to dismiss
                    if attempt == max_attempts - 1:
                        raise
                else:
                    raise

    def type(self, locator, text):
        """Набирает тест"""
        self.browser.find_element(*locator).send_keys(text)

    def handle_basic_auth(self, login: str | None = None, password: str | None = None, timeout: int = 5):
        """Обработка диалога базовой автентификации.
        
        Для Firefox: диалог открывается. Мы кликаем OK чтобы Firefox использовал
        встроенные в URL учетные данные (https://user:pass@host).
        """
        try:
            alert = WebDriverWait(self.browser, timeout).until(EC.alert_is_present())
            alert.accept()  # кликаем OK для использования встроенных в URL учетных данных
            logger.info('Basic auth dialog accepted')
        except Exception:
            pass  # если нет никакого алерта

    def get_text(self, locator):
        elem = self.find_elem(locator)
        if elem:
            return elem.text

    def custom_clear(self, locator):
        """Кастомный метод очистки текстового поля"""
        try:
            elem = self.find_elem(locator)
            if elem:
                elem.click()
                elem.send_keys(Keys.BACKSPACE*10)
                time.sleep(0.5)  # После удаления фронт дописывает 0, жмем Backspace ещё раз
                elem.send_keys(Keys.BACKSPACE)
        except Exception as e:
            logger.warning('Не удалось очистить текстовое поле кастомным методом класса base_page')


