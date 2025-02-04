import time
import allure
import pytest
from src.pages.main_page import MainPage
from src.pages.auth_page import Auth
from config.config import SUOP

@pytest.fixture
def pre_post_dns(browser):
    print('!!!Предусловие' * 10)
    yield
    print('###Постусловие' * 10)
    auth_page = Auth(browser)
    auth_page.logout()
    print('Автотест завершен')

@allure.story('Управление DNS. Добавление домена.')
def test_dns(pre_post_dns, browser):
    """Тест DNS СУ ОП"""
    main_page = MainPage(browser, SUOP.MAIN_URL)  # экземпляр главной страницы с url
    auth_page = Auth(browser)

    main_page.wait_for_page_loaded(main_page.showcase_card)
    main_page.save_scr('main_page')
    main_page.auth_main_page()
    main_page.wait_for_page_loaded(auth_page.submit_btn)
    main_page.save_scr('form_page')
    auth_page.login()
    auth_page.save_scr('Личный кабинет клиент')
    auth_page.login_as_admin_suop()
    auth_page.wait_for_page_loaded(auth_page.profile_name)
    auth_page.save_scr('Личный кабинет Администратор СУОП')
