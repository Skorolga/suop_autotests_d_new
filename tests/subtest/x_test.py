import allure
from allure_commons.types import AttachmentType
import pytest
from src.pages.main_page import MainPage
from src.pages.auth_page import AuthPage
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
from src.pages.DNS_service import DnsPage
from config.config import SUOP
from src.logger.formatted_logger import logger

@pytest.fixture
def pre_post_dns(browser):
    """TODO вынести в отдельную фикстуру, в conftest.py"""
    yield
    browser.get(SUOP.MAIN_URL + '/logout')  # TODO логаут по URL, т.к. тест может остановиться на странице где нет меню для выхода, например модальное окно выбора организации

@allure.story('Тестирование фреймворка')
@pytest.mark.serial
def test_x(pre_post_dns, browser):
    """Тест DNS СУ ОП"""

    main_page = MainPage(browser)  # экземпляр главной страницы с url
    auth_page = AuthPage(browser)
    client_page = ClientPage(browser)
    orders_page = OrdersPage(browser)
    order_page = DnsPage(browser)

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
            name=step_name,
            attachment_type=AttachmentType.PNG
        )
    order_num = '124164'
    domain = 'autotest'

    step_name = 'Добавление поддомена'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        orders_page.find_order(order_num)
        order_page.add_sub_domain(domain)
        order_page.browser.refresh()  # TODO без обновления кнопка добавления DNS записи неактивна

    step_name = 'Добавление DNS запись типа CNAME'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_page.add_dns_entry_cname(domain)
        allure.attach(
            body=order_page.browser.get_screenshot_as_png(),
            name='DNS запись типа CNAME',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Добавление DNS запись типа MX'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_page.add_dns_entry_mx(domain)
        allure.attach(
            body=order_page.browser.get_screenshot_as_png(),
            name='DNS запись типа MX',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Добавление DNS запись типа SRV'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_page.add_dns_entry_srv(domain)
        allure.attach(
            body=order_page.browser.get_screenshot_as_png(),
            name='DNS запись типа SRV',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Добавление DNS запись типа TXT'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_page.add_dns_entry_txt(domain)
        allure.attach(
            body=order_page.browser.get_screenshot_as_png(),
            name='DNS запись типа TXT',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Добавление DNS запись типа A'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_page.add_dns_entry_a()
        allure.attach(
            body=order_page.browser.get_screenshot_as_png(),
            name='DNS запись типа А',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Удаление домена'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_page.del_sub_domain(domain)
        allure.attach(
            body=order_page.browser.get_screenshot_as_png(),
            name=step_name,
            attachment_type=AttachmentType.PNG
        )
