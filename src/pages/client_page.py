from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage

from src.logger.formatted_logger import logger

class ClientPage(BasicPage):
    """Класс описывает страницу клиента"""

    MENU_MAKE_ORDER = (By.XPATH, '//span[contains(text(), "Заказать услугу")]')
    BANNER_MAKE_ORDER = (By.XPATH, '//h4[contains(text(), "Виртуальная инфраструктура")]')
    TABLE_WITH_ORDERS_IN_LK = (By.XPATH, '//div[contains(@class, "items-table__dropdown")]')  # проверка загрузки стр.

    def __init__(self, browser):
        super().__init__(browser)

    def create_order(self):
        """Метод создает заказ Публичное облако под уже авторизованным клиентом"""
        logger.info('Создание заказа Публичное облако за клиента')
        self.click_on_element(self.MENU_MAKE_ORDER)
        self.wait_for_page_loaded(self.BANNER_MAKE_ORDER)
        self.click_on_element(self.BANNER_MAKE_ORDER)

