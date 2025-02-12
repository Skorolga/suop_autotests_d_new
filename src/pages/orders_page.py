import time
from datetime import datetime
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.basic_page import BasicPage
from src.pages.client_page import ClientPage
from src.logger.formatted_logger import logger


class OrdersPage(BasicPage):
    """Класс описывает страницу с заказами в личном кабинете"""

    FILTER_CLEAN_BUTTON = (By.XPATH, '//button[contains(text(), "Очистить все")]')
    FILTER_FOR_FIND_ORDERS = (By.XPATH, '//header/div[contains(@class,"btn-wrapper--single-icon")]/button')
    FILTER_INPUT_ID_ORDER = (By.XPATH, '//input[@name="id"]')
    FILTER_FORM_APPLY_BUTTON = (By.XPATH, '//button[contains(text(), "Применить")]')

    # создание заказа
    ORDER_PARAM_TAB = (By.XPATH, '//button[contains(text(), "Параметры и ограничения")]')
    ORDER_BUTTON_APPROVE_MANAGER = (By.XPATH, '//button[contains(text(), "Согласовать перевод заказа в тестовый режим")]')
    ORDER_BUTTON_APPROVE_MANAGER_2 = (By.XPATH, '//button[contains(text(), "Перевести в тестовый режим")]')  # Еще раз подтверждаем согласование заказа

    # заказ
    ORDER_STATUS = (By.XPATH, '//div[contains(@class, "statusText")]')
    ORDER_STATUS_CHANGE = (By.XPATH, '//div[contains(text(), "Изменение объема ресурсов")]')
    ORDER_STATUS_READY = (By.XPATH, '//div[contains(text(), "Работает")]')
    ORDER_STATUS_SHUTDOWN = (By.XPATH, '//div[contains(text(), "Выключение")]')
    ORDER_STATUS_STOPPED = (By.XPATH, '//div[contains(text(), "Выключен")]')
    ORDER_STATUS_DELETED = (By.XPATH, '//div[contains(text(), "Удален")]')
    ORDER_POWER_OFF = (By.XPATH, '//button[contains(text(), "Выключить заказ")]')
    ORDER_POWER_OFF_MODAL_YES = (By.XPATH, '//button[contains(text(), "Да")]')
    ORDER_DELETE = (By.XPATH, '//button[contains(text(), "Освободить ресурсы")]')
    ORDER_DELETE_MODAL_YES = (By.XPATH, '//button[contains(text(), "Да")]')


    def __init__(self, browser):
        super().__init__(browser)

    def find_order(self, num_order:str):
        self.browser.refresh()
        self.click_on_element(self.FILTER_CLEAN_BUTTON)  # Сброс фильтров для поиска заказов
        WebDriverWait(self.browser, 30).until(EC.invisibility_of_element(self.FILTER_CLEAN_BUTTON))  # ждем когда элемент исчезнет
        # self.wait_for_page_loaded(ClientPage.TABLE_WITH_ORDERS_IN_LK, 60)
        time.sleep(2)
        self.click_on_element(self.FILTER_FOR_FIND_ORDERS)
        time.sleep(2)
        self.send_text(self.FILTER_INPUT_ID_ORDER, num_order)
        time.sleep(2)
        self.click_on_element(self.FILTER_FORM_APPLY_BUTTON)
        self.wait_for_page_loaded(ClientPage.TABLE_WITH_ORDERS_IN_LK)
        composite_locator = (By.XPATH, f'//div[contains(@class, "orderRow")]/div[contains(text(), "{num_order}")]')
        self.wait_for_page_loaded(composite_locator, 60)

    def clean_filter_for_find_orders(self):
        """Очистка параметров фильтра поиска страницы с заказами"""
        self.click_on_element(self.FILTER_CLEAN_BUTTON)

    def del_order(self, num_order):
        logger.info('Удаление заказа')
        self.browser.refresh()
        logger.info('Обновление')
        self.find_order(num_order)
        self.click_on_element(self.ORDER_POWER_OFF)
        self.click_on_element(self.ORDER_POWER_OFF_MODAL_YES)
        self.browser.refresh()
        self.wait_for_page_loaded(self.ORDER_STATUS_SHUTDOWN, 540)
        self.browser.refresh()
        self.wait_for_page_loaded(self.ORDER_STATUS_STOPPED, 540)
        self.browser.refresh()
        self.wait_for_page_loaded(self.ORDER_DELETE, 540)
        self.click_on_element(self.ORDER_DELETE)
        self.click_on_element(self.ORDER_DELETE_MODAL_YES)
        self.browser.refresh()
        self.wait_for_page_loaded(self.ORDER_STATUS_CHANGE, 540)
        self.browser.refresh()
        self.wait_for_page_loaded(self.ORDER_STATUS_DELETED, 540)

    def approve_order(self, num_order):
        logger.info('Согласование заказа')
        # self.wait_for_page_loaded(self.ORDER_BUTTON_APPROVE_MANAGER)
        # self.find_elem(self.ORDER_BUTTON_APPROVE_MANAGER)
        self.click_on_element(self.ORDER_BUTTON_APPROVE_MANAGER)
        self.click_on_element(self.ORDER_BUTTON_APPROVE_MANAGER_2)
        self.wait_for_page_loaded(self.ORDER_STATUS_CHANGE, 540)
        self.wait_for_page_loaded(self.ORDER_STATUS_READY, 540)

    def text_check(self, locator, text_trigger, timeout):
        start_time = datetime.now()
        current_text = self.find_elem(locator).text
        logger.info(f'Состояние заказа: {current_text}')
        i = 0
        while True:
            # установка таймаута
            time_difference = datetime.now() - start_time
            if time_difference.total_seconds() > timeout:
                logger.error('timeout при ожидании изменения статуса')
                return False

            i += 1
            logger.info(f'Итерация №: {i} Прошло: {time_difference} сек')
            self.browser.refresh()
            actual_text = self.find_elem(locator).text
            if actual_text == text_trigger:
                logger.info(f'Ожидаемое состояние достигнуто: {actual_text}')
                return True
            elif current_text != actual_text:
                logger.info(f'Состояние изменилось: {actual_text}')
                current_text = actual_text
            else:  # Если найдено триггерное слово завершаем проверку
                logger.info(f'Состояние не изменилось')
            time.sleep(10)

    def del_order_dev(self, num_order):
        logger.info('Удаление заказа del_order_dev()')
        self.browser.refresh()  # обновляем страницу, баг с появлением УЗ Клиента
        logger.info('Обновление страницы')
        self.find_order(num_order)
        self.click_on_element(self.ORDER_POWER_OFF)
        self.click_on_element(self.ORDER_POWER_OFF_MODAL_YES)
        self.text_check(self.ORDER_STATUS, 'Выключен', 60*10)
        self.browser.refresh()
        # self.wait_for_page_loaded(self.ORDER_STATUS_SHUTDOWN, 540)
        # self.browser.refresh()
        # self.wait_for_page_loaded(self.ORDER_STATUS_STOPPED, 540)
        # self.browser.refresh()
        # self.wait_for_page_loaded(self.ORDER_DELETE, 540)
        self.click_on_element(self.ORDER_DELETE, 60*3)
        self.click_on_element(self.ORDER_DELETE_MODAL_YES, 60*3)
        # self.browser.refresh()
        # self.wait_for_page_loaded(self.ORDER_STATUS_CHANGE, 540)
        # self.browser.refresh()
        # self.wait_for_page_loaded(self.ORDER_STATUS_DELETED, 540)
        self.text_check(self.ORDER_STATUS, 'Удален', 60 * 10)





