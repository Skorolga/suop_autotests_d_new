from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage


class MainPage(BasicPage):
    """Класс главной страницы СУ ОП"""

    LK_BUTTON = (By.XPATH, '//button[contains(text(),"Личный кабинет")]')  # переход на форму авторизации
    SHOWCASE_CARD = (By.XPATH, '//div[contains(@class, "showcase-card")]')  # карусель для проверки загрузки страницы


    def __init__(self, browser, url=None):
        super().__init__(browser)
        if url:
            self.browser.get(url)

    def go_to(self, set_url):
        self.browser.get(set_url)

    def auth_main_page(self):
        """Функция авторизации через главную страницу"""
        self.click(self.LK_BUTTON)


