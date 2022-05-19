import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pytest
import pdb
import string
import secrets


# delete messages by topic and sender
# delete all messages

@pytest.mark.usefixtures("driver_init")
class Util:
    def __init__(self, driver, locators, settings):
        self.driver = driver
        self.locators = locators
        self.settings = settings


    def is_element_findable(self, locator):
        try:
            self.driver.find_element(locator)
        except NoSuchElementException:
            return False
        return True


    def is_message_container_present(self):
        # pdb.set_trace()
        is_present = False
        msg_container_loop = int(self.settings["msg_container_loop"])
        msg_container_loop_sleep = int(self.settings["msg_container_loop_sleep"])
        msg_container_rt_sleep = float(self.settings["msg_container_rt_sleep"])
        for i in range(msg_container_loop):
            is_present = self.is_element_findable(locate_with(By.XPATH, self.locators["message_list_container_path"]))
            if is_present:
                break
            time.sleep(msg_container_loop_sleep)
        # give browser time to load component
        time.sleep(msg_container_rt_sleep)
        return is_present

    def click_inbox_btn(self):
        click_inbox_rt_sleep = int(self.settings["click_inbox_rt_sleep"])
        inbox_btn = self.driver.find_element(By.CSS_SELECTOR, self.locators["inbox_btn"])
        inbox_btn.click()
        self.driver.implicitly_wait(click_inbox_rt_sleep)

    def get_all_by_me(self):
        res = []
        self.click_inbox_btn()
        if self.is_message_container_present():
            container = self.driver.find_element(By.XPATH, self.locators["message_list_container_path"])
            # pdb.set_trace()
            messages = container.find_elements(By.CSS_SELECTOR, self.locators["messages_in_container_css"])
            # skip first two
            messages_slice_from = int(self.settings["messages_slice_from"])
            messages_sl = messages[messages_slice_from:]
            if len(messages_sl) == 0:
                return res

            sender_name_test = self.settings["sender_name_test"]
            for message in messages_sl:
                sender = message.find_element(By.XPATH, self.locators["message_sender"])
                sender_name = sender.text
                if sender_name == sender_name_test:
                    res.append(message)
        return res

    def delete_all(self):
        select_dropdown_btn = self.driver.find_element(By.XPATH, self.locators["select_dropdown_btn"])
        select_dropdown_btn.click()
        select_all_btn_wait = int(self.settings["select_all_btn_wait"])
        wait = WebDriverWait(self.driver, select_all_btn_wait)
        wait.until(EC.presence_of_element_located((By.XPATH, self.locators["select_all_btn"])))
        select_all_btn = self.driver.find_element(By.XPATH, self.locators["select_all_btn"])
        select_all_btn.click()
        delete_btn = self.driver.find_element(By.XPATH, self.locators['delete_btn'])
        delete_btn.click()

    def send_mail(self, str_tup):
        assert len(str_tup) == int(self.settings["tup_len"])
        address = self.locators["user_address"]
        compose_btn = self.driver.find_element(By.CSS_SELECTOR, self.locators["compose_btn"])
        compose_btn.click()

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
