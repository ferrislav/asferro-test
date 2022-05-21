from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.base import CommonPage
from src.login_page import LoginPage
import time
import logging


class HomePage(CommonPage):

    def __init__(self, driver, locators, settings):
        super().__init__(driver, locators, settings)
        self.driver = driver
        self.locators = locators
        self.settings = settings

        self.wait_time = int(self.settings["driver_wait"])

# common div for signin and logged
# div._yb_31tgj
#
# span with user name. when logged in
# span._yb_ynfjo
#
# class name of link to sign in
# a._yb_1vuak

# check if logged in
# if not call loginpage to login.

    def click_mail_button(self):
        """
        Check if on home page if not go there, click mail button on the top right corner
        check if url changes to inbox url.
        :return: bool
        """
        if not self.is_logged():
            lp = LoginPage(self.driver, self.locators, self.settings)
            lp.login()

        wait = WebDriverWait(self.driver, self.wait_time)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators["mail_link"])))
        mail_button = self.driver.find_element(By.CSS_SELECTOR, self.locators["mail_link"])
        mail_button.click()
        time.sleep(0.3)


