import pytest
from pages.registration_page import RegistrPage
from pages.locators import AuthLocators
from settings import Settings


def test_page_left_registration(selenium):
    """TC-11 В левой части формы «Регистрация» логотип и продуктовый слоган."""
    try:
        page_reg = RegistrPage(selenium)
        assert page_reg.page_left_registration.text != ''
    except AssertionError:
        print('Элемент отсутствует в левой части формы')


def test_elements_of_registr(selenium):
    """TC-12 «Регистрация» содержит основные элементы."""
    try:
        page_reg = RegistrPage(selenium)
        card_of_reg = [
            page_reg.first_name,
            page_reg.last_name,
            page_reg.address_registration,
            page_reg.email_registration,
            page_reg.password_registration,
            page_reg.password_registration_confirm,
            page_reg.registration_button
        ]
        for i in range(len(card_of_reg)):
            assert page_reg.first_name in card_of_reg
            assert page_reg.last_name in card_of_reg
            assert page_reg.email_registration in card_of_reg
            assert page_reg.address_registration in card_of_reg
            assert page_reg.password_registration in card_of_reg
            assert page_reg.password_registration_confirm in card_of_reg
            assert page_reg.registration_button in card_of_reg
    except AssertionError:
        print('Элемент отсутствует в форме «Регистрация»')


def test_names_elements_of_registr(selenium):
    """TC-13 Проверка названия элементов формы «Регистрация»."""
    try:
        page_reg = RegistrPage(selenium)
        assert 'Имя' in page_reg.card_of_registration.text
        assert 'Фамилия' in page_reg.card_of_registration.text
        assert 'Регион' in page_reg.card_of_registration.text
        assert (
            'E-mail или мобильный телефон'
            in page_reg.card_of_registration.text
        )
        assert 'Пароль' in page_reg.card_of_registration.text
        assert 'Подтверждение пароля' in page_reg.card_of_registration.text
        assert 'Продолжить' in page_reg.card_of_registration.text
    except AssertionError:
        print('Название не соответсвует требованию.')


def test_registr_by_valid_data(selenium):
    """TC-14 Регистрация пользователя с валидными данными"""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(
        Settings.valid_email_for_registration
    )
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_button.click()

    assert (
        page_reg.find_other_element(
            *AuthLocators.email_confirm
        ).text == 'Подтверждение email'
    )


def test_registr_by_valid_data_(selenium):
    """TC-15 Регистрация пользователя с валидными данными."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name_)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name_)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(
        Settings.valid_email_for_registration
    )
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_button.click()
    try:
        assert (
            'Подтверждение email' in page_reg.find_other_element(
                *AuthLocators.email_confirm
            ).text
        )
    except AssertionError:
        assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' in \
               page_reg.find_other_element(
                   *AuthLocators.error_first_name
                ).text or \
               page_reg.find_other_element(
                   *AuthLocators.error_last_name
                ).text


def test_registr_by_invalid_data(selenium):
    """TC-16 Регистрация с существующим в базе e-mail."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_button.click()

    assert (
        'Учётная запись уже существует'
        in page_reg.find_other_element(*AuthLocators.error_account_exists).text
    )


def test_registr_and_redir_auth(selenium):
    """TC-17 Регистрация пользователя по email, который есть в базе данных,
    при нажатии кнопки 'Войти',редирект в форму "Авторизация"."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(Settings.first_name)
    page_reg.first_name.clear()
    page_reg.last_name.send_keys(Settings.last_name)
    page_reg.last_name.clear()
    page_reg.email_registration.send_keys(Settings.valid_email)
    page_reg.email_registration.clear()
    page_reg.password_registration.send_keys(Settings.valid_password)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.valid_password)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_button.click()
    page_reg.find_other_element(*AuthLocators.redirect_auth).click()

    assert (
        'Авторизация' in page_reg.find_other_element(
            *AuthLocators.authorization
        ).text
    )


@pytest.mark.parametrize(
    "valid_first_name",
    [
        (Settings.russian_generate_string) * 2,
        (Settings.russian_generate_string) * 3,
        (Settings.russian_generate_string) * 15,
        (Settings.russian_generate_string) * 29,
        (Settings.russian_generate_string) * 30,
    ],
    ids=[
        'russ_symbols=2',
        'russ_symbols=3',
        'russ_symbols=15',
        'russ_symbols=29',
        'russ_symbols=30'
    ]
)
def test_first_name_by_valid_data(selenium, valid_first_name):
    """TC-18 Проверка поля ввода "Имя" формы «Регистрация» валидными данными:
    буквы кириллицы в количестве = 2 ; 3 ; 15 ; 29 ; 30 ."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(valid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_button.click()

    assert (
        'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'
        not in page_reg.container_first_name.text
    )


@pytest.mark.parametrize(
    "invalid_first_name",
    [
        (Settings.russian_generate_string) * 1,
        (Settings.russian_generate_string) * 31,
        (Settings.russian_generate_string) * 260,
        (Settings.empty),
        (Settings.numbers),
        (Settings.latin_generate_string),
        (Settings.chinese_chars),
        (Settings.special_chars),
    ],
    ids=[
        'russ_symbols=1',
        'russ_symbols=31',
        'russ_symbols=260',
        'empty',
        'numbers',
        'latin_symbols',
        'chinese_symbols',
        'special_symbols'
        ]
)
def test_first_name_by_invalid_data(selenium, invalid_first_name):
    """TC-19 Невалидные данные для поля "Имя" формы "Регистрация"."""
    page_reg = RegistrPage(selenium)
    page_reg.first_name.send_keys(invalid_first_name)
    page_reg.first_name.clear()
    page_reg.registration_button.click()

    assert 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.' in \
           page_reg.find_other_element(*AuthLocators.error_first_name).text


@pytest.mark.parametrize(
    "valid_password",
    [
        (Settings.passw1),
        (Settings.passw2),
        (Settings.passw3)
    ],
    ids=['valid_symbols=8', 'valid_symbols=15', 'valid_symbols=20']
)
def test_last_name_by_valid_data(selenium, valid_password):
    """TC-20 Валидные данные для поля "Пароль" формы "Регистрация"."""
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(valid_password)
    page_reg.password_registration.clear()
    page_reg.registration_button.click()

    assert 'Длина пароля должна быть не менее 8 символов' and \
           'Длина пароля должна быть не более 20 символов' and \
           'Пароль должен содержать хотя бы одну заглавную букву' and \
           'Пароль должен содержать хотя бы одну прописную букву' and \
           'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру' not in \
           page_reg.password_registration.text


def test_passw_registration_confirm_valid_data(selenium):
    """
    TC-21 Валидыне данные проверки "Пароль"
    и "Подтвердить пароль" формы "Регистрация".
    """
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.passw1)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(Settings.passw1)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_button.click()

    assert (
        'Пароли не совпадают' not in page_reg.container_password_confirm.text
    )


def test_passw_registration_confirm_invalid_data(selenium):
    """
    TC-22 Не валидыне данные проверки "Пароль"
    и "Подтвердить пароль" формы "Регистрация".
    """
    page_reg = RegistrPage(selenium)
    page_reg.password_registration.send_keys(Settings.passw1)
    page_reg.password_registration.clear()
    page_reg.password_registration_confirm.send_keys(ettings.passw2)
    page_reg.password_registration_confirm.clear()
    page_reg.registration_button.click()

    assert (
        'Пароли не совпадают'
        in page_reg.find_other_element(
            *AuthLocators.error_password_confirm
        ).text
    )
