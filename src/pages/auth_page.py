import time

from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage
from config.config import SUOP


class Auth(BasicPage):
    """Класс описывающий авторизацию и выбор роли (организации)"""

    login_form = (By.ID, 'username')
    password_form = (By.ID, 'password')
    submit_btn = (By.XPATH, '//button[@type="submit"]')

    # Остальные локаторы
    cab_avatar = (By.XPATH, '//a[contains(@class, "cab cab--select")]')  # выпадающее меню профиля
    logout_profile_menu = (By.XPATH, '//p[contains(text(), "Выход")]')

    adminSUOP = (By.XPATH, '//div[contains(text(), "Администраторы СУ ОП")]')

    def __init__(self, browser, url=None):
        super().__init__(browser)
        if url:
            self.browser.get(url)

    def login(self):
        """Авторизация пользователя, по умолчанию под ролью администратора"""
        self.send_text(self.login_form, SUOP.CLIENT_LOGIN)
        self.send_text(self.password_form, SUOP.CLIENT_PASSWORD)
        self.save_scr('after_send_cred')
        self.click_on_element(self.submit_btn)
        self.save_scr('after_auth')
        self.select_role(SUOP.ORGANIZATION_CLIENT)
        time.sleep(10)

    def select_role(self, role:str):
        """Выбирает роль (организацию по названию)"""
        el_constructor = (By.XPATH, f"//div[contains(text(), '{role}')]")  # f-строка с двойными кавычками, название!
        if self.find_elem(el_constructor):
            self.click_on_element(el_constructor)

    def logout(self):
        self.click_on_element(self.cab_avatar)
        self.click_on_element(self.logout_profile_menu)

