import time
from asyncio import timeout

import allure
from allure_commons.types import AttachmentType
import pytest
from src.pages.main_page import MainPage
from src.pages.auth_page import Auth
from src.pages.client_page import ClientPage
from config.config import SUOP
from src.logger.formatted_logger import logger

@pytest.fixture
def pre_post_dns(browser):
    """TODO вынести в отдельную фикстуру, в conftest.py"""
    yield
    browser.get(SUOP.MAIN_URL + '/logout')  # TODO логаут по URL, т.к. тест может остановиться на странице где нет меню для выхода, например модальное окно выбора организации

@allure.tag('dns')
@allure.testcase('https://jira.rt-dc.ru/secure/Tests.jspa#/v2/testCases')
@allure.story('Управление DNS. Добавление домена.')
def test_dns(pre_post_dns, browser):
    """Тест DNS СУ ОП"""

    main_page = MainPage(browser)  # экземпляр главной страницы с url
    auth_page = Auth(browser)
    client_page = ClientPage(browser)

    step_name = 'Открываем главную страницу'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        main_page.go_to(SUOP.MAIN_URL)
        main_page.wait_for_page_loaded(main_page.SHOWCASE_CARD)

    step_name = 'Личный кабинет клиента'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.auth_as_client()
        main_page.wait_for_page_loaded(auth_page.PROFILE_NAME_CLIENT)  # Ожидание появление элемента
        client_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Личный_кабинет_клиента',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Создание заказа'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_num = client_page.make_order()
        logger.info(f'Создан и получен номер заказа №:{order_num}')

    step_name = 'Авторизация за менеджера'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_manager()
        time.sleep(5)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Manager',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Личный кабинет администратора'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_admin_suop()
        auth_page.wait_for_page_loaded(auth_page.PROFILE_NAME_ADMIN)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Личный_кабинет_Администратор_СУОП',
            attachment_type=AttachmentType.PNG
        )
