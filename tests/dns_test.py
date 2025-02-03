import time
import allure
from src.pages.main_page import MainPage
from src.pages.auth_page import Auth
from config.config import SUOP

@allure.story('Управление DNS. Добавление домена.')
def test_dns(browser):
    """Тест DNS СУ ОП"""
    main_page = MainPage(browser, SUOP.MAIN_URL)  # экземпляр главной страницы с url
    auth_page = Auth(browser)
    main_page.save_scr('main_page')
    main_page.auth_main_page()
    main_page.save_scr('form_page')
    auth_page.login()
    auth_page.save_scr('Личный кабинет')
    auth_page.logout()