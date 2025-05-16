import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from src.pages.basic_page import BasicPage
from src.pages.client_page import ClientPage
from src.pages.auth_page import AuthPage
from config.config import SUOP
from src.logger.formatted_logger import logger


class OrdersPage(BasicPage):
    """Класс описывает страницу с заказами в личном кабинете клиента"""

    FILTER_CLEAN_BUTTON = (By.XPATH, '//button[contains(text(), "Очистить все")]')
    FILTER_FOR_FIND_ORDERS = (By.XPATH, '//header/div[contains(@class,"btn-wrapper--single-icon")]/button')
    FILTER_INPUT_ID_ORDER = (By.XPATH, '//input[@name="id"]')
    FILTER_FORM_APPLY_BUTTON = (By.XPATH, '//button[contains(text(), "Применить")]')

    # Создание заказа
    ORDER_PARAM_TAB = (By.XPATH, '//button[contains(text(), "Параметры и ограничения")]')
    ORDER_BUTTON_APPROVE_MANAGER = (By.XPATH, '//button[contains(text(), "Согласовать перевод заказа в тестовый режим")]')
    ORDER_BUTTON_APPROVE_MANAGER_2 = (By.XPATH, '//button[contains(text(), "Перевести в тестовый режим")]')  # Еще раз подтверждаем согласование заказа

    # Заказ
    ORDER_STATUS = (By.XPATH, '//div[contains(@class, "statusText")]')
    ORDER_STATUS_CHANGE = (By.XPATH, '//div[contains(text(), "Изменение объема ресурсов")]')
    ORDER_STATUS_READY = (By.XPATH, '//div[contains(text(), "Работает")]')
    ORDER_STATUS_SHUTDOWN = (By.XPATH, '//div[contains(text(), "Выключение")]')
    ORDER_STATUS_STOPPED = (By.XPATH, '//div[contains(text(), "Выключен")]')
    ORDER_STATUS_DELETED = (By.XPATH, '//div[contains(text(), "Удален")]')
    ORDER_POWER_OFF = (By.XPATH, '//button[contains(text(), "Выключить заказ")]')
    ORDER_POWER_OFF_MODAL_YES = (By.XPATH, '//button[contains(text(), "Да")]')
    ORDER_DELETE = (By.XPATH, '//button[contains(text(), "Освободить ресурсы")]')
    ORDER_DELETE_MODAL_YES = (By.XPATH, '//button[contains(text(), "Да")]')
    ORDER_STATUS_ALL_SUBORDERS = (By.XPATH, '//div[(text()="Состояние")]/following-sibling::div')  # Для поиска всех элементов со статусом дочерних заказах
    READY_STATUS_ALL_SUBORDERS = (By.XPATH, '//div[(text()="Состояние")]/following-sibling::div[text()="Работает"]')  # Для поиска всех элементов со статусом "Работает" дочерних заказах
    RIGHTS_FOR_CHANGE_RESOURCES = (By.XPATH, '//div[text()="Разрешить менять объем услуг"]/following-sibling::div[last()]/div')  # Кнопка для изменения ресурсов
    RIGHTS_FOR_CHANGE_RESOURCES_SELECT = (By.XPATH, '//div[text()="Разрешить менять объем услуг"]/following-sibling::div[1]')  # Выпадающее меню Да/Нет
    RIGHTS_FOR_CHANGE_RESOURCES_SELECT_YES = (By.XPATH, '//div[contains(@id, "option-0")]') # Значение Да в выпадающем меню (не select)
    RIGHTS_FOR_CHANGE_RESOURCES_CONFIRM = (By.XPATH, '//*[@id="confirm"]')
    RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON = (By.XPATH, '//div[contains(@class, "loader-local")]')  # Иконка ожидания применения изменений
    ORDER_INFO_TITLE = (By.XPATH, '//button[contains(@class, "button--tab-active")]')  # Для ожидания загрузки заказа (менеджер и администратор)



    def __init__(self, browser):
        super().__init__(browser)

    def find_order(self, num_order:str):
        """
        Находит заказ по номеру и открывает его.
        clear_filter под клиентом нет кнопки "Очистить все" если нет созданных заказов
        Под клиентом, через поиск заказ нужно дополнительно открывать в отличие от админа и менеджера
        """

        if self.wait_for_page_loaded(self.FILTER_CLEAN_BUTTON, 3):
            self.click(self.FILTER_CLEAN_BUTTON)  # Сброс фильтров для поиска заказов (если он есть)
        WebDriverWait(self.browser, 30).until(EC.invisibility_of_element(self.FILTER_CLEAN_BUTTON))  # Ждем когда элемент исчезнет
        # time.sleep(2)
        self.click(self.FILTER_FOR_FIND_ORDERS)
        # time.sleep(2)
        self.type(self.FILTER_INPUT_ID_ORDER, num_order)
        # time.sleep(2)
        self.click(self.FILTER_FORM_APPLY_BUTTON)
        self.wait_for_page_loaded(ClientPage.TABLE_WITH_ORDERS_IN_LK)
        composite_locator = (By.XPATH, f'//div[@class="orderRow"]//div[contains(text(),"{num_order}")] | '
                                       f'//td[contains(text(),"{num_order}")]')
        self.wait_for_page_loaded(composite_locator, 15)  # TODO локаторы клиента и администратора отличаются (под клиентом верстка элемента в <table>)
        profile = self.find_elem(AuthPage.PROFILE_NAME, 5)
        # logger.info(f'{profile.text} == {SUOP.ORGANIZATION_CLIENT}')
        if type(profile) != bool and profile.text == SUOP.ORGANIZATION_CLIENT:
            # Если заказ ищется под клиентом его нужно дополнительно раскрыть, т.к. у клиента заказ выглядит иначе
            self.click(composite_locator)
            self.wait_for_page_loaded(ClientPage.VIRT_MACH_TITLE)
        else:
            # Заказ ищется за менеджера или клиента, ждем загрузки информации (активный таб заголовок)
            self.wait_for_page_loaded(self.ORDER_INFO_TITLE)

    def approve_order(self, num_order):
        """Согласовывает заказ за менеджера"""
        logger.info('Согласование заказа')
        self.click(self.ORDER_BUTTON_APPROVE_MANAGER)
        self.click(self.ORDER_BUTTON_APPROVE_MANAGER_2)
        self.text_check(self.ORDER_STATUS, 'Изменение объема ресурсов', 60 * 10)
        self.text_check(self.ORDER_STATUS, 'Работает', 60 * 10)
        logger.info('Ожидание состояние "Работает" у дочерних заказов')
        assert self.wait_ready_for_all_child_orders(), f'Не удалось согласовать заказ {num_order}'

    def text_check(self, locator, text_trigger, timeout, hover_element=None) -> bool:
        """
        Ожидает изменения текста элемента до установленного
        :param locator: локатор в котором проверяется текст
        :param text_trigger: ожидаемый текст
        :param timeout: таймаут для цикла проверки
        :param hover_element: навести курсор на элемент перед считыванием текста
        :return: bool
        """
        start_time = datetime.now()
        if hover_element:
            status_element = self.find_elem(hover_element)
            ActionChains(self.browser).move_to_element(status_element).perform()
        current_text = self.find_elem(locator).text
        logger.info(f'Состояние заказа: {current_text}')
        i = 0
        while True:
            # установка таймаута
            time_difference = datetime.now() - start_time
            if time_difference.total_seconds() > timeout:
                logger.error('timeout при ожидании изменения статуса')
                return False

            i += 1
            logger.info(f'Итерация №: {i} Прошло: {time_difference} сек')
            # self.browser.refresh()
            if hover_element:
                status_element = self.find_elem(hover_element)
                ActionChains(self.browser).move_to_element(status_element).perform()
            elem_for_actual_text = self.find_elem(locator)
            if elem_for_actual_text:
                elem_for_actual_text = elem_for_actual_text.text
            if type(elem_for_actual_text) != str:
                time.sleep(10)
                continue
            if elem_for_actual_text == text_trigger:
                logger.info(f'Ожидаемое состояние достигнуто: {elem_for_actual_text}')
                return True
            elif current_text != elem_for_actual_text:
                logger.info(f'Состояние изменилось: {elem_for_actual_text}')
                current_text = elem_for_actual_text
            else:  # Если найдено триггерное слово завершаем проверку
                logger.info(f'Состояние не изменилось')
            self.browser.refresh()
            time.sleep(10)

    def del_order(self, num_order):
        """Удаляет заказ по номеру"""
        logger.info('Удаление заказа del_order_dev()')
        self.browser.refresh()  # Обновляем страницу, баг с появлением УЗ Клиента
        logger.info('Обновление страницы')
        self.find_order(num_order)
        self.click(self.ORDER_POWER_OFF)
        self.click(self.ORDER_POWER_OFF_MODAL_YES)
        self.text_check(self.ORDER_STATUS, 'Выключен', 60*10)
        self.browser.refresh()
        self.click(self.ORDER_DELETE, 60 * 3)
        self.click(self.ORDER_DELETE_MODAL_YES, 60 * 3)
        assert self.text_check(self.ORDER_STATUS, 'Удален', 60 * 10), 'Заказ не перешел в состояние "Удален"'

    def wait_ready_for_all_child_orders(self, locator=READY_STATUS_ALL_SUBORDERS, timeout=600) -> bool:
        """Находит на странице элементы и ждет когда их статус изменится на Работает"""

        elem_count = 4  # Количество ожидаемых элементов со статусом "Работает"
        logger.info(f'Количество ожидаемых элементов со статусом "Работает": {elem_count} ед.')
        try:
            WebDriverWait(self.browser, timeout).until(lambda b: len(self.find_all_elem(locator)) >= elem_count)
            logger.warning(f'Все заказы перешли в состояние "Работает".')
            return True
        except Exception as error:
            logger.warning(f'Дочерние заказы не перешли в состояние "Работает". Ошибка: {error}')
            return False

    def set_rights_resources(self):
        """Устанавливает разрешение на изменение ресурсов в заказе"""
        logger.info('Устанавливает разрешение на изменение ресурсов в заказе')
        # self.browser.refresh()
        self.click(self.RIGHTS_FOR_CHANGE_RESOURCES)
        time.sleep(2)
        self.click(self.RIGHTS_FOR_CHANGE_RESOURCES_SELECT)
        time.sleep(2)
        self.click(self.RIGHTS_FOR_CHANGE_RESOURCES_SELECT_YES)  # Значение Да в выпадающем меню (не select)
        time.sleep(2)
        self.click(self.RIGHTS_FOR_CHANGE_RESOURCES_CONFIRM)
        WebDriverWait(self.browser, 30).until(
            EC.invisibility_of_element(self.RIGHTS_FOR_CHANGE_RESOURCES_LOADER_ICON))  # Ждем когда элемент исчезнет
