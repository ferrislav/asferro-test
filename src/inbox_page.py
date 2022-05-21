import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from src.base import CommonPage
import logging
import pdb


class InboxPage(CommonPage):

    def __init__(self, driver, locators, settings):
        super().__init__(driver, locators, settings)
        self.driver = driver
        self.locators = locators
        self.settings = settings


    def click_inbox_btn(self):
        if not self.is_on_inbox_page():
            self.go_to_inbox_page()
        inbox_btn = self.driver.find_element(By.XPATH, self.locators["inbox_btn"])
        inbox_btn.click()

    def get_all_by_me(self):
        """
        Search for messages and filter out these which I didn't send
        :return: List of links for messages
        """
        res = []
        if not self.is_on_inbox_page():
            self.go_to_inbox_page()

        messages = self.driver.find_elements(By.XPATH, self.locators["all_messages"])
        if len(messages) == 0:
            return res
        sender_name_test = self.settings["sender_name_test"]
        for message in messages:
            try:
                sender = self.driver.find_element(By.XPATH, self.locators["message_sender"])
                sender_name = sender.text
                if sender_name.__eq__(sender_name_test):
                    res.append(message)
            except Exception as e:
                logging.info(f"{e.__class__}")
        return res

    def delete_all(self):
        if not self.is_on_inbox_page():
            self.go_to_inbox_page()
        select_all_btn_wait = int(self.settings["select_all_btn_wait"])
        wait = WebDriverWait(self.driver, select_all_btn_wait)

        wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["select_dropdown_btn"])))
        select_dropdown_btn = self.driver.find_element(By.XPATH, self.locators["select_dropdown_btn"])
        select_dropdown_btn.click()
        wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["select_all_btn"])))
        select_all_btn = self.driver.find_element(By.XPATH, self.locators["select_all_btn"])
        select_all_btn.click()
        wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["delete_btn"])))
        delete_btn = self.driver.find_element(By.XPATH, self.locators["delete_btn"])
        delete_btn.click()


    def is_inbox_empty(self):
        """
        Loops and wait for at least some messages appear in inbox.
        :return: bool; true if inbox is empty, false otherwise
        """
        if not self.is_on_inbox_page():
            self.go_to_inbox_page()

        WebDriverWait(self.driver, 10)\
            .until(EC.presence_of_element_located((By.ID, self.locators["mail_app_component_id"])))
        # loop while empty or exceeds
        for _ in range(5):
            try:
                info_message = self.driver.find_element(By.XPATH, self.locators["info_message_path"])
                info_message_srt = info_message.text
                if "folder is empty" in info_message_srt:
                    time.sleep(2)
                    self.click_inbox_btn()
                    continue
            except NoSuchElementException:
                return False
        return True



    def all_messages_arrived(self):
        """
        Loops and wait for all messages to arrive.
        :return: bool; true if all arrived, false otherwise
        """
        if not self.is_on_inbox_page():
            self.go_to_inbox_page()
        m_length = int(self.settings["messages_quantity"])
        for i in range(4):
            messages = self.get_all_by_me()
            time.sleep(0.3)
            if len(messages) == m_length:
                return True
            else:
                time.sleep(5)
                self.click_inbox_btn()
        return False
