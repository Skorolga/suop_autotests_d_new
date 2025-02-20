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
    DOMAIN_TITLE = (By.XPATH, '')
    DOMAIN_TITLE = (By.XPATH, '')
    DOMAIN_TITLE = (By.XPATH, '')
    DOMAIN_TITLE = (By.XPATH, '')
    DOMAIN_TITLE = (By.XPATH, '')
    DOMAIN_TITLE = (By.XPATH, '')
    DOMAIN_TITLE = (By.XPATH, '')
