import time
from datetime import datetime
from typing import Tuple

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

    K8S_MAKE_ORDER_TITLE = (By.XPATH, '//h4[contains(text(), "Конфигурация кластера")]')
    K8S_MAKE_ORDER_PARENT_ORDER_INPUT = (By.XPATH, '//label[text()="Выберите заказ"]/ancestor::div[1]/preceding-sibling::div')
    ORDER_STATUS = (By.XPATH, '//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
    ORDER_STATUS_TEXT = (By.XPATH, '//div[@class="suborder-state-status"]//p[@class="icon-hint__text"]')
    # K8S_ORDER_DROPDOWN = (By.XPATH, '//table//tbody/tr//td[5]')  # Раскрыть заказ kubernetes
    # K8S_ORDER_DROPDOWN_COLLAPSED = (By.XPATH, '//table//tbody/tr//td[5]'
    #                                 '/div/button/div[not(contains(@class, "active"))]')  # Раскрыть заказ kubernetes (только свернутый)
    K8S_ORDER_NAME_FIELD = (By.XPATH, '//*[@name="title"]')  # Форма создания kaas, наименование заказа
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
    K8S_ORDER_VOLUMES_ADDED_VOLUME = (By.XPATH, '//td//*[contains(text(), "Файловый")]')  # Добавленный том (строка в табл.)
    K8S_ORDER_VOLUMES_DEL = (By.XPATH, '//td//*[contains(text(), "Файловый")]'
                                       '//ancestor::td[1]/following-sibling::td[4]')  # Кнопка удаления тома

    def make_k8s_order(self, parent_order=None, timeout=360) -> bool | tuple[str, str]:
        """Создает заказ kubernetes"""
        logger.info('Создание заказа kubernetes')
        self.click(ClientPage.MENU_MAKE_ORDER)  # Верхнее меню
        self.click(ClientPage.BANNER_MAKE_KUBER_ORDER)  # Карточка с услугой kubernetes
        self.click(ClientPage.BUTTON_MAKE_ORDER)  # Кнопка заказать
        self.wait_for_page_loaded(self.K8S_MAKE_ORDER_TITLE)
        if parent_order:
            self.click(self.K8S_MAKE_ORDER_PARENT_ORDER_INPUT)
            self.click((By.XPATH, f'//label[text()="Выберите заказ"]/ancestor::div[1]/ancestor::div[1]//div[contains(text(), "{parent_order}")]'))
        # проверяем начисление
        day_cost = self.client_page.check_cost(ClientPage.DAY_COST)
        month_cost = self.client_page.check_cost(ClientPage.MONTH_COST)
        logger.info(f'Начисленная стоимость за заказ KaaS в сутки: {str(day_cost)} в месяц: {str(month_cost)}')
        if not all([bool(day_cost), bool(month_cost)]):
            logger.warning(f'Ошибка в начислении стоимости услуг')

        kaas_name = self.find_elem(self.K8S_ORDER_NAME_FIELD).get_attribute("value")
        logger.info(f'Наименование kaas: {kaas_name}')
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
                logger.info(f'Создан заказ KaaS № {order_num}')
                break
            time.sleep(0.5)
        allure.attach(
            body=str(order_num),
            name="Номер созданного заказа KaaS (дочернего)",
            attachment_type=AttachmentType.TEXT,
        )
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Модальное окно созданного заказа KaaS (дочернего)',
            attachment_type=AttachmentType.PNG
        )
        self.click(ClientPage.GO_TO_ORDER)
        ORDER_STATUS_TEXT = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                       f'/following-sibling::td[2]//p[@class="icon-hint__text"]')
        ORDER_STATUS = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                  f'//following-sibling::td[2]'
                                  f'//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60*3,
                                   hover_element=ORDER_STATUS)
        return order_num, kaas_name

    def check_info_tab(self, kaas_name):
        """Проверка вкладки Информация в заказе Kubernetes"""
        # K8S_ORDER_DROPDOWN = self.make_locator_kaas(kaas_name)
        self.expand_k8s_order(kaas_name)
        # self.wait_for_page_loaded(K8S_ORDER_DROPDOWN)
        # self.click(K8S_ORDER_DROPDOWN)
        elem_for_scroll = self.find_elem(self.K8S_ORDER_INFO_DATE)
        self.scroll_to_element(elem_for_scroll)
        assert self.wait_for_page_loaded(self.K8S_ORDER_INFO_TITLE), 'Отсутствует заголовок вкладки Информация'

    def check_nodes_tab(self, kaas_name):
        """Проверка вкладки Узлы в заказе Kubernetes"""
        K8S_ORDER_DROPDOWN = self.make_locator_kaas(kaas_name)
        ORDER_STATUS_TEXT = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                       f'/following-sibling::td[2]//p[@class="icon-hint__text"]')
        ORDER_STATUS = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                  f'//following-sibling::td[2]'
                                  f'//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
        self.browser.refresh()
        time.sleep(5)
        self.browser.refresh()
        # self.wait_for_page_loaded(K8S_ORDER_DROPDOWN)
        self.click(self.K8S_ORDER_NODES)  # открываем вкладку Узлы
        self.wait_for_page_loaded(self.K8S_ORDER_NODES_MASTER_DATA)
        self.scroll_to_element(self.find_elem(K8S_ORDER_DROPDOWN))
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
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Изменение ресурсов',
                                   refresh_timeout=60 * 3,
                                   hover_element=ORDER_STATUS)
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60 * 3,
                                   hover_element=ORDER_STATUS)
        self.wait_for_page_loaded((By.XPATH, f'//p[text()="{node_name}"]'))  # Ждем появления созданного узла
        assert self.find_elem((By.XPATH, f'//p[text()="{node_name}"]')), f'Группа узлов Kubernetes не найдена'
        self.scroll_to_element(self.find_elem(K8S_ORDER_DROPDOWN))
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Созданная группа узлов',
            attachment_type=AttachmentType.PNG
        )
        # Удаление созданного узла
        logger.info(f'Удаление созданной группы узлов Kubernetes {node_name}')
        DEL_NODE_LOCATOR = (By.XPATH, f'//td[./div/p[contains(text(), "{node_name}")]]'
                                      f'//following-sibling::td[6]')
        self.click(DEL_NODE_LOCATOR)
        self.click(self.K8S_ORDER_NODES_ADD_NODES_DEL_BUTTON)
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Изменение ресурсов',
                                   refresh_timeout=60 * 3,
                                   hover_element=ORDER_STATUS)
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60 * 3,
                                   hover_element=ORDER_STATUS)

        self.scroll_to_element(self.find_elem(K8S_ORDER_DROPDOWN))
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Раздел группа узлов после удаления',
            attachment_type=AttachmentType.PNG
        )
        time.sleep(10)  # ждем завершения анимации удаления узлов
        # assert bool(self.find_elem((By.XPATH, f'//p[text()="{node_name}"]'), timeout=5)) == False, \
        #     'Не удалось подтвердить удаление узла Kubernetes'
        if self.find_elem((By.XPATH, f'//p[text()="{node_name}"]'), timeout=5):
            logger.warning('Не удалось подтвердить удаление узла Kubernetes')


    def check_net_tab(self, kaas_name):
        """Проверка раздела Сеть"""
        logger.info('Проверка раздела Сети')
        # K8S_ORDER_DROPDOWN = self.make_locator_kaas(kaas_name)
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
            EC.invisibility_of_element(OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда иконка ожидания исчезнет
        WebDriverWait(self.browser, 60).until(
            EC.invisibility_of_element(
                self.K8S_ORDER_NET_ADDED_RULE))  # Ждем когда правило Сети исчезнет
        if self.find_elem(self.K8S_ORDER_NET_ADDED_RULE, timeout=5):
            logger.warning('Созданное правило не удалено')
        else:
            logger.info('Созданное правило успешно удалено')
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Раздел Сеть после удаления правила',
            attachment_type=AttachmentType.PNG
        )

    def check_volume_tab(self, kaas_name):
        """Проверка вкладки Постоянные тома в заказе Kubernetes"""
        K8S_ORDER_DROPDOWN = self.make_locator_kaas(kaas_name)
        ORDER_STATUS_TEXT = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                       f'/following-sibling::td[2]//p[@class="icon-hint__text"]')
        ORDER_STATUS = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                  f'//following-sibling::td[2]'
                                  f'//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
        self.browser.refresh()
        time.sleep(5)
        self.browser.refresh()  # Баг с правами, нужна доп. перезагрузка
        # self.wait_for_page_loaded(K8S_ORDER_DROPDOWN)
        self.click(self.K8S_ORDER_VOLUMES)  # Открываем вкладку Постоянные тома
        self.wait_for_page_loaded(self.K8S_ORDER_VOLUMES_TABLE_DATA)
        self.scroll_to_element(self.find_elem(K8S_ORDER_DROPDOWN))
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Раздел Постоянные тома',
            attachment_type=AttachmentType.PNG
        )
        # Добавление тома
        logger.info('Добавление тома')
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
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Работает',
                                   refresh_timeout=60 * 10,
                                   hover_element=ORDER_STATUS)
        # self.wait_for_page_loaded(K8S_ORDER_DROPDOWN)
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Добавленный том',
            attachment_type=AttachmentType.PNG
        )
        # Удаление тома
        logger.info('Удаление добавленного тома')
        self.click(self.K8S_ORDER_VOLUMES_DEL)
        self.click(OrdersPage.ORDER_DELETE_MODAL_YES)
        # WebDriverWait(self.browser, 60).until(
        #     EC.invisibility_of_element(
        #         OrdersPage.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда иконка ожидания исчезнет
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Удаление хранилища',
                                   hover_element=ORDER_STATUS)
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Работает',
                                   hover_element=ORDER_STATUS)
        WebDriverWait(self.browser, 60).until(
            EC.invisibility_of_element(
                self.K8S_ORDER_VOLUMES_ADDED_VOLUME))  # Ждем когда элемент исчезнет
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Раздел тома после удаления',
            attachment_type=AttachmentType.PNG
        )


    def expand_k8s_order(self, kaas_name, tab=None, wait_locator=None):
        """
        Раскрывает заказ k8s, фикс бага https://tasks.rt-dc.ru/browse/CLOUDDEV-11294
        :param kaas_name: Наименование kaas заказа
        :param tab: локатор вкладки заказа (Информация, Узлы, Сеть и т.д.)
        :param wait_locator: локатор для ожидания загрузки
        :return: None
        """
        # локатор для свернутого заказа
        K8S_ORDER_DROPDOWN_COLLAPSED = (
        By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                  f'/following-sibling::td[4]'
                  f'/div/button/div[not(contains(@class, "active"))]')
        try:
            self.wait_for_page_loaded(K8S_ORDER_DROPDOWN_COLLAPSED, timeout=15)
            self.click(K8S_ORDER_DROPDOWN_COLLAPSED, timeout=5)  # Раскрываем заказ k8s
            if tab:
                self.click(tab)  # Открываем вкладку
            if wait_locator:
                self.wait_for_page_loaded(wait_locator)  # Ожидаем загрузки данных
        except Exception as e:
            logger.info(f'Раскрыть заказ Kubernetes не потребовалось: {e}')

    def del_k8s_order(self, kaas_name):
        """Удаление дочернего заказа Kubernetes"""
        KAAS_FOR_DEL_LOCATOR = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                          f'/following-sibling::td[3]//*[@id="close"]')
        ORDER_STATUS_TEXT = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                       f'/following-sibling::td[2]//p[@class="icon-hint__text"]')
        ORDER_STATUS = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                  f'//following-sibling::td[2]'
                                  f'//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
        self.click(KAAS_FOR_DEL_LOCATOR)
        self.click(OrdersPage.ORDER_POWER_OFF_MODAL_YES)
        self.find_elem(self.ORDER_STATUS_TEXT)
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Удаление сетевой связности',
                                   refresh_timeout=60*2,
                                   hover_element=ORDER_STATUS)
        self.order_page.text_check(ORDER_STATUS_TEXT,
                                   'Удаление кластера',
                                   refresh_timeout=60*2,
                                   hover_element=ORDER_STATUS)
        WebDriverWait(self.browser, 60*45).until(
            EC.invisibility_of_element_located(KAAS_FOR_DEL_LOCATOR)
        )  # Ждем когда элемент исчезнет
        assert self.find_elem(KAAS_FOR_DEL_LOCATOR, 10) == False  # Ждем удаления

    def make_locator_kaas(self, kaas_name) -> tuple[str, str]:
        """Возвращает локатор заказа kaas"""
        return By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]/following-sibling::td[4]'