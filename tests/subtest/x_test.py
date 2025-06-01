import time

import allure
from allure_commons.types import AttachmentType
from src.pages.main_page import MainPage
from src.pages.auth_page import AuthPage
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
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
    order_num = '134848'

    # step_name = f'Заказ услуги kubernetes из витрины'
    # with allure.step(step_name):
    #     logger.info('Шаг: ' + step_name)
    #     auth_page.auth_as_client()
    #     _, kaas_name = kuber_service.make_k8s_order()
    #     allure.attach(
    #         body=auth_page.browser.get_screenshot_as_png(),
    #         name='Страница созданного заказа',
    #         attachment_type=AttachmentType.PNG
    #     )
    kaas_name = 'Кластер Kubernetes 01.06.2025, 18:30:35'

    step_name = f'Операции с имеющимся заказом Kubernetes'
    ORDER_STATUS_TEXT = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                                   f'/following-sibling::td[2]//p[@class="icon-hint__text"]')
    ORDER_STATUS = (By.XPATH, f'//p[text()="{kaas_name}"]/ancestor::td[1]'
                              f'//following-sibling::td[2]'
                              f'//div[@class="suborder-state-status"]/div[@class="order-subitem-status"]')
    # с созданным заказом k8s
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_page.find_order(order_num)
        MENU_CONTAINERS = (By.XPATH, '//span[contains(text(), "Контейнеры")]')
        MENU_CONTAINERS_K8S = (By.XPATH, '//button[contains(text(), "Kubernetes как сервис")]')
        order_page.click(MENU_CONTAINERS)
        order_page.click(MENU_CONTAINERS_K8S)
        order_page.text_check(ORDER_STATUS_TEXT,
                              'Работает',
                              refresh_timeout=60,
                              hover_element=ORDER_STATUS)
        allure.attach(
            body=kuber_service.browser.get_screenshot_as_png(),
            name='Созданный заказ Kubernetes',
            attachment_type=AttachmentType.PNG
        )

    step_name = f'Проверка вкладки Информация'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        kuber_service.check_info_tab(kaas_name)
        allure.attach(
            body=kuber_service.browser.get_screenshot_as_png(),
            name=step_name,
            attachment_type=AttachmentType.PNG
        )

    step_name = f'Проверка вкладки Узлы'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        kuber_service.check_nodes_tab(kaas_name)

    step_name = f'Проверка раздела Сеть'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        kuber_service.check_net_tab(kaas_name)

    step_name = f'Проверка раздела Постоянные тома'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        kuber_service.check_volume_tab(kaas_name)


    step_name = f'Удаление заказа'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        kuber_service.del_k8s_order(kaas_name)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Удаленный заказ',
            attachment_type=AttachmentType.PNG
        )


