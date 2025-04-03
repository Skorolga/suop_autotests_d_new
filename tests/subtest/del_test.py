import time
from asyncio import timeout

import allure
from allure_commons.types import AttachmentType
import pytest
from src.pages.main_page import MainPage
from src.pages.auth_page import AuthPage
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
from config.config import SUOP
from src.logger.formatted_logger import logger

@pytest.fixture
def pre_post_dns(browser):
    """TODO вынести в отдельную фикстуру, в conftest.py"""
    yield
    browser.get(SUOP.MAIN_URL + '/logout')  # TODO логаут по URL, т.к. тест может остановиться на странице где нет меню для выхода, например модальное окно выбора организации

@allure.testcase('https://jira.rt-dc.ru/secure/Tests.jspa#/v2/testCases')
@allure.story('Управление DNS. Удаление.')
def test_del(pre_post_dns, browser):
    """Тест DNS СУ ОП"""

    main_page = MainPage(browser)  # экземпляр главной страницы с url
    auth_page = AuthPage(browser)
    client_page = ClientPage(browser)
    orders_page = OrdersPage(browser)

    step_name = 'Открываем главную страницу'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        main_page.go_to(SUOP.MAIN_URL)
        main_page.wait_for_page_loaded(main_page.SHOWCASE_CARD)

    step_name = 'Личный кабинет клиента'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.auth_as_client(first_auth=True)
        main_page.wait_for_page_loaded(auth_page.PROFILE_NAME_CLIENT)  # Ожидание появление элемента
        client_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Личный_кабинет_клиента',
            attachment_type=AttachmentType.PNG
        )
    order_num = '126880'
    # step_name = 'Согласование созданного заказа за менеджера'
    # with allure.step(step_name):
    #     logger.info('Шаг: ' + step_name)
    #     orders_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
    #     allure.attach(
    #         body=auth_page.browser.get_screenshot_as_png(),
    #         name='Список заказов',
    #         attachment_type=AttachmentType.PNG
    #     )
    #     orders_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
    #     allure.attach(
    #         body=auth_page.browser.get_screenshot_as_png(),
    #         name='Список заказов после очистки фильтра поиска',
    #         attachment_type=AttachmentType.PNG
    #     )
    #
    #     orders_page.find_order(order_num)
    #     allure.attach(
    #         body=auth_page.browser.get_screenshot_as_png(),
    #         name='Найденный заказ',
    #         attachment_type=AttachmentType.PNG
    #     )
    #
    #     orders_page.approve_order(order_num)

    # step_name = f'Разрешение на изменение ресурсов заказа {order_num}'
    # with allure.step(step_name):
    #     logger.info('Шаг: ' + step_name)
    #     auth_page.relogin_as_manager()
    #     orders_page.find_order(order_num)
    #     orders_page.set_rights_resources()
    #     allure.attach(
    #         body=auth_page.browser.get_screenshot_as_png(),
    #         name='Разрешение на изменение ресурсов',
    #         attachment_type=AttachmentType.PNG
    #     )


    step_name = 'Удаление заказа'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_admin_suop()
        orders_page.del_order(order_num)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Статус заказа удален',
            attachment_type=AttachmentType.PNG
        )
        time.sleep(30)
