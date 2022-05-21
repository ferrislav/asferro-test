import secrets
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.base import CommonPage


class ComposePage(CommonPage):

    def __init__(self, driver, locators, settings):
        super(ComposePage, self).__init__(driver, locators, settings)
        self.driver = driver
        self.locators = locators
        self.settings = settings
        # self.compose_button_locator = (By.CSS_SELECTOR, locators["compose_btn"])

    def click_compose_button(self):
        # work on pre assumption that driver is on compose page.
        t = int(self.settings["driver_wait"])
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locators["compose_btn"])))
        button = self.driver.find_element(By.CSS_SELECTOR, self.locators["compose_btn"])
        button.click()
        time.sleep(0.3)
        assert EC.url_contains(self.locators["compose_partial_url"])

    # to go to compose page driver must be on inbox page first
    # compose page url changes so have to use controllers to navigate
    def go_to_compose_page(self):
        if super(ComposePage, self).is_on_compose_page():
            return
        elif super(ComposePage, self).is_on_inbox_page():
            self.click_compose_button()
        else:
            super(ComposePage, self).go_to_inbox_page()
            self.click_compose_button()

    def get_random_str(self):
        r = int(self.settings["str_len"])
        chars = string.ascii_letters + string.digits + string.digits
        return ''.join(secrets.choice(chars) for i in range(r))

    def get_list_tup(self):
        r = int(self.settings["messages_quantity"])
        t_r = int(self.settings["tup_len"])
        l = []
        for i in range(r):
            tmp = []
            for x in range(t_r):
                tmp.append(self.get_random_str())
            l.append(tuple(tmp))
        return l

    def send(self):
        # make sure that driver is in the right location
        if not self.is_on_compose_page():
            self.go_to_compose_page()
        t = int(self.settings["driver_wait"])
        tup_l = int(self.settings["messages_quantity"])
        tup_list = self.get_list_tup()
        assert len(tup_list) == tup_l
        # Make sure that no messages send by me in inbox
        # util.clear_messages()
        # util = Util(self.driver, self.locators, self.settings)
        # messages = util.get_all_by_me()
        #
        # logging.info(f"messages len before delete: {len(messages)}")
        # if len(messages) > 0:
        #     util.delete_all()
        for tup in tup_list:
            self.driver.implicitly_wait(t)
            self.click_compose_button()
            self.send_mail(tup)

    def send_mail(self, str_tup):
        assert len(str_tup) == int(self.settings["tup_len"])
        address = self.locators["user_address"]

        send_mail_wait = int(self.settings["send_mail_wait"])
        wait = WebDriverWait(self.driver, send_mail_wait)
        # must wait until to field is ready
        wait.until(EC.presence_of_element_located((By.ID, self.locators["to_fld_id"])))
        to_fld = self.driver.find_element(By.ID, self.locators["to_fld_id"])

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.locators["subject_fld"])))
        subject_fld = self.driver.find_element(By.CSS_SELECTOR, self.locators["subject_fld"])

        # by this time fields  below are already visible
        body_fld = self.driver.find_element(By.CLASS_NAME, self.locators["body_fld_class"])
        send_button = self.driver.find_element(By.CLASS_NAME, self.locators["send_mail_btn_class"])

        to_fld.send_keys(address)
        subject_fld.send_keys(str_tup[0])
        body_fld.send_keys(str_tup[1])
        send_button.click()
        # otherwise it sends soo quick email box can not distinguish requests.
        time.sleep(0.4)
