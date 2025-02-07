import time
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
    yield
    auth_page = Auth(browser)
    auth_page.logout()

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
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Главня_страница',
            attachment_type=AttachmentType.PNG
        )

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
        client_page.make_order()
        client_page.wait_for_page_loaded(client_page.FORM_TITLE_CONF)
        order_cost_without_tax = client_page.find_elem(client_page.COST_WITHOUT_TAX)
        logger.info(order_cost_without_tax.text)
        while True:
            logger.info(order_cost_without_tax.text.strip())
            if order_cost_without_tax.text.strip() == '':
                continue
            cost = float(order_cost_without_tax.text.strip())
            if cost > 0:
                break
            time.sleep(0.5)
        allure.attach(
            body=main_page.browser.get_screenshot_as_png(),
            name='Страница с формой для создания заказа',
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
