import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


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
        return EC.url_contains(self.locators["compose_partial_url"])

    def is_on_inbox_page(self):
        return EC.url_contains(self.locators["inbox_partial_url"])

    def is_on_home_page(self):
        self.driver.implicitly_wait(2)
        # if it has this button must be home page
        return EC.visibility_of_element_located(By.CSS_SELECTOR, self.locators["mail_link"])

    def is_on_login_page(self):
        return EC.url_contains(self.locators["login_url"])


    def is_on_messages_page(self):
        return EC.url_contains(self.locators["messages_partial_url"])


    # inbox page url is always the same so easiest way is simply navigate
    def go_to_inbox_page(self):
        self.driver.get(self.locators["inbox_url"])
        time.sleep(0.5)
        assert self.is_on_inbox_page()


    def go_to_home_page(self):
        self.driver.get(self.locators["home_page"])
        time.sleep(0.5)
        assert self.is_on_home_page()

    def go_to_login_page(self):
        self.driver.get(self.locators["login_url"])
        time.sleep(0.5)
        assert self.is_on_login_page()

    # def is_element_findable(self, locator):
    #     try:
    #         self.driver.find_element(locator)
    #     except NoSuchElementException:
    #         return False
    #     return True

   #  def is_message_container_present(self):
   #      # pdb.set_trace()
   #      is_present = False
   #      msg_container_loop = int(self.settings["msg_container_loop"])
   #      msg_container_loop_sleep = int(self.settings["msg_container_loop_sleep"])
   #      msg_container_rt_sleep = float(self.settings["msg_container_rt_sleep"])
   #      for i in range(msg_container_loop):
   #          is_present = self.is_element_findable(
   #              locate_with(By.CSS_SELECTOR, self.locators["message_list_container_ul"]))
   #          if is_present:
   #              break
   #          time.sleep(msg_container_loop_sleep)
   #      # give browser time to load component
   #      time.sleep(msg_container_rt_sleep)
   #      return is_present
