from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

class CommonPage:
    def __init__(self, driver, locators, settings):
        self.driver = driver
        self.locators = locators
        self.settings = settings

    def is_logged(self):
        user_name_span = self.locators["user_name_span"]
        try:
            self.driver.find_element(By.CSS_SELECTOR, user_name_span)
        except NoSuchElementException:
            return False

        return True

    def is_not_logged(self):
        signup_locator = self.locators["signup_locator"]
        # find link and check if it's sign pu
        try:
            link = self.driver.find_element(By.CSS_SELECTOR, signup_locator)
        except NoSuchElementException:
            return True

        assert "Sign up" == link.text
        return False

    # functions to check location.
    def is_on_compose_page(self):
        url = self.driver.current_url
        return url == self.locators["compose_partial_url"]

    def is_on_inbox_page(self):
        url = self.driver.current_url
        return url == self.locators["inbox_partial_url"]

    def is_on_home_page(self):
        wait = WebDriverWait(self.driver, 3)
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators["mail_link"])))
            return True
        except NoSuchElementException:
            return False

    def is_on_login_page(self):
        url = self.driver.current_url
        return url == self.locators["login_url"]


    def is_on_messages_page(self):
        url = self.driver.current_url
        return url == self.locators["messages_partial_url"]


    # inbox page url is always the same so easiest way is simply navigate
    def go_to_inbox_page(self):
        self.driver.get(self.locators["inbox_url"])
        time.sleep(0.5)


    def go_to_home_page(self):
        self.driver.get(self.locators["home_page"])
        time.sleep(0.5)

    def go_to_login_page(self):
        self.driver.get(self.locators["login_url"])
        time.sleep(0.5)