import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pytest
import string
import secrets


# delete messages by topic and sender
# delete all messages

@pytest.mark.usefixtures("driver_init")
class Util:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators

    def is_message_container_visible(self):
        for i in range(3):
            try:
                logging.log(logging.INFO, f"Try for message container {i + 1} attempt of 3")
                el = self.driver.find_element(By.XPATH, self.locators["message_list_container_path"])
                if el:
                    break
            except NoSuchElementException:
                time.sleep(3)
                self.driver.refresh()

        return EC.visibility_of_element_located((By.XPATH, self.locators["message_list_container_path"]))

    def get_message_sender(self, msg_elements):
        # go through all message elements and get string sender.
        pass

    def get_all_by_me(self):
        res = []
        inbox_btn = self.driver.find_element(By.CSS_SELECTOR, self.locators["inbox_btn"])
        inbox_btn.click()

        if self.is_message_container_visible():
            messages = self.driver.find_elements(By.CLASS_NAME, self.locators["message_list_item_class"])
            if len(messages) == 0:
                return res
            for message in messages:
                sender = message.find_element(By.XPATH, self.locators["message_sender"])
                sender_name = sender.text
                if sender_name == "me":
                    res.append(message)
        return res

    def delete_all(self):
        select_dropdown_btn = self.driver.find_element(By.XPATH, self.locators["select_dropdown_btn"])
        select_dropdown_btn.click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, self.locators["select_all_btn"])))
        select_all_btn = self.driver.find_element(By.XPATH, self.locators["select_all_btn"])
        select_all_btn.click()
        delete_btn = self.driver.find_element(By.XPATH, self.locators['delete_btn'])
        delete_btn.click()

    def send_mail(self, str_tup):
        assert len(str_tup) == 2
        address = self.locators["user_address"]
        compose_btn = self.driver.find_element(By.CSS_SELECTOR, self.locators["compose_btn"])
        compose_btn.click()
        wait = WebDriverWait(self.driver, 10)
        # must wait until to field is ready
        wait.until(EC.presence_of_element_located((By.ID, self.locators["to_fld_id"])))
        to_fld = self.driver.find_element(By.ID, self.locators["to_fld_id"])
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.locators["subject_fld"])))
        subject_fld = self.driver.find_element(By.CSS_SELECTOR, self.locators["subject_fld"])
        body_fld = self.driver.find_element(By.CLASS_NAME, self.locators["body_fld_class"])
        send_button = self.driver.find_element(By.CLASS_NAME, self.locators["send_mail_btn_class"])
        to_fld.send_keys(address)
        subject_fld.send_keys(str_tup[0])
        body_fld.send_keys(str_tup[1])
        send_button.click()
        self.driver.implicitly_wait(1)
