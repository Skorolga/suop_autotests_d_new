from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage

from src.logger.formatted_logger import logger

class ClientPage(BasicPage):
    """Класс описывает страницу клиента"""

    MENU_MAKE_ORDER = (By.XPATH, '//span[contains(text(), "Заказать услугу")]')
    BANNER_MAKE_ORDER = (By.XPATH, '//h4[contains(text(), "Виртуальная инфраструктура")]')
    BUTTON_MAKE_ORDER = (By.XPATH, '//button[contains(text(), "Заказать")]')
    TABLE_WITH_ORDERS_IN_LK = (By.XPATH, '//div[contains(@class, "items-table__dropdown")]')  # проверка загрузки стр. с заказами

    # локаторы заказа за клиента
    FORM_TITLE_CONF = (By.XPATH, '//h3[contains(text(), "Конфигурация")]')  # Для проверки загрузки страницы с формой заказа iaas
    COST_WITHOUT_TAX = (By.XPATH, '//div[@class="costs-value"]')

    def __init__(self, browser):
        super().__init__(browser)

    def make_order(self):
        """Метод создает заказ Публичное облако под уже авторизованным клиентом"""
        logger.info('Создание заказа Публичное облако за клиента')
        self.click_on_element(self.MENU_MAKE_ORDER)
        self.wait_for_page_loaded(self.BANNER_MAKE_ORDER)
        self.click_on_element(self.BANNER_MAKE_ORDER)
        self.click_on_element(self.BUTTON_MAKE_ORDER)

