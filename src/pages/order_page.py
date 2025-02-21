import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pages.basic_page import BasicPage
from src.pages.client_page import ClientPage
from src.logger.formatted_logger import logger


class OrderPage(BasicPage):
    """Класс описывает страницу заказа за клиента"""

    def __init__(self, browser):
        super().__init__(browser)

    MENU_INF_NETWORK = (By.XPATH, '//span[contains(text(), "Инфраструктура и")]')
    MENU_INF_NETWORK__DNS = (By.XPATH, '//button[contains(text(), "Управление DNS")]')

    DOMAIN_TITLE = (By.XPATH, '//div[@class="section-title section-title--left"]')
    DOMAIN_ORDER_DROPDOWN = (By.XPATH, '//table//tbody/tr//td[4]')
    DOMAIN_ORDER_ADD_AN_ENTRY = (By.XPATH, '//div[contains(@class, "dns-records-bar__actions-wrapper")]//*[3]')  # Кнопка добавить ДНС запись
    DOMAIN_ENTRY_TITLE = (By.XPATH, '//div[contains(text(), "DNS записи")]')  # Для проверки загрузки настройки домена
    DOMAIN_ENTRY_SELECT = (By.XPATH, '//div[contains(@class, "select__value-container")]')  # Выпадающее меню "Тип записи"
    DOMAIN_ENTRY_SELECT_TYPE_A = (By.XPATH, '//div[contains(@id, "option") and text()="A"]')  # Тип А в выпадающем меню
    DOMAIN_ENTRY_TYPE_A_HOST = (By.XPATH, '//input[contains(@name, "owner") and @class="input-element"]')  # Поле ввода хост
    DOMAIN_ENTRY_TYPE_A_IP = (By.XPATH, '//input[contains(@name, "rdata[ipv4addr]") and @class="input-element"]')  # Поле ввода ip
    DOMAIN_ENTRY_ADD_BUTTON = (By.XPATH, '//button[@type="button" and text()="Добавить"]')  # Кнопка добавить запись
    # DOMAIN_TITLE = (By.XPATH, '')

