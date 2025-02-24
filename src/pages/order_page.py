import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from allure_commons.types import AttachmentType
from src.pages.basic_page import BasicPage
from src.pages.orders_page import OrdersPage
from src.pages.client_page import ClientPage
from src.logger.formatted_logger import logger


class OrderPage(BasicPage):
    """Класс описывает страницу заказа за клиента"""

    def __init__(self, browser):
        super().__init__(browser)

    MENU_INF_NETWORK = (By.XPATH, '//span[contains(text(), "Инфраструктура и")]')
    MENU_INF_NETWORK__DNS = (By.XPATH, '//button[contains(text(), "Управление DNS")]')
    DOMAIN_ADD_BUTTON = (By.XPATH, '//button[contains(text(), "Заказать")]')  # Кнопка добавления домена (Заказать)
    DOMAIN_ADD_SELECT = (By.XPATH, '//div[contains(@class, "select__value-container select__value-container--has-value")]')
    DOMAIN_ADD_SELECT_VALUE = (By.XPATH, '//div[contains(@id, "option-1")]')  # Выпадающее меню, выбор поддомена
    DOMAIN_ADD_INPUT = (By.XPATH, '//input[contains(@name, "domain") and @class="input-element"]')  # Кнопка добавления домена (Заказать)
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

    def add_sub_domain(self, sub_domain):
        """Добавляет поддомен в домен cloud.rt-dc.ru"""
        self.click(self.MENU_INF_NETWORK)
        self.click(self.MENU_INF_NETWORK__DNS)  # Раскрываем в меню настройки ДНС
        # self.wait_for_page_loaded(self.DOMAIN_TITLE)
        self.click(self.DOMAIN_ADD_BUTTON)
        self.click(self.DOMAIN_ADD_SELECT)
        self.click(self.DOMAIN_ADD_SELECT_VALUE)
        self.type(self.DOMAIN_ADD_INPUT, sub_domain)
        self.click(self.DOMAIN_ENTRY_ADD_BUTTON)
        time.sleep(1)
        WebDriverWait(self.browser, 30).until(
            EC.invisibility_of_element(OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда элемент исчезнет
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Добавленный домен',
            attachment_type=AttachmentType.PNG
        )
        
    def add_dns_entry_a(self):
        self.click(self.DOMAIN_ORDER_DROPDOWN)
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)
        assert self.wait_for_page_loaded(self.DOMAIN_ENTRY_TITLE), 'Отсутствует заголовок ДНС записей'
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)  # Добавить запись
        self.click(self.DOMAIN_ENTRY_SELECT)
        self.click(self.DOMAIN_ENTRY_SELECT_TYPE_A)
        self.type(self.DOMAIN_ENTRY_TYPE_A_HOST, 'www')
        self.type(self.DOMAIN_ENTRY_TYPE_A_IP, '1.1.1.1')
        self.click(self.DOMAIN_ENTRY_ADD_BUTTON)
        WebDriverWait(self.browser, 30).until(
            EC.invisibility_of_element(
                OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда элемент исчезнет
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='DNS запись типа А',
            attachment_type=AttachmentType.PNG
        )