from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.base import CommonPage


# it's actually two pages for login name and login pass, but will use one object
class LoginPage(CommonPage):

    def __init__(self, driver, locators, settings):
        super(LoginPage, self).__init__(driver, locators, settings)
        self.driver = driver
        self.locators = locators
        self.settings = settings
        self.wait_time = settings["driver_wait"]

    def enter_login(self):
        self.go_to_login_page()
        # Enter user name and got to next page
        wait = WebDriverWait(self.driver, self.wait_time)
        wait.until(EC.presence_of_element_located((By.ID, self.locators["login_username_next_btn"])))
        login_fld = self.driver.find_element(By.ID, self.locators["login_username_id"])
        login_fld.send_keys(self.locators["user_login"])
        submit = self.driver.find_element(By.ID, self.locators["login_username_next_btn"])
        submit.click()
        assert EC.url_contains(self.locators["login_pass_partial_url"])

    def enter_pass(self):
        self.enter_login()
        assert EC.url_contains("password")
        # enter user pass and submit
        wait = WebDriverWait(self.driver, self.wait_time)
        passwd = self.locators["user_password"]
        wait.until(EC.visibility_of_element_located((By.ID, self.locators["login_pass_fld_id"])))
        pass_fld = self.driver.find_element(By.ID, self.locators["login_pass_fld_id"])
        wait.until(EC.visibility_of_element_located((By.ID, self.locators["login_pass_submit_id"])))
        pass_submit_btn = self.driver.find_element(By.ID, self.locators["login_pass_submit_id"])
        pass_fld.send_keys(passwd)
        pass_submit_btn.click()

    def login(self):
        if self.is_not_logged():
            # enter_pass calls enter_login
            self.enter_pass()
