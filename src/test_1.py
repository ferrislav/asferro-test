from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.login_page import LoginPage
import pytest

@pytest.mark.usefixtures("driver_init", "tests_init")
class TestLogin:

    def login_test(self):
        lp = LoginPage(self.driver, self.locators, self.settings)
        lp.login()
        assert EC.url_contains(self.locators["home_url"])
        assert lp.is_logged()
