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

@allure.story('Поиск заказа')
def test_find_order(pre_post_dns, browser):
    """Поиск заказа через форму"""

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
    order_num1 = '140319'

    # step_name = 'Поиск заказа за клиента'
    # with allure.step(step_name):
    #     logger.info('Шаг: ' + step_name)
    #     auth_page.auth_as_client()
    #     orders_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
    #     orders_page.find_order(order_num1)
    #     allure.attach(
    #         body=auth_page.browser.get_screenshot_as_png(),
    #         name='Найденный заказ за клиента',
    #         attachment_type=AttachmentType.PNG
    #     )
    #
    # step_name = 'Поиск заказа за менеджера'
    # with allure.step(step_name):
    #     logger.info('Шаг: ' + step_name)
    #     auth_page.relogin_as_manager()
    #     orders_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
    #     orders_page.find_order(order_num1)
    #     allure.attach(
    #         body=auth_page.browser.get_screenshot_as_png(),
    #         name='Найденный заказ за менеджера',
    #         attachment_type=AttachmentType.PNG
    #     )

    step_name = 'Поиск заказа за администратора'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_admin_suop()
        orders_page.find_order(order_num1)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Найденный заказ за администратора',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Поиск заказа за менеджера 2'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_manager()
        orders_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
        orders_page.find_order(order_num1)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Найденный заказ за менеджера 2',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Поиск заказа за администратора 2'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_admin_suop()
        orders_page.find_order(order_num1)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Найденный заказ за администратора 2',
            attachment_type=AttachmentType.PNG
        )