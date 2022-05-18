import time

import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pdb
from src.util import Util


@pytest.mark.usefixtures("driver_init", "locators_init")
class TestReceive:

    # For the sake of simplicity would continue from where I'm in drive nav.
    # Should be in account mailbox.

    # click on inbox button.
    # will need to have values in several tests in this class
    msg_values = dict()
    # def __init__(self):
    #     self.msg_values = dict()


    def count_test(self):
        assert EC.url_contains(self.locators["mail_home_partial_url"])
        util = Util(self.driver, self.locators)
        inbox_btn = self.driver.find_element(By.CSS_SELECTOR, self.locators["inbox_btn"])
        inbox_btn.click()
        if util.is_message_container_visible():
            # Loop and wait for all messages to arrive
            for i in range(5):
                logging.log(logging.INFO, f"Wait for all messages to arrive, {i+1} of 5")
                messages = self.driver.find_elements(By.CLASS_NAME, self.locators["message_list_item_class"])
                if len(messages) < 10:
                    time.sleep(4)
                else:
                    break
        # pdb.set_trace()
        assert len(messages) == 10


    # Collect data to map
    # Parse map as required get topic, body, count letters and digits
    #def get_list_tup(self):
    #    l = []
    #    util = Util(self.driver)
    #    if
    #    for message in messages:
    #        cla = message.value_of_css_property('class')
    #        logging.log(logging.INFO, f"{cla}")
    #        # tmp = []
    #        # for x in range(2):
    #        #     tmp.append(self.get_random_str())
    #        # l.append(tuple(tmp))
    #    return l

    def some_test(self):
        assert len(TestReceive.msg_values) == 0
