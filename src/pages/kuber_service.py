import time
from datetime import datetime

import allure
from allure_commons.types import AttachmentType

from src.logger.formatted_logger import logger
from src.pages.basic_page import BasicPage
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
from src.pages.auth_page import AuthPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class KuberService(BasicPage):
    """Класс описывает сервис kubernetes. Роль - клиент"""

    def __init__(self, browser):
        super().__init__(browser)
        self.client_page = ClientPage(browser)
        self.order_page = OrdersPage(browser)
        self.auth_page = AuthPage(browser)

    KUBER_MAKE_ORDER_TITLE = (By.XPATH, '//h4[contains(text(), "Конфигурация кластера")]')
    ORDER_STATUS = (By.XPATH, '//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
    ORDER_STATUS_TEXT = (By.XPATH, '//div[@class="suborder-state-status"]//p[@class="icon-hint__text"]')
    K8S_ORDER_DROPDOWN = (By.XPATH, '//table//tbody/tr//td[5]')  # Раскрыть заказ kubernetes
    K8S_ORDER_DROPDOWN_COLLAPSED = (By.XPATH, '//table//tbody/tr//td[5]'
                                    '/div/button/div[not(contains(@class, "active"))]')  # Раскрыть заказ kubernetes (только свернутый)
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
    K8S_ORDER_NODES_ADD_NODES_DEL_BUTTON = (By.XPATH, '//*[@id="simple_confirm"]/div/div/div/div[6]/div[2]/button')  # Кнопка добавления узла
    K8S_ORDER_NET = (By.XPATH, '//button[contains(text(), "Сеть")]')  # Раздел Сеть в заказе k8s
    K8S_ORDER_NET_TABLE_TITLE = (By.XPATH, '//th[text()="NAT правило"]'
                                           '[following-sibling::th[1][text()="Статус"]]'
                                           '[following-sibling::th[2][text()="ВМ"]]')  # Заголовок таблицы Сеть
    K8S_ORDER_NET_ADD_RULE = (By.XPATH, '//span[text()="Добавить правило"]')
    K8S_ORDER_NET_ADD_RULE_NAME = (By.XPATH, '//input[@name="title"]')  # Поле ввода наименования правила
    K8S_ORDER_NET_ADD_RULE_SOURCE = (By.XPATH, '//input[@name="source"]')  # Поле ввода источника
    K8S_ORDER_NET_ADD_RULE_DEST_PORT = (By.XPATH, '//input[@name="destination_port"]')  # Поле ввода порт назначения
    K8S_ORDER_NET_ADD_RULE_TRANSLATION = (By.XPATH, '//input[@name="translated"]')  # Поле ввода адреса трансляции
    K8S_ORDER_NET_ADD_RULE_TRANSLATION_PORT = (By.XPATH, '//input[@name="translated_port"]')  # Поле ввода порта трансляции
    K8S_ORDER_NET_ADDED_RULE = (By.XPATH, '//td/div/p[text()="autotest"]')  # Добавленное правило
    K8S_ORDER_NET_DEL_RULE = (By.XPATH, '//td[div/p[text()="autotest"]]'
                                        '//following-sibling::td[11]')  # Удаление сетевого правила
    K8S_ORDER_NET_DEL_RULE_MODAL_YES = (By.XPATH, '//button[text()="Да"]')  # Кнопка да в модальном окне удаления
    K8S_ORDER_VOLUMES = (By.XPATH, '//button[contains(text(), "Постоянные тома")]')  # Раздел Постоянные тома в заказе k8s
    K8S_ORDER_VOLUMES_TABLE_DATA = (By.XPATH, '//p[contains(text(), "Блочный")]')  # Данные из таблицы для ожидания загрузки
    K8S_ORDER_VOLUMES_ADD = (By.XPATH, '//button[text()="Добавить хранилище постоянных томов"]')  # Кнопка добавления томов
    K8S_ORDER_VOLUMES_SAS = (By.XPATH, '//input[contains(@name, "sas")]')  # Поле формы добавления объема диска (тома)
    K8S_ORDER_VOLUMES_SAVE_FORM = (By.XPATH, '//button[text()="Сохранить"]')  # Кнопка сохранить модального окна

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
        self.browser.refresh()
        self.wait_for_page_loaded(self.K8S_ORDER_DROPDOWN)
        self.expand_k8s_order_nodes()  # Открываем вкладку Узлы
        self.wait_for_page_loaded(self.K8S_ORDER_NODES_MASTER_DATA)
        self.scroll_to_element(self.find_elem(self.K8S_ORDER_DROPDOWN))
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Раздел Узлы',
            attachment_type=AttachmentType.PNG
        )
        logger.info('Создание группы узлов')
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
        self.expand_k8s_order_nodes()
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60 * 3,
                                   hover_element=self.ORDER_STATUS)
        self.expand_k8s_order_nodes()
        self.wait_for_page_loaded((By.XPATH, f'//p[text()="{node_name}"]'))  # Ждем появления созданного узла
        assert self.find_elem((By.XPATH, f'//p[text()="{node_name}"]')), f'Группа узлов Kubernetes не найдена'
        self.scroll_to_element(self.find_elem(self.K8S_ORDER_DROPDOWN))
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Созданная группа узлов',
            attachment_type=AttachmentType.PNG
        )
        # Удаление созданного узла
        logger.info(f'Удаление созданной группы узлов Kubernetes {node_name}')
        del_locator = (By.XPATH, f'//td[./div/p[contains(text(), "{node_name}")]]'
                              '//following-sibling::td[6]')
        self.click(del_locator)
        self.click(self.K8S_ORDER_NODES_ADD_NODES_DEL_BUTTON)
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Изменение ресурсов',
                                   refresh_timeout=60 * 3,
                                   hover_element=self.ORDER_STATUS)
        self.expand_k8s_order_nodes()
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60 * 3,
                                   hover_element=self.ORDER_STATUS)
        self.expand_k8s_order_nodes()
        self.scroll_to_element(self.find_elem(self.K8S_ORDER_DROPDOWN))
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
        logger.info('Добавление правила Сети')
        self.click(self.K8S_ORDER_NET_ADD_RULE)
        # rule_name = f'autotest{abs(hash(datetime.now()))}'
        self.type(self.K8S_ORDER_NET_ADD_RULE_NAME, 'autotest')
        self.type(self.K8S_ORDER_NET_ADD_RULE_SOURCE, '192.168.2.1')
        self.type(self.K8S_ORDER_NET_ADD_RULE_DEST_PORT, '3232')
        self.type(self.K8S_ORDER_NET_ADD_RULE_TRANSLATION, '192.168.2.2')
        self.type(self.K8S_ORDER_NET_ADD_RULE_TRANSLATION_PORT, '3232')
        time.sleep(0.5)  # Ждем завершения анимации для скриншота
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Форма добавления правила сети',
            attachment_type=AttachmentType.PNG
        )
        self.click(self.K8S_ORDER_NODES_ADD_NODES_ADD_BUTTON)
        self.wait_for_page_loaded(self.K8S_ORDER_NET_ADDED_RULE)
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Добавленное правило',
            attachment_type=AttachmentType.PNG
        )
        # Удаление сетевого правила
        self.click(self.K8S_ORDER_NET_DEL_RULE)
        self.click(self.K8S_ORDER_NET_DEL_RULE_MODAL_YES)
        WebDriverWait(self.browser, 60).until(
            EC.invisibility_of_element(OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда элемент исчезнет
        WebDriverWait(self.browser, 60).until(
            EC.invisibility_of_element(
                self.K8S_ORDER_NET_ADDED_RULE))  # Ждем когда правило Сети исчезнет
        if self.find_elem(self.K8S_ORDER_NET_ADDED_RULE, timeout=5):
            logger.warning('Созданное правило не удалено')
        else:
            logger.info('Созданное правило успешно удалено')
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Удаленное правило',
            attachment_type=AttachmentType.PNG
        )

    def check_volume_tab(self):
        """Проверка вкладки Постоянные тома в заказе Kubernetes"""
        self.browser.refresh()
        self.wait_for_page_loaded(self.K8S_ORDER_DROPDOWN)
        self.expand_k8s_order_volumes()
        self.wait_for_page_loaded(self.K8S_ORDER_VOLUMES_TABLE_DATA)
        self.scroll_to_element(self.find_elem(self.K8S_ORDER_DROPDOWN))
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Раздел Постоянные тома',
            attachment_type=AttachmentType.PNG
        )
        # Добавление тома
        self.click(self.K8S_ORDER_VOLUMES_ADD)
        self.custom_clear(self.K8S_ORDER_VOLUMES_SAS)
        self.type(self.K8S_ORDER_VOLUMES_SAS, '10')
        time.sleep(0.5)  # Ждем завершения анимации
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Форма добавления тома',
            attachment_type=AttachmentType.PNG
        )
        self.click(self.K8S_ORDER_VOLUMES_SAVE_FORM)
        WebDriverWait(self.browser, 60).until(
            EC.invisibility_of_element(
                self.K8S_ORDER_VOLUMES_SAVE_FORM))  # Ждем когда элемент исчезнет
        self.order_page.text_check(self.ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60 * 10,
                                   hover_element=self.ORDER_STATUS)
        self.wait_for_page_loaded(self.K8S_ORDER_DROPDOWN)
        self.expand_k8s_order_volumes()
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Добавленный том',
            attachment_type=AttachmentType.PNG
        )



    def expand_k8s_order_nodes(self):
        """Раскрывает заказ k8s, вкладку узлы фикс бага https://tasks.rt-dc.ru/browse/CLOUDDEV-11294"""
        try:
            self.click(self.K8S_ORDER_DROPDOWN, timeout=5)  # Раскрываем заказ k8s
            self.click(self.K8S_ORDER_NODES)  # Открываем вкладку Узлы
            self.wait_for_page_loaded(self.K8S_ORDER_NODES_MASTER_DATA)  # Ожидаем загрузки данных раздела Узлы
        except Exception as e:
            logger.info('Раскрыть заказ Kubernetes не потребовалось')

    def expand_k8s_order_volumes(self):
        """Раскрывает заказ k8s, вкладку Постоянные тома фикс бага https://tasks.rt-dc.ru/browse/CLOUDDEV-11294"""
        try:
            self.click(self.K8S_ORDER_DROPDOWN_COLLAPSED, timeout=5)  # Раскрываем заказ k8s
            self.click(self.K8S_ORDER_VOLUMES)  # Открываем вкладку Узлы
            self.wait_for_page_loaded(self.K8S_ORDER_VOLUMES)  # Ожидаем загрузки данных раздела Узлы
        except Exception as e:
            logger.info('Раскрыть заказ Kubernetes не потребовалось')

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
