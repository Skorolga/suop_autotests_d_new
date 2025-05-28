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
    K8S_ORDER_NODES = (By.XPATH, '//button[contains(text(), "Узлы")]')  # Раздел Узлы в заказе k8s
    K8S_ORDER_NODES_MASTER_DATA = (By.XPATH, '//p[contains(text(), "Мастер-узлы")]')  # Строка Мастер-узлы в таблице
    K8S_ORDER_NODES_ADD_NODES = (By.XPATH, '//div/span[contains(text(), "Добавить группу узлов")]')  # Строка Мастер-узлы в таблице
    K8S_ORDER_NODES_ADD_NODES_NAME = (By.XPATH, '//input[contains(@id, "name")]')  # Название узла
    K8S_ORDER_NODES_ADD_NODES_COUNTS = (By.XPATH, '//input[contains(@name, "workers_count")]')  # Количество узлов
    K8S_ORDER_NODES_ADD_NODES_VCPU = (By.XPATH, '//input[contains(@name, "vcpu")]')  # Количество CPU
    K8S_ORDER_NODES_ADD_NODES_RAM = (By.XPATH, '//input[contains(@name, "vram")]')  # Количество RAM
    K8S_ORDER_NODES_ADD_NODES_DISK_SIZE = (By.XPATH, '//input[contains(@name, "datastore_size")]')  # Объем диска
    K8S_ORDER_NODES_ADD_NODES_ADD_BUTTON = (By.XPATH, '//button[text()="Добавить"]')  # Кнопка добавления узла
    K8S_ORDER_NODES_ADD_NODES_DEL_BUTTON = (By.XPATH, '//button[text()="Да"]')  # Кнопка добавления узла
    K8S_ORDER_NET = (By.XPATH, '//button[contains(text(), "Сеть")]')  # Раздел Сеть в заказе k8s
    K8S_ORDER_NET_TABLE_TITLE = (By.XPATH, '//th[text()="NAT правило"]'
                                           '[following-sibling::th[1][text()="Статус"]]'
                                           '[following-sibling::th[2][text()="ВМ"]]')  # Заголовок таблицы Сеть
    K8S_ORDER_NET_ADD_RULE = (By.XPATH, '//span[text()="Добавить правило"]')
    K8S_ORDER_NET_ADD_RULE_NAME = (By.XPATH, '//input[@name="title"]')  # поле ввода наименования правила
    K8S_ORDER_NET_ADD_RULE_SOURCE = (By.XPATH, '//input[@name="source"]')  # поле ввода источника
    K8S_ORDER_NET_ADD_RULE_DEST_PORT = (By.XPATH, '//input[@name="destination_port"]')  # поле ввода порт назначения
    K8S_ORDER_NET_ADD_RULE_TRANSLATION = (By.XPATH, '//input[@name="translated"]')  # поле ввода адреса трансляции
    K8S_ORDER_NET_ADD_RULE_TRANSLATION_PORT = (By.XPATH, '//input[@name="translated_port"]')  # поле ввода порта трансляции


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
                logger.info(f'Создан заказ Kubernetes № {order_num}')
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
        self.click(self.K8S_ORDER_DROPDOWN)  # TODO вынести в отдельную фн.
        elem_for_scroll = self.find_elem(self.K8S_ORDER_INFO_DATE)
        self.scroll_to_element(elem_for_scroll)
        assert self.wait_for_page_loaded(self.K8S_ORDER_INFO_TITLE), 'Отсутствует заголовок вкладки Информация'

    def check_nodes_tab(self):
        """Проверка вкладки Узлы в заказе Kubernetes"""
        self.click(self.K8S_ORDER_NODES)  # Открываем вкладку Узлы
        self.wait_for_page_loaded(self.K8S_ORDER_NODES_MASTER_DATA)
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Раздел Узлы',
            attachment_type=AttachmentType.PNG
        )
        self.click(self.K8S_ORDER_NODES_ADD_NODES)
        # time.sleep(5)
        node_name = f'autotest{abs(hash(datetime.now()))}'  # Наименование группы узлов
        self.type(self.K8S_ORDER_NODES_ADD_NODES_NAME, node_name)
        self.custom_clear(self.K8S_ORDER_NODES_ADD_NODES_COUNTS)
        self.type(self.K8S_ORDER_NODES_ADD_NODES_COUNTS, '4')
        self.custom_clear(self.K8S_ORDER_NODES_ADD_NODES_VCPU)
        self.type(self.K8S_ORDER_NODES_ADD_NODES_VCPU, '8')
        self.custom_clear(self.K8S_ORDER_NODES_ADD_NODES_RAM)
        self.type(self.K8S_ORDER_NODES_ADD_NODES_RAM, '8')
        self.custom_clear(self.K8S_ORDER_NODES_ADD_NODES_DISK_SIZE)
        self.type(self.K8S_ORDER_NODES_ADD_NODES_DISK_SIZE, '50')
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Форма добавления Группы Узлов',
            attachment_type=AttachmentType.PNG
        )
        # Добавление новых узлов
        self.click(self.K8S_ORDER_NODES_ADD_NODES_ADD_BUTTON)
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Изменение ресурсов',
                                   refresh_timeout=60 * 3,
                                   hover_element=self.ORDER_STATUS)
        try:
            self.click(self.K8S_ORDER_DROPDOWN)
            self.click(self.K8S_ORDER_NODES)  # Открываем вкладку Узлы
        except Exception as e:
            logger.info('Раскрыть заказ Kubernetes не потребовалось')
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60 * 3,
                                   hover_element=self.ORDER_STATUS)
        try:
            self.click(self.K8S_ORDER_DROPDOWN)
            self.click(self.K8S_ORDER_NODES)  # Открываем вкладку Узлы
        except Exception as e:
            logger.info('Раскрыть заказ Kubernetes не потребовалось')
        self.wait_for_page_loaded((By.XPATH, f'//p[text()="{node_name}"]'))  # Ждем появления созданного узла
        assert self.find_elem((By.XPATH, f'//p[text()="{node_name}"]')), f'Группа узлов Kubernetes не найдена'
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Созданная группа узлов',
            attachment_type=AttachmentType.PNG
        )
        # Удаление созданного узла
        logger.info(f'Удаление созданного узла Kubernetes {node_name}')
        del_locator = (By.XPATH, f'//td[./div/p[contains(text(), "{node_name}")]]'
                              '//following-sibling::td[6]')
        self.click(del_locator)
        self.click(self.K8S_ORDER_NODES_ADD_NODES_DEL_BUTTON)
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Изменение ресурсов',
                                   refresh_timeout=60 * 3,
                                   hover_element=self.ORDER_STATUS)
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60 * 3,
                                   hover_element=self.ORDER_STATUS)
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Удаленная группа узлов',
            attachment_type=AttachmentType.PNG
        )
        time.sleep(3)  # ждем завершения анимации удаления узлов
        assert bool(self.find_elem((By.XPATH, f'//p[text()="{node_name}"]'), timeout=5)) == False, \
            'Не удалось подтвердить удаление узла Kubernetes'

    def check_net_tab(self):
        self.click(self.K8S_ORDER_NET)  # Открываем вкладку Сеть
        self.wait_for_page_loaded(self.K8S_ORDER_NET_TABLE_TITLE)
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Раздел Сеть',
            attachment_type=AttachmentType.PNG
        )
        # Добавляет правило сети
        self.click(self.K8S_ORDER_NET_ADD_RULE)
        # rule_name = f'autotest{abs(hash(datetime.now()))}'
        self.type(self.K8S_ORDER_NET_ADD_RULE_NAME, 'autotest')
        self.type(self.K8S_ORDER_NET_ADD_RULE_SOURCE, '10.10.10.10')
        self.type(self.K8S_ORDER_NET_ADD_RULE_DEST_PORT, '3232')
        self.type(self.K8S_ORDER_NET_ADD_RULE_TRANSLATION, '12.12.12.12')
        self.type(self.K8S_ORDER_NET_ADD_RULE_TRANSLATION_PORT, '3232')
        time.sleep(0.5)  # Ждем завершения анимации для скриншота
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Форма добавления правила сети',
            attachment_type=AttachmentType.PNG
        )
        self.click(self.K8S_ORDER_NODES_ADD_NODES_ADD_BUTTON)
        self.wait_for_page_loaded((By.XPATH, f'//td/div/p[text()="autotest"]'))
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Добавленное правило',
            attachment_type=AttachmentType.PNG
        )



    def del_k8s_order(self):
        """Удаление дочернего заказа Kubernetes"""
        elem_for_del = (By.XPATH, '//td/div/*[contains(text(), "Кластер Kubernetes")]/following::td[3]//*[@id="close"]')
        self.click(elem_for_del)
        self.click(OrdersPage.ORDER_POWER_OFF_MODAL_YES)
        self.find_elem(self.ORDER_STATUS_TEXT)
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Удаление сетевой связности',
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
