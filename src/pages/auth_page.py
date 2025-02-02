from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage
from config.config import SUOP


class Auth(BasicPage):
    login_form = (By.ID, 'username')
    password_form = (By.ID, 'password')
    submit_btn = (By.XPATH, '// button[ @ type = "submit"]')

    def __init__(self, browser, url=None):
        super().__init__(browser)
        if url:
            self.browser.get(url)

    def login(self):
        self.send_text(self.login_form, SUOP.CLIENT_LOGIN)
        self.send_text(self.password_form, SUOP.CLIENT_PASSWORD)
        self.save_scr('after_send_cred')
        self.click_on_element(self.submit_btn)
        self.save_scr('after_auth')
