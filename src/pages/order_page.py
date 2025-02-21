import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.basic_page import BasicPage
from src.pages.client_page import ClientPage
from src.logger.formatted_logger import logger


class OrderPage(BasicPage):
    """Класс описывает страницу заказа"""

    def __init__(self, browser):
        super().__init__(browser)

    MENU_INF_NETWORK = (By.XPATH, '//span[contains(text(), "Инфраструктура и")]')
    MENU_INF_NETWORK__DNS = (By.XPATH, '//button[contains(text(), "Управление DNS")]')

    DOMAIN_TITLE = (By.XPATH, '//div[@class="section-title section-title--left"]')
    DOMAIN_ORDER_DROPDOWN = (By.XPATH, '//table//tbody/tr//td[4]')
    DOMAIN_ORDER_ADD_AN_ENTRY = (By.XPATH, '//div[contains(@class, "dns-records-bar__action-icon")]//'
                                           '*[local-name()="svg" and @id="add"]')  # кнопка добавить ДНС запись
    # DOMAIN_TITLE = (By.XPATH, '')

