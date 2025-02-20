import time
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
import pytest
from src.pages.main_page import MainPage
from src.pages.auth_page import Auth
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
from src.pages.order_page import OrderPage
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
    auth_page = Auth(browser)
    client_page = ClientPage(browser)
    orders_page = OrdersPage(browser)
    order_page = OrderPage(browser)

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
    order_num = '120853'
    step_name = 'Открытие заказа за клиента'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        orders_page.find_order(order_num, clear_filter=False)
        composite_locator = (By.XPATH, f'//td[contains(text(),"{order_num}")]')
        orders_page.click(composite_locator)
        order_page.click(order_page.MENU_INF_NETWORK)
        order_page.click(order_page.MENU_INF_NETWORK__DNS)  # Раскрываем в меню настройки ДНС
        order_page.wait_for_page_loaded(order_page.DOMAIN_TITLE)
        # logger.info(order_page.get_text(order_page.DOMAIN_TITLE))
        assert 'Домены' in order_page.find_elem(order_page.DOMAIN_TITLE).text, 'Заголовок "Домены" не найден'
        domains_count = int(''.join([i for i in order_page.find_elem(order_page.DOMAIN_TITLE).text if i.isdigit()]))
        assert domains_count
        assert domains_count > 0, 'не указано количество доменов в заголовке'
        time.sleep(3)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Найденный заказ',
            attachment_type=AttachmentType.PNG
        )

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
    #
    #
    # step_name = 'Удаление заказа'
    # with allure.step(step_name):
    #     logger.info('Шаг: ' + step_name)
    #     auth_page.relogin_as_admin_suop()
    #     orders_page.del_order(order_num)
    #     allure.attach(
    #         body=main_page.browser.get_screenshot_as_png(),
    #         name='Статус заказа удален',
    #         attachment_type=AttachmentType.PNG
    #     )
    #     time.sleep(30)
