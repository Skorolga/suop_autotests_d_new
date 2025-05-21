import time
from datetime import datetime
import allure
from allure_commons.types import AttachmentType

from src.logger.formatted_logger import logger
from src.pages.basic_page import BasicPage
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class KuberService(BasicPage):
    """Класс описывает сервис kubernetes. Роль - клиент"""

    def __init__(self, browser):
        super().__init__(browser)
        self.client_page = ClientPage(browser)
        self.order_page = OrdersPage(browser)

    KUBER_MAKE_ORDER_TITLE = (By.XPATH, '//h4[contains(text(), "Конфигурация кластера")]')
    ORDER_STATUS = (By.XPATH, '//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
    ORDER_STATUS_TEXT = (By.XPATH, '//div[@class="suborder-state-status"]//p[@class="icon-hint__text"]')
    K8S_ORDER_DROPDOWN = (By.XPATH, '//table//tbody/tr//td[5]')  # Раскрыть заказ kubernetes
    K8S_ORDER_INFO_TITLE = (By.XPATH, '//div[@class="heading-title"][contains(text(), "Параметры кластера Kubernetes")]')
    K8S_ORDER_INFO_DATE = (By.XPATH, '//div[contains(text(), "Дата создания")]')
    K8S_ORDER_DEL = (By.XPATH, '//*[@id="close"]/parent::*')  # Кнопка удаления заказа


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
            name='Модальное окно созданного заказа (дочернего)',
            attachment_type=AttachmentType.PNG
        )
        self.click(ClientPage.GO_TO_ORDER)
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60*3,
                                   hover_element=self.ORDER_STATUS)

    def check_info_tab(self):
        """Проверка вкладки Информация в заказе Kubernetes"""
        self.click(self.K8S_ORDER_DROPDOWN)
        elem_for_scroll = self.find_elem(self.K8S_ORDER_INFO_DATE)
        self.scroll_to_element(elem_for_scroll)
        assert self.wait_for_page_loaded(self.K8S_ORDER_INFO_TITLE), 'Отсутствует заголовок вкладки Информация'

    def del_k8s_order(self):
        """Удаление дочернего заказа Kubernetes"""
        elem_for_del = (By.XPATH, '//td/div/*[contains(text(), "Кластер Kubernetes")]/following::td[3]//*[@id="close"]')
        self.click(elem_for_del)
        self.click(OrdersPage.ORDER_POWER_OFF_MODAL_YES)
        self.find_elem(self.ORDER_STATUS_TEXT)
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Удаление хранилища',
                                   refresh_timeout=60*3,
                                   hover_element=self.ORDER_STATUS)
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Удаление кластера',
                                   refresh_timeout=60*3,
                                   hover_element=self.ORDER_STATUS)
        WebDriverWait(self.browser, 60*30).until(
            EC.invisibility_of_element_located((By.XPATH, '//td/div/*[contains(text(), "Кластер Kubernetes")]'))
        )  # Ждем когда элемент исчезнет
        assert self.find_elem(elem_for_del, 10) == False  # Ждем удаления
