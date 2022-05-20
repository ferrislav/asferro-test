import time

import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pdb
from src.util import Util
from src.tests_context import Context


@pytest.mark.usefixtures("driver_init", "tests_init")
class TestReceive:


    def count_test(self):
        mail_app_component_wait = int(self.settings["mail_app_component_wait"])
        assert EC.url_contains(self.locators["mail_home_partial_url"])
        util = Util(self.driver, self.locators, self.settings)
        util.click_inbox_btn()
        # check if inbox is empty
        WebDriverWait(self.driver, mail_app_component_wait)\
            .until(EC.presence_of_element_located((By.ID, self.locators["mail_app_component_id"])))
        try:
            mail_component = self.driver.find_element(By.ID, self.locators["mail_app_component_id"])

            info_message = mail_component.find_element(By.XPATH, self.locators["info_message_path"])
            info_message_srt = info_message.text
            # text is visible must return no future check is required.
            if "folder is empty" in info_message_srt:
                assert EC.visibility_of(info_message)
                return
        except NoSuchElementException:
            Context.is_no_messages = True
            pass
        # as a precaution wrap in condition and conduct message counting loop
        # TODO: message counting loop must be separate function in class will use it twice.
        # if util.is_message_container_present():
            # Loop and wait for all messages to arrive
        mess_quant = int(self.settings["messages_quantity"])
        loops = int(self.settings["loops_for_all_msgs"])
        messages_wait = int(self.settings["messages_arrive_wait"])
        for i in range(loops):
            logging.info(f"Wait for all messages to arrive, {i+1} of 5")
            messages = self.driver.find_elements(By.CLASS_NAME, self.locators["message_list_item_class"])
            if len(messages) < mess_quant:
                time.sleep(messages_wait)
                self.driver.refresh()
            else:
                break
        assert len(messages) == mess_quant




    def get_message(self):
        assert EC.url_contains('messages')
        msg_hldr_wait = int(self.settings["message_holder_wait"])
        # wait for message body container
        WebDriverWait(self.driver, msg_hldr_wait)\
            .until(EC.presence_of_element_located((By.CLASS_NAME, self.locators["message_body_div_class"])))

        topic = self.driver.find_element(By.CSS_SELECTOR, self.locators["message_topic_css"])
        # message_holder = message.find_element(By.CSS_SELECTOR, self.locators["message_holder_css"])
        message_container = self.driver.find_element(By.CLASS_NAME, self.locators["message_body_div_class"])
        message_body = message_container.find_element(By.XPATH, self.locators["message_body_path"])
        logging.info(f"{topic.text}: {message_body.text}")
        self.driver.back()

    def get_list_tup(self):
        """
        Collects topic's and body's text and put them in a list of tuples
        :return: List of Tuples (topic.text, body.text)
        """
        logging.info("Start getting tuples")
        l = []
        util = Util(self.driver, self.locators, self.settings)
        #if util.is_message_container_present():
        # messages = util.get_all_by_me()
        # WebDriverWait(self.driver, 10)\
        #    .until(EC.presence_of_element_located((By.XPATH, self.locators["message_list_container_path"])))
        container = self.driver.find_element(By.XPATH, self.locators["message_list_container_ul"])
        # pdb.set_trace()
        self.driver.implicitly_wait(5)
        messages = container.find_elements(By.CSS_SELECTOR, self.locators["messages_in_container"])
        logging.info(f"messages len = {len(messages)}")
        # skip first two don't put them in settings because it's structural
        # messages_sl = messages[2:]
        # logging.info(f"messages_sl len = {len(messages_sl)}")
        # Settings are done until here.
        for message in messages:
            # get url for message.
            # pdb.set_trace()
            logging.info(f"{message.get_attribute('class')}")
            link = message.find_element(By.XPATH, "./a[1]")
            link_txt = link.get_attribute('href')
            logging.info(f"{link_txt}")
            link.click()
            time.sleep(2)
            self.get_message()

                # logging.log(logging.INFO, f"{link.get_attribute('aria-label')}")
                # topic = message.find_element(By.XPATH, self.locators["message_topic"])
                # body = message.find_element(By.XPATH, self.locators["message_body"])
                # l.append((topic.text, body.text))
        return l



    def some_test(self):
        if Context.is_no_messages:
            return
        assert EC.url_contains('folders')
        logging.info("Before calling get list")
        self.get_list_tup()
        # for message in messages:
        #     logging.log(logging.INFO, f"{message[0]}: {message[1]}")
        assert 0 == 0
