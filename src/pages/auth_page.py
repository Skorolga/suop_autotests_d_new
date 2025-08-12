import time

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.logger.formatted_logger import logger
from src.pages.basic_page import BasicPage
from src.pages.main_page import MainPage
from src.pages.client_page import ClientPage
from config.config import SUOP


class AuthPage(BasicPage):
    """Класс описывающий авторизацию и выбор роли (организации)"""

    # Форма авторизации
    LOGIN_FORM = (By.ID, 'username')
    PASSWORD_FORM = (By.ID, 'password')
    SUBMIT_BTN = (By.XPATH, '//button[@type="submit"]')

    # Модальное окно выбора организации
    AUTH_MODAL_PAGINATION_NEXT = (By.XPATH, '//li[@class="pagination__next"]')
    AUTH_MODAL_MAIN_TABLE = (By.XPATH, '//table/tbody[contains(@class, "table-body")]')  # Для ожидания загрузки

    # Остальные локаторы
    CAB_AVATAR = (By.XPATH, '//a[contains(@class, "cab cab--select")]')  # Выпадающее меню профиля
    LOGOUT_PROFILE_MENU = (By.XPATH, '//p[contains(text(), "Выход")]')
    MENU_CHANGE_ROLE = (By.XPATH, '//p[contains(text(), "Сменить организацию")]')

    ADMIN_SUOP = (By.XPATH, f'//div[contains(text(), "{SUOP.ORGANIZATION_ADMIN}")]')
    PROFILE_NAME_ADMIN = (By.XPATH, f'//p[text()="{SUOP.ORGANIZATION_ADMIN}"]')  # Для проверки выбора роли Администратор СУ ОП
    PROFILE_NAME_MANAGER = (By.XPATH, f'//p[text()="{SUOP.ORGANIZATION_MANAGER}"]')  # Для проверки выбора роли менеджер
    PROFILE_NAME_CLIENT = (By.XPATH, f'''//p[text()='{SUOP.ORGANIZATION_CLIENT}']''')  # Для проверки выбора роли Клиента
    PROFILE_NAME = (By.XPATH, f'''//div[@class="wrapper--profile"]
                                  //div[@class="text"]//div
                                  //p[contains(@class, "grLHgo")]''')  # Для получения имени организации


    def __init__(self, browser, url=None):
        super().__init__(browser)
        if url:
            self.browser.get(url)

    def auth_as_client(self, first_auth=False):
        """
        Авторизация под ролью клиента (первичная)
        first_auth - указатель это первичная авторизация или релогин (разные шаги)
        """
        if not first_auth:
            self.click(self.CAB_AVATAR)
            self.click(self.MENU_CHANGE_ROLE)
        else:
            self.click(MainPage.LK_BUTTON)  # Переходим на главную форму авторизации из главной
            self.wait_for_page_loaded(self.LOGIN_FORM)
            self.type(self.LOGIN_FORM, SUOP.CLIENT_LOGIN)
            self.type(self.PASSWORD_FORM, SUOP.CLIENT_PASSWORD)
        if first_auth:
            self.click(self.SUBMIT_BTN)
        self.select_role(SUOP.ORGANIZATION_CLIENT)
        time.sleep(3)
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Авторизация за клиента',
            attachment_type=AttachmentType.PNG
        )

    def relogin_as_admin_suop(self, first_auth=False):
        """Авторизация под ролью Администратора"""
        if not first_auth:
            # Если это не первая авторизация сначала переходим на страницу выбора организации
            self.click(self.CAB_AVATAR)
            self.click(self.MENU_CHANGE_ROLE)
        self.select_role(SUOP.ORGANIZATION_ADMIN)
        self.wait_for_page_loaded(self.PROFILE_NAME_ADMIN)
        self.wait_for_page_loaded(ClientPage.TABLE_WITH_ORDERS_IN_LK)
        time.sleep(3)

    def relogin_as_manager(self, first_auth=False):
        """Авторизация под ролью ООО «ЦХД» B2B Менеджер по продажам и по работе с клиентами"""
        if not first_auth:
            # Если это не первая авторизация сначала переходим на страницу выбора организации
            self.click(self.CAB_AVATAR)
            self.click(self.MENU_CHANGE_ROLE)
        self.select_role(SUOP.ORGANIZATION_MANAGER)
        self.wait_for_page_loaded(self.PROFILE_NAME_MANAGER)
        time.sleep(3)

    def select_role_(self, role:str):
        """Выбирает роль (организацию) по названию"""
        el_constructor = (By.XPATH, f"""//div[contains(text(), '{role}')]""")  # f-строка с двойными кавычками в названии!
        self.wait_for_page_loaded(self.AUTH_MODAL_MAIN_TABLE)
        if self.find_elem(el_constructor, 2):
            self.click(el_constructor, 2)
        else:
            # TODO доделать перебор пагинации (сделать когда снимут ограничение в 2 сессии)
            self.click(self.AUTH_MODAL_PAGINATION_NEXT)
            self.click(el_constructor)

    def select_role(self, role:str) -> bool:
        """Выбирает роль (организацию) по названию"""
        el_constructor = (By.XPATH, f"""//div[contains(text(), '{role}')]""")  # f-строка с двойными кавычками в названии!
        self.wait_for_page_loaded(self.AUTH_MODAL_MAIN_TABLE)
        try:
            self.click(el_constructor, 2)
            return True
        except Exception as E:
            logger.info('Обходим страницы пагинации')
        next_page = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(self.AUTH_MODAL_PAGINATION_NEXT))
        i = 0
        while next_page:
            i += 1
            try:
                self.click(self.AUTH_MODAL_PAGINATION_NEXT, 1)
                self.click(el_constructor, 1)
                logger.info(f'Роль {role} найдена на странице: {i}')
                return True
            except Exception as E:
                try:
                    next_page = WebDriverWait(self.browser, 2).until(
                        EC.presence_of_element_located(self.AUTH_MODAL_PAGINATION_NEXT))
                    logger.info(f'Переходим страницу пагинации: {i + 1}')
                except Exception as E:
                    next_page = False
                    logger.error(f'Роль {role} не найдена. Пройдено страниц пагинации: {i} next_page {bool(next_page)}')
        return False

    def logout(self):
        """Выход из учетной записи"""
        self.click(self.CAB_AVATAR)
        self.click(self.LOGOUT_PROFILE_MENU)
