import allure
from allure_commons.types import AttachmentType
from src.logger.formatted_logger import logger
from src.pages.main_page import MainPage
from src.pages.auth_page import AuthPage
from src.pages.client_page import ClientPage
from src.pages.orders_page import OrdersPage
from src.pages.kuber_service import KuberService
from config.config import SUOP

def test_kuber(pre_post_browser, browser):
    """Тест услуги kubernetes"""
    main_page = MainPage(browser)  # экземпляр главной страницы с url
    auth_page = AuthPage(browser)
    client_page = ClientPage(browser)
    orders_page = OrdersPage(browser)
    kuber_service = KuberService(browser)

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

    step_name = 'Создание заказа'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        order_num = client_page.make_order()
        logger.info(f'Создан и получен номер заказа №:{order_num}')

    step_name = 'Авторизация за менеджера'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_manager()
        auth_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Личный кабинет менеджера',
            attachment_type=AttachmentType.PNG
        )

    step_name = 'Согласование созданного заказа за менеджера'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        orders_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
        # orders_page.wait_for_page_loaded(client_page.TABLE_WITH_ORDERS_IN_LK)
        orders_page.find_order(order_num)
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Найденный заказ',
            attachment_type=AttachmentType.PNG
        )
        orders_page.approve_order(order_num)

    step_name = f'Разрешение на изменение ресурсов заказа {order_num}'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_manager()
        orders_page.find_order(order_num)
        orders_page.set_rights_resources()
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Разрешение на изменение ресурсов',
            attachment_type=AttachmentType.PNG
        )

    step_name = f'Заказ услуги kubernetes из витрины'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.auth_as_client()
        kuber_service.make_k8s_order()
        allure.attach(
            body=kuber_service.browser.get_screenshot_as_png(),
            name='Страница созданного заказа',
            attachment_type=AttachmentType.PNG
        )

    step_name = f'Вкладка раздела Информация'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        kuber_service.check_info_tab()
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Вкладка раздела Информация',
            attachment_type=AttachmentType.PNG
        )

    step_name = f'Удаление заказа'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        kuber_service.del_k8s_order()
        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Удаленный заказ',
            attachment_type=AttachmentType.PNG
        )

    step_name = f'Удаление заказа {order_num}'
    with allure.step(step_name):
        logger.info('Шаг: ' + step_name)
        auth_page.relogin_as_admin_suop()
        orders_page.del_order(order_num)

        allure.attach(
            body=auth_page.browser.get_screenshot_as_png(),
            name='Удаленный заказ',
            attachment_type=AttachmentType.PNG
        )
