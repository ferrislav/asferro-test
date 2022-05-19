import pdb
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
import string
import secrets
from src.util import Util


@pytest.mark.usefixtures("driver_init", "locators_init")
class TestSend:

    def get_random_str(self):
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for i in range(10))

    @pytest.fixture(scope="function")
    def get_list_tup(self):
        l = []
        for i in range(10):
            tmp = []
            for x in range(2):
                tmp.append(self.get_random_str())
            l.append(tuple(tmp))
        return l

    def login_test(self):
        self.driver.get(self.locators["login_url"])
        # Enter user name and got to next page
        wait = WebDriverWait(self.driver, 10)
        login_fld = self.driver.find_element(By.ID, self.locators["login_username_id"])
        login_fld.send_keys(self.locators["user_login"])
        submit = self.driver.find_element(By.ID, self.locators["login_username_next_btn"])
        submit.click()
        assert EC.url_changes(self.locators["login_url"])
        assert EC.url_contains(self.locators["login_pass_partial_url"])
        # enter user pass and submit
        curr_url = self.driver.current_url
        passwd = self.locators["user_password"]
        wait.until(EC.presence_of_element_located((By.ID, self.locators["login_pass_fld_id"])))
        pass_fld = self.driver.find_element(By.ID, self.locators["login_pass_fld_id"])
        pass_submit_btn = self.driver.find_element(By.ID, self.locators["login_pass_submit_id"])
        pass_fld.send_keys(passwd)
        pass_submit_btn.click()
        assert EC.url_changes(curr_url)
        curr_url = self.driver.current_url
        wait.until(EC.presence_of_element_located((By.ID, self.locators["mail_link"])))
        mail_btn = self.driver.find_element(By.ID, self.locators["mail_link"])
        mail_btn.click()
        assert EC.url_changes(curr_url)
        assert EC.url_contains(self.locators["mail_home_partial_url"])

    def send_test(self, get_list_tup):
        assert len(get_list_tup) == 10
        assert EC.url_contains(self.locators["mail_home_partial_url"])
        # Make sure that no messages which send by me in inbox
        util = Util(self.driver, self.locators)
        messages = util.get_all_by_me()
        if len(messages) > 0:
            util.delete_all()
        # must be in right location now. And ready to conduct tests.
        # address = self.locators["user_address"]
        # compose_btn = self.driver.find_element(By.CSS_SELECTOR, self.locators["compose_btn"])
        # compose_btn.click()
        for tup in get_list_tup:
            self.driver.implicitly_wait(2)
            util.send_mail(tup)
