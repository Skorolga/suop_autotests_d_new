import time
from datetime import datetime
import allure
from allure_commons.types import AttachmentType

from src.logger.formatted_logger import logger
from src.pages.basic_page import BasicPage
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
from selenium.webdriver.common.by import By


class KuberService(BasicPage):
    """Класс описывает сервис kubernetes. Роль - клиент"""

    def __init__(self, browser):
        super().__init__(browser)
        self.client_page = ClientPage(browser)
        self.order_page = OrdersPage(browser)

    KUBER_MAKE_ORDER_TITLE = (By.XPATH, '//h4[contains(text(), "Конфигурация кластера")]')
    ORDER_STATUS = (By.XPATH, '//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
    ORDER_STATUS_TEXT = (By.XPATH, '//div[@class="suborder-state-status"]//p[@class="icon-hint__text"]')


    def make_k8s_order(self, timeout=360) -> str | bool:
        """Создает заказ kubernetes"""
        logger.info('Создание заказа kubernetes')
        self.click(ClientPage.MENU_MAKE_ORDER)  # Верхнее меню
        self.click(ClientPage.BANNER_MAKE_KUBER_ORDER)  # Карточка с услугой kubernetes
        self.click(ClientPage.BUTTON_MAKE_ORDER)  # Кнопка заказать
        self.wait_for_page_loaded(self.KUBER_MAKE_ORDER_TITLE)
        # проверяем начисление
        cost = self.client_page.check_cost(ClientPage.COST_WITHOUT_TAX)
        logger.info(f'Начисленная стоимость за заказ "Виртуальная инфраструктура" в сутки без НДС: {str(cost)}')
        assert cost, f'Ошибка в начислении суммы заказа по локатору {ClientPage.COST_WITHOUT_TAX}'
        self.click(ClientPage.SUBMIT_BUTTON)  # Итоговая кнопка создания заказа
        # ждем создания заказа и получаем его номер
        self.wait_for_page_loaded(ClientPage.NEW_ORDER_NUM, 180)
        start_time = datetime.now()
        while True:
            time_difference = datetime.now() - start_time
            if time_difference.total_seconds() > timeout:
                logger.error('timeout при создании заказа')
                return False
            order_num = self.find_elem(ClientPage.NEW_ORDER_NUM).text
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
        self.click(ClientPage.GO_TO_ORDER)
        self.order_page.text_check(self.ORDER_STATUS_TEXT, 'Работает', 60*15, self.ORDER_STATUS)

    # @staticmethod
    # def is_ready(timeout=60*20) -> bool:
    #     """Ждет перехода в состояние Работает"""
    #     start_time = datetime.now()
    #     while True:
    #         # Установка таймаута
    #         time_difference = datetime.now() - start_time
    #         if time_difference.total_seconds() > timeout:
    #             logger.error('timeout при ожидании изменения статуса')
    #             return False

