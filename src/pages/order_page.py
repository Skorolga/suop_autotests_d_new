import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from allure_commons.types import AttachmentType
from src.pages.basic_page import BasicPage
from src.pages.orders_page import OrdersPage


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
    DOMAIN_DEL_BUTTON_YES = (By.XPATH, '//button[text()="Да"]')  # Кнопка удаления домена
    DOMAIN_TITLE = (By.XPATH, '//div[@class="section-title section-title--left"]')

    DOMAIN_ORDER_DROPDOWN = (By.XPATH, '//table//tbody/tr//td[4]')
    DOMAIN_ORDER_ADD_AN_ENTRY = (By.XPATH, '//div[contains(@class, "dns-records-bar__actions-wrapper")]//*[3]')  # Кнопка добавить ДНС запись
    DOMAIN_ENTRY_TITLE = (By.XPATH, '//div[contains(text(), "DNS записи")]')  # Для проверки загрузки настройки домена
    DOMAIN_ENTRY_SELECT = (By.XPATH, '//div[contains(@class, "select__value-container")]')  # Выпадающее меню "Тип записи"
    DOMAIN_ENTRY_SELECT_TYPE_A = (By.XPATH, '//div[contains(@id, "option") and text()="A"]')  # Тип А в выпадающем меню
    DOMAIN_ENTRY_SELECT_TYPE_MX = (By.XPATH, '//div[contains(@id, "option") and text()="MX"]')  # Тип MX в выпадающем меню
    DOMAIN_ENTRY_SELECT_TYPE_SRV = (By.XPATH, '//div[contains(@id, "option") and text()="SRV"]')  # Тип SRV в выпадающем меню
    DOMAIN_ENTRY_TYPE_A_HOST = (By.XPATH, '//input[contains(@name, "owner") and @class="input-element"]')  # Поле ввода хост
    DOMAIN_ENTRY_TYPE_A_IP = (By.XPATH, '//input[contains(@name, "rdata[ipv4addr]") and @class="input-element"]')  # Поле ввода ip
    DOMAIN_ENTRY_ADD_BUTTON = (By.XPATH, '//button[@type="button" and text()="Добавить"]')  # Кнопка добавить запись
    DOMAIN_ENTRY_TYPE_CNAME = (By.XPATH, '//input[contains(@name, "rdata[name]") and @class="input-element"]')  # Поле ввода поля "Хост назначения"
    DOMAIN_ENTRY_TYPE_MX_P = (By.XPATH, '//input[contains(@name, "rdata[preference]") and @class="input-element"]')  # Поле ввода поля "Приоритет"
    DOMAIN_ENTRY_TYPE_MX_HOST_DEST = (By.XPATH, '//input[contains(@name, "rdata[mail_exchanger]") and @class="input-element"]')  # Поле ввода поля "Хост назначения"
    DOMAIN_ENTRY_TYPE_SRV_HOST_DEST = (By.XPATH, '//input[contains(@name, "rdata[target]") and @class="input-element"]')  # Поле ввода поля "Хост назначения SRV"
    DOMAIN_ENTRY_TYPE_SRV_PORT = (By.XPATH, '//input[contains(@name, "rdata[port]") and @class="input-element"]')  # Поле ввода "Порт"
    DOMAIN_ENTRY_TYPE_SRV_WEIGHT = (By.XPATH, '//input[contains(@name, "rdata[weight]") and @class="input-element"]')  # Поле ввода "Вес"
    DOMAIN_ENTRY_TYPE_SRV_PRIORITY = (By.XPATH, '//input[contains(@name, "rdata[priority]") and @class="input-element"]')  # Поле ввода "Приоритет"


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

    def add_dns_entry_cname(self, sub_domain):
        """Добавляет DNS запись типа CNAME"""
        self.click(self.DOMAIN_ORDER_DROPDOWN)
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)
        assert self.wait_for_page_loaded(self.DOMAIN_ENTRY_TITLE), 'Отсутствует заголовок ДНС записей'
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)  # Добавить запись
        self.click(self.DOMAIN_ENTRY_SELECT)
        self.type(self.DOMAIN_ENTRY_TYPE_A_HOST, 'www')
        self.type(self.DOMAIN_ENTRY_TYPE_CNAME, f'{sub_domain}.cloud.rt-dc.ru')
        self.click(self.DOMAIN_ENTRY_ADD_BUTTON)
        WebDriverWait(self.browser, 30).until(
            EC.invisibility_of_element(
                OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда элемент исчезнет
        # self.browser.refresh()

    def add_dns_entry_mx(self, sub_domain):
        """Добавляет DNS запись типа MX"""
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)
        assert self.wait_for_page_loaded(self.DOMAIN_ENTRY_TITLE), 'Отсутствует заголовок ДНС записей'
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)  # Добавить запись
        self.click(self.DOMAIN_ENTRY_SELECT)
        self.click(self.DOMAIN_ENTRY_SELECT_TYPE_MX)
        self.type(self.DOMAIN_ENTRY_TYPE_A_HOST, sub_domain)
        self.type(self.DOMAIN_ENTRY_TYPE_MX_P, '10')  # Поле приоритет
        self.type(self.DOMAIN_ENTRY_TYPE_MX_HOST_DEST, 'mail.host.local')  # Поле приоритет
        self.click(self.DOMAIN_ENTRY_ADD_BUTTON)
        WebDriverWait(self.browser, 30).until(
            EC.invisibility_of_element(
                OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда элемент исчезнет

    def add_dns_entry_srv(self, sub_domain):
        """Добавляет DNS запись типа SRV (настройки для отдельных протоколов, например SIP)"""
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)
        assert self.wait_for_page_loaded(self.DOMAIN_ENTRY_TITLE), 'Отсутствует заголовок ДНС записей'
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)  # Добавить запись
        self.click(self.DOMAIN_ENTRY_SELECT)
        self.click(self.DOMAIN_ENTRY_SELECT_TYPE_SRV)
        self.type(self.DOMAIN_ENTRY_TYPE_A_HOST, sub_domain)
        self.type(self.DOMAIN_ENTRY_TYPE_SRV_HOST_DEST, 'target.host.local')  # Поле "Хост назначения"
        self.type(self.DOMAIN_ENTRY_TYPE_SRV_PORT, '8080')  # Поле приоритет
        self.type(self.DOMAIN_ENTRY_TYPE_SRV_WEIGHT, '10')
        self.type(self.DOMAIN_ENTRY_TYPE_SRV_PRIORITY, '50')
        self.click(self.DOMAIN_ENTRY_ADD_BUTTON)
        WebDriverWait(self.browser, 30).until(
            EC.invisibility_of_element(
                OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда элемент исчезнет

    def add_dns_entry_a(self):
        """Добавляет DNS запись типа A"""
        # self.click(self.DOMAIN_ORDER_DROPDOWN)  # Настройки домена уже раскрыты функцией add_dns_entry_cname()
        self.click(self.DOMAIN_ORDER_ADD_AN_ENTRY)
        assert self.wait_for_page_loaded(self.DOMAIN_ENTRY_TITLE), 'Отсутствует заголовок ДНС записей'
        self.click(self.DOMAIN_ENTRY_SELECT)  # Выпадающее меню выбора
        self.click(self.DOMAIN_ENTRY_SELECT_TYPE_A)
        self.type(self.DOMAIN_ENTRY_TYPE_A_HOST, 'www')  # Локатор идентичный А записи
        self.type(self.DOMAIN_ENTRY_TYPE_A_IP, '1.1.1.1')
        self.click(self.DOMAIN_ENTRY_ADD_BUTTON)
        WebDriverWait(self.browser, 30).until(
            EC.invisibility_of_element(
                OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда элемент исчезнет

    def del_sub_domain(self, sub_domain):
        """Удаление добавленного поддомена"""
        DEL_SUB_DOMAIN = (By.XPATH, f'//td[contains(text(), "{sub_domain}")]/following::td[2]/div')
        self.click(DEL_SUB_DOMAIN)
        self.click(self.DOMAIN_DEL_BUTTON_YES)
        assert self.wait_for_page_loaded(self.DOMAIN_ADD_BUTTON)  # Ждем удаления домена