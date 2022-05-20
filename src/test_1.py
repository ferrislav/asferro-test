import logging
import pdb
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
import string
import secrets
from src.util import Util


@pytest.mark.usefixtures("driver_init", "tests_init")
class TestLogin:

    def get_random_str(self):
        r = int(self.settings["str_len"])
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for i in range(r))

    @pytest.fixture(scope="function")
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

    def send_login_test(self):
        t = int(self.settings["driver_wait"])
        self.driver.get(self.locators["login_url"])
        # Enter user name and got to next page
        wait = WebDriverWait(self.driver, t)
        wait.until(EC.presence_of_element_located((By.ID, self.locators["login_username_next_btn"])))
        login_fld = self.driver.find_element(By.ID, self.locators["login_username_id"])
        login_fld.send_keys(self.locators["user_login"])
        submit = self.driver.find_element(By.ID, self.locators["login_username_next_btn"])
        submit.click()
        assert EC.url_changes(self.locators["login_url"])
        assert EC.url_contains(self.locators["login_pass_partial_url"])

    def send_pass_test(self):
        # enter user pass and submit
        t = int(self.settings["driver_wait"])
        wait = WebDriverWait(self.driver, t)
        curr_url = self.driver.current_url
        passwd = self.locators["user_password"]
        wait.until(EC.visibility_of_element_located((By.ID, self.locators["login_pass_fld_id"])))
        pass_fld = self.driver.find_element(By.ID, self.locators["login_pass_fld_id"])
        wait.until(EC.visibility_of_element_located((By.ID, self.locators["login_pass_submit_id"])))
        pass_submit_btn = self.driver.find_element(By.ID, self.locators["login_pass_submit_id"])
        pass_fld.send_keys(passwd)
        pass_submit_btn.click()
        assert EC.url_changes(curr_url)
        assert EC.url_contains("password")

    def go_to_inbox_test(self):
        t = int(self.settings["driver_wait"])
        wait = WebDriverWait(self.driver, t)
        curr_url = self.driver.current_url
        wait.until(EC.visibility_of_element_located((By.ID, self.locators["mail_link"])))
        mail_btn = self.driver.find_element(By.ID, self.locators["mail_link"])
        mail_btn.click()
        assert EC.url_changes(curr_url)
        assert EC.url_contains(self.locators["mail_home_partial_url"])

    def send_test(self, get_list_tup):
        t = int(self.settings["driver_wait"])
        tup_l = int(self.settings["messages_quantity"])
        assert len(get_list_tup) == tup_l
        assert EC.url_contains(self.locators["mail_home_partial_url"])
        # Make sure that no messages send by me in inbox
        util = Util(self.driver, self.locators, self.settings)
        messages = util.get_all_by_me()
        logging.info(f"messages len before delete: {len(messages)}")
        if len(messages) > 0:
            util.delete_all()
        for tup in get_list_tup:
            self.driver.implicitly_wait(t)
            util.send_mail(tup)
