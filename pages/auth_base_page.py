from .locators import AuthLocators
from urllib.parse import urlparse


class BasePage(object):

    def __init__(self, driver, url, timeout=10):
        self.driver = driver
        self.url = url
        self.driver.implicitly_wait(timeout)

    def get_relative_link(self):
        url = urlparse(self.driver.current_url)
        return url.path

    def scroll_down(self, offset=0):

        if offset:
            self.driver.execute_script(
                'window.scrollTo(0, {0});'.format(offset)
            )
        else:
            self.driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);'
            )

    def scroll_up(self, offset=0):

        if offset:
            self.driver.execute_script(
                'window.scrollTo(0, -{0});'.format(offset)
            )
        else:
            self.driver.execute_script(
                'window.scrollTo(0, -document.body.scrollHeight);'
            )


class AuthPage(BasePage):

    def __init__(self, driver, timeout=10, ):
        super().__init__(driver, timeout)
        url = 'https://b2c.passport.rt.ru'
        driver.get(url)

        self.tab_phone = driver.find_element(
            *AuthLocators.tab_phone
        )
        self.active_tab_phone = driver.find_element(
            *AuthLocators.active_tab_phone
        )
        self.tab_email = driver.find_element(
            *AuthLocators.tab_email
        )
        self.email = driver.find_element(
            *AuthLocators.auth_email
        )
        self.password_email = driver.find_element(
            *AuthLocators.auth_pass_email
        )
        self.button_enter = driver.find_element(
            *AuthLocators.auth_button_enter
        )
        self.tab_login = driver.find_element(
            *AuthLocators.tab_login
        )
        self.login = driver.find_element(
            *AuthLocators.auth_login
        )
        self.password_login = driver.find_element(
            *AuthLocators.auth_password_login
        )
        self.tab_ls = driver.find_element(
            *AuthLocators.tab_ls
        )
        self.placeholder_name_of_user = driver.find_element(
            *AuthLocators.placeholder_name_of_user
        )
        self.forgot_password_link = driver.find_element(
            *AuthLocators.forgot_password_link
        )
        self.register_link = driver.find_element(
            *AuthLocators.register_link
        )
        self.page_right = driver.find_element(
            *AuthLocators.page_right
        )
        self.page_left = driver.find_element(
            *AuthLocators.page_left
        )
        self.card_of_auth = driver.find_element(
            *AuthLocators.card_of_auth
        )
        self.menu_tab = driver.find_element(
            *AuthLocators.menu_tab
        )

    def find_other_element(self, by, location):
        return self.driver.find_element(by, location)
