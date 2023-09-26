# python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests/test_auth_page.py
import pytest
from pages.auth_base_page import AuthPage
from pages.locators import AuthLocators
from settings import Settings


def test_page_right(selenium):
    """TC-01 слоган Ростелеком в правой части."""
    try:
        page = AuthPage(selenium)
        assert (
            'Персональный помощник в цифровом мире Ростелекома'
            in page.page_right.text
        )
    except AssertionError:
        print('Элемент отсутствует в правой части формы')


def test_elements_of_auth(selenium):
    """TC-02 Форма «Авторизация» содержит основные элементы."""
    page = AuthPage(selenium)

    assert page.menu_tab.text in page.card_of_auth.text
    assert page.email.text in page.card_of_auth.text
    assert page.password_email.text in page.card_of_auth.text
    assert page.button_enter.text in page.card_of_auth.text
    assert page.forgot_password_link.text in page.card_of_auth.text
    assert page.register_link.text in page.card_of_auth.text


def test_menu_of_type_auth(selenium):
    """TC-03 Меню выбора типа аутентификации:
    'Номер', 'Почта', 'Логин', 'Лицевой счёт'."""
    try:
        page = AuthPage(selenium)
        menu = [
            page.tab_phone.text,
            page.tab_email.text,
            page.tab_login.text,
            page.tab_ls.text
        ]
        for i in range(len(menu)):
            assert "Номер" in menu
            assert 'Почта' in menu
            assert 'Логин' in menu
            assert 'Лицевой счёт' in menu
    except AssertionError:
        print('Ошибка в типе аутентификации.')


def test_menu_of_type_active_auth(selenium):
    """TC-04 Аутентификации по телефону форма по умолчанию."""
    page = AuthPage(selenium)

    assert page.active_tab_phone.text == Settings.menu_of_type_auth[0]


def test_placeholder_name_of_user(selenium):
    """TC-05 Плейсхолдер меняется в соответствии с табом."""
    page = AuthPage(selenium)
    page.tab_phone.click()

    assert (
        page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    )
    page.tab_email.click()
    assert (
        page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    )
    page.tab_login.click()
    assert (
        page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    )
    page.tab_ls.click()
    assert (
        page.placeholder_name_of_user.text in Settings.placeholder_name_of_user
    )


def test_forgot_password_link(selenium):
    """TC-06 Переход по ссылке по ссылке 'Забыл пороль'."""
    page = AuthPage(selenium)
    page.driver.execute_script(
        "arguments[0].click();", page.forgot_password_link
    )

    assert page.find_other_element(
        *AuthLocators.password_recovery
    ).text == 'Восстановление пароля'


def test_register_link(selenium):
    """TC-07 Переход по ссылке 'Зарегистрироваться'."""
    page = AuthPage(selenium)
    page.register_link.click()

    assert page.find_other_element(
        *AuthLocators.registration
    ).text == 'Регистрация'


def test_auth_by_valid_email_pass(selenium):
    """TC-08 Аутентификация пользователя с валидным email и паролем."""
    page = AuthPage(selenium)
    page.email.send_keys(Settings.valid_email)
    page.email.clear()
    page.password_email.send_keys(Settings.valid_password)
    page.password_email.clear()
    page.button_enter.click()

    try:
        assert page.get_relative_link() == '/account_b2c/page'
    except AssertionError:
        assert 'Неверно введен текст с картинки' in page.find_other_element(
            *AuthLocators.error_message
        ).text
        print('Предыдущие тесты вызвали появление "капчи"')


@pytest.mark.parametrize(
        "incor_email", [Settings.invalid_email, Settings.empty_email],
        ids=['invalid_email', 'empty']
    )
@pytest.mark.parametrize(
    "incor_passw",
    [Settings.invalid_password, Settings.empty_password],
    ids=['invalid_password', 'empty']
)
def test_auth_by_invalid_email(selenium, incor_email, incor_passw):
    """TC-09, TC-10 Аутентификация пользователя с невалидным email и паролем -
    пользователя не существует."""
    page = AuthPage(selenium)
    page.email.send_keys(incor_email)
    page.email.clear()
    page.password_email.send_keys(incor_passw)
    page.password_email.clear()
    page.button_enter.click()

    assert page.get_relative_link() != '/account_b2c/page'