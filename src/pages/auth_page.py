import time
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage
from src.pages.main_page import MainPage
from config.config import SUOP


class Auth(BasicPage):
    """Класс описывающий авторизацию и выбор роли (организации)"""

    # Форма авторизации
    LOGIN_FORM = (By.ID, 'username')
    PASSWORD_FORM = (By.ID, 'password')
    SUBMIT_BTN = (By.XPATH, '//button[@type="submit"]')

    # Остальные локаторы
    CAB_AVATAR = (By.XPATH, '//a[contains(@class, "cab cab--select")]')  # выпадающее меню профиля
    LOGOUT_PROFILE_MENU = (By.XPATH, '//p[contains(text(), "Выход")]')
    MENU_CHANGE_ROLE = (By.XPATH, '//p[contains(text(), "Сменить организацию")]')

    ADMIN_SUOP = (By.XPATH, '//div[contains(text(), "Администраторы СУ ОП")]')
    PROFILE_NAME_ADMIN = (By.XPATH, '//p[text()="Администраторы СУ ОП"]')  # для проверки выбора роли Администратор СУ ОП
    PROFILE_NAME_CLIENT = (By.XPATH, '''//p[text()='ООО "ТЦИ"']''')  # для проверки выбора роли Администратор СУ ОП

    def __init__(self, browser, url=None):
        super().__init__(browser)
        if url:
            self.browser.get(url)

    def auth_as_client(self):
        """Авторизация под ролью клиента"""
        self.click_on_element(MainPage.LK_BUTTON)  # переходим на главную форму авторизации из главной
        self.send_text(self.LOGIN_FORM, SUOP.CLIENT_LOGIN)
        self.send_text(self.PASSWORD_FORM, SUOP.CLIENT_PASSWORD)
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name='Форма_авторизации',
            attachment_type=AttachmentType.PNG
        )
        self.click_on_element(self.SUBMIT_BTN)
        self.select_role(SUOP.ORGANIZATION_CLIENT)

    def relogin_as_admin_suop(self, first_auth=False):
        """Авторизация под ролью Администратора"""
        if not first_auth:
            # Если это не первая авторизация сначала переходим на страницу выбора организации
            self.click_on_element(self.CAB_AVATAR)
            self.click_on_element(self.MENU_CHANGE_ROLE)

        self.select_role('Администраторы СУ ОП')

    def select_role(self, role:str):
        """Выбирает роль (организацию) по названию"""
        el_constructor = (By.XPATH, f"""//div[contains(text(), '{role}')]""")  # f-строка с двойными кавычками в названии!
        if self.find_elem(el_constructor):
            self.click_on_element(el_constructor)

    def logout(self):
        """Выход из учетной записи"""
        self.click_on_element(self.CAB_AVATAR)
        self.click_on_element(self.LOGOUT_PROFILE_MENU)
