import time
from datetime import datetime
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage
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

    def find_order(self, num_order):
        self.click_on_element(self.FILTER_CLEAN_BUTTON)  # Сброс фильтров для поиска заказов
        self.click_on_element(self.FILTER_FOR_FIND_ORDERS)
        self.send_text(self.FILTER_INPUT_ID_ORDER, num_order)
        self.click_on_element(self.FILTER_FORM_APPLY_BUTTON)
        self.wait_for_page_loaded(self.ORDER_BUTTON_APPROVE_MANAGER)

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
        self.wait_for_page_loaded(self.ORDER_DELETE)
        self.click_on_element(self.ORDER_DELETE)
        self.click_on_element(self.ORDER_DELETE_MODAL_YES)
        self.browser.refresh()
        self.wait_for_page_loaded(self.ORDER_STATUS_CHANGE, 540)
        self.browser.refresh()
        self.wait_for_page_loaded(self.ORDER_STATUS_DELETED, 540)

    def approve_order(self, num_order):
        logger.info('Согласование заказа')
        self.find_elem(self.ORDER_BUTTON_APPROVE_MANAGER)
        self.click_on_element(self.ORDER_BUTTON_APPROVE_MANAGER)
        self.click_on_element(self.ORDER_BUTTON_APPROVE_MANAGER_2)
        self.wait_for_page_loaded(self.ORDER_STATUS_CHANGE, 540)
        self.wait_for_page_loaded(self.ORDER_STATUS_READY, 540)

    def check_order_status(self, num_order, timeout):
        pass

