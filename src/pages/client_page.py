import time
from datetime import datetime
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage
from src.logger.formatted_logger import logger


class ClientPage(BasicPage):
    """Класс описывает страницу клиента"""

    MENU_MAKE_ORDER = (By.XPATH, '//span[contains(text(), "Заказать услугу")]')
    BANNER_MAKE_ORDER = (By.XPATH, '//a[@href="/showcase/services/iaas"]')
    BUTTON_MAKE_ORDER = (By.XPATH, '//button[contains(text(), "Заказать")]')
    TABLE_WITH_ORDERS_IN_LK = (By.XPATH, '//div[contains(@class, "items-table__dropdown")]')  # Проверка загрузки стр. с заказами

    # локаторы заказа за клиента
    FORM_TITLE_CONF = (By.XPATH, '//h3[contains(text(), "Конфигурация")]')  # Для проверки загрузки страницы с формой заказа iaas
    RADIOBUTTON_NEW_ORDER = (By.XPATH, '//div[contains(text(), "Создать новый заказ")]')  # Радиобаттон создать iaas в новом заказе
    COST_WITHOUT_TAX = (By.XPATH, '//div[@class="costs-value"]')
    SUBMIT_BUTTON = (By.XPATH, '//button[@type="submit"]')  # Кнопка заказать
    NEW_ORDER_NUM = (By.XPATH, '//p[contains(text(), "№")]')  # Локатор модального окна с номером созданного заказа
    PARENT_ORDER_NUM = (By.XPATH, '//span[contains(text(), "Заказ №")]')  # Локатор для получения номера родительского заказа
    GO_TO_ORDER = (By.XPATH, '//button[contains(text(), "К заказу")]')  # Кнопка для перехода к заказу из модального окна при создании нового заказа
    VIRT_MACH_TITLE = (By.XPATH, '//div[contains(text(), "Виртуальные машины")]')  # Заголовок в заказе для ожидания загрузки страницы

    def __init__(self, browser):
        super().__init__(browser)

    def make_order(self, timeout=360) -> str:
        """Метод создает заказ Публичное облако под уже авторизованным клиентом и возвращает номер заказа"""
        logger.info('Создание заказа Публичное облако за клиента')
        self.click(self.MENU_MAKE_ORDER)
        # self.wait_for_page_loaded(self.BANNER_MAKE_ORDER)
        self.click(self.BANNER_MAKE_ORDER)
        self.click(self.BUTTON_MAKE_ORDER)
        self.wait_for_page_loaded(self.FORM_TITLE_CONF)
        self.click(self.RADIOBUTTON_NEW_ORDER)  # Радиокнопка для создания iaas в новом заказе
        # проверяем начисление
        cost = self.check_cost(self.COST_WITHOUT_TAX)
        logger.info(f'Начисленная стоимость за заказ "Виртуальная инфраструктура" в сутки без НДС: {str(cost)}')
        assert cost, f'Ошибка в начислении суммы заказа по локатору {self.COST_WITHOUT_TAX}'
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Страница с формой для создания заказа',
            attachment_type=AttachmentType.PNG
        )
        self.click(self.SUBMIT_BUTTON)  # Итоговая кнопка создания заказа
        # ждем создания заказа и получаем его номер
        self.wait_for_page_loaded(self.NEW_ORDER_NUM, 180)
        start_time = datetime.now()
        while True:
            time_difference = datetime.now() - start_time
            if time_difference.total_seconds() > timeout:
                logger.error('timeout при создании заказа')
                return False
            order_num = self.find_elem(self.NEW_ORDER_NUM).text
            if type(order_num) != str:
                continue
            order_num = ''.join([symb for symb in order_num if symb.isdigit()])
            if int(order_num) > 0:
                logger.info(f'Создан заказ № {order_num}')
                break
            time.sleep(0.5)
        allure.attach(
            body=str(order_num),
            name="Номер созданного заказа (дочернего)",
            attachment_type=AttachmentType.TEXT,
        )
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Скриншот созданного заказа (дочернего)',
            attachment_type=AttachmentType.PNG
        )
        self.click(self.GO_TO_ORDER)
        self.wait_for_page_loaded(self.VIRT_MACH_TITLE)
        parent_order_name = self.find_elem(self.PARENT_ORDER_NUM).text
        parent_order_name = ''.join([symb for symb in parent_order_name if symb.isdigit()])
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Страница созданного заказа',
            attachment_type=AttachmentType.PNG
        )
        allure.attach(
            body=str(order_num),
            name="Номер созданного заказа (родительского)",
            attachment_type=AttachmentType.TEXT,
        )
        return parent_order_name

    def check_cost(self, cost_locator, timeout=20) -> float|bool:
        """Проверяет наличие суммы > 0 по локатору"""
        start_time = datetime.now()
        while True:
            # Следим за timeout
            time_difference = datetime.now() - start_time
            if time_difference.total_seconds() > timeout:
                logger.error('timeout при поиске и проверке начисления стоимости заказа без НДС')
                return False
            try:
                order_cost_without_tax = self.find_elem(cost_locator).text
                order_cost_without_tax = float(order_cost_without_tax.strip())
                logger.info(order_cost_without_tax)
                if order_cost_without_tax > 0:
                    return order_cost_without_tax
            except Exception as e:
                continue
            time.sleep(1)
