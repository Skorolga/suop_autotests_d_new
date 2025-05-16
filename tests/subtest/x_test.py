import time

import allure
from allure_commons.types import AttachmentType
from src.pages.main_page import MainPage
from src.pages.auth_page import AuthPage
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
from src.pages.DNS_service import DnsPage
from src.pages.kuber_service import KuberService
from config.config import SUOP
from src.logger.formatted_logger import logger
from selenium.webdriver.common.by import By


def test_x(pre_post_browser, browser):
    """Тест DNS СУ ОП"""

    main_page = MainPage(browser)  # экземпляр главной страницы с url
    auth_page = AuthPage(browser)
    client_page = ClientPage(browser)
    kuber_service = KuberService(browser)
    order_page = OrdersPage(browser)

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
    order_num = '132811'

    # step_name = f'Заказ услуги kubernetes из витрины'
    # with allure.step(step_name):
    #     logger.info('Шаг: ' + step_name)
    #     auth_page.auth_as_client()
    #     kuber_service.make_k8s_order()
    #     allure.attach(
    #         body=auth_page.browser.get_screenshot_as_png(),
    #         name='Страница создания заказа',
    #         attachment_type=AttachmentType.PNG
    #     )

    step_name = f'Заказ услуги kubernetes из витрины'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_page.find_order(order_num)
        MENU_CONTAINERS = (By.XPATH, '//span[contains(text(), "Контейнеры")]')
        MENU_CONTAINERS_K8S = (By.XPATH, '//button[contains(text(), "Kubernetes как сервис")]')
        order_page.click(MENU_CONTAINERS)
        order_page.click(MENU_CONTAINERS_K8S)
        order_page.text_check(kuber_service.ORDER_STATUS_TEXT, 'Работает', 60 * 15, kuber_service.ORDER_STATUS)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Созданный заказ Kubernetes',
            attachment_type=AttachmentType.PNG
        )

    step_name = f'Проверка вкладки Информация'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        kuber_service.check_info_tab()
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name=step_name,
            attachment_type=AttachmentType.PNG
        )

