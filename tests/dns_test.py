import allure
from allure_commons.types import AttachmentType
import pytest
from src.pages.main_page import MainPage
from src.pages.auth_page import Auth
from config.config import SUOP
from src.logger.formatted_logger import logger

@pytest.fixture
def pre_post_dns(browser):
    yield
    auth_page = Auth(browser)
    auth_page.logout()

@allure.tag('dns')
@allure.testcase('https://jira.rt-dc.ru/secure/Tests.jspa#/v2/testCases')
@allure.story('Управление DNS. Добавление домена.')
def test_dns(pre_post_dns, browser):
    """Тест DNS СУ ОП"""

    main_page = MainPage(browser, SUOP.MAIN_URL)  # экземпляр главной страницы с url
    auth_page = Auth(browser)
    print('Управление DNS. Добавление домена')
    with allure.step('Открываем главную страницу'):
        logger.info('Открываем главную страницу')
        main_page.wait_for_page_loaded(main_page.showcase_card)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Главня_страница',
            attachment_type=AttachmentType.PNG
        )

    with allure.step('Личный кабинет клиента'):
        main_page.auth_main_page()
        main_page.wait_for_page_loaded(auth_page.submit_btn)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Форма_авторизации',
            attachment_type=AttachmentType.PNG
        )
        auth_page.login()
        main_page.wait_for_page_loaded(auth_page.profile_name_client)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Личный_кабинет_клиента',
            attachment_type=AttachmentType.PNG
        )

    with allure.step('Личный кабинет администратора'):
        auth_page.login_as_admin_suop()
        auth_page.wait_for_page_loaded(auth_page.profile_name_admin)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Личный_кабинет_Администратор_СУОП',
            attachment_type=AttachmentType.PNG
        )
