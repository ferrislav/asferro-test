import pdb
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
import string
import secrets


@pytest.mark.usefixtures("driver_init")
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

    def login_test(self, locators):
        self.driver.get(locators["login_url"])
        # Enter user name and got to next page
        wait = WebDriverWait(self.driver, 10)
        login_fld = self.driver.find_element(By.ID, locators["login_username_id"])
        login_fld.send_keys(locators["user_login"])
        submit = self.driver.find_element(By.ID, locators["login_username_next_btn"])
        submit.click()
        assert EC.url_changes(locators["login_url"])
        assert EC.url_contains(locators["login_pass_partial_url"])
        # enter user pass and submit
        curr_url = self.driver.current_url
        passwd = locators["user_password"]
        wait.until(EC.presence_of_element_located((By.ID, locators["login_pass_fld_id"])))
        pass_fld = self.driver.find_element(By.ID, locators["login_pass_fld_id"])
        pass_submit_btn = self.driver.find_element(By.ID, locators["login_pass_submit_id"])
        pass_fld.send_keys(passwd)
        pass_submit_btn.click()
        assert EC.url_changes(curr_url)
        curr_url = self.driver.current_url
        wait.until(EC.presence_of_element_located((By.ID, locators["mail_link"])))
        mail_btn = self.driver.find_element(By.ID, locators["mail_link"])
        mail_btn.click()
        assert EC.url_changes(curr_url)
        assert EC.url_contains(locators["mail_home_partial_url"])

    def send_test(self, get_list_tup, locators):
        assert len(get_list_tup) == 10
        assert EC.url_contains(locators["mail_home_partial_url"])
        # must be in right location now.
        address = locators["user_address"]
        compose_btn = self.driver.find_element(By.CSS_SELECTOR, locators["compose_btn"])
        compose_btn.click()

        def send_mail(str_tup):
            assert len(str_tup) == 2
            compose_btn.click()
            wait = WebDriverWait(self.driver, 10)
            # must wait until to field is ready
            wait.until(EC.presence_of_element_located((By.ID, locators["to_fld_id"])))
            to_fld = self.driver.find_element(By.ID, locators["to_fld_id"])
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locators["subject_fld"])))
            subject_fld = self.driver.find_element(By.CSS_SELECTOR, locators["subject_fld"])
            body_fld = self.driver.find_element(By.CLASS_NAME, locators["body_fld_class"])
            send_button = self.driver.find_element(By.CLASS_NAME, locators["send_mail_btn_class"])
            to_fld.send_keys(address)
            subject_fld.send_keys(str_tup[0])
            body_fld.send_keys(str_tup[1])
            send_button.click()
            self.driver.implicitly_wait(1)

        for tup in get_list_tup:
            self.driver.implicitly_wait(1)
            send_mail(tup)
