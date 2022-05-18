from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
import string
import secrets
# delete messages by topic and sender
# delete all messages

@pytest.mark.usefixtures("driver_init")
class Util:
    def __init__(self, driver):
        self.driver = driver


    def get_message_sender(self, locators, msg_elements):
        # go through all message elements and get string sender.
        pass

    def get_all_by_me(self, locators):
        # press inbox
        res = []
        inbox_btn = self.driver.find_element(By.CSS_SELECTOR, locators["inbox_btn"])
        inbox_btn.click()
        wait = WebDriverWait(self.driver, 180, 1)
        wait.until(EC.presence_of_element_located((By.XPATH, locators["message_list_container_path"])))

        if EC.visibility_of_element_located((By.XPATH, locators["message_list_container_path"])):
            messages = self.driver.find_elements(By.CLASS_NAME, locators["message_list_item_class"])
            if len(messages) == 0:
                return
            for message in messages:
                sender = message.find_element(By.CSS_SELECTOR, locators["message_sender"])
                sender_name = sender.text
                if sender_name == "me":
                    res.append(message)
        return res

    def delete_all(self, locators):
        select_dropdown_btn = self.driver.find_element(By.XPATH, locators["select_dropdown_btn"])
        select_dropdown_btn.click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, locators["select_all_btn"])))
        select_all_btn = self.driver.find_element(By.XPATH, locators["select_all_btn"])
        select_all_btn.click()
        delete_btn = self.driver.find_element(By.XPATH, locators['delete_btn'])
        delete_btn.click()