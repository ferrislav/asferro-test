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
        # self.driver.implicitly_wait(3)
        # original:            //*[@id="mail-app-component"]/div/div/div/div[2]/div/div/div[3]/div/div[1]/ul
        # what is in browser: //*[@id="mail-app-component"]/div/div/div/div[2]/div/div
        # in browser get all://*[@id="mail-app-component"]/div/div/div/div[2]/div/div//ul/li
        # some time it return 1 extra li, sometime 2.
        # must implement try except
        # container = self.driver.find_element(By.XPATH, self.locators["message_list_container_ul"])
        if not self.is_on_inbox_page():
            self.go_to_inbox_page()

        messages = self.driver.find_elements(By.XPATH, self.locators["all_messages"])
        # sender_locator = "//*[@id=\"mail-app-component\"]/div/div/div/div[2]/div/div//ul/li/a/div/div[1]/div[2]/span"
        # pdb.set_trace()
        if len(messages) == 0:
            return res
        sender_name_test = self.settings["sender_name_test"]
        for message in messages:
            try:
                sender = self.driver.find_element(By.XPATH, self.locators["message_sender"])
                sender_name = sender.text
                # logging.info(f"sender: {sender_name}")
                if sender_name.__eq__(sender_name_test):
                    res.append(message)
            except Exception as e:
                logging.info(f"{e.__class__}")
        # logging.info(f"res len in find all before return: {len(res)}")
        return res

    def delete_all(self):
        if not self.is_on_inbox_page():
            self.go_to_inbox_page()
        select_dropdown_btn = self.driver.find_element(By.XPATH, self.locators["select_dropdown_btn"])
        select_dropdown_btn.click()
        select_all_btn_wait = int(self.settings["select_all_btn_wait"])
        wait = WebDriverWait(self.driver, select_all_btn_wait)
        wait.until(EC.visibility_of_element_located((By.XPATH, self.locators["select_all_btn"])))
        select_all_btn = self.driver.find_element(By.XPATH, self.locators["select_all_btn"])
        select_all_btn.click()
        delete_btn = self.driver.find_element(By.XPATH, self.locators['delete_btn'])
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
            logging.warn("Exit loop in is_inbox_empty")
        return True



    def all_messages_arrived(self):
        """
        Loops and wait for all messages to arrive.
        :return: bool; true if all arrived, false otherwise
        """
        if not self.is_on_inbox_page():
            self.go_to_inbox_page()
        m_length = int(self.settings["messages_quantity"])
        for _ in range(4):
            messages = self.get_all_by_me()
            if len(messages) == m_length:
                return True
            else:
                time.sleep(3)
                self.click_inbox_btn()
        return False

                # browser find it like this, but will try other shorter option
                # //div[@id="mail-app-component"]/div[2]/div/div[2]/div/span
                # I think some time path after div[2] changes.
                # text is visible must return no future check is required.
