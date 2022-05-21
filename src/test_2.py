import pytest
from selenium.webdriver.support import expected_conditions as EC

from src.home_page import HomePage


@pytest.mark.usefixtures("driver_init", "tests_init")
class TestHomePage:

    def is_logged_test(self):
        hp = HomePage(self.driver, self.locators, self.settings)
        assert hp.is_logged()

    def go_to_inbox_test(self):
        hp = HomePage(self.driver, self.locators, self.settings)
        hp.click_mail_button()
        assert EC.url_contains(self.locators["inbox_partial_url"])
